"""evals.gate_check tests — pure comparison logic, no retrieval."""

import json

from evals.gate_check import compare, main, newest_result


def _result(recall5=0.68, *, n=50, citable=True, version="1.0", commit="abc1234", **over):
    overall = {
        "n": n,
        "recall@3": 0.62,
        "recall@5": recall5,
        "recall@10": 0.84,
        "mrr": 0.58,
        "ndcg@10": 0.61,
        **over,
    }
    return {
        "citable": citable,
        "dataset": {"name": "t", "version": version, "path": "x"},
        "config": {"commit": commit, "k_values": [3, 5, 10], "timestamp": "t"},
        "overall": overall,
    }


def test_pass_when_equal():
    res = compare(_result(0.68), _result(0.68))
    assert res.passed and not res.failures and not res.errors


def test_pass_when_improved():
    res = compare(_result(0.68), _result(0.75))
    assert res.passed
    assert res.deltas["recall@5"] == 0.07


def test_fail_when_recall5_drops_past_threshold():
    res = compare(_result(0.68), _result(0.65))  # drop 0.03 > 0.02
    assert not res.passed and res.failures
    assert "recall@5 dropped" in res.failures[0]


def test_boundary_exact_threshold_passes():
    # drop of exactly 0.02 is not > 0.02 → allowed
    res = compare(_result(0.70, n=50), _result(0.68, n=50))
    assert res.passed


def test_small_drop_within_tolerance_passes():
    res = compare(_result(0.70, n=100), _result(0.69, n=100))  # 0.01 drop
    assert res.passed


def test_version_mismatch_is_precondition_error():
    res = compare(_result(0.68, version="1.0"), _result(0.90, version="1.1"))
    assert not res.passed and res.errors and not res.failures  # improved but uncomparable


def test_noncitable_is_precondition_error():
    res = compare(_result(0.68), _result(0.68, citable=False))
    assert not res.passed and any("citable" in e for e in res.errors)


def test_small_n_warns_but_does_not_fail():
    res = compare(_result(0.68, n=28), _result(0.68, n=28))  # 1/28=0.036 > 0.02
    assert res.passed  # equal metrics → pass
    assert any("unmeasurable" in w for w in res.warnings)


def test_large_n_no_resolution_warning():
    res = compare(_result(0.68, n=100), _result(0.68, n=100))
    assert not any("unmeasurable" in w for w in res.warnings)


def test_newest_result_picks_latest(tmp_path):
    (tmp_path / "retrieval_20260101T000000Z.json").write_text("{}", encoding="utf-8")
    (tmp_path / "retrieval_20260708T000000Z.json").write_text("{}", encoding="utf-8")
    assert newest_result(tmp_path).name == "retrieval_20260708T000000Z.json"
    assert newest_result(tmp_path / "empty") is None if (tmp_path / "empty").exists() else True


def test_main_exit_codes(tmp_path, capsys):
    base = tmp_path / "base.json"
    cand = tmp_path / "cand.json"
    base.write_text(json.dumps(_result(0.68)), encoding="utf-8")

    cand.write_text(json.dumps(_result(0.68)), encoding="utf-8")
    assert main(["--baseline", str(base), "--candidate", str(cand)]) == 0

    cand.write_text(json.dumps(_result(0.60)), encoding="utf-8")  # big drop
    assert main(["--baseline", str(base), "--candidate", str(cand)]) == 1

    cand.write_text(json.dumps(_result(0.90, version="2.0")), encoding="utf-8")  # uncomparable
    assert main(["--baseline", str(base), "--candidate", str(cand)]) == 2


def _run_and_get_output(base_result, cand_result, tmp_path, capsys):
    base = tmp_path / "b.json"
    cand = tmp_path / "c.json"
    base.write_text(json.dumps(base_result), encoding="utf-8")
    cand.write_text(json.dumps(cand_result), encoding="utf-8")
    main(["--baseline", str(base), "--candidate", str(cand)])
    return capsys.readouterr().out


def test_output_is_ascii_safe(tmp_path, capsys):
    # the owner's console is cp950 — non-ASCII output crashes the CLI there.
    # Cover ALL three verdict paths: FAIL+warn, PASS, and precondition-error.
    fail_out = _run_and_get_output(_result(0.70, n=28), _result(0.60, n=28), tmp_path, capsys)
    pass_out = _run_and_get_output(_result(0.68, n=100), _result(0.68, n=100), tmp_path, capsys)
    err_out = _run_and_get_output(
        _result(0.68, version="1.0"), _result(0.90, version="2.0", citable=False), tmp_path, capsys
    )
    for out in (fail_out, pass_out, err_out):
        out.encode("ascii")  # raises UnicodeEncodeError if any non-ASCII slipped in
