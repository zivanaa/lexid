"""evals.run_generation tests — LLMs stubbed; no network, no quota."""

import json

import pytest

import evals.run_generation as gen
from evals.run_generation import (
    JudgeCache,
    aggregate,
    answer_hash,
    has_citation,
    is_refusal,
)
from rag.retrieve import RetrievedChunk


# --- scripted checks ---


def test_is_refusal():
    assert is_refusal("Saya tidak menemukan jawabannya di dokumen.")
    assert is_refusal("Informasi itu TIDAK DITEMUKAN.")
    assert not is_refusal("Tarifnya 22% [uu-hpp, Pasal 17].")


def test_has_citation():
    assert has_citation("Tarif 22% [uu-hpp-2021-bt, Pasal 17, ayat 1].")
    assert not has_citation("Tarif 22 persen. Catatan: ini alat riset.")


def test_answer_hash_stable_and_sensitive():
    assert answer_hash("abc") == answer_hash("abc")
    assert answer_hash("abc") != answer_hash("abd")


# --- judge cache ---


def test_judge_cache_roundtrip_and_versioning(tmp_path):
    c = JudgeCache(tmp_path / "cache.json")
    v = {"faithfulness": {"score": 1.0}, "correctness": {"score": 1.0}}
    c.put("d01", "jawaban", 1, v)
    assert c.get("d01", "jawaban", 1) == v
    assert c.get("d01", "jawaban", 2) is None  # different prompt version → miss
    assert c.get("d01", "jawaban berbeda", 1) is None  # different answer → miss
    # persisted to disk
    assert JudgeCache(tmp_path / "cache.json").get("d01", "jawaban", 1) == v


# --- aggregation ---


def _row(item_id, diff, refused, expected_refusal, cited, faith=None, corr=None):
    return {
        "item_id": item_id,
        "difficulty": diff,
        "refused": refused,
        "expected_refusal": expected_refusal,
        "refusal_correct": refused == expected_refusal,
        "has_citation": cited,
        "faithfulness": faith,
        "correctness": corr,
    }


def test_aggregate_metrics():
    rows = [
        _row("d1", "direct", False, False, True, faith=1.0, corr=1.0),
        _row("d2", "direct", False, False, True, faith=0.5, corr=0.0),
        _row("p1", "paraphrase", True, False, False),  # false refusal on answerable
        _row("u1", "unanswerable", True, True, False),  # correct refusal
        _row("u2", "unanswerable", False, True, False),  # missed refusal (answered), uncited
    ]
    agg = aggregate(rows)
    assert agg["faithfulness_mean"] == 0.75  # (1.0+0.5)/2, only judged rows
    assert agg["correctness_mean"] == 0.5
    assert agg["refusal_accuracy_unanswerable"] == 0.5  # 1 of 2 unanswerable refused
    assert agg["false_refusal_rate_answerable"] == 0.3333  # 1 of 3 answerable refused (4dp)
    assert agg["citation_rate"] == 0.6667  # of the 3 non-refused rows (d1,d2,u2), 2 cited
    assert agg["n_judged"] == 2


# --- judge JSON parsing ---


def test_parse_judge_json_tolerates_fences():
    from evals.run_generation import _parse_judge_json

    txt = '```json\n{"faithfulness": {"verdict": "supported", "score": 1.0}}\n```'
    assert _parse_judge_json(txt)["faithfulness"]["score"] == 1.0


def test_parse_judge_json_raises_without_json():
    from evals.run_generation import GenerationEvalError, _parse_judge_json

    with pytest.raises(GenerationEvalError, match="no JSON"):
        _parse_judge_json("maaf saya tidak bisa menilai")


def test_parse_judge_json_skips_reasoning_thought():
    # Gemma emits <thought> (with a DRAFT json) then the final fenced json;
    # we must return the FINAL verdict, not the draft inside the thought.
    from evals.run_generation import _parse_judge_json

    txt = (
        '<thought>Draft: {"faithfulness": {"score": 0.0}} hmm let me reconsider...</thought>'
        "```json\n"
        '{"faithfulness": {"verdict": "supported", "score": 1.0, "reasoning": "ok"}, '
        '"correctness": {"verdict": "correct", "score": 0.9, "reasoning": "ok"}}\n'
        "```"
    )
    out = _parse_judge_json(txt)
    assert out["faithfulness"]["score"] == 1.0  # final, not the 0.0 draft in the thought
    assert out["correctness"]["score"] == 0.9


