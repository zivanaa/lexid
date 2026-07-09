"""evals.run_retrieval tests — metric math hand-checked, retrieval stubbed."""

import json

import pytest

from evals.run_retrieval import (
    EvalItem,
    aggregate,
    evaluate_item,
    group_recall_at_k,
    load_items,
    mrr,
    ndcg_at_k,
    precision_at_k,
)

RET = ["a", "b", "c", "d", "e"]


def test_group_recall_counts_facts_not_chunks():
    # fact 1 lives in a OR z (overlap twins); fact 2 only in x (missed)
    groups = [["a", "z"], ["x"]]
    assert group_recall_at_k(RET, groups, 3) == 0.5
    assert group_recall_at_k(RET, [["z", "a"]], 1) == 1.0
    assert group_recall_at_k(RET, [["x"]], 5) == 0.0


def test_precision_at_k():
    assert precision_at_k(RET, [["a"], ["c"]], 3) == pytest.approx(2 / 3)
    assert precision_at_k(RET, [["x"]], 5) == 0.0


def test_mrr_first_relevant_rank():
    assert mrr(RET, [["c"]]) == pytest.approx(1 / 3)
    assert mrr(RET, [["a"], ["e"]]) == 1.0
    assert mrr(RET, [["x"]]) == 0.0


def test_ndcg_perfect_and_zero():
    assert ndcg_at_k(["a", "b"], [["a"], ["b"]], 10) == pytest.approx(1.0)
    assert ndcg_at_k(RET, [["x"]], 10) == 0.0
    # relevant at rank 2 of 1-relevant ideal: dcg=1/log2(3), idcg=1
    assert ndcg_at_k(["z", "a"], [["a"]], 10) == pytest.approx(0.6309, abs=1e-3)


def _item(i, difficulty="direct", groups=None, reviewed=True):
    return {
        "id": f"i{i}",
        "question": "q?",
        "difficulty": difficulty,
        "relevant_chunk_groups": [["a"]] if groups is None else groups,
        "reference_answer": "ref",
        "reviewed_by_human": reviewed,
    }


def test_evaluate_item_keys():
    row = evaluate_item(RET, EvalItem(**_item(1)))
    assert row["recall@3"] == 1.0 and row["mrr"] == 1.0 and row["difficulty"] == "direct"


def test_aggregate_per_difficulty():
    rows = [
        evaluate_item(RET, EvalItem(**_item(1, "direct"))),
        evaluate_item(RET, EvalItem(**_item(2, "paraphrase", groups=[["x"]]))),
    ]
    agg = aggregate(rows)
    assert agg["overall"]["n"] == 2
    assert agg["overall"]["recall@5"] == 0.5
    assert agg["per_difficulty"]["paraphrase"]["recall@5"] == 0.0


def test_load_items_filters(tmp_path):
    ds = {
        "name": "t",
        "version": "0",
        "items": [
            _item(1, reviewed=True),
            _item(2, reviewed=False),
            _item(3, difficulty="unanswerable", groups=[]),
        ],
    }
    p = tmp_path / "ds.json"
    p.write_text(json.dumps(ds), encoding="utf-8")

    _, items, skipped = load_items(p, include_unreviewed=False)
    assert [i.id for i in items] == ["i1"]
    assert skipped == {"unanswerable": 1, "unreviewed": 1}

    _, items, _ = load_items(p, include_unreviewed=True)
    assert [i.id for i in items] == ["i1", "i2"]


def test_committed_dataset_invariants():
    # Holds whether the set is frozen or mid-growth (a "-draft" version has
    # unreviewed items pending owner sign-off): reviewed items must be scoreable,
    # and EVERY answerable item (reviewed or draft) must reference chunk groups.
    from evals.run_retrieval import DATASET_DEFAULT

    data, reviewed_items, skipped = load_items(DATASET_DEFAULT, include_unreviewed=False)
    assert len(reviewed_items) >= 25  # the frozen v1.0 core stays scoreable
    for it in reviewed_items:
        assert it.reviewed_by_human
        assert it.relevant_chunk_groups, f"{it.id}: reviewed answerable item without chunk groups"

    _, all_answerable, _ = load_items(DATASET_DEFAULT, include_unreviewed=True)
    for it in all_answerable:
        assert it.relevant_chunk_groups, f"{it.id}: answerable item without chunk groups"

    # a "-draft" version means growth in progress; a clean version must be fully reviewed
    if not data["version"].endswith("-draft"):
        assert skipped["unreviewed"] == 0, "clean (frozen) version must have no unreviewed items"
