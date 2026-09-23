"""Integration tests for README examples."""

import tempfile
import unittest
from pathlib import Path

import vagen as va
from helpers import strip_va_header


def build_readme_example_1():
    """Build the DCDC stimulus example shown in README Example 1."""
    mod = va.HiLevelMod("DCDC_STML")

    vdd = mod.vdc("VDD", 1, direction="inout")
    out = mod.idc("OUT", 1, direction="inout")
    clk = mod.clock(
        mod.dig(vdd, "CLK", 1, direction="output", rise=100e-12, fall=100e-12)
    )
    rst = mod.dig(
        vdd, "RST", 1, value=0, direction="output", rise=100e-12, fall=100e-12
    )
    ready = mod.dig(vdd, "READY", 1, direction="input")
    config_vout = mod.dig(
        vdd,
        "CONFIG_VOUT",
        4,
        value=0,
        direction="output",
        rise=100e-12,
        fall=100e-12,
    )

    evnt_ready = va.Cross(ready.diffHalfDomain, "rising")

    mod.seq(True)(
        vdd.setRiseFall(10e-6, 10e-6),
        vdd.applyV(5.0),
        va.WaitUs(10),
        clk.on(4e6),
        va.WaitUs(1),
        rst.write(True),
        va.WaitSignal(evnt_ready),
        out.setRiseFall(100e-9, 100e-9),
        out.applyI(100e-3),
        va.WaitUs(10),
        config_vout.write(5),
        va.WaitUs(20),
        va.Finish(),
    )
    return mod


def build_readme_example_2():
    """Build the multi-sequence example shown in README Example 2."""
    mod = va.HiLevelMod("MULTI_SEQ")
    vdd = mod.vdc("VDD", 1, direction="output")
    seq_par = mod.par(0, "testSeq")

    mod.seq(seq_par == 1)(
        vdd.applyV(1.0),
        va.Finish(),
    )
    mod.seq(seq_par == 2)(
        vdd.applyV(2.0),
        va.Finish(),
    )
    return mod


def build_readme_example_3():
    """Build the configurable resistor model shown in README Example 3."""
    mod = va.HiLevelMod("CONFIG_RES")

    vdd = mod.electrical("VDD", 1, direction="inout")
    in1 = mod.electrical("IN1", 1, direction="inout")
    in2 = mod.electrical("IN2", 1, direction="inout")
    config = mod.dig(
        vdd, "CONFIG", 4, inCap=100e-15, direction="input"
    )
    alfa = mod.par(10.0, "alfa")

    branch = va.Branch(in1, in2)
    mod.analog(
        branch.vCont(
            branch.i
            * (va.Real(config.read(signed=False)) + 1)
            * alfa
        )
    )
    return mod


class TestReadmeExamples(unittest.TestCase):
    def test_readme_example_1_generates_veriloga(self):
        mod = build_readme_example_1()
        va_code = strip_va_header(mod.getVA())

        self.assertIn('module DCDC_STML(', va_code)
        self.assertIn("VDD", va_code)
        self.assertIn("CLK", va_code)
        self.assertIn("CONFIG_VOUT", va_code)
        self.assertIn("cross(", va_code)
        self.assertIn("_$runSt_1", va_code)

    def test_readme_example_2_generates_veriloga(self):
        mod = build_readme_example_2()
        va_code = strip_va_header(mod.getVA())

        self.assertIn('module MULTI_SEQ(', va_code)
        self.assertIn("parameter integer testSeq", va_code)
        self.assertIn("_$runSt_1", va_code)
        self.assertIn("_$runSt_2", va_code)

    def test_readme_example_3_generates_veriloga(self):
        mod = build_readme_example_3()
        va_code = strip_va_header(mod.getVA())

        self.assertIn('module CONFIG_RES(', va_code)
        self.assertIn("parameter real alfa", va_code)
        self.assertIn("CONFIG", va_code)
        self.assertIn("analog begin", va_code)

    def test_writeVa_writes_file(self):
        mod = build_readme_example_1()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.va"
            mod.writeVa(path)
            content = path.read_text(encoding="utf-8")
            self.assertIn("module DCDC_STML(", content)


if __name__ == "__main__":
    unittest.main()
