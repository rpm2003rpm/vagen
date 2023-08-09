## @package vagen
#  VerilogA generator
#

##
#  @mainpage  VAGEN - VerilogA generator
#
#  @section description_main Description
#  vagen is a verilogA  generator that can be used for  transient verification
#  and modeling of complex analog IPs. It provides a   wide range   of   basic 
#  models with voltage sources, current sources,  digital  interfaces, clocks, 
#  switches, and source measure units that you  can  use  to  build your model 
#  upon.
#
#  @section license_main License
#     
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    14/02/23 13:37:31
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

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------
from vagen.hilevelmod import HiLevelMod, Module, Branch, Cmd, CmdList, Electrical, \
                     Real, Integer, Bool,\
                     RealVar, IntegerVar, Vdc, Smu, DigIn, DigOut, DigInOut, \
                     DigBusIn, DigBusOut, DigBusInOut, \
                     If, For, While, Case, Repeat, At, \
                     Cross, Above, Timer, InitialStep, FinalStep, \
                     temp, vt, abstime, \
                     random, uDistReal, uDistInt, uDistInt, \
                     gaussDistInt, gaussDistReal, expDistInt, expDistReal, \
                     poissonDistInt, poissonDistReal, \
                     lastCrossing, analysis, acStim, \
                     absDelay, transition, slew, ternary, \
                     limexp, exp, ddt, idt, ceil, floor, ln, log, sqrt, \
                     sin, cos, tan, asin, acos, atan, atan2, hypot, \
                     sinh, cosh, tanh, asinh, acosh, atanh, \
                     Strobe, Write, Discontinuity, BoundStep, \
                     Fopen, Fwrite, Fstrobe, Fclose, \
                     Finish, Error, Fatal, WaitUs, WaitSignal
            
            