def test_fill_prompt_preserves_literal_json_braces():
    # the judge prompt shows a JSON example with literal braces; substitution
    # must fill {question} etc. WITHOUT choking on {"faithfulness": ...}
    from evals.run_generation import _fill_prompt

    t = 'PERTANYAAN: {question}\nBentuk: {"faithfulness": {"score": 0.0}}'
    out = _fill_prompt(t, question="tarif?", context="c", answer="a", reference="r")
    assert "PERTANYAAN: tarif?" in out
    assert '{"faithfulness": {"score": 0.0}}' in out  # literal braces survive verbatim


def test_real_judge_prompt_fills_without_error():
    # regression: exercise the committed judge prompt end-to-end substitution
    from pathlib import Path

    from prompts.loader import load

    from evals.run_generation import _fill_prompt

    text, _ = load("generation_judge", directory=Path("evals/judge_prompts"))
    out = _fill_prompt(text, question="q?", context="ctx", answer="ans", reference="ref")
    assert "q?" in out and "ctx" in out and "ans" in out and "ref" in out
    assert "{question}" not in out and "{answer}" not in out


# --- end-to-end main with stubs (no network) ---


def _chunk(cid):
    return RetrievedChunk(
        chunk_id=cid, doc_id="uu-hpp-2021-bt", page_start=1, page_end=1, text="isi", score=0.9
    )


class _Resp:
    def __init__(self, answer):
        self.answer = answer
        self.chunks = [_chunk("uu-hpp-2021-bt:0057")]


def test_main_smoke_uses_cache_and_scripts(tmp_path, monkeypatch, capsys):
    # tiny dataset: one answerable, one unanswerable
    ds = {
        "name": "t",
        "version": "1.1",
        "items": [
            {
                "id": "d1",
                "question": "tarif?",
                "difficulty": "direct",
                "relevant_chunk_groups": [["uu-hpp-2021-bt:0057"]],
                "reference_answer": "22%",
                "reviewed_by_human": True,
            },
            {
                "id": "u1",
                "question": "hal di luar korpus?",
                "difficulty": "unanswerable",
                "relevant_chunk_groups": [],
                "reference_answer": "Tidak ditemukan.",
                "reviewed_by_human": True,
            },
        ],
    }
    dpath = tmp_path / "ds.json"
    dpath.write_text(json.dumps(ds), encoding="utf-8")

    # answerable → substantive cited answer; unanswerable → refusal
    def _fake_ask(q, retriever, provider):
        if "luar korpus" in q:
            return _Resp("Saya tidak menemukan jawabannya di dokumen.")
        return _Resp("Tarifnya 22% [uu-hpp-2021-bt, Pasal 17, ayat 1].")

    monkeypatch.setattr("rag.pipeline.ask", _fake_ask)
    monkeypatch.setattr(gen, "CACHE_PATH", tmp_path / "cache.json")
    monkeypatch.setattr(gen, "RESULTS_DIR", tmp_path / "results")

    judge_calls = {"n": 0}

    def _fake_judge(question, context, answer, reference, provider="gemini"):
        judge_calls["n"] += 1
        return {"faithfulness": {"score": 1.0}, "correctness": {"score": 0.8}}, 1

    monkeypatch.setattr(gen, "judge_generation", _fake_judge)

    rc = gen.main(["--dataset", str(dpath), "--throttle", "0"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "faithfulness 1.0" in out
    assert "refusal_accuracy (unanswerable) 1.0" in out
    assert judge_calls["n"] == 1  # only the answerable item judged; refusal not judged


def test_main_survives_flaky_judge(tmp_path, monkeypatch, capsys):
    # a transient judge failure must NOT abort the run; the result still writes
    from evals.run_generation import GenerationEvalError

    ds = {
        "name": "t",
        "version": "1.1",
        "items": [
            {
                "id": "d1",
                "question": "tarif?",
                "difficulty": "direct",
                "relevant_chunk_groups": [["uu-hpp-2021-bt:0057"]],
                "reference_answer": "22%",
                "reviewed_by_human": True,
            }
        ],
    }
    dpath = tmp_path / "ds.json"
    dpath.write_text(json.dumps(ds), encoding="utf-8")

    monkeypatch.setattr(
        "rag.pipeline.ask", lambda q, retriever, provider: _Resp("22% [uu, Pasal 17].")
    )
    monkeypatch.setattr(gen, "CACHE_PATH", tmp_path / "cache.json")
    monkeypatch.setattr(gen, "RESULTS_DIR", tmp_path / "results")

    def _boom(*a, **kw):
        raise GenerationEvalError("judge gemini/gemma failed: 500 Internal error")

    monkeypatch.setattr(gen, "judge_generation", _boom)

    rc = gen.main(["--dataset", str(dpath), "--throttle", "0"])
    assert rc == 0  # did not crash
    out = capsys.readouterr().out
    assert "judge errors 1" in out
    assert "faithfulness None" in out  # nothing judged, but the run completed
