## @package test
# 
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    24/02/23 01:05:02
#
#  #LICENSE# 
#    
#  Copyright (c) 2023 Rodrigo Pedroso Mendes
#
#  Permission is hereby granted, free of charge, to any  person   obtaining  a 
#  copy of this software and associated  documentation files (the "Software"), 
#  to deal in the Software without restriction, including  without  limitation 
#  the rights to use, copy, modify,  merge,  publish,  distribute, sublicense, 
#  and/or sell copies of the Software, and  to  permit  persons  to  whom  the 
#  Software is furnished to do so, subject to the following conditions:        
#   
#  The above copyright notice and this permission notice shall be included  in 
#  all copies or substantial portions of the Software.                         
#   
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,  EXPRESS OR 
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY, 
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#  AUTHORS OR COPYRIGHT HOLDERS BE  LIABLE FOR ANY  CLAIM,  DAMAGES  OR  OTHER 
#  LIABILITY, WHETHER IN AN ACTION OF  CONTRACT, TORT  OR  OTHERWISE,  ARISING 
#  FROM, OUT OF OR IN CONNECTION  WITH  THE  SOFTWARE  OR  THE  USE  OR  OTHER  
#  DEALINGS IN THE SOFTWARE. 
#    
################################################################################
import sys
sys.path.insert(0, "../")
import unittest
from vagen import *


