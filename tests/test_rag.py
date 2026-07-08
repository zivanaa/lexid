"""rag.retrieve / rag.generate / rag.pipeline tests — embedding + LLM stubbed."""

import numpy as np
import pytest
from qdrant_client import QdrantClient

import rag.generate
import rag.pipeline
import rag.retrieve
from ingestion.chunk import Chunk
from ingestion.index import build_index
from rag.generate import GenerationError, format_context, generate
from rag.pipeline import DISCLAIMER, ask
from rag.retrieve import RetrievalError, RetrievedChunk, retrieve

DIM = 8


def _chunks(n: int) -> list[Chunk]:
    return [
        Chunk(
            chunk_id=f"doc:{i:04d}",
            doc_id="doc",
            seq=i,
            text=f"Pasal {i} berisi ketentuan nomor {i}.",
            page_start=i + 1,
            page_end=i + 1,
            n_words=5,
        )
        for i in range(n)
    ]


def _vec(i: int) -> np.ndarray:
    v = np.zeros(DIM, dtype=np.float32)
    v[i % DIM] = 1.0
    return v


@pytest.fixture
def indexed_client(tmp_path, monkeypatch):
    client = QdrantClient(path=str(tmp_path / "q"))
    vecs = np.stack([_vec(i) for i in range(4)])
    build_index(client, _chunks(4), vecs, collection="t")
    # query embedding == chunk 2's vector → chunk 2 must rank first
    monkeypatch.setattr(rag.retrieve, "embed_texts", lambda texts: np.stack([_vec(2)]))
    return client


# --- retrieve ---


def test_retrieve_ranks_by_similarity(indexed_client):
    out = retrieve("apa isi pasal 2?", k=2, client=indexed_client, collection="t")
    assert len(out) == 2
    assert out[0].chunk_id == "doc:0002"
    assert out[0].score == pytest.approx(1.0)
    assert all(isinstance(c, RetrievedChunk) for c in out)


def test_retrieve_empty_query_rejected(indexed_client):
    with pytest.raises(RetrievalError, match="empty"):
        retrieve("  ", client=indexed_client, collection="t")


def test_retrieve_missing_collection(indexed_client):
    with pytest.raises(RetrievalError, match="ingestion.run"):
        retrieve("x", client=indexed_client, collection="nope")


# --- generate ---


class _FakeCompletion:
    def __init__(self, text):
        msg = type("M", (), {"content": text})
        self.choices = [type("C", (), {"message": msg})]


class _FakeClient:
    def __init__(self, text):
        self._text = text
        self.last_kwargs = None
        outer = self

        class _Completions:
            def create(self, **kwargs):
                outer.last_kwargs = kwargs
                return _FakeCompletion(outer._text)

        self.chat = type("Chat", (), {"completions": _Completions()})

    def with_options(self, **_):
        return self


def _retrieved(n=2) -> list[RetrievedChunk]:
    return [
        RetrievedChunk(
            chunk_id=f"doc:{i:04d}",
            doc_id="doc",
            page_start=1,
            page_end=2,
            text=f"isi {i}",
            score=0.9,
        )
        for i in range(n)
    ]


def test_format_context_carries_ids_and_pages():
    ctx = format_context(_retrieved())
    assert "[doc:0000 | hlm. 1-2]" in ctx and "isi 1" in ctx


def test_generate_fills_prompt_and_metadata(monkeypatch):
    fake = _FakeClient("Jawaban. [uu_hpp, pasal 17, ayat 1]")
    monkeypatch.setattr(rag.generate.llm_client, "client", lambda p: fake)
    out = generate("tanya?", _retrieved(), provider="gemini")
    sent = fake.last_kwargs["messages"][0]["content"]
    assert "tanya?" in sent and "doc:0000" in sent  # prompt got question + context
    assert out.provider == "gemini" and out.prompt_version >= 1 and out.latency_ms >= 0


def test_generate_no_chunks_refuses_upstream():
    with pytest.raises(GenerationError, match="refuse"):
        generate("tanya?", [], provider="gemini")


def test_generate_empty_answer_rejected(monkeypatch):
    monkeypatch.setattr(rag.generate.llm_client, "client", lambda p: _FakeClient("  "))
    with pytest.raises(GenerationError, match="empty"):
        generate("tanya?", _retrieved(), provider="gemini")


# --- pipeline ---


def test_ask_appends_disclaimer_when_missing(monkeypatch):
    monkeypatch.setattr(rag.pipeline, "retrieve", lambda q, k: _retrieved())
    monkeypatch.setattr(
        rag.generate.llm_client, "client", lambda p: _FakeClient("Jawaban tanpa disclaimer.")
    )
    resp = ask("tanya?")
    assert resp.answer.endswith(DISCLAIMER)
    assert resp.chunks and resp.total_latency_ms >= 0


def test_ask_keeps_single_disclaimer(monkeypatch):
    monkeypatch.setattr(rag.pipeline, "retrieve", lambda q, k: _retrieved())
    monkeypatch.setattr(
        rag.generate.llm_client, "client", lambda p: _FakeClient(f"Jawaban. {DISCLAIMER}")
    )
    resp = ask("tanya?")
    assert resp.answer.count(DISCLAIMER) == 1


# --- CLI ---


def test_cli_retrieve_only(monkeypatch, capsys):
    import rag.__main__ as cli

    monkeypatch.setattr(cli, "retrieve", lambda q, k: _retrieved())
    monkeypatch.setattr("sys.argv", ["rag", "--retrieve-only", "tanya?"])
    assert cli.main() == 0
    out = capsys.readouterr().out
    assert "[doc:0000]" in out and DISCLAIMER in out


def test_cli_falls_back_without_api_key(monkeypatch, capsys):
    import rag.__main__ as cli

    def _no_key(*a, **kw):
        raise RuntimeError("No API key configured for provider 'gemini'")

    monkeypatch.setattr(cli, "ask", _no_key)
    monkeypatch.setattr(cli, "retrieve", lambda q, k: _retrieved())
    monkeypatch.setattr("sys.argv", ["rag", "tanya?"])
    assert cli.main() == 0
    out = capsys.readouterr().out
    assert "retrieve-only" in out and "[doc:0000]" in out and DISCLAIMER in out
