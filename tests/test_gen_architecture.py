"""scripts.gen_architecture tests — AST graph over the real project, no imports."""

from scripts.gen_architecture import build_edges, discover_modules, render


def test_discovers_known_modules():
    mods = discover_modules()
    for expected in ("config", "rag.pipeline", "rag.retrieve", "ingestion.index", "prompts.loader"):
        assert expected in mods, f"{expected} not discovered"


def test_edges_capture_real_and_lazy_imports():
    mods = discover_modules()
    edges = build_edges(mods)
    # module-level imports
    assert ("rag.generate", "prompts.loader") in edges
    assert ("rag.llm_client", "config") in edges
    assert ("rag.retrieve", "ingestion.index") in edges
    # lazy/in-function import (pipeline dispatches to hybrid inside a function)
    assert ("rag.pipeline", "rag.hybrid") in edges


def test_no_self_edges_and_targets_are_known():
    mods = discover_modules()
    edges = build_edges(mods)
    for src, dst in edges:
        assert src != dst
        assert src in mods and dst in mods


def test_render_is_valid_mermaid_markdown():
    mods = discover_modules()
    md = render(mods, build_edges(mods))
    assert "```mermaid" in md and "graph LR" in md
    assert md.count("```") == 2  # opening + closing fence
    assert 'config["config"]' in md  # top-level module rendered
    assert "subgraph rag" in md


def test_render_is_deterministic():
    mods = discover_modules()
    edges = build_edges(mods)
    assert render(mods, edges) == render(mods, edges)  # no timestamps / set ordering leaks
