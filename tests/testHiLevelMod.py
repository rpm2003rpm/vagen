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
        evnt1 = Cross(pin7.v, Real(0.5), "both")
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
        ref = '''`include "constants.vams"
`include "disciplines.vams"

/******************************************************************************
 *                             Module declaration                             * 
 ******************************************************************************/
module tb(pin1,
          pin2,
          pin3,
          pin4,
          pin5,
          pin6,
          pin7,
          pin8,
          pin9,
          pin10,
          pin11,
          pin12,
          pin13,
          pin14,
          MARK_seq1,
          MARK_seq2);

/******************************************************************************
 *                                   Ports                                    * 
 ******************************************************************************/
inout [2:0] pin1;
inout pin2;
output [2:0] pin3;
output pin4;
output [2:0] pin5;
output pin6;
inout pin7;
input [2:0] pin8;
input pin9;
output [2:0] pin10;
output pin11;
inout [2:0] pin12;
inout pin13;
inout pin14;
output MARK_seq1;
output MARK_seq2;

/******************************************************************************
 *                                 Disciplines                                * 
 ******************************************************************************/
electrical [2:0] pin1;
electrical pin2;
electrical [2:0] pin3;
electrical pin4;
electrical [2:0] pin5;
electrical pin6;
electrical pin7;
electrical [2:0] pin8;
electrical pin9;
electrical [2:0] pin10;
electrical pin11;
electrical [2:0] pin12;
electrical _$3;
electrical _$4;
electrical _$5;
electrical pin13;
electrical _$6;
electrical pin14;
electrical MARK_seq1;
electrical MARK_seq2;

/******************************************************************************
 *                                 Parameters                                 * 
 ******************************************************************************/
parameter integer TEST_SEQ_PARAM = 0;
parameter real parameter1 = 0.000000e+00;

/******************************************************************************
 *                                 Variables                                  * 
 ******************************************************************************/
integer _$1;
integer _$2;
real pin1_$0$_$volt$;
real pin1_$0$_$maxCur;
real pin1_$0$_$minCur$;
real pin1_$0$_$res$;
real pin1_$0$_$vDelay$;
real pin1_$0$_$iDelay$;
real pin1_$0$_$rDelay$;
real pin1_$0$_$riseFall$;
real pin1_$0$_$voltTran$;
real pin1_$0$_$maxCurTran$;
real pin1_$0$_$minCurTran$;
real pin1_$0$_$resTran$;
real pin1_$1$_$volt$;
real pin1_$1$_$maxCur;
real pin1_$1$_$minCur$;
real pin1_$1$_$res$;
real pin1_$1$_$vDelay$;
real pin1_$1$_$iDelay$;
real pin1_$1$_$rDelay$;
real pin1_$1$_$riseFall$;
real pin1_$1$_$voltTran$;
real pin1_$1$_$maxCurTran$;
real pin1_$1$_$minCurTran$;
real pin1_$1$_$resTran$;
real pin1_$2$_$volt$;
real pin1_$2$_$maxCur;
real pin1_$2$_$minCur$;
real pin1_$2$_$res$;
real pin1_$2$_$vDelay$;
real pin1_$2$_$iDelay$;
real pin1_$2$_$rDelay$;
real pin1_$2$_$riseFall$;
real pin1_$2$_$voltTran$;
real pin1_$2$_$maxCurTran$;
real pin1_$2$_$minCurTran$;
real pin1_$2$_$resTran$;
real pin2_$volt$;
real pin2_$maxCur;
real pin2_$minCur$;
real pin2_$res$;
real pin2_$vDelay$;
real pin2_$iDelay$;
real pin2_$rDelay$;
real pin2_$riseFall$;
real pin2_$voltTran$;
real pin2_$maxCurTran$;
real pin2_$minCurTran$;
real pin2_$resTran$;
real pin3_$0$_$value$;
real pin3_$0$_$rise$;
real pin3_$0$_$fall$;
real pin3_$1$_$value$;
real pin3_$1$_$rise$;
real pin3_$1$_$fall$;
real pin3_$2$_$value$;
real pin3_$2$_$rise$;
real pin3_$2$_$fall$;
real pin4_$value$;
real pin4_$rise$;
real pin4_$fall$;
real pin5_$0$_$value$;
real pin5_$0$_$rise$;
real pin5_$0$_$fall$;
real pin5_$1$_$value$;
real pin5_$1$_$rise$;
real pin5_$1$_$fall$;
real pin5_$2$_$value$;
real pin5_$2$_$rise$;
real pin5_$2$_$fall$;
real pin6_$value$;
real pin6_$rise$;
real pin6_$fall$;
real pin8_$0$_$inCap$;
real pin8_$1$_$inCap$;
real pin8_$2$_$inCap$;
real pin9_$inCap$;
integer pin10_$0$_$state$;
real pin10_$0$_$serRes$;
real pin10_$0$_$delay$;
real pin10_$0$_$rise$;
real pin10_$0$_$fall$;
integer pin10_$1$_$state$;
real pin10_$1$_$serRes$;
real pin10_$1$_$delay$;
real pin10_$1$_$rise$;
real pin10_$1$_$fall$;
integer pin10_$2$_$state$;
real pin10_$2$_$serRes$;
real pin10_$2$_$delay$;
real pin10_$2$_$rise$;
real pin10_$2$_$fall$;
integer pin11_$state$;
real pin11_$serRes$;
real pin11_$delay$;
real pin11_$rise$;
real pin11_$fall$;
integer pin12_$0$_$state$;
real pin12_$0$_$serRes$;
real pin12_$0$_$inCap$;
real pin12_$0$_$res$;
real pin12_$0$_$delay$;
real pin12_$0$_$rise$;
real pin12_$0$_$fall$;
integer pin12_$1$_$state$;
real pin12_$1$_$serRes$;
real pin12_$1$_$inCap$;
real pin12_$1$_$res$;
real pin12_$1$_$delay$;
real pin12_$1$_$rise$;
real pin12_$1$_$fall$;
integer pin12_$2$_$state$;
real pin12_$2$_$serRes$;
real pin12_$2$_$inCap$;
real pin12_$2$_$res$;
real pin12_$2$_$delay$;
real pin12_$2$_$rise$;
real pin12_$2$_$fall$;
integer pin13_$state$;
real pin13_$serRes$;
real pin13_$inCap$;
real pin13_$res$;
real pin13_$delay$;
real pin13_$rise$;
real pin13_$fall$;
real sw1_$cond$;
real sw1_$rise$;
real sw1_$fall$;
integer clk1_$out$;
integer clk1_$isOn$;
real clk1_$halfPeriod$;
real clk1_$time$;
integer _$markSt_seq1;
real _$evntTime_1;
integer _$state_1;
integer _$runSt_1;
integer _$eventId_1;
integer _$markSt_seq2;
real _$evntTime_2;
integer _$state_2;
integer _$runSt_2;
integer _$eventId_2;

/******************************************************************************
 *                                Analog block                                * 
 ******************************************************************************/
analog begin
    if( analysis("static") ) begin
        _$1 = 0;
        _$2 = 9;
        pin1_$0$_$volt$ = 0.000000e+00;
        pin1_$0$_$maxCur = 0.000000e+00;
        pin1_$0$_$minCur$ = 0.000000e+00;
        pin1_$0$_$res$ = 1.000000e+12;
        pin1_$0$_$vDelay$ = 0.000000e+00;
        pin1_$0$_$iDelay$ = 0.000000e+00;
        pin1_$0$_$rDelay$ = 0.000000e+00;
        pin1_$0$_$riseFall$ = 1.000000e-06;
        pin1_$0$_$voltTran$ = 0.000000e+00;
        pin1_$0$_$maxCurTran$ = 0.000000e+00;
        pin1_$0$_$minCurTran$ = 0.000000e+00;
        pin1_$0$_$resTran$ = 0.000000e+00;
        pin1_$1$_$volt$ = 0.000000e+00;
        pin1_$1$_$maxCur = 0.000000e+00;
        pin1_$1$_$minCur$ = 0.000000e+00;
        pin1_$1$_$res$ = 1.000000e+12;
        pin1_$1$_$vDelay$ = 0.000000e+00;
        pin1_$1$_$iDelay$ = 0.000000e+00;
        pin1_$1$_$rDelay$ = 0.000000e+00;
        pin1_$1$_$riseFall$ = 1.000000e-06;
        pin1_$1$_$voltTran$ = 0.000000e+00;
        pin1_$1$_$maxCurTran$ = 0.000000e+00;
        pin1_$1$_$minCurTran$ = 0.000000e+00;
        pin1_$1$_$resTran$ = 0.000000e+00;
        pin1_$2$_$volt$ = 0.000000e+00;
        pin1_$2$_$maxCur = 0.000000e+00;
        pin1_$2$_$minCur$ = 0.000000e+00;
        pin1_$2$_$res$ = 1.000000e+12;
        pin1_$2$_$vDelay$ = 0.000000e+00;
        pin1_$2$_$iDelay$ = 0.000000e+00;
        pin1_$2$_$rDelay$ = 0.000000e+00;
        pin1_$2$_$riseFall$ = 1.000000e-06;
        pin1_$2$_$voltTran$ = 0.000000e+00;
        pin1_$2$_$maxCurTran$ = 0.000000e+00;
        pin1_$2$_$minCurTran$ = 0.000000e+00;
        pin1_$2$_$resTran$ = 0.000000e+00;
        pin2_$volt$ = 0.000000e+00;
        pin2_$maxCur = 0.000000e+00;
        pin2_$minCur$ = 0.000000e+00;
        pin2_$res$ = 1.000000e+12;
        pin2_$vDelay$ = 0.000000e+00;
        pin2_$iDelay$ = 0.000000e+00;
        pin2_$rDelay$ = 0.000000e+00;
        pin2_$riseFall$ = 1.000000e-06;
        pin2_$voltTran$ = 0.000000e+00;
        pin2_$maxCurTran$ = 0.000000e+00;
        pin2_$minCurTran$ = 0.000000e+00;
        pin2_$resTran$ = 0.000000e+00;
        pin3_$0$_$value$ = 0.000000e+00;
        pin3_$0$_$rise$ = 0.000000e+00;
        pin3_$0$_$fall$ = 0.000000e+00;
        pin3_$1$_$value$ = 0.000000e+00;
        pin3_$1$_$rise$ = 0.000000e+00;
        pin3_$1$_$fall$ = 0.000000e+00;
        pin3_$2$_$value$ = 0.000000e+00;
        pin3_$2$_$rise$ = 0.000000e+00;
        pin3_$2$_$fall$ = 0.000000e+00;
        pin4_$value$ = 0.000000e+00;
        pin4_$rise$ = 0.000000e+00;
        pin4_$fall$ = 0.000000e+00;
        pin5_$0$_$value$ = 0.000000e+00;
        pin5_$0$_$rise$ = 0.000000e+00;
        pin5_$0$_$fall$ = 0.000000e+00;
        pin5_$1$_$value$ = 0.000000e+00;
        pin5_$1$_$rise$ = 0.000000e+00;
        pin5_$1$_$fall$ = 0.000000e+00;
        pin5_$2$_$value$ = 0.000000e+00;
        pin5_$2$_$rise$ = 0.000000e+00;
        pin5_$2$_$fall$ = 0.000000e+00;
        pin6_$value$ = 0.000000e+00;
        pin6_$rise$ = 0.000000e+00;
        pin6_$fall$ = 0.000000e+00;
        pin8_$0$_$inCap$ = 1.000000e-14;
        pin8_$1$_$inCap$ = 1.000000e-14;
        pin8_$2$_$inCap$ = 1.000000e-14;
        pin9_$inCap$ = 1.000000e-14;
        pin10_$0$_$state$ = 0;
        pin10_$0$_$serRes$ = 1.000000e+02;
        pin10_$0$_$delay$ = 0.000000e+00;
        pin10_$0$_$rise$ = 1.000000e-12;
        pin10_$0$_$fall$ = 1.000000e-12;
        pin10_$1$_$state$ = 0;
        pin10_$1$_$serRes$ = 1.000000e+02;
        pin10_$1$_$delay$ = 0.000000e+00;
        pin10_$1$_$rise$ = 1.000000e-12;
        pin10_$1$_$fall$ = 1.000000e-12;
        pin10_$2$_$state$ = 0;
        pin10_$2$_$serRes$ = 1.000000e+02;
        pin10_$2$_$delay$ = 0.000000e+00;
        pin10_$2$_$rise$ = 1.000000e-12;
        pin10_$2$_$fall$ = 1.000000e-12;
        pin11_$state$ = 0;
        pin11_$serRes$ = 1.000000e+02;
        pin11_$delay$ = 0.000000e+00;
        pin11_$rise$ = 1.000000e-12;
        pin11_$fall$ = 1.000000e-12;
        pin12_$0$_$state$ = 0;
        pin12_$0$_$serRes$ = 1.000000e+02;
        pin12_$0$_$inCap$ = 1.000000e-14;
        pin12_$0$_$res$ = 1.000000e+02;
        pin12_$0$_$delay$ = 0.000000e+00;
        pin12_$0$_$rise$ = 1.000000e-12;
        pin12_$0$_$fall$ = 1.000000e-12;
        pin12_$1$_$state$ = 0;
        pin12_$1$_$serRes$ = 1.000000e+02;
        pin12_$1$_$inCap$ = 1.000000e-14;
        pin12_$1$_$res$ = 1.000000e+02;
        pin12_$1$_$delay$ = 0.000000e+00;
        pin12_$1$_$rise$ = 1.000000e-12;
        pin12_$1$_$fall$ = 1.000000e-12;
        pin12_$2$_$state$ = 0;
        pin12_$2$_$serRes$ = 1.000000e+02;
        pin12_$2$_$inCap$ = 1.000000e-14;
        pin12_$2$_$res$ = 1.000000e+02;
        pin12_$2$_$delay$ = 0.000000e+00;
        pin12_$2$_$rise$ = 1.000000e-12;
        pin12_$2$_$fall$ = 1.000000e-12;
        pin13_$state$ = 0;
        pin13_$serRes$ = 1.000000e+02;
        pin13_$inCap$ = 1.000000e-14;
        pin13_$res$ = 1.000000e+02;
        pin13_$delay$ = 0.000000e+00;
        pin13_$rise$ = 1.000000e-12;
        pin13_$fall$ = 1.000000e-12;
        sw1_$cond$ = 1.000000e-02;
        sw1_$rise$ = 1.000000e-06;
        sw1_$fall$ = 1.000000e-06;
        clk1_$out$ = pin11_$state$;
        clk1_$isOn$ = 0;
        clk1_$halfPeriod$ = 1.000000e+06;
        clk1_$time$ = 1.000000e+06;
        _$markSt_seq1 = 0;
        _$evntTime_1 = 1.000000e-09;
        _$state_1 = 0;
        _$runSt_1 = 0;
        _$eventId_1 = 0;
        _$markSt_seq2 = 0;
        _$evntTime_2 = 1.000000e-09;
        _$state_2 = 0;
        _$runSt_2 = 0;
        _$eventId_2 = 0;
    end
    @( initial_step("tran") ) begin
        _$1 = 0;
        _$2 = 9;
        pin1_$0$_$volt$ = 0.000000e+00;
        pin1_$0$_$maxCur = 0.000000e+00;
        pin1_$0$_$minCur$ = 0.000000e+00;
        pin1_$0$_$res$ = 1.000000e+12;
        pin1_$0$_$vDelay$ = 0.000000e+00;
        pin1_$0$_$iDelay$ = 0.000000e+00;
        pin1_$0$_$rDelay$ = 0.000000e+00;
        pin1_$0$_$riseFall$ = 1.000000e-06;
        pin1_$0$_$voltTran$ = 0.000000e+00;
        pin1_$0$_$maxCurTran$ = 0.000000e+00;
        pin1_$0$_$minCurTran$ = 0.000000e+00;
        pin1_$0$_$resTran$ = 0.000000e+00;
        pin1_$1$_$volt$ = 0.000000e+00;
        pin1_$1$_$maxCur = 0.000000e+00;
        pin1_$1$_$minCur$ = 0.000000e+00;
        pin1_$1$_$res$ = 1.000000e+12;
        pin1_$1$_$vDelay$ = 0.000000e+00;
        pin1_$1$_$iDelay$ = 0.000000e+00;
        pin1_$1$_$rDelay$ = 0.000000e+00;
        pin1_$1$_$riseFall$ = 1.000000e-06;
        pin1_$1$_$voltTran$ = 0.000000e+00;
        pin1_$1$_$maxCurTran$ = 0.000000e+00;
        pin1_$1$_$minCurTran$ = 0.000000e+00;
        pin1_$1$_$resTran$ = 0.000000e+00;
        pin1_$2$_$volt$ = 0.000000e+00;
        pin1_$2$_$maxCur = 0.000000e+00;
        pin1_$2$_$minCur$ = 0.000000e+00;
        pin1_$2$_$res$ = 1.000000e+12;
        pin1_$2$_$vDelay$ = 0.000000e+00;
        pin1_$2$_$iDelay$ = 0.000000e+00;
        pin1_$2$_$rDelay$ = 0.000000e+00;
        pin1_$2$_$riseFall$ = 1.000000e-06;
        pin1_$2$_$voltTran$ = 0.000000e+00;
        pin1_$2$_$maxCurTran$ = 0.000000e+00;
        pin1_$2$_$minCurTran$ = 0.000000e+00;
        pin1_$2$_$resTran$ = 0.000000e+00;
        pin2_$volt$ = 0.000000e+00;
        pin2_$maxCur = 0.000000e+00;
        pin2_$minCur$ = 0.000000e+00;
        pin2_$res$ = 1.000000e+12;
        pin2_$vDelay$ = 0.000000e+00;
        pin2_$iDelay$ = 0.000000e+00;
        pin2_$rDelay$ = 0.000000e+00;
        pin2_$riseFall$ = 1.000000e-06;
        pin2_$voltTran$ = 0.000000e+00;
        pin2_$maxCurTran$ = 0.000000e+00;
        pin2_$minCurTran$ = 0.000000e+00;
        pin2_$resTran$ = 0.000000e+00;
        pin3_$0$_$value$ = 0.000000e+00;
        pin3_$0$_$rise$ = 0.000000e+00;
        pin3_$0$_$fall$ = 0.000000e+00;
        pin3_$1$_$value$ = 0.000000e+00;
        pin3_$1$_$rise$ = 0.000000e+00;
        pin3_$1$_$fall$ = 0.000000e+00;
        pin3_$2$_$value$ = 0.000000e+00;
        pin3_$2$_$rise$ = 0.000000e+00;
        pin3_$2$_$fall$ = 0.000000e+00;
        pin4_$value$ = 0.000000e+00;
        pin4_$rise$ = 0.000000e+00;
        pin4_$fall$ = 0.000000e+00;
        pin5_$0$_$value$ = 0.000000e+00;
        pin5_$0$_$rise$ = 0.000000e+00;
        pin5_$0$_$fall$ = 0.000000e+00;
        pin5_$1$_$value$ = 0.000000e+00;
        pin5_$1$_$rise$ = 0.000000e+00;
        pin5_$1$_$fall$ = 0.000000e+00;
        pin5_$2$_$value$ = 0.000000e+00;
        pin5_$2$_$rise$ = 0.000000e+00;
        pin5_$2$_$fall$ = 0.000000e+00;
        pin6_$value$ = 0.000000e+00;
        pin6_$rise$ = 0.000000e+00;
        pin6_$fall$ = 0.000000e+00;
        pin8_$0$_$inCap$ = 1.000000e-14;
        pin8_$1$_$inCap$ = 1.000000e-14;
        pin8_$2$_$inCap$ = 1.000000e-14;
        pin9_$inCap$ = 1.000000e-14;
        pin10_$0$_$state$ = 0;
        pin10_$0$_$serRes$ = 1.000000e+02;
        pin10_$0$_$delay$ = 0.000000e+00;
        pin10_$0$_$rise$ = 1.000000e-12;
        pin10_$0$_$fall$ = 1.000000e-12;
        pin10_$1$_$state$ = 0;
        pin10_$1$_$serRes$ = 1.000000e+02;
        pin10_$1$_$delay$ = 0.000000e+00;
        pin10_$1$_$rise$ = 1.000000e-12;
        pin10_$1$_$fall$ = 1.000000e-12;
        pin10_$2$_$state$ = 0;
        pin10_$2$_$serRes$ = 1.000000e+02;
        pin10_$2$_$delay$ = 0.000000e+00;
        pin10_$2$_$rise$ = 1.000000e-12;
        pin10_$2$_$fall$ = 1.000000e-12;
        pin11_$state$ = 0;
        pin11_$serRes$ = 1.000000e+02;
        pin11_$delay$ = 0.000000e+00;
        pin11_$rise$ = 1.000000e-12;
        pin11_$fall$ = 1.000000e-12;
        pin12_$0$_$state$ = 0;
        pin12_$0$_$serRes$ = 1.000000e+02;
        pin12_$0$_$inCap$ = 1.000000e-14;
        pin12_$0$_$res$ = 1.000000e+02;
        pin12_$0$_$delay$ = 0.000000e+00;
        pin12_$0$_$rise$ = 1.000000e-12;
        pin12_$0$_$fall$ = 1.000000e-12;
        pin12_$1$_$state$ = 0;
        pin12_$1$_$serRes$ = 1.000000e+02;
        pin12_$1$_$inCap$ = 1.000000e-14;
        pin12_$1$_$res$ = 1.000000e+02;
        pin12_$1$_$delay$ = 0.000000e+00;
        pin12_$1$_$rise$ = 1.000000e-12;
        pin12_$1$_$fall$ = 1.000000e-12;
        pin12_$2$_$state$ = 0;
        pin12_$2$_$serRes$ = 1.000000e+02;
        pin12_$2$_$inCap$ = 1.000000e-14;
        pin12_$2$_$res$ = 1.000000e+02;
        pin12_$2$_$delay$ = 0.000000e+00;
        pin12_$2$_$rise$ = 1.000000e-12;
        pin12_$2$_$fall$ = 1.000000e-12;
        pin13_$state$ = 0;
        pin13_$serRes$ = 1.000000e+02;
        pin13_$inCap$ = 1.000000e-14;
        pin13_$res$ = 1.000000e+02;
        pin13_$delay$ = 0.000000e+00;
        pin13_$rise$ = 1.000000e-12;
        pin13_$fall$ = 1.000000e-12;
        sw1_$cond$ = 1.000000e-02;
        sw1_$rise$ = 1.000000e-06;
        sw1_$fall$ = 1.000000e-06;
        clk1_$out$ = pin11_$state$;
        clk1_$isOn$ = 0;
        clk1_$halfPeriod$ = 1.000000e+06;
        clk1_$time$ = 1.000000e+06;
        _$markSt_seq1 = 0;
        _$evntTime_1 = 1.000000e-09;
        _$state_1 = 0;
        _$runSt_1 = 0;
        _$eventId_1 = 0;
        _$markSt_seq2 = 0;
        _$evntTime_2 = 1.000000e-09;
        _$state_2 = 0;
        _$runSt_2 = 0;
        _$eventId_2 = 0;
    end
    @( timer(_$evntTime_1) )
        if( ( _$eventId_1 ) == ( 0 ) )
            _$runSt_1 = 1;
    @( timer(_$evntTime_2) )
        if( ( _$eventId_2 ) == ( 0 ) )
            _$runSt_2 = 1;
    @( cross(V(pin7) - 5.000000e-01, 0) )
        if( ( _$eventId_2 ) == ( 1 ) )
            _$runSt_2 = 1;
    if( ( TEST_SEQ_PARAM ) == ( 1 ) )
        while( _$runSt_1 ) begin
            _$runSt_1 = 0;
            case( _$state_1 )
                0: begin
                    pin1_$0$_$volt$ = 2.000000e+00;
                    pin1_$0$_$maxCur = abs( 1.000000e-02 );
                    pin1_$0$_$minCur$ = -( abs( 1.000000e-02 ) );
                    pin1_$0$_$res$ = ( 1.000000e+04 )/( ( abs( 1.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin1_$0$_$vDelay$ = 0.000000e+00;
                    pin1_$0$_$iDelay$ = 1.000000e-06;
                    pin1_$0$_$rDelay$ = 1.000000e-06;
                    pin1_$0$_$riseFall$ = 1.000000e-06;
                    pin1_$1$_$volt$ = 2.000000e+00;
                    pin1_$1$_$maxCur = abs( 1.000000e-02 );
                    pin1_$1$_$minCur$ = -( abs( 1.000000e-02 ) );
                    pin1_$1$_$res$ = ( 1.000000e+04 )/( ( abs( 1.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin1_$1$_$vDelay$ = 0.000000e+00;
                    pin1_$1$_$iDelay$ = 1.000000e-06;
                    pin1_$1$_$rDelay$ = 1.000000e-06;
                    pin1_$1$_$riseFall$ = 1.000000e-06;
                    pin1_$2$_$volt$ = 2.000000e+00;
                    pin1_$2$_$maxCur = abs( 1.000000e-02 );
                    pin1_$2$_$minCur$ = -( abs( 1.000000e-02 ) );
                    pin1_$2$_$res$ = ( 1.000000e+04 )/( ( abs( 1.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin1_$2$_$vDelay$ = 0.000000e+00;
                    pin1_$2$_$iDelay$ = 1.000000e-06;
                    pin1_$2$_$rDelay$ = 1.000000e-06;
                    pin1_$2$_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 1;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                1: begin
                    pin1_$0$_$volt$ = 5.000000e+00;
                    pin1_$0$_$maxCur = ( 5.000000e-01 )*( ( -2.000000e-02 ) + ( abs( -2.000000e-02 ) ) );
                    pin1_$0$_$minCur$ = ( 5.000000e-01 )*( ( -2.000000e-02 ) - ( abs( -2.000000e-02 ) ) );
                    pin1_$0$_$res$ = ( 1.000000e+04 )/( ( abs( -2.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin1_$0$_$vDelay$ = 1.000000e-06;
                    pin1_$0$_$iDelay$ = 0.000000e+00;
                    pin1_$0$_$rDelay$ = 0.000000e+00;
                    pin1_$0$_$riseFall$ = 1.000000e-06;
                    pin1_$1$_$volt$ = 5.000000e+00;
                    pin1_$1$_$maxCur = ( 5.000000e-01 )*( ( -2.000000e-02 ) + ( abs( -2.000000e-02 ) ) );
                    pin1_$1$_$minCur$ = ( 5.000000e-01 )*( ( -2.000000e-02 ) - ( abs( -2.000000e-02 ) ) );
                    pin1_$1$_$res$ = ( 1.000000e+04 )/( ( abs( -2.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin1_$1$_$vDelay$ = 1.000000e-06;
                    pin1_$1$_$iDelay$ = 0.000000e+00;
                    pin1_$1$_$rDelay$ = 0.000000e+00;
                    pin1_$1$_$riseFall$ = 1.000000e-06;
                    pin1_$2$_$volt$ = 5.000000e+00;
                    pin1_$2$_$maxCur = ( 5.000000e-01 )*( ( -2.000000e-02 ) + ( abs( -2.000000e-02 ) ) );
                    pin1_$2$_$minCur$ = ( 5.000000e-01 )*( ( -2.000000e-02 ) - ( abs( -2.000000e-02 ) ) );
                    pin1_$2$_$res$ = ( 1.000000e+04 )/( ( abs( -2.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin1_$2$_$vDelay$ = 1.000000e-06;
                    pin1_$2$_$iDelay$ = 0.000000e+00;
                    pin1_$2$_$rDelay$ = 0.000000e+00;
                    pin1_$2$_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 2;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                2: begin
                    pin1_$0$_$volt$ = 0.000000e+00;
                    pin1_$0$_$maxCur = 0.000000e+00;
                    pin1_$0$_$minCur$ = 0.000000e+00;
                    pin1_$0$_$res$ = 1.000000e+00;
                    pin1_$0$_$vDelay$ = 1.000000e-06;
                    pin1_$0$_$iDelay$ = 0.000000e+00;
                    pin1_$0$_$rDelay$ = 0.000000e+00;
                    pin1_$0$_$riseFall$ = 1.000000e-06;
                    pin1_$1$_$volt$ = 0.000000e+00;
                    pin1_$1$_$maxCur = 0.000000e+00;
                    pin1_$1$_$minCur$ = 0.000000e+00;
                    pin1_$1$_$res$ = 1.000000e+00;
                    pin1_$1$_$vDelay$ = 1.000000e-06;
                    pin1_$1$_$iDelay$ = 0.000000e+00;
                    pin1_$1$_$rDelay$ = 0.000000e+00;
                    pin1_$1$_$riseFall$ = 1.000000e-06;
                    pin1_$2$_$volt$ = 0.000000e+00;
                    pin1_$2$_$maxCur = 0.000000e+00;
                    pin1_$2$_$minCur$ = 0.000000e+00;
                    pin1_$2$_$res$ = 1.000000e+00;
                    pin1_$2$_$vDelay$ = 1.000000e-06;
                    pin1_$2$_$iDelay$ = 0.000000e+00;
                    pin1_$2$_$rDelay$ = 0.000000e+00;
                    pin1_$2$_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 3;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                3: begin
                    pin1_$0$_$volt$ = 2.000000e+00;
                    pin1_$0$_$maxCur = abs( 1.000000e-02 );
                    pin1_$0$_$minCur$ = -( abs( 1.000000e-02 ) );
                    pin1_$0$_$res$ = ( 1.000000e+04 )/( ( abs( 1.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin1_$0$_$vDelay$ = 0.000000e+00;
                    pin1_$0$_$iDelay$ = 1.000000e-06;
                    pin1_$0$_$rDelay$ = 1.000000e-06;
                    pin1_$0$_$riseFall$ = 1.000000e-06;
                    pin1_$1$_$volt$ = 2.000000e+00;
                    pin1_$1$_$maxCur = abs( 1.000000e-02 );
                    pin1_$1$_$minCur$ = -( abs( 1.000000e-02 ) );
                    pin1_$1$_$res$ = ( 1.000000e+04 )/( ( abs( 1.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin1_$1$_$vDelay$ = 0.000000e+00;
                    pin1_$1$_$iDelay$ = 1.000000e-06;
                    pin1_$1$_$rDelay$ = 1.000000e-06;
                    pin1_$1$_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 4;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                4: begin
                    pin2_$volt$ = 5.000000e+00;
                    pin2_$maxCur = ( 5.000000e-01 )*( ( -2.000000e-02 ) + ( abs( -2.000000e-02 ) ) );
                    pin2_$minCur$ = ( 5.000000e-01 )*( ( -2.000000e-02 ) - ( abs( -2.000000e-02 ) ) );
                    pin2_$res$ = ( 1.000000e+04 )/( ( abs( -2.000000e-02 ) ) + ( 1.000000e-09 ) );
                    pin2_$vDelay$ = 1.000000e-06;
                    pin2_$iDelay$ = 0.000000e+00;
                    pin2_$rDelay$ = 0.000000e+00;
                    pin2_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 5;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                5: begin
                    _$markSt_seq1 = !_$markSt_seq1;
                    pin3_$0$_$rise$ = 3.000000e-05;
                    pin3_$0$_$fall$ = 3.000000e-05;
                    pin3_$1$_$rise$ = 3.000000e-05;
                    pin3_$1$_$fall$ = 3.000000e-05;
                    pin3_$2$_$rise$ = 3.000000e-05;
                    pin3_$2$_$fall$ = 3.000000e-05;
                    pin3_$0$_$value$ = 2.000000e+00;
                    pin3_$1$_$value$ = 2.000000e+00;
                    pin3_$2$_$value$ = 2.000000e+00;
                    _$eventId_1 = 0;
                    _$state_1 = 6;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                6: begin
                    pin3_$1$_$value$ = 0.000000e+00;
                    _$eventId_1 = 0;
                    _$state_1 = 7;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                7: begin
                    pin4_$value$ = 2.000000e+00;
                    _$eventId_1 = 0;
                    _$state_1 = 8;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                8: begin
                    _$markSt_seq1 = !_$markSt_seq1;
                    pin5_$0$_$rise$ = 5.000000e-05;
                    pin5_$0$_$fall$ = 5.000000e-05;
                    pin5_$1$_$rise$ = 5.000000e-05;
                    pin5_$1$_$fall$ = 5.000000e-05;
                    pin5_$2$_$rise$ = 5.000000e-05;
                    pin5_$2$_$fall$ = 5.000000e-05;
                    pin5_$0$_$value$ = -1.000000e-02;
                    pin5_$1$_$value$ = -1.000000e-02;
                    pin5_$2$_$value$ = -1.000000e-02;
                    _$eventId_1 = 0;
                    _$state_1 = 9;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                9: begin
                    pin5_$1$_$value$ = 0.000000e+00;
                    pin5_$2$_$value$ = 0.000000e+00;
                    _$eventId_1 = 0;
                    _$state_1 = 10;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                10: begin
                    pin6_$value$ = -2.000000e-02;
                    _$eventId_1 = 0;
                    _$state_1 = 11;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                11: begin
                    _$markSt_seq1 = !_$markSt_seq1;
                    _$eventId_1 = 0;
                    _$state_1 = 12;
                    _$evntTime_1 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                12:
                    $finish;
            endcase
        end
    if( ( TEST_SEQ_PARAM ) == ( 2 ) )
        while( _$runSt_2 ) begin
            _$runSt_2 = 0;
            case( _$state_2 )
                0: begin
                    pin4_$value$ = 2.000000e+00;
                    _$eventId_2 = 0;
                    _$state_2 = 1;
                    _$evntTime_2 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                1: begin
                    pin11_$state$ = 1;
                    _$eventId_2 = 0;
                    _$state_2 = 2;
                    _$evntTime_2 = ( $abstime ) + ( ( 1.000000e-06 )*( 1.000000e+02 ) );
                end
                2: begin
                    pin12_$0$_$res$ = 1.000000e+12;
                    pin12_$1$_$res$ = 1.000000e+12;
                    pin12_$2$_$res$ = 1.000000e+12;
                    pin13_$res$ = 1.000000e+12;
                    _$eventId_2 = 1;
                    _$state_2 = 3;
                end
                3: begin
                    pin12_$0$_$res$ = pin12_$0$_$serRes$;
                    pin12_$1$_$res$ = pin12_$1$_$serRes$;
                    pin12_$2$_$res$ = pin12_$2$_$serRes$;
                    pin13_$res$ = pin13_$serRes$;
                    pin13_$state$ = 1;
                    pin12_$0$_$state$ = ( ( 5 ) & ( 1 ) ) != ( 0 );
                    pin12_$1$_$state$ = ( ( 5 ) & ( 2 ) ) != ( 0 );
                    pin12_$2$_$state$ = ( ( 5 ) & ( 4 ) ) != ( 0 );
                    clk1_$halfPeriod$ = ( 5.000000e-01 )/( 1.000000e+05 );
                    clk1_$isOn$ = 1;
                    clk1_$time$ = ( $abstime ) + ( 1.000000e-09 );
                    sw1_$cond$ = 0.000000e+00;
                    _$eventId_2 = 0;
                    _$state_2 = 4;
                    _$evntTime_2 = ( $abstime ) + ( ( 1.000000e-06 )*( 2.000000e+02 ) );
                end
                4:
                    $finish;
            endcase
        end
    @( timer(clk1_$time$) ) begin
        clk1_$out$ = !clk1_$out$;
        pin11_$state$ = clk1_$out$;
        if( ( clk1_$isOn$ ) || ( clk1_$out$ ) )
            clk1_$time$ = ( $abstime ) + ( clk1_$halfPeriod$ );
    end
    pin1_$0$_$voltTran$ = transition(pin1_$0$_$volt$, pin1_$0$_$vDelay$, pin1_$0$_$riseFall$, pin1_$0$_$riseFall$);
    pin1_$0$_$maxCurTran$ = transition(pin1_$0$_$maxCur, pin1_$0$_$iDelay$, pin1_$0$_$riseFall$, pin1_$0$_$riseFall$);
    pin1_$0$_$minCurTran$ = transition(pin1_$0$_$minCur$, pin1_$0$_$iDelay$, pin1_$0$_$riseFall$, pin1_$0$_$riseFall$);
    pin1_$0$_$resTran$ = transition(pin1_$0$_$res$, pin1_$0$_$rDelay$, pin1_$0$_$riseFall$, pin1_$0$_$riseFall$);
    I(pin1[0]) <+ ( ( ( tanh(( 5.000000e+01 )*( ( V(pin1[0]) ) - ( pin1_$0$_$voltTran$ ) )) )*( 5.000000e-01 ) )*( ( pin1_$0$_$maxCurTran$ ) - ( pin1_$0$_$minCurTran$ ) ) ) + ( ( 5.000000e-01 )*( ( pin1_$0$_$maxCurTran$ ) + ( pin1_$0$_$minCurTran$ ) ) );
    I(pin1[0]) <+ ( V(pin1[0]) )/( pin1_$0$_$resTran$ );
    I(pin1[0]) <+ ( 1.000000e-12 )*( ddt(V(pin1[0])) );
    pin1_$1$_$voltTran$ = transition(pin1_$1$_$volt$, pin1_$1$_$vDelay$, pin1_$1$_$riseFall$, pin1_$1$_$riseFall$);
    pin1_$1$_$maxCurTran$ = transition(pin1_$1$_$maxCur, pin1_$1$_$iDelay$, pin1_$1$_$riseFall$, pin1_$1$_$riseFall$);
    pin1_$1$_$minCurTran$ = transition(pin1_$1$_$minCur$, pin1_$1$_$iDelay$, pin1_$1$_$riseFall$, pin1_$1$_$riseFall$);
    pin1_$1$_$resTran$ = transition(pin1_$1$_$res$, pin1_$1$_$rDelay$, pin1_$1$_$riseFall$, pin1_$1$_$riseFall$);
    I(pin1[1]) <+ ( ( ( tanh(( 5.000000e+01 )*( ( V(pin1[1]) ) - ( pin1_$1$_$voltTran$ ) )) )*( 5.000000e-01 ) )*( ( pin1_$1$_$maxCurTran$ ) - ( pin1_$1$_$minCurTran$ ) ) ) + ( ( 5.000000e-01 )*( ( pin1_$1$_$maxCurTran$ ) + ( pin1_$1$_$minCurTran$ ) ) );
    I(pin1[1]) <+ ( V(pin1[1]) )/( pin1_$1$_$resTran$ );
    I(pin1[1]) <+ ( 1.000000e-12 )*( ddt(V(pin1[1])) );
    pin1_$2$_$voltTran$ = transition(pin1_$2$_$volt$, pin1_$2$_$vDelay$, pin1_$2$_$riseFall$, pin1_$2$_$riseFall$);
    pin1_$2$_$maxCurTran$ = transition(pin1_$2$_$maxCur, pin1_$2$_$iDelay$, pin1_$2$_$riseFall$, pin1_$2$_$riseFall$);
    pin1_$2$_$minCurTran$ = transition(pin1_$2$_$minCur$, pin1_$2$_$iDelay$, pin1_$2$_$riseFall$, pin1_$2$_$riseFall$);
    pin1_$2$_$resTran$ = transition(pin1_$2$_$res$, pin1_$2$_$rDelay$, pin1_$2$_$riseFall$, pin1_$2$_$riseFall$);
    I(pin1[2]) <+ ( ( ( tanh(( 5.000000e+01 )*( ( V(pin1[2]) ) - ( pin1_$2$_$voltTran$ ) )) )*( 5.000000e-01 ) )*( ( pin1_$2$_$maxCurTran$ ) - ( pin1_$2$_$minCurTran$ ) ) ) + ( ( 5.000000e-01 )*( ( pin1_$2$_$maxCurTran$ ) + ( pin1_$2$_$minCurTran$ ) ) );
    I(pin1[2]) <+ ( V(pin1[2]) )/( pin1_$2$_$resTran$ );
    I(pin1[2]) <+ ( 1.000000e-12 )*( ddt(V(pin1[2])) );
    pin2_$voltTran$ = transition(pin2_$volt$, pin2_$vDelay$, pin2_$riseFall$, pin2_$riseFall$);
    pin2_$maxCurTran$ = transition(pin2_$maxCur, pin2_$iDelay$, pin2_$riseFall$, pin2_$riseFall$);
    pin2_$minCurTran$ = transition(pin2_$minCur$, pin2_$iDelay$, pin2_$riseFall$, pin2_$riseFall$);
    pin2_$resTran$ = transition(pin2_$res$, pin2_$rDelay$, pin2_$riseFall$, pin2_$riseFall$);
    I(pin2) <+ ( ( ( tanh(( 5.000000e+01 )*( ( V(pin2) ) - ( pin2_$voltTran$ ) )) )*( 5.000000e-01 ) )*( ( pin2_$maxCurTran$ ) - ( pin2_$minCurTran$ ) ) ) + ( ( 5.000000e-01 )*( ( pin2_$maxCurTran$ ) + ( pin2_$minCurTran$ ) ) );
    I(pin2) <+ ( V(pin2) )/( pin2_$resTran$ );
    I(pin2) <+ ( 1.000000e-12 )*( ddt(V(pin2)) );
    V(pin3[0]) <+ transition(pin3_$0$_$value$, 0.000000e+00, pin3_$0$_$rise$, pin3_$0$_$fall$);
    V(pin3[1]) <+ transition(pin3_$1$_$value$, 0.000000e+00, pin3_$1$_$rise$, pin3_$1$_$fall$);
    V(pin3[2]) <+ transition(pin3_$2$_$value$, 0.000000e+00, pin3_$2$_$rise$, pin3_$2$_$fall$);
    V(pin4) <+ transition(pin4_$value$, 0.000000e+00, pin4_$rise$, pin4_$fall$);
    I(pin5[0]) <+ transition(pin5_$0$_$value$, 0.000000e+00, pin5_$0$_$rise$, pin5_$0$_$fall$);
    I(pin5[1]) <+ transition(pin5_$1$_$value$, 0.000000e+00, pin5_$1$_$rise$, pin5_$1$_$fall$);
    I(pin5[2]) <+ transition(pin5_$2$_$value$, 0.000000e+00, pin5_$2$_$rise$, pin5_$2$_$fall$);
    I(pin6) <+ transition(pin6_$value$, 0.000000e+00, pin6_$rise$, pin6_$fall$);
    I(pin8[0]) <+ ( ddt(V(pin8[0])) )*( pin8_$0$_$inCap$ );
    I(pin8[1]) <+ ( ddt(V(pin8[1])) )*( pin8_$1$_$inCap$ );
    I(pin8[2]) <+ ( ddt(V(pin8[2])) )*( pin8_$2$_$inCap$ );
    I(pin9) <+ ( ddt(V(pin9)) )*( pin9_$inCap$ );
    V(pin10[0]) <+ ( V(pin4) )*( transition(pin10_$0$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin10_$0$_$delay$, pin10_$0$_$rise$, pin10_$0$_$fall$) );
    V(pin10[0]) <+ ( I(pin10[0]) )*( pin10_$0$_$serRes$ );
    V(pin10[1]) <+ ( V(pin4) )*( transition(pin10_$1$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin10_$1$_$delay$, pin10_$1$_$rise$, pin10_$1$_$fall$) );
    V(pin10[1]) <+ ( I(pin10[1]) )*( pin10_$1$_$serRes$ );
    V(pin10[2]) <+ ( V(pin4) )*( transition(pin10_$2$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin10_$2$_$delay$, pin10_$2$_$rise$, pin10_$2$_$fall$) );
    V(pin10[2]) <+ ( I(pin10[2]) )*( pin10_$2$_$serRes$ );
    V(pin11) <+ ( V(pin4) )*( transition(pin11_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin11_$delay$, pin11_$rise$, pin11_$fall$) );
    V(pin11) <+ ( I(pin11) )*( pin11_$serRes$ );
    V(_$3) <+ ( V(pin4) )*( transition(pin12_$0$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin12_$0$_$delay$, pin12_$0$_$rise$, pin12_$0$_$fall$) );
    V(_$3, pin12[0]) <+ ( I(_$3, pin12[0]) )*( transition(pin12_$0$_$res$, pin12_$0$_$delay$, pin12_$0$_$rise$, pin12_$0$_$fall$) );
    I(pin12[0]) <+ ( ddt(V(pin12[0])) )*( pin12_$0$_$inCap$ );
    V(_$4) <+ ( V(pin4) )*( transition(pin12_$1$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin12_$1$_$delay$, pin12_$1$_$rise$, pin12_$1$_$fall$) );
    V(_$4, pin12[1]) <+ ( I(_$4, pin12[1]) )*( transition(pin12_$1$_$res$, pin12_$1$_$delay$, pin12_$1$_$rise$, pin12_$1$_$fall$) );
    I(pin12[1]) <+ ( ddt(V(pin12[1])) )*( pin12_$1$_$inCap$ );
    V(_$5) <+ ( V(pin4) )*( transition(pin12_$2$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin12_$2$_$delay$, pin12_$2$_$rise$, pin12_$2$_$fall$) );
    V(_$5, pin12[2]) <+ ( I(_$5, pin12[2]) )*( transition(pin12_$2$_$res$, pin12_$2$_$delay$, pin12_$2$_$rise$, pin12_$2$_$fall$) );
    I(pin12[2]) <+ ( ddt(V(pin12[2])) )*( pin12_$2$_$inCap$ );
    V(_$6) <+ ( V(pin4) )*( transition(pin13_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin13_$delay$, pin13_$rise$, pin13_$fall$) );
    V(_$6, pin13) <+ ( I(_$6, pin13) )*( transition(pin13_$res$, pin13_$delay$, pin13_$rise$, pin13_$fall$) );
    I(pin13) <+ ( ddt(V(pin13)) )*( pin13_$inCap$ );
    I(pin7, pin14) <+ ( V(pin7, pin14) )*( transition(sw1_$cond$, 0.000000e+00, sw1_$rise$, sw1_$fall$) );
    V(MARK_seq1) <+ transition(_$markSt_seq1 ? ( 1.0 ) : ( 0.0 ), 0.000000e+00, 1.000000e-10, 1.000000e-10);
    V(MARK_seq2) <+ transition(_$markSt_seq2 ? ( 1.0 ) : ( 0.0 ), 0.000000e+00, 1.000000e-10, 1.000000e-10);
end
endmodule'''
        self.maxDiff = None
        self.assertEqual(mod.getVA()[323:], ref)
        #print(mod.getVA())
         
        
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
        evnt1 = Cross(pin7.v, 0.5, "both")
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
   
        ref = '''`include "constants.vams"
`include "disciplines.vams"

/******************************************************************************
 *                             Module declaration                             * 
 ******************************************************************************/
module tb(pin1,
          pin2,
          pin3,
          pin4,
          pin5,
          pin6,
          pin7,
          pin8,
          pin9,
          pin10,
          pin11,
          pin12,
          pin13,
          pin14,
          MARK_seq1,
          MARK_seq2);

/******************************************************************************
 *                                   Ports                                    * 
 ******************************************************************************/
inout [2:0] pin1;
inout pin2;
output [2:0] pin3;
output pin4;
output [2:0] pin5;
output pin6;
inout pin7;
input [2:0] pin8;
input pin9;
output [2:0] pin10;
output pin11;
inout [2:0] pin12;
inout pin13;
inout pin14;
output MARK_seq1;
output MARK_seq2;

/******************************************************************************
 *                                 Disciplines                                * 
 ******************************************************************************/
electrical [2:0] pin1;
electrical pin2;
electrical [2:0] pin3;
electrical pin4;
electrical [2:0] pin5;
electrical pin6;
electrical pin7;
electrical [2:0] pin8;
electrical pin9;
electrical [2:0] pin10;
electrical pin11;
electrical [2:0] pin12;
electrical _$3;
electrical _$4;
electrical _$5;
electrical pin13;
electrical _$6;
electrical pin14;
electrical MARK_seq1;
electrical MARK_seq2;

/******************************************************************************
 *                                 Parameters                                 * 
 ******************************************************************************/
parameter integer TEST_SEQ_PARAM = 0;
parameter real parameter1 = 0.000000e+00;

/******************************************************************************
 *                                 Variables                                  * 
 ******************************************************************************/
integer _$1;
integer _$2;
real pin1_$0$_$volt$;
real pin1_$0$_$maxCur;
real pin1_$0$_$minCur$;
real pin1_$0$_$res$;
real pin1_$0$_$vDelay$;
real pin1_$0$_$iDelay$;
real pin1_$0$_$rDelay$;
real pin1_$0$_$riseFall$;
real pin1_$0$_$voltTran$;
real pin1_$0$_$maxCurTran$;
real pin1_$0$_$minCurTran$;
real pin1_$0$_$resTran$;
real pin1_$1$_$volt$;
real pin1_$1$_$maxCur;
real pin1_$1$_$minCur$;
real pin1_$1$_$res$;
real pin1_$1$_$vDelay$;
real pin1_$1$_$iDelay$;
real pin1_$1$_$rDelay$;
real pin1_$1$_$riseFall$;
real pin1_$1$_$voltTran$;
real pin1_$1$_$maxCurTran$;
real pin1_$1$_$minCurTran$;
real pin1_$1$_$resTran$;
real pin1_$2$_$volt$;
real pin1_$2$_$maxCur;
real pin1_$2$_$minCur$;
real pin1_$2$_$res$;
real pin1_$2$_$vDelay$;
real pin1_$2$_$iDelay$;
real pin1_$2$_$rDelay$;
real pin1_$2$_$riseFall$;
real pin1_$2$_$voltTran$;
real pin1_$2$_$maxCurTran$;
real pin1_$2$_$minCurTran$;
real pin1_$2$_$resTran$;
real pin2_$volt$;
real pin2_$maxCur;
real pin2_$minCur$;
real pin2_$res$;
real pin2_$vDelay$;
real pin2_$iDelay$;
real pin2_$rDelay$;
real pin2_$riseFall$;
real pin2_$voltTran$;
real pin2_$maxCurTran$;
real pin2_$minCurTran$;
real pin2_$resTran$;
real pin3_$0$_$value$;
real pin3_$0$_$rise$;
real pin3_$0$_$fall$;
real pin3_$1$_$value$;
real pin3_$1$_$rise$;
real pin3_$1$_$fall$;
real pin3_$2$_$value$;
real pin3_$2$_$rise$;
real pin3_$2$_$fall$;
real pin4_$value$;
real pin4_$rise$;
real pin4_$fall$;
real pin5_$0$_$value$;
real pin5_$0$_$rise$;
real pin5_$0$_$fall$;
real pin5_$1$_$value$;
real pin5_$1$_$rise$;
real pin5_$1$_$fall$;
real pin5_$2$_$value$;
real pin5_$2$_$rise$;
real pin5_$2$_$fall$;
real pin6_$value$;
real pin6_$rise$;
real pin6_$fall$;
real pin8_$0$_$inCap$;
real pin8_$1$_$inCap$;
real pin8_$2$_$inCap$;
real pin9_$inCap$;
integer pin10_$0$_$state$;
real pin10_$0$_$serRes$;
real pin10_$0$_$delay$;
real pin10_$0$_$rise$;
real pin10_$0$_$fall$;
integer pin10_$1$_$state$;
real pin10_$1$_$serRes$;
real pin10_$1$_$delay$;
real pin10_$1$_$rise$;
real pin10_$1$_$fall$;
integer pin10_$2$_$state$;
real pin10_$2$_$serRes$;
real pin10_$2$_$delay$;
real pin10_$2$_$rise$;
real pin10_$2$_$fall$;
integer pin11_$state$;
real pin11_$serRes$;
real pin11_$delay$;
real pin11_$rise$;
real pin11_$fall$;
integer pin12_$0$_$state$;
real pin12_$0$_$serRes$;
real pin12_$0$_$inCap$;
real pin12_$0$_$res$;
real pin12_$0$_$delay$;
real pin12_$0$_$rise$;
real pin12_$0$_$fall$;
integer pin12_$1$_$state$;
real pin12_$1$_$serRes$;
real pin12_$1$_$inCap$;
real pin12_$1$_$res$;
real pin12_$1$_$delay$;
real pin12_$1$_$rise$;
real pin12_$1$_$fall$;
integer pin12_$2$_$state$;
real pin12_$2$_$serRes$;
real pin12_$2$_$inCap$;
real pin12_$2$_$res$;
real pin12_$2$_$delay$;
real pin12_$2$_$rise$;
real pin12_$2$_$fall$;
integer pin13_$state$;
real pin13_$serRes$;
real pin13_$inCap$;
real pin13_$res$;
real pin13_$delay$;
real pin13_$rise$;
real pin13_$fall$;
real sw1_$cond$;
real sw1_$rise$;
real sw1_$fall$;
integer clk1_$out$;
integer clk1_$isOn$;
real clk1_$halfPeriod$;
real clk1_$time$;
integer _$markSt_seq1;
real _$evntTime_1;
integer _$state_1;
integer _$runSt_1;
integer _$eventId_1;
integer _$markSt_seq2;
real _$evntTime_2;
integer _$state_2;
integer _$runSt_2;
integer _$eventId_2;

/******************************************************************************
 *                                Analog block                                * 
 ******************************************************************************/
analog begin
    if( analysis("static") ) begin
        _$1 = 0;
        _$2 = 9;
        pin1_$0$_$volt$ = 0.000000e+00;
        pin1_$0$_$maxCur = 0.000000e+00;
        pin1_$0$_$minCur$ = 0.000000e+00;
        pin1_$0$_$res$ = 1.000000e+12;
        pin1_$0$_$vDelay$ = 0.000000e+00;
        pin1_$0$_$iDelay$ = 0.000000e+00;
        pin1_$0$_$rDelay$ = 0.000000e+00;
        pin1_$0$_$riseFall$ = 1.000000e-06;
        pin1_$0$_$voltTran$ = 0.000000e+00;
        pin1_$0$_$maxCurTran$ = 0.000000e+00;
        pin1_$0$_$minCurTran$ = 0.000000e+00;
        pin1_$0$_$resTran$ = 0.000000e+00;
        pin1_$1$_$volt$ = 0.000000e+00;
        pin1_$1$_$maxCur = 0.000000e+00;
        pin1_$1$_$minCur$ = 0.000000e+00;
        pin1_$1$_$res$ = 1.000000e+12;
        pin1_$1$_$vDelay$ = 0.000000e+00;
        pin1_$1$_$iDelay$ = 0.000000e+00;
        pin1_$1$_$rDelay$ = 0.000000e+00;
        pin1_$1$_$riseFall$ = 1.000000e-06;
        pin1_$1$_$voltTran$ = 0.000000e+00;
        pin1_$1$_$maxCurTran$ = 0.000000e+00;
        pin1_$1$_$minCurTran$ = 0.000000e+00;
        pin1_$1$_$resTran$ = 0.000000e+00;
        pin1_$2$_$volt$ = 0.000000e+00;
        pin1_$2$_$maxCur = 0.000000e+00;
        pin1_$2$_$minCur$ = 0.000000e+00;
        pin1_$2$_$res$ = 1.000000e+12;
        pin1_$2$_$vDelay$ = 0.000000e+00;
        pin1_$2$_$iDelay$ = 0.000000e+00;
        pin1_$2$_$rDelay$ = 0.000000e+00;
        pin1_$2$_$riseFall$ = 1.000000e-06;
        pin1_$2$_$voltTran$ = 0.000000e+00;
        pin1_$2$_$maxCurTran$ = 0.000000e+00;
        pin1_$2$_$minCurTran$ = 0.000000e+00;
        pin1_$2$_$resTran$ = 0.000000e+00;
        pin2_$volt$ = 0.000000e+00;
        pin2_$maxCur = 0.000000e+00;
        pin2_$minCur$ = 0.000000e+00;
        pin2_$res$ = 1.000000e+12;
        pin2_$vDelay$ = 0.000000e+00;
        pin2_$iDelay$ = 0.000000e+00;
        pin2_$rDelay$ = 0.000000e+00;
        pin2_$riseFall$ = 1.000000e-06;
        pin2_$voltTran$ = 0.000000e+00;
        pin2_$maxCurTran$ = 0.000000e+00;
        pin2_$minCurTran$ = 0.000000e+00;
        pin2_$resTran$ = 0.000000e+00;
        pin3_$0$_$value$ = 0.000000e+00;
        pin3_$0$_$rise$ = 0.000000e+00;
        pin3_$0$_$fall$ = 0.000000e+00;
        pin3_$1$_$value$ = 0.000000e+00;
        pin3_$1$_$rise$ = 0.000000e+00;
        pin3_$1$_$fall$ = 0.000000e+00;
        pin3_$2$_$value$ = 0.000000e+00;
        pin3_$2$_$rise$ = 0.000000e+00;
        pin3_$2$_$fall$ = 0.000000e+00;
        pin4_$value$ = 0.000000e+00;
        pin4_$rise$ = 0.000000e+00;
        pin4_$fall$ = 0.000000e+00;
        pin5_$0$_$value$ = 0.000000e+00;
        pin5_$0$_$rise$ = 0.000000e+00;
        pin5_$0$_$fall$ = 0.000000e+00;
        pin5_$1$_$value$ = 0.000000e+00;
        pin5_$1$_$rise$ = 0.000000e+00;
        pin5_$1$_$fall$ = 0.000000e+00;
        pin5_$2$_$value$ = 0.000000e+00;
        pin5_$2$_$rise$ = 0.000000e+00;
        pin5_$2$_$fall$ = 0.000000e+00;
        pin6_$value$ = 0.000000e+00;
        pin6_$rise$ = 0.000000e+00;
        pin6_$fall$ = 0.000000e+00;
        pin8_$0$_$inCap$ = 1.000000e-14;
        pin8_$1$_$inCap$ = 1.000000e-14;
        pin8_$2$_$inCap$ = 1.000000e-14;
        pin9_$inCap$ = 1.000000e-14;
        pin10_$0$_$state$ = 0;
        pin10_$0$_$serRes$ = 1.000000e+02;
        pin10_$0$_$delay$ = 0.000000e+00;
        pin10_$0$_$rise$ = 1.000000e-12;
        pin10_$0$_$fall$ = 1.000000e-12;
        pin10_$1$_$state$ = 0;
        pin10_$1$_$serRes$ = 1.000000e+02;
        pin10_$1$_$delay$ = 0.000000e+00;
        pin10_$1$_$rise$ = 1.000000e-12;
        pin10_$1$_$fall$ = 1.000000e-12;
        pin10_$2$_$state$ = 0;
        pin10_$2$_$serRes$ = 1.000000e+02;
        pin10_$2$_$delay$ = 0.000000e+00;
        pin10_$2$_$rise$ = 1.000000e-12;
        pin10_$2$_$fall$ = 1.000000e-12;
        pin11_$state$ = 0;
        pin11_$serRes$ = 1.000000e+02;
        pin11_$delay$ = 0.000000e+00;
        pin11_$rise$ = 1.000000e-12;
        pin11_$fall$ = 1.000000e-12;
        pin12_$0$_$state$ = 0;
        pin12_$0$_$serRes$ = 1.000000e+02;
        pin12_$0$_$inCap$ = 1.000000e-14;
        pin12_$0$_$res$ = 1.000000e+02;
        pin12_$0$_$delay$ = 0.000000e+00;
        pin12_$0$_$rise$ = 1.000000e-12;
        pin12_$0$_$fall$ = 1.000000e-12;
        pin12_$1$_$state$ = 0;
        pin12_$1$_$serRes$ = 1.000000e+02;
        pin12_$1$_$inCap$ = 1.000000e-14;
        pin12_$1$_$res$ = 1.000000e+02;
        pin12_$1$_$delay$ = 0.000000e+00;
        pin12_$1$_$rise$ = 1.000000e-12;
        pin12_$1$_$fall$ = 1.000000e-12;
        pin12_$2$_$state$ = 0;
        pin12_$2$_$serRes$ = 1.000000e+02;
        pin12_$2$_$inCap$ = 1.000000e-14;
        pin12_$2$_$res$ = 1.000000e+02;
        pin12_$2$_$delay$ = 0.000000e+00;
        pin12_$2$_$rise$ = 1.000000e-12;
        pin12_$2$_$fall$ = 1.000000e-12;
        pin13_$state$ = 0;
        pin13_$serRes$ = 1.000000e+02;
        pin13_$inCap$ = 1.000000e-14;
        pin13_$res$ = 1.000000e+02;
        pin13_$delay$ = 0.000000e+00;
        pin13_$rise$ = 1.000000e-12;
        pin13_$fall$ = 1.000000e-12;
        sw1_$cond$ = 1.000000e-02;
        sw1_$rise$ = 1.000000e-06;
        sw1_$fall$ = 1.000000e-06;
        clk1_$out$ = pin11_$state$;
        clk1_$isOn$ = 0;
        clk1_$halfPeriod$ = 1.000000e+06;
        clk1_$time$ = 1.000000e+06;
        _$markSt_seq1 = 0;
        _$evntTime_1 = 1.000000e-09;
        _$state_1 = 0;
        _$runSt_1 = 0;
        _$eventId_1 = 0;
        _$markSt_seq2 = 0;
        _$evntTime_2 = 1.000000e-09;
        _$state_2 = 0;
        _$runSt_2 = 0;
        _$eventId_2 = 0;
    end
    @( initial_step("tran") ) begin
        _$1 = 0;
        _$2 = 9;
        pin1_$0$_$volt$ = 0.000000e+00;
        pin1_$0$_$maxCur = 0.000000e+00;
        pin1_$0$_$minCur$ = 0.000000e+00;
        pin1_$0$_$res$ = 1.000000e+12;
        pin1_$0$_$vDelay$ = 0.000000e+00;
        pin1_$0$_$iDelay$ = 0.000000e+00;
        pin1_$0$_$rDelay$ = 0.000000e+00;
        pin1_$0$_$riseFall$ = 1.000000e-06;
        pin1_$0$_$voltTran$ = 0.000000e+00;
        pin1_$0$_$maxCurTran$ = 0.000000e+00;
        pin1_$0$_$minCurTran$ = 0.000000e+00;
        pin1_$0$_$resTran$ = 0.000000e+00;
        pin1_$1$_$volt$ = 0.000000e+00;
        pin1_$1$_$maxCur = 0.000000e+00;
        pin1_$1$_$minCur$ = 0.000000e+00;
        pin1_$1$_$res$ = 1.000000e+12;
        pin1_$1$_$vDelay$ = 0.000000e+00;
        pin1_$1$_$iDelay$ = 0.000000e+00;
        pin1_$1$_$rDelay$ = 0.000000e+00;
        pin1_$1$_$riseFall$ = 1.000000e-06;
        pin1_$1$_$voltTran$ = 0.000000e+00;
        pin1_$1$_$maxCurTran$ = 0.000000e+00;
        pin1_$1$_$minCurTran$ = 0.000000e+00;
        pin1_$1$_$resTran$ = 0.000000e+00;
        pin1_$2$_$volt$ = 0.000000e+00;
        pin1_$2$_$maxCur = 0.000000e+00;
        pin1_$2$_$minCur$ = 0.000000e+00;
        pin1_$2$_$res$ = 1.000000e+12;
        pin1_$2$_$vDelay$ = 0.000000e+00;
        pin1_$2$_$iDelay$ = 0.000000e+00;
        pin1_$2$_$rDelay$ = 0.000000e+00;
        pin1_$2$_$riseFall$ = 1.000000e-06;
        pin1_$2$_$voltTran$ = 0.000000e+00;
        pin1_$2$_$maxCurTran$ = 0.000000e+00;
        pin1_$2$_$minCurTran$ = 0.000000e+00;
        pin1_$2$_$resTran$ = 0.000000e+00;
        pin2_$volt$ = 0.000000e+00;
        pin2_$maxCur = 0.000000e+00;
        pin2_$minCur$ = 0.000000e+00;
        pin2_$res$ = 1.000000e+12;
        pin2_$vDelay$ = 0.000000e+00;
        pin2_$iDelay$ = 0.000000e+00;
        pin2_$rDelay$ = 0.000000e+00;
        pin2_$riseFall$ = 1.000000e-06;
        pin2_$voltTran$ = 0.000000e+00;
        pin2_$maxCurTran$ = 0.000000e+00;
        pin2_$minCurTran$ = 0.000000e+00;
        pin2_$resTran$ = 0.000000e+00;
        pin3_$0$_$value$ = 0.000000e+00;
        pin3_$0$_$rise$ = 0.000000e+00;
        pin3_$0$_$fall$ = 0.000000e+00;
        pin3_$1$_$value$ = 0.000000e+00;
        pin3_$1$_$rise$ = 0.000000e+00;
        pin3_$1$_$fall$ = 0.000000e+00;
        pin3_$2$_$value$ = 0.000000e+00;
        pin3_$2$_$rise$ = 0.000000e+00;
        pin3_$2$_$fall$ = 0.000000e+00;
        pin4_$value$ = 0.000000e+00;
        pin4_$rise$ = 0.000000e+00;
        pin4_$fall$ = 0.000000e+00;
        pin5_$0$_$value$ = 0.000000e+00;
        pin5_$0$_$rise$ = 0.000000e+00;
        pin5_$0$_$fall$ = 0.000000e+00;
        pin5_$1$_$value$ = 0.000000e+00;
        pin5_$1$_$rise$ = 0.000000e+00;
        pin5_$1$_$fall$ = 0.000000e+00;
        pin5_$2$_$value$ = 0.000000e+00;
        pin5_$2$_$rise$ = 0.000000e+00;
        pin5_$2$_$fall$ = 0.000000e+00;
        pin6_$value$ = 0.000000e+00;
        pin6_$rise$ = 0.000000e+00;
        pin6_$fall$ = 0.000000e+00;
        pin8_$0$_$inCap$ = 1.000000e-14;
        pin8_$1$_$inCap$ = 1.000000e-14;
        pin8_$2$_$inCap$ = 1.000000e-14;
        pin9_$inCap$ = 1.000000e-14;
        pin10_$0$_$state$ = 0;
        pin10_$0$_$serRes$ = 1.000000e+02;
        pin10_$0$_$delay$ = 0.000000e+00;
        pin10_$0$_$rise$ = 1.000000e-12;
        pin10_$0$_$fall$ = 1.000000e-12;
        pin10_$1$_$state$ = 0;
        pin10_$1$_$serRes$ = 1.000000e+02;
        pin10_$1$_$delay$ = 0.000000e+00;
        pin10_$1$_$rise$ = 1.000000e-12;
        pin10_$1$_$fall$ = 1.000000e-12;
        pin10_$2$_$state$ = 0;
        pin10_$2$_$serRes$ = 1.000000e+02;
        pin10_$2$_$delay$ = 0.000000e+00;
        pin10_$2$_$rise$ = 1.000000e-12;
        pin10_$2$_$fall$ = 1.000000e-12;
        pin11_$state$ = 0;
        pin11_$serRes$ = 1.000000e+02;
        pin11_$delay$ = 0.000000e+00;
        pin11_$rise$ = 1.000000e-12;
        pin11_$fall$ = 1.000000e-12;
        pin12_$0$_$state$ = 0;
        pin12_$0$_$serRes$ = 1.000000e+02;
        pin12_$0$_$inCap$ = 1.000000e-14;
        pin12_$0$_$res$ = 1.000000e+02;
        pin12_$0$_$delay$ = 0.000000e+00;
        pin12_$0$_$rise$ = 1.000000e-12;
        pin12_$0$_$fall$ = 1.000000e-12;
        pin12_$1$_$state$ = 0;
        pin12_$1$_$serRes$ = 1.000000e+02;
        pin12_$1$_$inCap$ = 1.000000e-14;
        pin12_$1$_$res$ = 1.000000e+02;
        pin12_$1$_$delay$ = 0.000000e+00;
        pin12_$1$_$rise$ = 1.000000e-12;
        pin12_$1$_$fall$ = 1.000000e-12;
        pin12_$2$_$state$ = 0;
        pin12_$2$_$serRes$ = 1.000000e+02;
        pin12_$2$_$inCap$ = 1.000000e-14;
        pin12_$2$_$res$ = 1.000000e+02;
        pin12_$2$_$delay$ = 0.000000e+00;
        pin12_$2$_$rise$ = 1.000000e-12;
        pin12_$2$_$fall$ = 1.000000e-12;
        pin13_$state$ = 0;
        pin13_$serRes$ = 1.000000e+02;
        pin13_$inCap$ = 1.000000e-14;
        pin13_$res$ = 1.000000e+02;
        pin13_$delay$ = 0.000000e+00;
        pin13_$rise$ = 1.000000e-12;
        pin13_$fall$ = 1.000000e-12;
        sw1_$cond$ = 1.000000e-02;
        sw1_$rise$ = 1.000000e-06;
        sw1_$fall$ = 1.000000e-06;
        clk1_$out$ = pin11_$state$;
        clk1_$isOn$ = 0;
        clk1_$halfPeriod$ = 1.000000e+06;
        clk1_$time$ = 1.000000e+06;
        _$markSt_seq1 = 0;
        _$evntTime_1 = 1.000000e-09;
        _$state_1 = 0;
        _$runSt_1 = 0;
        _$eventId_1 = 0;
        _$markSt_seq2 = 0;
        _$evntTime_2 = 1.000000e-09;
        _$state_2 = 0;
        _$runSt_2 = 0;
        _$eventId_2 = 0;
    end
    @( timer(_$evntTime_1) )
        if( ( _$eventId_1 ) == ( 0 ) )
            _$runSt_1 = 1;
    @( timer(_$evntTime_2) )
        if( ( _$eventId_2 ) == ( 0 ) )
            _$runSt_2 = 1;
    @( cross(V(pin7) - 5.000000e-01, 0) )
        if( ( _$eventId_2 ) == ( 1 ) )
            _$runSt_2 = 1;
    if( ( TEST_SEQ_PARAM ) == ( 1 ) )
        while( _$runSt_1 ) begin
            _$runSt_1 = 0;
            case( _$state_1 )
                0: begin
                    pin1_$0$_$volt$ = 2.000000e+00;
                    pin1_$0$_$maxCur = 1.000000e-02;
                    pin1_$0$_$minCur$ = -1.000000e-02;
                    pin1_$0$_$res$ = 9.999999e+05;
                    pin1_$0$_$vDelay$ = 0.000000e+00;
                    pin1_$0$_$iDelay$ = 1.000000e-06;
                    pin1_$0$_$rDelay$ = 1.000000e-06;
                    pin1_$0$_$riseFall$ = 1.000000e-06;
                    pin1_$1$_$volt$ = 2.000000e+00;
                    pin1_$1$_$maxCur = 1.000000e-02;
                    pin1_$1$_$minCur$ = -1.000000e-02;
                    pin1_$1$_$res$ = 9.999999e+05;
                    pin1_$1$_$vDelay$ = 0.000000e+00;
                    pin1_$1$_$iDelay$ = 1.000000e-06;
                    pin1_$1$_$rDelay$ = 1.000000e-06;
                    pin1_$1$_$riseFall$ = 1.000000e-06;
                    pin1_$2$_$volt$ = 2.000000e+00;
                    pin1_$2$_$maxCur = 1.000000e-02;
                    pin1_$2$_$minCur$ = -1.000000e-02;
                    pin1_$2$_$res$ = 9.999999e+05;
                    pin1_$2$_$vDelay$ = 0.000000e+00;
                    pin1_$2$_$iDelay$ = 1.000000e-06;
                    pin1_$2$_$rDelay$ = 1.000000e-06;
                    pin1_$2$_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 1;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                1: begin
                    pin1_$0$_$volt$ = 5.000000e+00;
                    pin1_$0$_$maxCur = 0.000000e+00;
                    pin1_$0$_$minCur$ = -2.000000e-02;
                    pin1_$0$_$res$ = 5.000000e+05;
                    pin1_$0$_$vDelay$ = 1.000000e-06;
                    pin1_$0$_$iDelay$ = 0.000000e+00;
                    pin1_$0$_$rDelay$ = 0.000000e+00;
                    pin1_$0$_$riseFall$ = 1.000000e-06;
                    pin1_$1$_$volt$ = 5.000000e+00;
                    pin1_$1$_$maxCur = 0.000000e+00;
                    pin1_$1$_$minCur$ = -2.000000e-02;
                    pin1_$1$_$res$ = 5.000000e+05;
                    pin1_$1$_$vDelay$ = 1.000000e-06;
                    pin1_$1$_$iDelay$ = 0.000000e+00;
                    pin1_$1$_$rDelay$ = 0.000000e+00;
                    pin1_$1$_$riseFall$ = 1.000000e-06;
                    pin1_$2$_$volt$ = 5.000000e+00;
                    pin1_$2$_$maxCur = 0.000000e+00;
                    pin1_$2$_$minCur$ = -2.000000e-02;
                    pin1_$2$_$res$ = 5.000000e+05;
                    pin1_$2$_$vDelay$ = 1.000000e-06;
                    pin1_$2$_$iDelay$ = 0.000000e+00;
                    pin1_$2$_$rDelay$ = 0.000000e+00;
                    pin1_$2$_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 2;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                2: begin
                    pin1_$0$_$volt$ = 0.000000e+00;
                    pin1_$0$_$maxCur = 0.000000e+00;
                    pin1_$0$_$minCur$ = 0.000000e+00;
                    pin1_$0$_$res$ = 1.000000e+00;
                    pin1_$0$_$vDelay$ = 1.000000e-06;
                    pin1_$0$_$iDelay$ = 0.000000e+00;
                    pin1_$0$_$rDelay$ = 0.000000e+00;
                    pin1_$0$_$riseFall$ = 1.000000e-06;
                    pin1_$1$_$volt$ = 0.000000e+00;
                    pin1_$1$_$maxCur = 0.000000e+00;
                    pin1_$1$_$minCur$ = 0.000000e+00;
                    pin1_$1$_$res$ = 1.000000e+00;
                    pin1_$1$_$vDelay$ = 1.000000e-06;
                    pin1_$1$_$iDelay$ = 0.000000e+00;
                    pin1_$1$_$rDelay$ = 0.000000e+00;
                    pin1_$1$_$riseFall$ = 1.000000e-06;
                    pin1_$2$_$volt$ = 0.000000e+00;
                    pin1_$2$_$maxCur = 0.000000e+00;
                    pin1_$2$_$minCur$ = 0.000000e+00;
                    pin1_$2$_$res$ = 1.000000e+00;
                    pin1_$2$_$vDelay$ = 1.000000e-06;
                    pin1_$2$_$iDelay$ = 0.000000e+00;
                    pin1_$2$_$rDelay$ = 0.000000e+00;
                    pin1_$2$_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 3;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                3: begin
                    pin1_$0$_$volt$ = 2.000000e+00;
                    pin1_$0$_$maxCur = 1.000000e-02;
                    pin1_$0$_$minCur$ = -1.000000e-02;
                    pin1_$0$_$res$ = 9.999999e+05;
                    pin1_$0$_$vDelay$ = 0.000000e+00;
                    pin1_$0$_$iDelay$ = 1.000000e-06;
                    pin1_$0$_$rDelay$ = 1.000000e-06;
                    pin1_$0$_$riseFall$ = 1.000000e-06;
                    pin1_$1$_$volt$ = 2.000000e+00;
                    pin1_$1$_$maxCur = 1.000000e-02;
                    pin1_$1$_$minCur$ = -1.000000e-02;
                    pin1_$1$_$res$ = 9.999999e+05;
                    pin1_$1$_$vDelay$ = 0.000000e+00;
                    pin1_$1$_$iDelay$ = 1.000000e-06;
                    pin1_$1$_$rDelay$ = 1.000000e-06;
                    pin1_$1$_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 4;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                4: begin
                    pin2_$volt$ = 5.000000e+00;
                    pin2_$maxCur = 0.000000e+00;
                    pin2_$minCur$ = -2.000000e-02;
                    pin2_$res$ = 5.000000e+05;
                    pin2_$vDelay$ = 1.000000e-06;
                    pin2_$iDelay$ = 0.000000e+00;
                    pin2_$rDelay$ = 0.000000e+00;
                    pin2_$riseFall$ = 1.000000e-06;
                    _$eventId_1 = 0;
                    _$state_1 = 5;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                5: begin
                    _$markSt_seq1 = !_$markSt_seq1;
                    pin3_$0$_$rise$ = 3.000000e-05;
                    pin3_$0$_$fall$ = 3.000000e-05;
                    pin3_$1$_$rise$ = 3.000000e-05;
                    pin3_$1$_$fall$ = 3.000000e-05;
                    pin3_$2$_$rise$ = 3.000000e-05;
                    pin3_$2$_$fall$ = 3.000000e-05;
                    pin3_$0$_$value$ = 2.000000e+00;
                    pin3_$1$_$value$ = 2.000000e+00;
                    pin3_$2$_$value$ = 2.000000e+00;
                    _$eventId_1 = 0;
                    _$state_1 = 6;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                6: begin
                    pin3_$1$_$value$ = 2.000000e+00;
                    _$eventId_1 = 0;
                    _$state_1 = 7;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                7: begin
                    pin4_$value$ = 2.000000e+00;
                    _$eventId_1 = 0;
                    _$state_1 = 8;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                8: begin
                    _$markSt_seq1 = !_$markSt_seq1;
                    pin5_$0$_$rise$ = 5.000000e-05;
                    pin5_$0$_$fall$ = 5.000000e-05;
                    pin5_$1$_$rise$ = 5.000000e-05;
                    pin5_$1$_$fall$ = 5.000000e-05;
                    pin5_$2$_$rise$ = 5.000000e-05;
                    pin5_$2$_$fall$ = 5.000000e-05;
                    pin5_$0$_$value$ = -1.000000e-02;
                    pin5_$1$_$value$ = -1.000000e-02;
                    pin5_$2$_$value$ = -1.000000e-02;
                    _$eventId_1 = 0;
                    _$state_1 = 9;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                9: begin
                    pin5_$1$_$value$ = 2.000000e+00;
                    pin5_$2$_$value$ = 2.000000e+00;
                    _$eventId_1 = 0;
                    _$state_1 = 10;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                10: begin
                    pin6_$value$ = -2.000000e-02;
                    _$eventId_1 = 0;
                    _$state_1 = 11;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                11: begin
                    _$markSt_seq1 = !_$markSt_seq1;
                    _$eventId_1 = 0;
                    _$state_1 = 12;
                    _$evntTime_1 = ( $abstime ) + ( 1.000000e-04 );
                end
                12:
                    $finish;
            endcase
        end
    if( ( TEST_SEQ_PARAM ) == ( 2 ) )
        while( _$runSt_2 ) begin
            _$runSt_2 = 0;
            case( _$state_2 )
                0: begin
                    pin4_$value$ = 2.000000e+00;
                    _$eventId_2 = 0;
                    _$state_2 = 1;
                    _$evntTime_2 = ( $abstime ) + ( 1.000000e-04 );
                end
                1: begin
                    pin11_$state$ = 1;
                    _$eventId_2 = 0;
                    _$state_2 = 2;
                    _$evntTime_2 = ( $abstime ) + ( 1.000000e-04 );
                end
                2: begin
                    pin12_$0$_$res$ = 1.000000e+12;
                    pin12_$1$_$res$ = 1.000000e+12;
                    pin12_$2$_$res$ = 1.000000e+12;
                    pin13_$res$ = 1.000000e+12;
                    _$eventId_2 = 1;
                    _$state_2 = 3;
                end
                3: begin
                    pin12_$0$_$res$ = pin12_$0$_$serRes$;
                    pin12_$1$_$res$ = pin12_$1$_$serRes$;
                    pin12_$2$_$res$ = pin12_$2$_$serRes$;
                    pin13_$res$ = pin13_$serRes$;
                    pin13_$state$ = 1;
                    pin12_$0$_$state$ = 1;
                    pin12_$1$_$state$ = 0;
                    pin12_$2$_$state$ = 1;
                    clk1_$halfPeriod$ = 5.000000e-06;
                    clk1_$isOn$ = 1;
                    clk1_$time$ = ( $abstime ) + ( 1.000000e-09 );
                    sw1_$cond$ = 0.000000e+00;
                    _$eventId_2 = 0;
                    _$state_2 = 4;
                    _$evntTime_2 = ( $abstime ) + ( 2.000000e-04 );
                end
                4:
                    $finish;
            endcase
        end
    @( timer(clk1_$time$) ) begin
        clk1_$out$ = !clk1_$out$;
        pin11_$state$ = clk1_$out$;
        if( ( clk1_$isOn$ ) || ( clk1_$out$ ) )
            clk1_$time$ = ( $abstime ) + ( clk1_$halfPeriod$ );
    end
    pin1_$0$_$voltTran$ = transition(pin1_$0$_$volt$, pin1_$0$_$vDelay$, pin1_$0$_$riseFall$, pin1_$0$_$riseFall$);
    pin1_$0$_$maxCurTran$ = transition(pin1_$0$_$maxCur, pin1_$0$_$iDelay$, pin1_$0$_$riseFall$, pin1_$0$_$riseFall$);
    pin1_$0$_$minCurTran$ = transition(pin1_$0$_$minCur$, pin1_$0$_$iDelay$, pin1_$0$_$riseFall$, pin1_$0$_$riseFall$);
    pin1_$0$_$resTran$ = transition(pin1_$0$_$res$, pin1_$0$_$rDelay$, pin1_$0$_$riseFall$, pin1_$0$_$riseFall$);
    I(pin1[0]) <+ ( ( ( tanh(( 5.000000e+01 )*( ( V(pin1[0]) ) - ( pin1_$0$_$voltTran$ ) )) )*( 5.000000e-01 ) )*( ( pin1_$0$_$maxCurTran$ ) - ( pin1_$0$_$minCurTran$ ) ) ) + ( ( 5.000000e-01 )*( ( pin1_$0$_$maxCurTran$ ) + ( pin1_$0$_$minCurTran$ ) ) );
    I(pin1[0]) <+ ( V(pin1[0]) )/( pin1_$0$_$resTran$ );
    I(pin1[0]) <+ ( 1.000000e-12 )*( ddt(V(pin1[0])) );
    pin1_$1$_$voltTran$ = transition(pin1_$1$_$volt$, pin1_$1$_$vDelay$, pin1_$1$_$riseFall$, pin1_$1$_$riseFall$);
    pin1_$1$_$maxCurTran$ = transition(pin1_$1$_$maxCur, pin1_$1$_$iDelay$, pin1_$1$_$riseFall$, pin1_$1$_$riseFall$);
    pin1_$1$_$minCurTran$ = transition(pin1_$1$_$minCur$, pin1_$1$_$iDelay$, pin1_$1$_$riseFall$, pin1_$1$_$riseFall$);
    pin1_$1$_$resTran$ = transition(pin1_$1$_$res$, pin1_$1$_$rDelay$, pin1_$1$_$riseFall$, pin1_$1$_$riseFall$);
    I(pin1[1]) <+ ( ( ( tanh(( 5.000000e+01 )*( ( V(pin1[1]) ) - ( pin1_$1$_$voltTran$ ) )) )*( 5.000000e-01 ) )*( ( pin1_$1$_$maxCurTran$ ) - ( pin1_$1$_$minCurTran$ ) ) ) + ( ( 5.000000e-01 )*( ( pin1_$1$_$maxCurTran$ ) + ( pin1_$1$_$minCurTran$ ) ) );
    I(pin1[1]) <+ ( V(pin1[1]) )/( pin1_$1$_$resTran$ );
    I(pin1[1]) <+ ( 1.000000e-12 )*( ddt(V(pin1[1])) );
    pin1_$2$_$voltTran$ = transition(pin1_$2$_$volt$, pin1_$2$_$vDelay$, pin1_$2$_$riseFall$, pin1_$2$_$riseFall$);
    pin1_$2$_$maxCurTran$ = transition(pin1_$2$_$maxCur, pin1_$2$_$iDelay$, pin1_$2$_$riseFall$, pin1_$2$_$riseFall$);
    pin1_$2$_$minCurTran$ = transition(pin1_$2$_$minCur$, pin1_$2$_$iDelay$, pin1_$2$_$riseFall$, pin1_$2$_$riseFall$);
    pin1_$2$_$resTran$ = transition(pin1_$2$_$res$, pin1_$2$_$rDelay$, pin1_$2$_$riseFall$, pin1_$2$_$riseFall$);
    I(pin1[2]) <+ ( ( ( tanh(( 5.000000e+01 )*( ( V(pin1[2]) ) - ( pin1_$2$_$voltTran$ ) )) )*( 5.000000e-01 ) )*( ( pin1_$2$_$maxCurTran$ ) - ( pin1_$2$_$minCurTran$ ) ) ) + ( ( 5.000000e-01 )*( ( pin1_$2$_$maxCurTran$ ) + ( pin1_$2$_$minCurTran$ ) ) );
    I(pin1[2]) <+ ( V(pin1[2]) )/( pin1_$2$_$resTran$ );
    I(pin1[2]) <+ ( 1.000000e-12 )*( ddt(V(pin1[2])) );
    pin2_$voltTran$ = transition(pin2_$volt$, pin2_$vDelay$, pin2_$riseFall$, pin2_$riseFall$);
    pin2_$maxCurTran$ = transition(pin2_$maxCur, pin2_$iDelay$, pin2_$riseFall$, pin2_$riseFall$);
    pin2_$minCurTran$ = transition(pin2_$minCur$, pin2_$iDelay$, pin2_$riseFall$, pin2_$riseFall$);
    pin2_$resTran$ = transition(pin2_$res$, pin2_$rDelay$, pin2_$riseFall$, pin2_$riseFall$);
    I(pin2) <+ ( ( ( tanh(( 5.000000e+01 )*( ( V(pin2) ) - ( pin2_$voltTran$ ) )) )*( 5.000000e-01 ) )*( ( pin2_$maxCurTran$ ) - ( pin2_$minCurTran$ ) ) ) + ( ( 5.000000e-01 )*( ( pin2_$maxCurTran$ ) + ( pin2_$minCurTran$ ) ) );
    I(pin2) <+ ( V(pin2) )/( pin2_$resTran$ );
    I(pin2) <+ ( 1.000000e-12 )*( ddt(V(pin2)) );
    V(pin3[0]) <+ transition(pin3_$0$_$value$, 0.000000e+00, pin3_$0$_$rise$, pin3_$0$_$fall$);
    V(pin3[1]) <+ transition(pin3_$1$_$value$, 0.000000e+00, pin3_$1$_$rise$, pin3_$1$_$fall$);
    V(pin3[2]) <+ transition(pin3_$2$_$value$, 0.000000e+00, pin3_$2$_$rise$, pin3_$2$_$fall$);
    V(pin4) <+ transition(pin4_$value$, 0.000000e+00, pin4_$rise$, pin4_$fall$);
    I(pin5[0]) <+ transition(pin5_$0$_$value$, 0.000000e+00, pin5_$0$_$rise$, pin5_$0$_$fall$);
    I(pin5[1]) <+ transition(pin5_$1$_$value$, 0.000000e+00, pin5_$1$_$rise$, pin5_$1$_$fall$);
    I(pin5[2]) <+ transition(pin5_$2$_$value$, 0.000000e+00, pin5_$2$_$rise$, pin5_$2$_$fall$);
    I(pin6) <+ transition(pin6_$value$, 0.000000e+00, pin6_$rise$, pin6_$fall$);
    I(pin8[0]) <+ ( ddt(V(pin8[0])) )*( pin8_$0$_$inCap$ );
    I(pin8[1]) <+ ( ddt(V(pin8[1])) )*( pin8_$1$_$inCap$ );
    I(pin8[2]) <+ ( ddt(V(pin8[2])) )*( pin8_$2$_$inCap$ );
    I(pin9) <+ ( ddt(V(pin9)) )*( pin9_$inCap$ );
    V(pin10[0]) <+ ( V(pin4) )*( transition(pin10_$0$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin10_$0$_$delay$, pin10_$0$_$rise$, pin10_$0$_$fall$) );
    V(pin10[0]) <+ ( I(pin10[0]) )*( pin10_$0$_$serRes$ );
    V(pin10[1]) <+ ( V(pin4) )*( transition(pin10_$1$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin10_$1$_$delay$, pin10_$1$_$rise$, pin10_$1$_$fall$) );
    V(pin10[1]) <+ ( I(pin10[1]) )*( pin10_$1$_$serRes$ );
    V(pin10[2]) <+ ( V(pin4) )*( transition(pin10_$2$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin10_$2$_$delay$, pin10_$2$_$rise$, pin10_$2$_$fall$) );
    V(pin10[2]) <+ ( I(pin10[2]) )*( pin10_$2$_$serRes$ );
    V(pin11) <+ ( V(pin4) )*( transition(pin11_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin11_$delay$, pin11_$rise$, pin11_$fall$) );
    V(pin11) <+ ( I(pin11) )*( pin11_$serRes$ );
    V(_$3) <+ ( V(pin4) )*( transition(pin12_$0$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin12_$0$_$delay$, pin12_$0$_$rise$, pin12_$0$_$fall$) );
    V(_$3, pin12[0]) <+ ( I(_$3, pin12[0]) )*( transition(pin12_$0$_$res$, pin12_$0$_$delay$, pin12_$0$_$rise$, pin12_$0$_$fall$) );
    I(pin12[0]) <+ ( ddt(V(pin12[0])) )*( pin12_$0$_$inCap$ );
    V(_$4) <+ ( V(pin4) )*( transition(pin12_$1$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin12_$1$_$delay$, pin12_$1$_$rise$, pin12_$1$_$fall$) );
    V(_$4, pin12[1]) <+ ( I(_$4, pin12[1]) )*( transition(pin12_$1$_$res$, pin12_$1$_$delay$, pin12_$1$_$rise$, pin12_$1$_$fall$) );
    I(pin12[1]) <+ ( ddt(V(pin12[1])) )*( pin12_$1$_$inCap$ );
    V(_$5) <+ ( V(pin4) )*( transition(pin12_$2$_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin12_$2$_$delay$, pin12_$2$_$rise$, pin12_$2$_$fall$) );
    V(_$5, pin12[2]) <+ ( I(_$5, pin12[2]) )*( transition(pin12_$2$_$res$, pin12_$2$_$delay$, pin12_$2$_$rise$, pin12_$2$_$fall$) );
    I(pin12[2]) <+ ( ddt(V(pin12[2])) )*( pin12_$2$_$inCap$ );
    V(_$6) <+ ( V(pin4) )*( transition(pin13_$state$ ? ( 1.000000e+00 ) : ( 0.000000e+00 ), pin13_$delay$, pin13_$rise$, pin13_$fall$) );
    V(_$6, pin13) <+ ( I(_$6, pin13) )*( transition(pin13_$res$, pin13_$delay$, pin13_$rise$, pin13_$fall$) );
    I(pin13) <+ ( ddt(V(pin13)) )*( pin13_$inCap$ );
    I(pin7, pin14) <+ ( V(pin7, pin14) )*( transition(sw1_$cond$, 0.000000e+00, sw1_$rise$, sw1_$fall$) );
    V(MARK_seq1) <+ transition(_$markSt_seq1 ? ( 1.0 ) : ( 0.0 ), 0.000000e+00, 1.000000e-10, 1.000000e-10);
    V(MARK_seq2) <+ transition(_$markSt_seq2 ? ( 1.0 ) : ( 0.0 ), 0.000000e+00, 1.000000e-10, 1.000000e-10);
end
endmodule'''  
        #print(mod.getVA())
        self.maxDiff = None
        self.assertEqual(mod.getVA()[323:], ref)    
 
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
        evnt1 = Cross(pin7.v, Real(0.5), "both")
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
        evnt1 = Cross(pin7.v, Real(0.5), "both")
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
        evnt1 = Cross(pin7.v, Real(0.5), "both")
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
    

