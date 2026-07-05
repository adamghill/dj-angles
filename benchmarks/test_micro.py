"""Micro-benchmarks for specific potential optimisations in dj-angles.

Each finding has two variants — current vs proposed — so the numbers
directly answer "is this change worth it?".

Run with:
    uv run pytest benchmarks/test_micro.py --benchmark-only -v
"""

from __future__ import annotations

from functools import cache
from io import StringIO

from django.conf import settings

# ---------------------------------------------------------------------------
# Finding 1: get_setting() called inside a per-tag loop
#
# get_setting() does a hasattr + dict lookup on settings.ANGLES on every call.
# In replace_tags, `slots_enabled` and `initial_tag_regex` are read inside
# the finditer loop — once per matched tag. Two more settings are read in
# Tag.__init__ (`lower_case_tag`, `kebab_case_tag`) — also per tag.
# Hoisting all four out of the loop is a trivial one-liner each.
# ---------------------------------------------------------------------------

_N_TAGS = 20  # realistic number of tags in a template


def _get_setting_current(setting_name: str, default=None):
    if not hasattr(settings, "ANGLES"):
        settings.ANGLES = {}
    data = settings.ANGLES
    return data.get(setting_name, default)


def _get_setting_hoisted_result(default=None):
    """Simulates the result of hoisting: value already in a local variable."""
    return default  # pre-read value, no dict access in loop


def test_bench_get_setting_in_loop_current(benchmark):
    """get_setting() called N times (once per matched tag) — current behaviour."""

    def work():
        for _ in range(_N_TAGS):
            _ = _get_setting_current("slots_enabled", False)
            _ = _get_setting_current("initial_tag_regex", r"(dj-)")
            _ = _get_setting_current("lower_case_tag", False)
            _ = _get_setting_current("kebab_case_tag", True)

    benchmark(work)


def test_bench_get_setting_hoisted(benchmark):
    """All four settings read once before the loop — proposed behaviour."""

    def work():
        slots_enabled = _get_setting_current("slots_enabled", False)
        initial_tag_regex = _get_setting_current("initial_tag_regex", r"(dj-)")
        lower_case_tag = _get_setting_current("lower_case_tag", False)
        kebab_case_tag = _get_setting_current("kebab_case_tag", True)

        for _ in range(_N_TAGS):
            _ = slots_enabled
            _ = initial_tag_regex
            _ = lower_case_tag
            _ = kebab_case_tag

    benchmark(work)


# ---------------------------------------------------------------------------
# Finding 2: token += c string concatenation in yield_tokens
#
# Each character append creates a new str object. A list accumulator + join
# avoids repeated allocation for longer attribute strings.
# Tested on a realistic attribute string length (30-char tag args).
# ---------------------------------------------------------------------------

_ATTR_STRING = "template='partials/my-card.html' with title='Hello' class='foo'"


def _tokenize_concat(s: str, breaking_character: str):
    """Current: string concatenation."""
    token = ""
    for c in s:
        if c == breaking_character:
            yield token
            token = ""
        else:
            token += c
    if token:
        yield token


def _tokenize_list(s: str, breaking_character: str):
    """Proposed: list accumulator + join."""
    parts: list[str] = []
    for c in s:
        if c == breaking_character:
            yield "".join(parts)
            parts = []
        else:
            parts.append(c)
    if parts:
        yield "".join(parts)


def test_bench_tokenize_concat(benchmark):
    """yield_tokens inner loop using token += c (current)."""
    benchmark(lambda: list(_tokenize_concat(_ATTR_STRING, " ")))


def test_bench_tokenize_list(benchmark):
    """yield_tokens inner loop using list + join (proposed)."""
    benchmark(lambda: list(_tokenize_list(_ATTR_STRING, " ")))


# ---------------------------------------------------------------------------
# Finding 3: Attributes.__str__ O(n²) string build
#
# Current: s = f"{s} {attribute}" in a loop — quadratic for large attr counts.
# Proposed: " ".join(...)
# Tested with a realistic number of attributes (5).
# ---------------------------------------------------------------------------

_ATTR_VALUES = ["template='foo.html'", "with", "title='Hello'", "class='bar'", "id='baz'"]


def _str_current(attrs):
    s = ""
    for a in attrs:
        s = f"{s} {a}"
    return s.strip()


def _str_join(attrs):
    return " ".join(attrs)


def test_bench_attrs_str_current(benchmark):
    """Attributes.__str__ via f-string loop concatenation (current)."""
    benchmark(_str_current, _ATTR_VALUES)


