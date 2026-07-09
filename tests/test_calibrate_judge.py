"""evals.calibrate_judge tests — pure offline logic."""

import json

import pytest

from evals.calibrate_judge import (
    CalibrationError,
    agreement,
    build_sheet,
    judge_labels,
    judged_rows,
    main,
)


def _row(item_id, faith_v, corr_v, difficulty="direct"):
    return {
        "item_id": item_id,
        "difficulty": difficulty,
        "question": f"q {item_id}?",
        "reference_answer": "ref",
        "answer": f"ans {item_id} [uu, Pasal 1]",
        "context": "ctx",
        "judge_verdict": {
            "faithfulness": {"verdict": faith_v, "score": 1.0},
            "correctness": {"verdict": corr_v, "score": 1.0},
        },
    }


def test_judged_rows_filters_unjudged():
    result = {
        "per_item": [
            _row("d1", "supported", "correct"),
            {"item_id": "u1", "judge_verdict": None},
        ]
    }
    assert [r["item_id"] for r in judged_rows(result)] == ["d1"]


def test_judge_labels_extracts_verdicts_not_scores():
    labels = judge_labels([_row("d1", "supported", "partial")])
    assert labels == {"d1": {"faithfulness": "supported", "correctness": "partial"}}


def test_agreement_perfect_and_partial():
    judge = {
        "a": {"faithfulness": "supported", "correctness": "correct"},
        "b": {"faithfulness": "supported", "correctness": "correct"},
    }
    # human agrees on faithfulness both, disagrees on correctness for b
    human = {
        "a": {"faithfulness": "supported", "correctness": "correct"},
        "b": {"faithfulness": "supported", "correctness": "incorrect"},
    }
    res = agreement(human, judge)
    assert res["n_scored"] == 2
    assert res["per_dimension"]["faithfulness"] == 1.0
    assert res["per_dimension"]["correctness"] == 0.5
    assert res["overall"] == 0.75
    assert res["meets_target"] is False  # correctness 0.5 < 0.8


def test_agreement_skips_unscored_items():
    judge = {"a": {"faithfulness": "supported", "correctness": "correct"}}
    human = {"a": {"faithfulness": "", "correctness": ""}}  # not filled
    res = agreement(human, judge)
    assert res["n_scored"] == 0
    assert res["overall"] is None


def test_agreement_meets_target():
    judge = {i: {"faithfulness": "supported", "correctness": "correct"} for i in "abcde"}
    human = {i: {"faithfulness": "supported", "correctness": "correct"} for i in "abcde"}
    assert agreement(human, judge)["meets_target"] is True


def test_build_sheet_hides_judge_verdict():
    # the blind sheet must not depend on the judge's verdict at all: two rows
    # differing ONLY in judge_verdict must render identically
    sheet_bad = build_sheet([_row("d1", "unsupported", "incorrect")])
    sheet_good = build_sheet([_row("d1", "supported", "correct")])
    assert sheet_bad == sheet_good
    assert "d1" in sheet_bad and "q d1?" in sheet_bad


def test_make_and_score_roundtrip(tmp_path, monkeypatch, capsys):
    import evals.calibrate_judge as cj

    monkeypatch.setattr(cj, "CALIB_DIR", tmp_path / "calib")
    result = {"per_item": [_row(f"d{i}", "supported", "correct") for i in range(3)]}
    rpath = tmp_path / "generation_x.json"
    rpath.write_text(json.dumps(result), encoding="utf-8")

    assert main(["--result", str(rpath)]) == 0
    human_path = tmp_path / "calib" / "human_scores.json"
    assert human_path.exists()
    # human fills matching labels → perfect agreement
    human = {f"d{i}": {"faithfulness": "supported", "correctness": "correct"} for i in range(3)}
    human_path.write_text(json.dumps(human), encoding="utf-8")

    assert main(["--score"]) == 0
    out = capsys.readouterr().out
    assert "TRUSTWORTHY" in out


def test_score_without_make_errors(tmp_path, monkeypatch):
    import evals.calibrate_judge as cj

    monkeypatch.setattr(cj, "CALIB_DIR", tmp_path / "empty")
    assert main(["--score"]) == 2  # CalibrationError → exit 2


def test_agreement_disagreement_fails_target():
    judge = {i: {"faithfulness": "supported", "correctness": "correct"} for i in "abcde"}
    # human disagrees on faithfulness for 2 of 5 → 0.6 < 0.8
    human = {i: {"faithfulness": "supported", "correctness": "correct"} for i in "abc"}
    human["d"] = {"faithfulness": "partial", "correctness": "correct"}
    human["e"] = {"faithfulness": "unsupported", "correctness": "correct"}
    res = agreement(human, judge)
    assert res["per_dimension"]["faithfulness"] == 0.6
    assert res["meets_target"] is False


def test_missing_results_errors(tmp_path, monkeypatch):
    import evals.calibrate_judge as cj

    monkeypatch.setattr(cj, "RESULTS_DIR", tmp_path / "noresults")
    with pytest.raises(CalibrationError, match="no generation results"):
        cj.make(None)