class TestHiLevelMod(unittest.TestCase):



    ############################################################################
    # Real
    ############################################################################
    def testReals(self):  
        mod = HiLevelMod("tb")
        #Create an integer variable that will be initialized to 9
        var1 = mod.var(Integer(9))
        #Create a real parameter called TEST_SEQ_PARAM. Initial value is 0.
        tSeq = mod.par(0, "TEST_SEQ_PARAM")
        #Create a real parameter called parameter 1. Initial value is 0.
        par2 = mod.par(Real(0), "parameter1")
        #Create a source measure unit bus
        smu1 = mod.smu("pin1", 3, direction = "inout")
        #Create a source measure unit pin
        smu2 = mod.smu("pin2", 1, direction = "inout")
        #Create a voltage source bus
        vdc1 = mod.vdc("pin3", 3, direction = "output")
        #Create a voltage source pin
        vdc2 = mod.vdc("pin4", 1, direction = "output")
        #Create a current source bus
        idc1 = mod.idc("pin5", 3, direction = "output")
        #Create a current source pin
        idc2 = mod.idc("pin6", 1, direction = "output")
        #Create an electrical pin (No base model atached to it)
        pin7 = mod.electrical("pin7", 1, direction = "inout")
        #Create a digital input bus of width = 3. vdc2 will be the domain.
        dig1 = mod.dig(vdc2, "pin8",  3, direction = "input")
        #Create a digital input pin. vdc2 will be the domain.
        dig2 = mod.dig(vdc2, "pin9",  1, direction = "input")
        #Create a digital output bus of width = 3. vdc2 will be the domain.
        dig3 = mod.dig(vdc2, "pin10", 3, direction = "output")
        #Create a digital output pin. vdc2 will be the domain.
        dig4 = mod.dig(vdc2, "pin11", 1, direction = "output")
        #Create a ditial inout bus of width = 3. vdc2 will be the domain
        dig5 = mod.dig(vdc2, "pin12", 3, direction = "inout")
        #Create a digital inout pin. vdc2 will be the domain.
        dig6 = mod.dig(vdc2, "pin13", 1, direction = "inout")
        #Create an electrical pin (No base model atached to it)
        pin14 = mod.electrical("pin14", 1, direction = "inout")
        #Create a cross at 0.5 event based on the voltage of pin7 for both edges
        evnt1 = Cross(pin7.v - Real(0.5), "both")
        #Create a switch between pin7 and pin14. Initial conductance will be 10mS
        sw = mod.sw(pin7, pin14, Real(10e-3))
        #Create a clock source using the dig4 pin
        clk = mod.clock(dig4)
        #Create a marker for the first sequence. The MARK pin will be toggled at every mark.  
        marker = mod.marker("seq1")
        #First test sequence. This sequence will be run when TEST_SEQ_PARAM is equal to 1
        mod.seq(tSeq == 1)(
            #Apply 2V on pin1[2:0] current limited to 10mA
            smu1.applyV(Real(2), Real(10e-3)),
            #Wait 100us
            WaitUs(Real(100)),
            #Apply -20mA on pin1[2:0] voltage limited to 5V
            smu1.applyI(Real(-20e-3), Real(5)),
            #Wait 100us
            WaitUs(Real(100)),
            #configure pin1[2:0] as a 1Ohm resistor
            smu1.applyR(Real(1)),
            #Wait 100us
            WaitUs(Real(100)),
            #Apply 2V on pin1[1:0] current limited to 10mA
            smu1[1:0].applyV(Real(2), Real(10e-3)),
            #Wait 100us
            WaitUs(Real(100)),
            #Apply -20mA on pin2 voltage limited to 5V
            smu2.applyI(Real(-20e-3), Real(5)),
            #Wait 100us
            WaitUs(Real(100)),
            #Mark the end of the smu test by toggling the MARK pin
            marker.mark("END_SMU_TEST"),
            #Configure both the rise and the fall time of pin3[2:0] as 30us
            vdc1.setRiseFall(Real(30e-6), Real(30e-6)),
            #Apply 2V to pin3[2:0]
            vdc1.applyV(Real(2)),
            #Wait 100us
            WaitUs(Real(100)),
            #Apply 0V to pin3[1]
            vdc1[1].applyV(Real(0)),    
            #Wait 100us
            WaitUs(Real(100)),
            #Apply 2V to pin4
            vdc2.applyV(Real(2)),
            #Wait 100us
            WaitUs(Real(100)),
            #Mark the end of the vdc test by toggling the MARK pin
            marker.mark("END_VDC_TEST"),
            #Configure both the rise and the fall time of pin5[2:0] as 30us
            idc1.setRiseFall(Real(50e-6), Real(50e-6)),
            #Apply -10mA to pin5[2:0]
            idc1.applyI(Real(-10e-3)),
            #Wait 100us
            WaitUs(Real(100)),
            #Apply 0A to pin5[2:1]
            idc1[2:1].applyI(Real(0)),
            #Wait 100us
            WaitUs(Real(100)),
            #Apply -20mA to pin6
            idc2.applyI(Real(-20e-3)),
            #Wait 100us
            WaitUs(Real(100)),
            #Mark the end of the idc test by toggling the MARK pin
            marker.mark("END_IDC_TEST"),
            #Wait 100us
            WaitUs(Real(100)),
            Finish()
        )
        #Create a marker for the second sequence. The MARK pin will be toggled at every mark.  
        marker = mod.marker("seq2")
        #Second test sequence. This sequence will be run when TEST_SEQ_PARAM is equal to 2
        mod.seq(tSeq == 2)(
            #Apply 2V to pin4 in order to rise the domain of the digital pins
            vdc2.applyV(Real(2)),
            #Wait 100us
            WaitUs(Real(100)),
            #Write true to pin11
            dig4.write(Bool(True)),
            #Wait 100us
            WaitUs(Real(100)),
            #Configure both pin12[2:0] and pin13 as highz
            dig5.hiZ(),
            dig6.hiZ(),
            #Wait for the event1 (cross 0.5 based on the voltage of pin7 for both edges)
            WaitSignal(evnt1),       
            #Configure both pin12[2:0] and pin13 as lowZ
            dig5.lowZ(),
            dig6.lowZ(),  
            #Write True to pin13
            dig6.write(Bool(True)),
            #Write 5 to pin12
            dig5.write(Integer(5)),
            #Enable clock with a frequency of 100kHz
            clk.on(Real(100e3)),
            #Set the conductance of the switch to 0
            sw.setCond(Real(0)),
            #Wait 100us
            WaitUs(Real(200)),            
            Finish()
        )
        f = open("v1_ref.txt", "r")
        ref = f.read()
        f.close
        f = open("v1_gen.va", "w")
        f.write(mod.getVA())
        f.close   
        self.maxDiff = None
        self.assertEqual(mod.getVA()[323:], ref[:-1])     
         
        
    ############################################################################
    # Constants
    ############################################################################
    def testCtes(self): 
    
        #Create a module     
        mod = HiLevelMod("tb")
        #Create an integer variable that will be initialized to 9
        var1 = mod.var(9)
        #Create a real parameter called TEST_SEQ_PARAM. Initial value is 0.
        tSeq = mod.par(0, "TEST_SEQ_PARAM")
        #Create a real parameter called parameter 1. Initial value is 0.
        par2 = mod.par(0.0, "parameter1")
        #Create a source measure unit bus
        smu1 = mod.smu("pin1", 3, direction = "inout")
        #Create a source measure unit pin
        smu2 = mod.smu("pin2", 1, direction = "inout")
        #Create a voltage source bus
        vdc1 = mod.vdc("pin3", 3, direction = "output")
        #Create a voltage source pin
        vdc2 = mod.vdc("pin4", 1, direction = "output")
        #Create a current source bus
        idc1 = mod.idc("pin5", 3, direction = "output")
        #Create a current source pin
        idc2 = mod.idc("pin6", 1, direction = "output")
        #Create an electrical pin (No base model atached to it)
        pin7 = mod.electrical("pin7", 1, direction = "inout")
        #Create a digital input bus of width = 3. vdc2 will be the domain.
        dig1 = mod.dig(vdc2, "pin8",  3, direction = "input")
        #Create a digital input pin. vdc2 will be the domain.
        dig2 = mod.dig(vdc2, "pin9",  1, direction = "input")
        #Create a digital output bus of width = 3. vdc2 will be the domain.
        dig3 = mod.dig(vdc2, "pin10", 3, direction = "output")
        #Create a digital output pin. vdc2 will be the domain.
        dig4 = mod.dig(vdc2, "pin11", 1, direction = "output")
        #Create a ditial inout bus of width = 3. vdc2 will be the domain
        dig5 = mod.dig(vdc2, "pin12", 3, direction = "inout")
        #Create a digital inout pin. vdc2 will be the domain.
        dig6 = mod.dig(vdc2, "pin13", 1, direction = "inout")
        #Create an electrical pin (No base model atached to it)
        pin14 = mod.electrical("pin14", 1, direction = "inout")
        #Create a cross at 0.5 event based on the voltage of pin7 for both edges
        evnt1 = Cross(pin7.v - 0.5, "both")
        #Create a switch between pin7 and pin14. Initial conductance will be 10mS
        sw = mod.sw(pin7, pin14, 10e-3)
        #Create a clock source using the dig4 pin
        clk = mod.clock(dig4)
        #Create a marker for the first sequence. The MARK pin will be toggled at every mark.  
        marker = mod.marker("seq1")
        #First test sequence. This sequence will be run when TEST_SEQ_PARAM is equal to 1
        mod.seq(tSeq == 1)(
            #Apply 2V on pin1[2:0] current limited to 10mA
            smu1.applyV(2, 10e-3),
            #Wait 100us
            WaitUs(100),
            #Apply -20mA on pin1[2:0] voltage limited to 5V
            smu1.applyI(-20e-3, 5),
            #Wait 100us
            WaitUs(100),
            #configure pin1[2:0] as a 1Ohm resistor
            smu1.applyR(1),
            #Wait 100us
            WaitUs(100),
            #Apply 2V on pin1[1:0] current limited to 10mA
            smu1[1:0].applyV(2, 10e-3),
            #Wait 100us
            WaitUs(100),
            #Apply -20mA on pin2 voltage limited to 5V
            smu2.applyI(-20e-3, 5),
            #Wait 100us
            WaitUs(100),
            #Mark the end of the smu test by toggling the MARK pin
            marker.mark("END_SMU_TEST"),
            #Configure both the rise and the fall time of pin3[2:0] as 30us
            vdc1.setRiseFall(30e-6, 30e-6),
            #Apply 2V to pin3[2:0]
            vdc1.applyV(2),
            #Wait 100us
            WaitUs(100),
            #Apply 0V to pin3[1]
            vdc1[1].applyV(2),    
            #Wait 100us
            WaitUs(100),
            #Apply 2V to pin4
            vdc2.applyV(2),
            #Wait 100us
            WaitUs(100),
            #Mark the end of the vdc test by toggling the MARK pin
            marker.mark("END_VDC_TEST"),
            #Configure both the rise and the fall time of pin5[2:0] as 30us
            idc1.setRiseFall(50e-6, 50e-6),
            #Apply -10mA to pin5[2:0]
            idc1.applyI(-10e-3),
            #Wait 100us
            WaitUs(100),
            #Apply 0A to pin5[2:1]
            idc1[2:1].applyI(2),
            #Wait 100us
            WaitUs(100),
            #Apply -20mA to pin6
            idc2.applyI(-20e-3),
            #Wait 100us
            WaitUs(100),
            #Mark the end of the idc test by toggling the MARK pin
            marker.mark("END_IDC_TEST"),
            #Wait 100us
            WaitUs(100),
            Finish()
        )
        #Create a marker for the second sequence. The MARK pin will be toggled at every mark.  
        marker = mod.marker("seq2")
        #Second test sequence. This sequence will be run when TEST_SEQ_PARAM is equal to 2
        mod.seq(tSeq == 2)(
            #Apply 2V to pin4 in order to rise the domain of the digital pins
            vdc2.applyV(2),
            #Wait 100us
            WaitUs(100),
            #Write true to pin11
            dig4.write(True),
            #Wait 100us
            WaitUs(100),
            #Configure both pin12[2:0] and pin13 as highz
            dig5.hiZ(),
            dig6.hiZ(),
            #Wait for the event1 (cross 0.5 based on the voltage of pin7 for both edges)
            WaitSignal(evnt1),       
            #Configure both pin12[2:0] and pin13 as lowZ
            dig5.lowZ(),
            dig6.lowZ(),  
            #Write True to pin13
            dig6.write(True),
            #Write 5 to pin12
            dig5.write(5),
            #Enable clock with a frequency of 100kHz
            clk.on(100e3),
            #Set the conductance of the switch to 0
            sw.setCond(0),
            #Wait 100us
            WaitUs(200),            
            Finish()
        )
        
        f = open("v2_ref.txt", "r")
        ref = f.read()
        f.close
        f = open("v2_gen.va", "w")
        f.write(mod.getVA())
        f.close    
        self.maxDiff = None
        self.assertEqual(mod.getVA()[323:], ref[:-1])    
 
    ############################################################################
    # Constants
    ############################################################################
    def testRepeat(self):    
        mod = HiLevelMod("tb")
        #Create an integer variable that will be initialized to 9
        var1 = mod.var(Integer(9))
        #Create an electrical pin (No base model atached to it)
        pin7 = mod.electrical("pin7", 1, direction = "inout")
        #Create a cross at 0.5 event based on the voltage of pin7 for both edges
        evnt1 = Cross(pin7.v - Real(0.5), "both")
        mod.seq(True)(
            var1.eq(0),
            var1.eq(1),
            Repeat(10)(
                var1.eq(2),
                CmdList(
                    var1.eq(3),
                    var1.eq(4)
                )
            ),
            var1.eq(5)
        )
        #print(mod.getVA())
        mod = HiLevelMod("tb")
        #Create an integer variable that will be initialized to 9
        var1 = mod.var(Integer(9))
        #Create an electrical pin (No base model atached to it)
        pin7 = mod.electrical("pin7", 1, direction = "inout")
        #Create a cross at 0.5 event based on the voltage of pin7 for both edges
        evnt1 = Cross(pin7.v - Real(0.5), "both")
        mod.seq(True)(
            var1.eq(0),
            WaitUs(100),
            var1.eq(1),
            WaitUs(100),
            Repeat(10)(
                WaitUs(100),
                var1.eq(2),
                WaitUs(100),
                CmdList(
                    var1.eq(3),
                    var1.eq(4)
                ),
                WaitUs(100),
            ),
            WaitUs(100),
            var1.eq(5)
        )
        #print(mod.getVA())
        mod = HiLevelMod("tb")
        #Create an integer variable that will be initialized to 9
        var1 = mod.var(Integer(9))
        #Create an electrical pin (No base model atached to it)
        pin7 = mod.electrical("pin7", 1, direction = "inout")
        #Create a cross at 0.5 event based on the voltage of pin7 for both edges
        evnt1 = Cross(pin7.v - Real(0.5), "both")
        mod.seq(True)(
            var1.eq(0),
            WaitUs(100),
            var1.eq(1),
            WaitSignal(evnt1 | evnt1),
            Repeat(10)(
                Repeat(11)(
                    var1.eq(2),
                    WaitSignal(evnt1),
                ),
                CmdList(
                    var1.eq(3),
                    var1.eq(4)
                ),
                WaitUs(100),
                var1.eq(6)
            ),
            WaitUs(100),
            var1.eq(5)
        )
        mod.seq(True)(
            var1.eq(0),
            While(var1 > 10) (
                var1.eq(2),
                WaitUs(50),
            ),
            For(var1.eq(11), var1 < 11, var1.eq(var1 + 14))(
                var1.eq(22),
                WaitUs(50),
            ) 
        )
        mod.seq(True)(
            var1.eq(0),
            WaitUs(50),
            If(var1 > 10)(
                var1.eq(2),
                WaitUs(40),
                var1.eq(3),
                WaitUs(33),
                var1.eq(33),
                WaitSignal(evnt1)              
            ).Else(
                var1.eq(4),
                WaitUs(44),
                var1.eq(5),
                WaitUs(22),
                var1.eq(55)
            ),
            var1.eq(555),
            WaitUs(50)
        )
                
        #print(mod.getVA())
                                                                                                                                                        
if __name__ == '__main__':
    unittest.main()
    

