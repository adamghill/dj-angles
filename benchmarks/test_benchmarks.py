"""Benchmarks for dj-angles template parsing via pytest-benchmark.

Measures the cost of `convert_template` (the pure string-transformation step)
and the full Django template load+render cycle, with and without Django's
cached template loader.

Run with:
    uv run pytest benchmarks/ --benchmark-only -v
    uv run pytest benchmarks/ --benchmark-only --benchmark-histogram
    uv run pytest benchmarks/ --benchmark-only --benchmark-json=benchmark_results.json
"""

from __future__ import annotations

import re
from functools import cache
from pathlib import Path
from types import SimpleNamespace

from django.template import Context, Engine

from dj_angles.replacers import convert_template

BENCHMARKS_DIR = Path(__file__).parent
TEMPLATES_DIR = BENCHMARKS_DIR / "templates"

PLAIN_HTML = (TEMPLATES_DIR / "plain.html").read_text()
SIMPLE_ANGLES_HTML = (TEMPLATES_DIR / "simple_angles.html").read_text()
COMPLEX_ANGLES_HTML = (TEMPLATES_DIR / "complex_angles.html").read_text()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_engine(cached: bool) -> Engine:
    """Return a Django template Engine configured like a real project.

    Args:
        cached: When True, wraps dj_angles.template_loader.Loader in
                django.template.loaders.cached.Loader to mirror production
                settings where DEBUG=False.
    """
    loaders: list = [
        "dj_angles.template_loader.Loader",
        "django.template.loaders.filesystem.Loader",
    ]

    if cached:
        loaders = [("django.template.loaders.cached.Loader", loaders)]

    return Engine(
        dirs=[str(TEMPLATES_DIR)],
        loaders=loaders,
        builtins=["dj_angles.templatetags.dj_angles"],
    )


# ---------------------------------------------------------------------------
# 1. Pure conversion benchmarks (no Django template compilation or rendering)
#
# These isolate the cost of `convert_template`, which is the regex-parsing
# step that dj-angles adds on top of every template load.
# ---------------------------------------------------------------------------


def test_bench_convert_plain_html(benchmark):
    """Baseline: convert a template that has *no* dj-angles tags.

    Expected cost: essentially just one regex scan that finds no matches.
    """
    result = benchmark(convert_template, PLAIN_HTML)
    assert "<html" in result


def test_bench_convert_simple_angles(benchmark):
    """Convert a template with dj-if/dj-else attribute tags and plain Django for loops."""
    result = benchmark(convert_template, SIMPLE_ANGLES_HTML)
    assert "<html" in result


def test_bench_convert_complex_angles(benchmark):
    """Convert a heavier template: nested dj-if/dj-else attributes, plain Django for loops, and a dj-block tag."""
    result = benchmark(convert_template, COMPLEX_ANGLES_HTML)
    assert "<html" in result


# ---------------------------------------------------------------------------
# 2. Template loader benchmarks (file I/O + conversion, no render)
#
# These use a real Engine + Loader so that we exercise the full path that
# Django walks: find_template → get_contents → convert_template.
# The `cached=False` variant mirrors DEBUG=True; `cached=True` mirrors prod.
# ---------------------------------------------------------------------------


def test_bench_loader_plain_no_cache(benchmark):
    """Load `plain.html` through the dj-angles loader, no caching."""
    engine = _make_engine(cached=False)

    def load():
        return engine.get_template("plain.html")

    t = benchmark(load)
    assert t is not None


def test_bench_loader_plain_cached(benchmark):
    """Load `plain.html` through the cached loader (warm cache after 1st call).

    With Django's cached loader, every call after the first is effectively
    a dict lookup — the cost of `convert_template` is paid only once.
    """
    engine = _make_engine(cached=True)

    # Prime the cache so the benchmark measures warm-cache access
    engine.get_template("plain.html")

    def load():
        return engine.get_template("plain.html")

    t = benchmark(load)
    assert t is not None


def test_bench_loader_simple_angles_no_cache(benchmark):
    """Load `simple_angles.html` through the dj-angles loader, no caching."""
    engine = _make_engine(cached=False)

    def load():
        return engine.get_template("simple_angles.html")

    t = benchmark(load)
    assert t is not None


def test_bench_loader_simple_angles_cached(benchmark):
    """Load `simple_angles.html` via the cached loader (warm cache)."""
    engine = _make_engine(cached=True)
    engine.get_template("simple_angles.html")

    def load():
        return engine.get_template("simple_angles.html")

    t = benchmark(load)
    assert t is not None


def test_bench_loader_complex_angles_no_cache(benchmark):
    """Load `complex_angles.html` through the dj-angles loader, no caching."""
    engine = _make_engine(cached=False)

    def load():
        return engine.get_template("complex_angles.html")

    t = benchmark(load)
    assert t is not None


def test_bench_loader_complex_angles_cached(benchmark):
    """Load `complex_angles.html` via the cached loader (warm cache)."""
    engine = _make_engine(cached=True)
    engine.get_template("complex_angles.html")

    def load():
        return engine.get_template("complex_angles.html")

    t = benchmark(load)
    assert t is not None


# ---------------------------------------------------------------------------
# 3. Full render benchmarks (load + compile + render)
#
# Closest to real-world: a request comes in, a template is loaded and
# rendered with a context.  The cached variants show how little overhead
# dj-angles adds once the template is warm in Django's cache.
# ---------------------------------------------------------------------------

