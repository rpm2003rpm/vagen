"""Shared helpers for vagen golden-file tests."""

from pathlib import Path

VA_BODY_MARKER = '`include "constants.vams"'


def strip_va_header(va: str) -> str:
    """Return Verilog-A output without the generated date header block."""
    idx = va.find(VA_BODY_MARKER)
    if idx == -1:
        raise ValueError(
            "Verilog-A output is missing the expected include header "
            f"({VA_BODY_MARKER!r})"
        )
    return va[idx:]


def load_ref(filename: str) -> str:
    """Load a reference file from the tests directory."""
    return (Path(__file__).parent / filename).read_text(encoding="utf-8").rstrip("\n")


def assert_va_matches_ref(test_case, mod, ref_filename: str) -> None:
    """Assert module output matches a reference file, ignoring the date header."""
    test_case.maxDiff = None
    expected = load_ref(ref_filename)
    actual = strip_va_header(mod.getVA())
    test_case.assertEqual(actual, expected)
