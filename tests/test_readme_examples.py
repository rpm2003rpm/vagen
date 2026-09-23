"""Integration tests for README examples."""

import tempfile
import unittest
from pathlib import Path

import vagen as va
from helpers import strip_va_header


def build_readme_example_1():
    """Build the DCDC stimulus example shown in README Example 1."""
    
    #Create a module     
    mod = va.HiLevelMod("DCDC_STML")
    #Create pins
    VDD = mod.vdc(name = "VDD", width = 1, direction = "inout")
    OUT = mod.idc(name = "OUT", width = 1, direction = "inout")
    CLK = mod.clock(mod.dig(name = "CLK", domain = VDD, width = 1, direction = "output", rise = 100e-12, fall = 100e-12))
    RST = mod.dig(name = "RST", domain = VDD, width = 1, value = 0, direction = "output", rise = 100e-12, fall = 100e-12)
    READY = mod.dig(name = "READY", domain = VDD, width = 1, direction = "input")
    CONFIG_VOUT = mod.dig(name = "CONFIG_VOUT", domain = VDD, width = 4, value = 0, direction = "output", rise = 100e-12, fall = 100e-12)

    #READY positive event
    EVNT_READY = va.Cross(READY.diffHalfDomain, "rising")

    #Sequence
    mod.seq(True)(
        VDD.setRiseFall(10e-6, 10e-6),
        VDD.applyV(5.0),
        va.WaitUs(10), 
        CLK.on(4e6),
        va.WaitUs(1),
        RST.write(True),
        va.WaitSignal(EVNT_READY),
        OUT.setRiseFall(100e-9, 100e-9),
        OUT.applyI(100e-3), #Positive current enters the model
        va.WaitUs(10),
        CONFIG_VOUT.write(5),
        va.WaitUs(20),
        va.Finish()
     )
    return mod


def build_readme_example_2():
    """Build the multi-sequence example shown in README Example 2."""
    mod = va.HiLevelMod("MULTI_SEQ")
    vdd = mod.vdc("VDD", 1, direction="output")
    seqPar = mod.par(name = "testSeq", value = 0)

    mod.seq(seqPar == 1)(
        vdd.applyV(1.0),
        va.Finish(),
    )
    mod.seq(seqPar == 2)(
        vdd.applyV(2.0),
        va.Finish(),
    )
    return mod


def build_readme_example_3():
    """Build the configurable resistor model shown in README Example 3."""
    #Create a module
    mod = va.HiLevelMod("CONFIG_RES")

    #Create pins
    VDD = mod.electrical(name = "VDD", width = 1, direction = "inout")
    IN1 = mod.electrical(name = "IN1", width = 1, direction = "inout")
    IN2 = mod.electrical(name = "IN2", width = 1, direction = "inout")
    CONFIG = mod.dig(name = "CONFIG", domain = VDD, width = 4, inCap = 100e-15, direction = "input")

    #Parameters
    alfa = mod.par(name = "alfa", value = 10.0)

    #Analog block
    mod.analog(
        va.Branch(IN1, IN2).vCont(va.Branch(IN1, IN2).i*(va.Real(CONFIG.read(signed = False)) + 1)*alfa)
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