_RENDER_CONTEXT: dict = {
    "user": SimpleNamespace(is_authenticated=True, is_staff=False, username="alice"),
    "items": list(range(10)),
    "title": "Benchmark Page",
    "nav_links": [
        SimpleNamespace(url="/", label="Home"),
        SimpleNamespace(url="/about/", label="About"),
        SimpleNamespace(url="/contact/", label="Contact"),
    ],
    "show_banner": True,
    "banner_text": "Welcome to the benchmark page!",
    "sections": [
        SimpleNamespace(
            title=f"Section {i}",
            is_published=(i % 2 == 0),
            body=f"Body text for section {i}.",
            tags=[f"tag-{j}" for j in range(3)],
        )
        for i in range(5)
    ],
    "footer_items": ["Privacy", "Terms", "Contact"],
}


def test_bench_render_plain_no_cache(benchmark):
    """Render `plain.html` — no dj-angles tags, no caching (DEBUG=True baseline)."""
    engine = _make_engine(cached=False)

    def render():
        t = engine.get_template("plain.html")
        return t.render(Context(_RENDER_CONTEXT))

    result = benchmark(render)
    assert result


def test_bench_render_plain_cached(benchmark):
    """Render `plain.html` via cached loader (warm cache)."""
    engine = _make_engine(cached=True)
    engine.get_template("plain.html")

    def render():
        t = engine.get_template("plain.html")
        return t.render(Context(_RENDER_CONTEXT))

    result = benchmark(render)
    assert result


def test_bench_render_simple_angles_no_cache(benchmark):
    """Render `simple_angles.html` — dj-if/dj-else attributes, no caching."""
    engine = _make_engine(cached=False)

    def render():
        t = engine.get_template("simple_angles.html")
        return t.render(Context(_RENDER_CONTEXT))

    result = benchmark(render)
    assert result


def test_bench_render_simple_angles_cached(benchmark):
    """Render `simple_angles.html` via cached loader (warm cache)."""
    engine = _make_engine(cached=True)
    engine.get_template("simple_angles.html")

    def render():
        t = engine.get_template("simple_angles.html")
        return t.render(Context(_RENDER_CONTEXT))

    result = benchmark(render)
    assert result


def test_bench_render_complex_angles_no_cache(benchmark):
    """Render `complex_angles.html` — nested tags + block, no caching."""
    engine = _make_engine(cached=False)

    def render():
        t = engine.get_template("complex_angles.html")
        return t.render(Context(_RENDER_CONTEXT))

    result = benchmark(render)
    assert result


def test_bench_render_complex_angles_cached(benchmark):
    """Render `complex_angles.html` via cached loader (warm cache)."""
    engine = _make_engine(cached=True)
    engine.get_template("complex_angles.html")

    def render():
        t = engine.get_template("complex_angles.html")
        return t.render(Context(_RENDER_CONTEXT))

    result = benchmark(render)
    assert result


# ---------------------------------------------------------------------------
# 4. Regex compilation micro-benchmarks
#
# Python's `re` module has an internal LRU cache (512 entries in CPython), so
# calling re.finditer/re.match with a *static* literal string is essentially
# free after the first call — the compiled pattern is retrieved from the cache.
#
# The only patterns in attributes.py that are NOT already effectively cached
# are dynamic ones that embed runtime values (tag_name, prefix). These
# benchmarks quantify the actual cost difference:
#   a) `_find_element_end`: re.compile(f"<(/)? {tag_name}...") — called once
#      per matched element; result is NOT reused across calls.
#   b) Static patterns like r"<(\w+)" — already in re's cache (control).
# ---------------------------------------------------------------------------

_SAMPLE_HTML_FRAGMENT = "<div class='x'><p>inner</p><div>nested</div></div>"


def _find_end_current(tag_name: str, html: str, pos: int) -> int:
    """Current implementation: re.compile called on every invocation."""
    pattern = re.compile(rf"<(/)?{tag_name}(?:\s[^>]*)?\s*/?>", re.IGNORECASE)
    m = pattern.search(html, pos)
    return m.end() if m else pos


@cache
def _cached_tag_pattern(tag_name: str) -> re.Pattern:
    return re.compile(rf"<(/)?{tag_name}(?:\s[^>]*)?\s*/?>", re.IGNORECASE)


def _find_end_lru_cached(tag_name: str, html: str, pos: int) -> int:
    """Optimised: compiled Pattern retrieved from lru_cache keyed on tag_name."""
    pattern = _cached_tag_pattern(tag_name)
    m = pattern.search(html, pos)
    return m.end() if m else pos


def test_bench_regex_dynamic_current(benchmark):
    """Cost of re.compile for a dynamic (tag-name-dependent) pattern each call.

    Reflects the hot path in `_find_element_end` — called once per
    conditional element found in the template.
    """
    result = benchmark(_find_end_current, "div", _SAMPLE_HTML_FRAGMENT, 0)
    assert result > 0


def test_bench_regex_dynamic_lru_cached(benchmark):
    """Same dynamic pattern but retrieved from an lru_cache keyed on tag_name.

    Shows whether caching the compiled Pattern object is measurably faster.
    """
    result = benchmark(_find_end_lru_cached, "div", _SAMPLE_HTML_FRAGMENT, 0)
    assert result > 0


_STATIC_PATTERN_COMPILED = re.compile(r"<(\w+)")
_TAG_OPEN_STR = "<div class='foo'>"


def test_bench_regex_static_module_level(benchmark):
    """Module-level pre-compiled static pattern (best possible baseline)."""
    result = benchmark(_STATIC_PATTERN_COMPILED.match, _TAG_OPEN_STR)
    assert result is not None


def test_bench_regex_static_inline(benchmark):
    """Inline re.match with a static literal — hits re's internal cache.

    Expected to be within noise of the pre-compiled version because CPython's
    re cache avoids recompilation for repeated literal strings.
    """
    result = benchmark(re.match, r"<(\w+)", _TAG_OPEN_STR)
    assert result is not None
