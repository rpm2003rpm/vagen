"""Tests for vagen error handling and validation."""

import sys
from pathlib import Path

_TEST_DIR = Path(__file__).resolve().parent
if str(_TEST_DIR) not in sys.path:
    sys.path.insert(0, str(_TEST_DIR))

import unittest

from vagen import (
    Case,
    Cross,
    HiLevelMod,
    Integer,
    Module,
    Real,
    WaitUs,
    analysis,
)
from vagen.disciplines import Branch
from vagen.exceptions import (
    VagenNameError,
    VagenSequenceError,
    VagenTypeError,
    VagenValueError,
)


class TestErrors(unittest.TestCase):
    def test_analysis_requires_simulation_type(self):
        with self.assertRaises(VagenTypeError):
            analysis()

    def test_cross_rejects_invalid_edge(self):
        with self.assertRaises(VagenValueError):
            Cross(Real(0.5), "invalid")

    def test_bus_slice_requires_bounds(self):
        mod = HiLevelMod("tb")
        bus = mod.vdc("pins", 4, direction="output")
        with self.assertRaises(VagenValueError):
            bus[4:0]
        with self.assertRaises(VagenValueError):
            bus[None:0]

    def test_empty_sequence_is_rejected(self):
        mod = HiLevelMod("tb")
        with self.assertRaises(VagenValueError):
            mod.seq(True)()

    def test_wait_us_outside_sequence_raises(self):
        with self.assertRaises(VagenSequenceError):
            WaitUs(10).getVA(0)

    def test_mark_outside_sequence_raises(self):
        mod = HiLevelMod("tb")
        marker = mod.marker("seq1")
        mark = marker.mark("EVENT")
        with self.assertRaises(VagenSequenceError):
            mark.getVA(0)

    def test_case_inside_sequence_raises(self):
        mod = HiLevelMod("tb")
        state = mod.var(0)
        with self.assertRaises(VagenSequenceError):
            mod.seq(True)(
                Case(state)((Integer(1), state.eq(1))),
            )

    def test_branch_as_ground_reference_is_rejected(self):
        mod = HiLevelMod("tb")
        pos = mod.electrical("pos", 1, direction="inout")
        neg = mod.electrical("neg", 1, direction="inout")
        with self.assertRaises(VagenTypeError):
            mod.vdc("VOUT", 1, gnd=Branch(pos, neg))

    def test_module_var_rejects_invalid_type(self):
        mod = Module("test")
        with self.assertRaises(VagenTypeError):
            mod.var(vType=str)

    def test_duplicate_identifier_is_rejected(self):
        mod = Module("test")
        mod.var(name="shared")
        with self.assertRaises(VagenNameError):
            mod.var(name="shared")

    def test_unsigned_bus_read_width_limit(self):
        mod = HiLevelMod("tb")
        domain = mod.vdc("VDD", 1, direction="output")
        bus = mod.dig(domain, "DATA", 32, direction="input")
        with self.assertRaises(VagenValueError):
            bus.read(signed=False)

    def test_integer_rejects_out_of_range(self):
        with self.assertRaises(VagenValueError):
            Integer(2147483648)
        with self.assertRaises(VagenValueError):
            Integer(-2147483649)
        with self.assertRaises(VagenValueError):
            Integer(2147483648.0)

    def test_par_rejects_bool(self):
        mod = Module("test")
        with self.assertRaises(VagenTypeError):
            mod.par(True, "flag")

    def test_wide_bus_write_rejects_integer_expression(self):
        mod = HiLevelMod("tb")
        domain = mod.vdc("VDD", 1, direction="output")
        bus = mod.dig(
            domain, "DATA", 33, value=0, direction="output",
            rise=100e-12, fall=100e-12,
        )
        counter = mod.var(name="counter")
        with self.assertRaises(VagenValueError):
            bus.write(counter)


if __name__ == "__main__":
    unittest.main()