def test_bench_attrs_str_join(benchmark):
    """Attributes.__str__ via str.join (proposed)."""
    benchmark(_str_join, _ATTR_VALUES)


# ---------------------------------------------------------------------------
# Finding 4: Attributes.__getitem__ / pop materialise a full list each call
#
# list(self._attributes.keys())[index] and list(self._attributes.values())[index]
# allocate a throw-away list every access. next(iter(...)) avoids the allocation
# for index=0 (the only value used in practice).
# ---------------------------------------------------------------------------

_SAMPLE_DICT = {f"key{i}": f"val{i}" for i in range(5)}


def _getitem_list(d: dict, index: int):
    """Current: materialise full list."""
    return list(d.values())[index]


def _getitem_iter(d: dict):
    """Proposed for index=0: next(iter(...))."""
    return next(iter(d.values()))


def _pop_list(d: dict, index: int):
    key = list(d.keys())[index]
    return d.pop(key)


def _pop_iter(d: dict):
    key = next(iter(d))
    return d.pop(key)


def test_bench_getitem_list(benchmark):
    """Attributes.__getitem__(0) via list(values())[0] (current)."""
    benchmark(_getitem_list, _SAMPLE_DICT.copy(), 0)


def test_bench_getitem_iter(benchmark):
    """Attributes.__getitem__(0) via next(iter(values())) (proposed)."""
    benchmark(_getitem_iter, _SAMPLE_DICT.copy())


def test_bench_pop_list(benchmark):
    """Attributes.pop(0) via list(keys())[0] (current)."""

    def work():
        d = _SAMPLE_DICT.copy()
        return _pop_list(d, 0)

    benchmark(work)


def test_bench_pop_iter(benchmark):
    """Attributes.pop(0) via next(iter(d)) (proposed)."""

    def work():
        d = _SAMPLE_DICT.copy()
        return _pop_iter(d)

    benchmark(work)


# ---------------------------------------------------------------------------
# Finding 5: CaseConverter StringIO vs plain string iteration
#
# StringIO.read(1) has significant overhead compared to iterating the string
# directly. CaseConverter is called once per tag name during Tag.__init__.
# ---------------------------------------------------------------------------

_TAG_NAME = "my-component-with-a-long-name"


def _convert_stringio(s: str) -> str:
    """Current: read characters via StringIO.read(1)."""
    buf_in = StringIO(s)
    buf_out = StringIO()
    cc = buf_in.read(1)
    while cc:
        buf_out.write(cc.lower())
        cc = buf_in.read(1)
    return buf_out.getvalue()


def _convert_iter(s: str) -> str:
    """Proposed: iterate the string directly, accumulate into a list."""
    parts = []
    for c in s:
        parts.append(c.lower())
    return "".join(parts)


def test_bench_caseconverter_stringio(benchmark):
    """CaseConverter character loop via StringIO.read(1) (current pattern)."""
    benchmark(_convert_stringio, _TAG_NAME)


def test_bench_caseconverter_iter(benchmark):
    """CaseConverter character loop via direct string iteration (proposed)."""
    benchmark(_convert_iter, _TAG_NAME)


# ---------------------------------------------------------------------------
# Finding 6: attr_pattern built fresh each call to replace_conditionals /
#            replace_values vs cached via lru_cache on the prefix string.
# ---------------------------------------------------------------------------

_DEFAULT_PREFIX = r"(dj-)"


def _build_attr_pattern_current(prefix: str) -> str:
    return (
        rf'\s({prefix}(?:if|elif|else|endif|fi))(?:=(?:"(?P<v1>[^"]*)"|'
        r"'(?P<v2>[^']*)'"
        r"|(?P<v3>[^\s>]+)))?"
    )


@cache
def _build_attr_pattern_cached(prefix: str) -> str:
    return (
        rf'\s({prefix}(?:if|elif|else|endif|fi))(?:=(?:"(?P<v1>[^"]*)"|'
        r"'(?P<v2>[^']*)'"
        r"|(?P<v3>[^\s>]+)))?"
    )


def test_bench_attr_pattern_current(benchmark):
    """attr_pattern rebuilt from scratch on every replace_conditionals call (current)."""
    benchmark(_build_attr_pattern_current, _DEFAULT_PREFIX)


def test_bench_attr_pattern_cached(benchmark):
    """attr_pattern retrieved from lru_cache (proposed)."""
    benchmark(_build_attr_pattern_cached, _DEFAULT_PREFIX)
