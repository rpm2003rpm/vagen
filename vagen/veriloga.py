## @package va
#  VerilogA generator
# 
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    05/02/23 22:36:08
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
#  AUTHORS OR COPYRIGHT HOLDERS BE  LIABLE FOR ANY  CLAIM,  DAMAGES  OR  other 
#  LIABILITY, WHETHER IN AN ACTION OF  CONTRACT, TORT  OR  otherWISE,  ARISING 
#  FROM, OUT OF OR IN CONNECTION  WITH  THE  SOFTWARE  OR  THE  USE  OR  other  
#  DEALINGS IN THE SOFTWARE. 
#
################################################################################

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------
from datetime import date


#-------------------------------------------------------------------------------
# Check if the type of variable matches the Type. Raise an assertion error
# if doesn't 
# Parameters:
# param - string representing the name of the variable
# var - variable
# Type - type that the variable should match
#-------------------------------------------------------------------------------
def checkType(param, var, Type):
    assert type(var) == Type, \
           param + " must be a " + str(Type) + " but a " + \
           str(type(var)) + " was given"


#-------------------------------------------------------------------------------
# Check if the variable is instance of Type. Raise an assertion error if doesn't 
# Parameters:
# param - string representing the name of the variable
# var - variable
# Type - type that the variable should match
#-------------------------------------------------------------------------------
def checkInstance(param, var, Type):
    assert isinstance(var, Type), \
           param + " must be a " + str(Type) + " but a " + \
           str(type(var)) + " was given"


#-------------------------------------------------------------------------------
# Check if the variable isn't instance of Type. Raise an assertion error if 
# doesn't 
# Parameters:
# param - string representing the name of the variable
# var - variable
# Type - type that the variable should match
#-------------------------------------------------------------------------------
def checkNotInstance(param, var, Type):
    assert not isinstance(var, Type), \
           param + " can't be a " + str(Type)


#-------------------------------------------------------------------------------
# Creates a comment block
# Parameters:
# message - string representing the comment
# padding - number of tabs by which the text will be shifted left  
# align - center, left or right 
#-------------------------------------------------------------------------------
def blockComment(padding, message, align = "center"):
    #assertions 
    checkType("padding", padding, int)
    checkType("message", message, str)
    checkType("align", align, str)
    #Calculate the block size and the text line width.
    #If the text width is lower than 20 columns, don't return anything
    size = 80 - padding*4
    lineLen = size - 6
    if lineLen < 20:
        return '' 
    #Beginning of the block comment 
    result = "    "*padding + "/" + '*'*(size - 2) + "\n"
    #Look for \n and split the message in lines
    msgChunks = message.split('\n')
    #Go trough every line and build the message. If the message can't fit
    #in a row, it will be split in as many rows as necessary
    for item in msgChunks:
        lines = [item[i:i+lineLen] for i in range(0, len(item), lineLen)]
        for lineItem in lines:
            if align == "center":
                blankSpaceLen = lineLen-len(lineItem)
                half  = round(blankSpaceLen/2)
                left  = " * " + " "*half
                right = " "*(blankSpaceLen - half) + " * " 
            elif align == "left":
                left  = " * " 
                right = " "*(lineLen - len(lineItem)) + " * "
            else:
                left = " * " + " "*(lineLen - len(lineItem))
                right = " * "
            result = result + "    "*padding + left + lineItem + right + "\n"
    #End of the block comment
    result = result + "    "*padding + " " + '*'*(size - 2) + "/\n"
    return result 
         

#-------------------------------------------------------------------------------
# Class of Real operators
#-------------------------------------------------------------------------------
class RealOp():

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        self.value = value
    
    #---------------------------------------------------------------------------
    # Return the operator value
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value
    
    #---------------------------------------------------------------------------
    # adition override
    #---------------------------------------------------------------------------
    def __add__(self, other):
        checkInstance("other", other, RealOp)
        return RealOp("( " + str(self) + ' ) + ( ' + str(other) + " )")

    #---------------------------------------------------------------------------
    # subtraction override
    #---------------------------------------------------------------------------
    def __sub__(self, other):
        checkInstance("other", other, RealOp)
        return RealOp("( " + str(self) + ' ) - ( ' + str(other) + " )")

    #---------------------------------------------------------------------------
    # multiplication override
    #---------------------------------------------------------------------------
    def __mul__(self, other):
        checkInstance("other", other, RealOp)
        return RealOp('( '+ str(self) + ' )*( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # true division override
    #---------------------------------------------------------------------------
    def __truediv__(self, other):
        checkInstance("other", other, RealOp)
        return RealOp('( '+ str(self) + ' )/( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # power override
    #---------------------------------------------------------------------------
    def __pow__(self, other):
        checkInstance("other", other, RealOp)
        return RealOp('pow('+ str(self) + ', ' + str(other) + ')')

    #---------------------------------------------------------------------------
    # greater than override
    #---------------------------------------------------------------------------
    def __gt__(self, other):
        checkInstance("other", other, RealOp)
        return BoolOp('( '+ str(self) + ' ) > ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # less than override
    #---------------------------------------------------------------------------
    def __lt__(self, other):
        checkInstance("other", other, RealOp)
        return BoolOp('( '+ str(self) + ' ) < ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # less than equal override
    #---------------------------------------------------------------------------
    def __le__(self, other):
        checkInstance("other", other, RealOp)
        return BoolOp('( '+ str(self) + ' ) <= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # greater than equal override
    #---------------------------------------------------------------------------
    def __ge__(self, other):
        checkInstance("other", other, RealOp)
        return BoolOp('( '+ str(self) + ' ) >= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        checkInstance("other", other, RealOp)
        return BoolOp('( '+ str(self) + ' ) == ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # not equal override
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        checkInstance("other", other, RealOp)
        return BoolOp('( '+ str(self) + ' ) != ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # negation override
    #---------------------------------------------------------------------------
    def __neg__(self):
        return RealOp('-( '+ str(self) + ' )')
    
    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __pos__(self):
        return self

    #---------------------------------------------------------------------------
    # abs override
    #---------------------------------------------------------------------------
    def __abs__(self):
        return RealOp('abs( '+ str(self) + ' )')

    #---------------------------------------------------------------------------
    # String representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value


#-------------------------------------------------------------------------------
# class of binary operators
#-------------------------------------------------------------------------------
class BoolOp():

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        self.value = value
    
    #---------------------------------------------------------------------------
    # Return the operator value
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value

    #---------------------------------------------------------------------------
    # convert to integer type.
    #---------------------------------------------------------------------------
    def toInteger(self):
        return ternary(self, Integer(1), Integer(0)) 
        
    #---------------------------------------------------------------------------
    # convert to real type.
    #---------------------------------------------------------------------------
    def toReal(self):
        return ternary(self, Real(1), Real(0)) 

    #---------------------------------------------------------------------------
    # and logic override
    #---------------------------------------------------------------------------
    def __and__(self, other):
        checkInstance("other", other, BoolOp)
        return BoolOp('( ' + str(self) + ' ) && ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # or logic override
    #---------------------------------------------------------------------------
    def __or__(self, other):
        checkInstance("other", other, BoolOp)
        return BoolOp('( ' + str(self) + ' ) || ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # xor logic override
    #---------------------------------------------------------------------------
    def __xor__(self, other):
        checkInstance("other", other, BoolOp)
        return (self & ~other) | (~self & other)

    #---------------------------------------------------------------------------
    # iversion override
    #---------------------------------------------------------------------------
    def __invert__(self):
        return BoolOp('!( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # String representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value


#-------------------------------------------------------------------------------
# class of integer operators
#-------------------------------------------------------------------------------
class IntegerOp():

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        self.value = value
    
    #---------------------------------------------------------------------------
    # return the operator value
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value

    #---------------------------------------------------------------------------
    # convert to boolean type
    #---------------------------------------------------------------------------
    def toBool(self):
        return BoolOp(str(self))

    #---------------------------------------------------------------------------
    # convert to Real
    #---------------------------------------------------------------------------
    def toReal(self):
        return RealOp(str(self))

    #---------------------------------------------------------------------------
    # adition override
    #---------------------------------------------------------------------------
    def __add__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp("( " + str(self) + ' ) + ( ' + str(other) + " )")

    #---------------------------------------------------------------------------
    # subtraction override
    #---------------------------------------------------------------------------
    def __sub__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp("( " + str(self) + ' ) - ( ' + str(other) + " )")

    #---------------------------------------------------------------------------
    # multiplication override
    #---------------------------------------------------------------------------
    def __mul__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('( ' + str(self) + ' ) * ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # true division override
    #---------------------------------------------------------------------------
    def __truediv__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('( ' + str(self) + ' ) / ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # module override
    #---------------------------------------------------------------------------
    def __mod__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('( ' + str(self) + ' ) % ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # power override
    #---------------------------------------------------------------------------
    def __pow__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('pow(' + str(self) + ', ' + str(other) + ')')

    #---------------------------------------------------------------------------
    # right shift override
    #---------------------------------------------------------------------------
    def __rshift__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('( ' + str(self) + ' ) >> ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # left shift override
    #---------------------------------------------------------------------------
    def __lshift__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('( ' + str(self) + ' ) << ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # and logic override
    #---------------------------------------------------------------------------
    def __and__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('( ' + str(self) + ' ) & ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # or logic override
    #---------------------------------------------------------------------------
    def __or__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('( ' + str(self) + ' ) | ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # xor logic override
    #---------------------------------------------------------------------------
    def __xor__(self, other):
        checkInstance("other", other, IntegerOp)
        return IntegerOp('( ' + str(self) + ' ) ^ ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # less than override
    #---------------------------------------------------------------------------
    def __lt__(self, other):
        checkInstance("other", other, IntegerOp)
        return BoolOp('( ' + str(self) + ' ) < ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # greater than override
    #---------------------------------------------------------------------------
    def __gt__(self, other):
        checkInstance("other", other, IntegerOp)
        return BoolOp('( ' + str(self) + ' ) > ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # less than equal override
    #---------------------------------------------------------------------------
    def __le__(self, other):
        checkInstance("other", other, IntegerOp)
        return BoolOp('( ' + str(self) + ' ) <= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # greater than equal override
    #---------------------------------------------------------------------------
    def __ge__(self, other):
        checkInstance("other", other, IntegerOp)
        return BoolOp('( ' + str(self) + ' ) >= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        checkInstance("other", other, IntegerOp)
        return BoolOp('( ' + str(self) + ' ) == ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # not equal override
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        checkInstance("other", other, IntegerOp)
        return BoolOp('( ' + str(self) + ' ) != ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # negation override
    #---------------------------------------------------------------------------
    def __neg__(self):
        return IntegerOp('-( ' + str(self) + ' )')
    
    #---------------------------------------------------------------------------
    # abs override
    #---------------------------------------------------------------------------
    def __abs__(self):
        return IntegerOp('abs( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __pos__(self):
        return self

    #---------------------------------------------------------------------------
    # iversion override
    #---------------------------------------------------------------------------
    def __invert__(self):
        return IntegerOp('~( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # String representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value


#-------------------------------------------------------------------------------
# Integer constant class
#-------------------------------------------------------------------------------
class Integer(IntegerOp):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - integer
    #---------------------------------------------------------------------------
    def __init__(self, value):
        try:
            value = str(int(value))
        except:
            raise TypeError("Can't convert value to integer")
        super(Integer, self).__init__(value)


#-------------------------------------------------------------------------------
# Boolean constant class
#-------------------------------------------------------------------------------
class Bool(BoolOp):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - boolean value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        try:
            value = str(int(bool(value)))
        except:
            raise TypeError("Can't convert value to boolean")
        super(Bool, self).__init__(value)


#-------------------------------------------------------------------------------
# Real constant class
#-------------------------------------------------------------------------------
class Real(RealOp):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - real value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        try:
            value = "{:e}".format(float(value))
        except:
            raise TypeError("Can't convert value to float")
        super(Real, self).__init__(value)



#-------------------------------------------------------------------------------
# variable class
#-------------------------------------------------------------------------------
class Var():

    #---------------------------------------------------------------------------
    # Return a command representing the attribution to a variable
    # Parameters:
    # value - An IntegerOp representing the value
    #---------------------------------------------------------------------------
    def equal(self, value):
        assert isinstance(value, IntegerOp) or \
               isinstance(value, BoolOp) or  \
               isinstance(value, RealOp), \
               "Only numbers that can be converted integer are allowed, but " +\
               "a " + str(type(value)) + " was given instead"
        return Cmd(self.getValue() + ' = ' + str(value))
        
        
        
#-------------------------------------------------------------------------------
# Integer variable class
#-------------------------------------------------------------------------------
class IntegerVar(IntegerOp, Var):
    pass
    
#-------------------------------------------------------------------------------
# Real variable class
#-------------------------------------------------------------------------------
class RealVar(RealOp, Var):
    pass


#-------------------------------------------------------------------------------
# Boolean variable class
#-------------------------------------------------------------------------------
class BoolVar(BoolOp, Var):
    pass

#-------------------------------------------------------------------------------
# Class of events
#-------------------------------------------------------------------------------
class Event():

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        self.value = value
    
    #---------------------------------------------------------------------------
    # return the operator value
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value

    #---------------------------------------------------------------------------
    # or logic override
    #---------------------------------------------------------------------------
    def __or__(self, other):
        checkInstance("other", other, Event)
        return Event(str(self) + ' or ' + str(other))

    #---------------------------------------------------------------------------
    # String representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value
        
        
#-------------------------------------------------------------------------------
# Command class
#-------------------------------------------------------------------------------
class Cmd:
    
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # cmd - command to be added to the va
    #---------------------------------------------------------------------------
    def __init__(self, cmd):
        checkType("cmd", cmd, str)
        self.cmd = cmd

    #---------------------------------------------------------------------------
    # Return string representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.cmd

    #---------------------------------------------------------------------------
    # Return the VA verilog command
    # Parameters:
    # padding - number of tabs by which the text will be right shifted  
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        chunks = self.cmd.split("\n")
        result = "    "*padding + chunks[0]
        for item in chunks[1:]: 
            result = result + "\n" + "    "*padding + item
        result = result + ";\n"
        return result


#-------------------------------------------------------------------------------
# Command List class
#-------------------------------------------------------------------------------
class CmdList(list, Cmd):
    
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # cmds - command to be added to the va
    #---------------------------------------------------------------------------
    def __init__(self, *cmds):
        super(CmdList, self).__init__()
        self.append(*cmds)
        
    #---------------------------------------------------------------------------
    # Return string representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return ", ".join([str(x) for x in self])
        
    #---------------------------------------------------------------------------
    # Fatten
    #---------------------------------------------------------------------------
    def flat(self):
        ans = []
        for item in self:
            if type(item) == CmdList:   
                ans = ans + item.flat()
            else:
                ans.append(item)  
        return ans

    #---------------------------------------------------------------------------
    # append override 
    #---------------------------------------------------------------------------
    def append(self, *cmds):
        i = 1
        for cmd in cmds:
            assert isinstance(cmd, Cmd) and \
                   not isinstance(cmd, WaitAnalogEvent), "cmd[" + str(i) + "]"+\
                   " must be an instance of Cmd and can't be and instance of "+\
                   "WaitAnalogEvent, but a " + str(type(cmd)) +\
                   " was given instead"
            super(CmdList, self).append(cmd)
            i = i + 1
        
    #---------------------------------------------------------------------------
    # Return the VA verilog command
    # Parameters:
    # padding number of tabs by which the text will be right shifted
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        result = ""
        for item in self:
            result = result + item.getVA(padding)
        return result


#-------------------------------------------------------------------------------
# Command Block Class
#-------------------------------------------------------------------------------
class Block(CmdList):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # header - header of the command block
    # *cmds - variable number of commands to be added
    #---------------------------------------------------------------------------
    def __init__(self, header, *cmds):
        checkType("header", header, str)
        self.header  = header
        super(Block, self).__init__(*cmds)
        
    #---------------------------------------------------------------------------
    # Return the VA verilog command
    # Parameters:
    # padding number of tabs by which the text will be right shifted
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        length = len(self.flat())
        if length > 1:
            result = "    "*padding + self.header + " begin\n"
            result = result + super(Block, self).getVA(padding + 1)
            result = result + "    "*padding + "end\n"
        elif length == 1:
            result = "    "*padding + self.header + "\n"
            result = result + super(Block, self).getVA(padding + 1)            
        else:
            result = "    "*padding + self.header + ";\n"
        return result


#-------------------------------------------------------------------------------
# Class generated by the At function.
#-------------------------------------------------------------------------------
class WaitAnalogEvent(Block):
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # event - Event to be waited for
    # *cmds - variable number of commands to be added
    #---------------------------------------------------------------------------
    def __init__(self, event, *cmds):
        checkInstance("event", event, Event)
        super(WaitAnalogEvent, self).__init__('@( ' + str(event) + ' )', *cmds)
        
        
#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to an analog event
# Parameters:
# event - instance of the Event class representing the analog event
#-------------------------------------------------------------------------------
def At(event):
    def func (*cmds):
        return WaitAnalogEvent(event, *cmds)
    return func


#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to an analog event
# Parameters:
# header - header of the block
#-----------------------------------------------------------------------------
def block(header):
    def func (*cmds):
        return Block(header, *cmds)
    return func
        

#-------------------------------------------------------------------------------
# Cross Class
#-------------------------------------------------------------------------------
class Cross(Event):

    #---------------------------------------------------------------------------
    # Constructor
    # signal crossing function
    # Parameters:
    # signal - RealOp class representing the signal
    # threshold - RealOp class representing the threshold that must be crossed
    # edge: It can be rising, falling or both
    # *pars - optional parameters in order: timeTol and expTol both RealOp
    #---------------------------------------------------------------------------
    def __init__(self, signal, threshold, edge, *pars):
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        checkInstance("signal", signal, RealOp)
        checkInstance("threshold", threshold, RealOp)
        checkType("edge", edge, str)
        mapping = {'rising': '1', 'falling': '-1', 'both': '0'}  
        assert edge in mapping.keys(), "Wrong value for edge"
        params = [str(mapping[edge])]

        for par in pars:
            checkInstance("timeTol or expTol", par, RealOp)
            params.append(str(par))
        
        evnt = "cross(" + str(signal) + " - " + str(threshold) + ", " + \
                ", ".join(params) + ")" 
        super(Cross, self).__init__(evnt)


#-------------------------------------------------------------------------------
# Above Class
#-------------------------------------------------------------------------------
class Above(Event):

    #---------------------------------------------------------------------------
    # check if the signal is above a pre-define value
    # Parameters:
    # signal - RealOp class representing the signal
    # threshold - RealOp class representing the threshold that must be crossed
    # *pars - optional parameters in order: timeTol and expTol both RealOp
    #---------------------------------------------------------------------------
    def __init__(self, signal, threshold, *pars):
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        checkInstance("signal", signal, RealOp)
        checkInstance("threshold", threshold, RealOp)
        params = [str(signal) + " - " + str(threshold)] 

        for par in pars:
            checkInstance("timeTol or expTol", par, RealOp)
            params.append(str(par))

        evnt = "above(" + ", ".join(params) + ")" 
        super(Above, self).__init__(evnt)


#-------------------------------------------------------------------------------
# Timer Class
#-------------------------------------------------------------------------------
class Timer(Event):
    
    #----------------------------------------------------------------------------
    # check if the signal is above a pre-define value
    # Parameters:
    # startTime - RealOp class representing the time tolerance
    # *pars - optional parameters in order: period and timeTol both RealOp
    #----------------------------------------------------------------------------
    def __init__(self, startTime, *pars):
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        checkInstance("startTime", startTime, RealOp)
        params = [str(startTime)] 

        for par in pars:
            checkInstance("period or timeTol", par, RealOp)
            params.append(str(par))

        evnt = "timer(" + ", ".join(params) + ")" 
        super(Timer, self).__init__(evnt)


#-------------------------------------------------------------------------------
# types of analysis
#-------------------------------------------------------------------------------
anaTypes = ["ac", 
            "dc", 
            "ic", 
            "tran", 
            "pac", 
            "pnoise", 
            "pss", 
            "pxf", 
            "sp",
            "static", 
            "tdr", 
            "xf"]
            
            
#-------------------------------------------------------------------------------
# Unfold variable number of simulation types
#-------------------------------------------------------------------------------
def unfoldSimTypes(*simTypes):
    ans = []
    i = 1
    for simType in simTypes:
        assert simType in anaTypes, \
               "simType[" + str(i) + "] must be of of the following: " +\
               str(anaTypes)
        i = i + 1
        ans.append('"'+ simType + '"')
    return ", ".join(ans)
    
 #-------------------------------------------------------------------------------
# type of analysis
#-------------------------------------------------------------------------------
def analysis(*simTypes):
    return BoolOp('analysis(' + unfoldSimTypes(*simTypes) + ')')


#-------------------------------------------------------------------------------
# ac stimulus
#-------------------------------------------------------------------------------
def acStim(mag, phase = Real(0), simType = "ac"):
    assert simType in anaTypes, \
           "simType must be of of the following: " + str(anaTypes)
    checkInstance("mag", mag, RealOp)
    checkInstance("phase", phase, RealOp)
    return RealOp('ac_stim("' + str(simType) + '", ' + \
                                str(mag)     + ', ' + \
                                str(phase) + ')')
    
                   
#-------------------------------------------------------------------------------
# InitialStep class
#-------------------------------------------------------------------------------
class InitialStep(Event):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # *simTypes - optional parameters representing the simulation type
    #---------------------------------------------------------------------------
    def __init__(self, *simTypes):
        ans = "initial_step"
        simTypes = unfoldSimTypes(*simTypes)
        if simTypes != "":
            ans = ans + '(' + simTypes + ')'
        super(InitialStep, self).__init__(ans)
                                          

#-------------------------------------------------------------------------------
# FinalStep class
#-------------------------------------------------------------------------------
class FinalStep(Event):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # *simTypes - optional parameters representing the simulation type
    #---------------------------------------------------------------------------
    def __init__(self, *simTypes):
        ans = "final_step"
        simTypes = unfoldSimTypes(*simTypes)
        if simTypes != "":
            ans = ans + '(' + simTypes + ')'
        super(FinalStep, self).__init__(ans)


#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to an Block 
# Parameters:
# n - number of times the sequence of commands must be repeated
#-------------------------------------------------------------------------------
def Repeat(n):
    checkInstance("n", n, IntegerOp)
    return block("repeat( " + str(n) + " )")


#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to an Block 
# Parameters:
# cond - condition that must be satisfied in order repeat the sequence of 
#        commands in the block
#-------------------------------------------------------------------------------
def While(cond):
    checkInstance("cond", cond, BoolOp)
    return block("while( " + str(cond) + " )")  


#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to an Block 
# Parameters:
# start - command executed at the beggining
# cond - condition that must be satisfied in order repeat the sequence of 
#        commands in the block
# inc - command executed at the end of each step
#-------------------------------------------------------------------------------
def For(start, cond, inc):
    checkInstance("cond", cond, BoolOp)
    assert type(start) == Cmd or type(start) == CmdList, +\
           "start must be Cmd or CmdList but a " + str(type(start)) + " was" +\
           "given instead"
    assert type(inc) == Cmd or type(inc) == CmdList, +\
           "start must be Cmd or CmdList but a " + str(type(inc)) + " was" +\
           "given instead"
    initial = "for( " + str(start) + "; " + str(cond) + "; " + str(inc) + " )"  
    return block(initial) 


#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to an Block 
# Parameters:
# cond - condition that must be satisfied in order repeat the sequence of 
#        commands in the block
#-------------------------------------------------------------------------------
def If(cond):
    def ifFunc (*cmds):
        ans = Cond(cond, *cmds)
        return ans
    return ifFunc    


#-------------------------------------------------------------------------------
# Condition Class. It is used inside the function If in order to provide an If
# and else structure
#-------------------------------------------------------------------------------
class Cond(Cmd):

    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self, cond, *cmds):
        checkInstance("cond", cond, BoolOp)
        trueHead  = "if( " + str(cond) + " )"
        falseHead = "else"
        self.cmdDict = {True:Block(trueHead, *cmds), \
                        False:Block(falseHead)}

    #---------------------------------------------------------------------------
    # Add command
    # Parameters:
    # state - state in which this command needs to be executed 
    # cmd - command and list of commands
    #---------------------------------------------------------------------------
    def append(self, state = True, *cmds):
        checkType("state", state, bool)
        self.cmdDict[state].append(*cmds)

    #---------------------------------------------------------------------------
    # List of commands to be run when condition is false
    # *cmds - variable number of commands or command list
    #---------------------------------------------------------------------------
    def Else(self, *cmds):
        self.cmdDict[False].append(*cmds)
        return self

    #---------------------------------------------------------------------------
    # Return the VA verilog command
    # Parameters:
    # padding number of tabs by which the text will be right shifted
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        result = self.cmdDict[True].getVA(padding)
        if len(self.cmdDict[False]) > 0:
            result = result + self.cmdDict[False].getVA(padding)
        return result


#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to a Block 
# Parameters:
# test - variable under test of the case structure
#-------------------------------------------------------------------------------
def Case(test):
    def caseFunc(*cmds):
        return CaseClass(test, *cmds)
    return caseFunc


#-------------------------------------------------------------------------------
# Condition Class. It is used by the function Case in order to provide the case
# structure
#-------------------------------------------------------------------------------
class CaseClass(Cmd):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # test - Must be Integer, Bool, or Real
    # *cmd - variable number of tuples with case conditions and command objects
    #---------------------------------------------------------------------------
    def __init__(self, test, *cmds):
        assert isinstance(test, IntegerOp) or \
               isinstance(test, BoolOp) or  \
               isinstance(test, RealOp), \
               "Value to be tested must be real, integer, or boolean but a " +\
               str(type(test)) + " was given instead"
        self.cmds = []
        self.test = test
        self.append(*cmds)
                
    #---------------------------------------------------------------------------
    # Add command
    # Parameters:
    # *cmd - variable number of tuples with case conditions and command objects
    #---------------------------------------------------------------------------
    def append(self, *cmds):
        i = 1
        for cmd in cmds:
            assert type(cmd) == tuple, "cmd[" + str(i) + "] must be tuple"
            assert len(cmd) == 2, "cmd[" + str(i) + "] length must be 2"
            assert isinstance(self.test, IntegerOp) and \
                   isinstance(cmd[0], IntegerOp)    or  \
                   isinstance(self.test, RealOp)    and \
                   isinstance(cmd[0], RealOp)       or  \
                   isinstance(self.test, BoolOp)    and \
                   isinstance(cmd[0], BoolOp)       or  \
                   isinstance(cmd[0], type(None)), \
                   "cmd[" + str(i) + "] test and case types must be compatible"
            assert isinstance(cmd[1], Cmd) and \
                   not isinstance(cmd[1], WaitAnalogEvent), "cmd[" + str(i) +\
                   "] must be an instance of Cmd and can't be and instance "+\
                   "of WaitAnalogEvent, but a " + str(type(cmd)) +\
                   " was given instead"
            if isinstance(cmd[0], type(None)):
                self.cmds.append(Block("default : ", cmd[1]))   
            else:
                self.cmds.append(Block(str(cmd[0]) + " : ", cmd[1]))
            i = i + 1

    #---------------------------------------------------------------------------
    # Return the VA verilog command
    # Parameters:
    # padding number of tabs by which the text will be right shifted
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        result = "    "*padding + "case( " + str(self.test) + " ) \n"
        for item in self.cmds:
            result = result + item.getVA(padding + 1)
        result = result + "    "*padding + "endcase\n"
        return result


#-------------------------------------------------------------------------------
# Unfold variable number of parameters
#-------------------------------------------------------------------------------
def unfoldParams(*params):
    cmd = ""
    i = 1
    for param in params:
        assert isinstance(param, IntegerOp) or \
               isinstance(param, BoolOp) or  \
               isinstance(param, RealOp), \
               "param[" + str(i) + "] must be real, integer, or boolean but " +\
               "a " + str(type(param)) + " was given instead"
        i = i + 1
        cmd = cmd + ", " + str(param)
    return cmd


#-------------------------------------------------------------------------------
# Strobe
#-------------------------------------------------------------------------------
def Strobe(msg, *params):
    checkType("msg", msg, str)
    return Cmd('$strobe("' + msg + '"' + unfoldParams(*params) + ")")


#-------------------------------------------------------------------------------
# Write
#-------------------------------------------------------------------------------
def Write(msg, *params):
    checkType("msg", msg, str)
    return Cmd('$write("' + msg + '"' + unfoldParams(*params) + ")")


#-------------------------------------------------------------------------------
# Fopen
#-------------------------------------------------------------------------------
def Fopen(msg):
    checkType("msg", msg, str)
    return IntegerOp('$fopen("' + msg + '")') 


#-------------------------------------------------------------------------------
# Fwrite
#-------------------------------------------------------------------------------
def Fclose(desc):
    checkInstance("desc", desc, IntegerOp)
    return Cmd('$fclose(' + str(desc) + ')') 


#-------------------------------------------------------------------------------
# Fstrobe
#-------------------------------------------------------------------------------
def Fstrobe(desc, msg, *params):
    checkInstance("desc", desc, IntegerOp)
    checkType("msg", msg, str)
    return Cmd('$fstrobe(' + str(desc) + ', "' + \
                         msg + '"' + \
                         unfoldParams(*params) + ")")


#-------------------------------------------------------------------------------
# Fwrite
#-------------------------------------------------------------------------------
def Fwrite(desc, msg, *params):
    checkInstance("desc", desc, IntegerOp)
    checkType("msg", msg, str)
    return Cmd('$fwrite(' + str(desc) + ', "' + \
                         msg + '"' + \
                         unfoldParams(*params) + ")")

#-------------------------------------------------------------------------------
# discontinuity
#-------------------------------------------------------------------------------
def Discontinuity(degree = Integer(0)):
    checkInstance("degree", degree, IntegerOp)
    return Cmd('$discontinuity(' + str(degree) + ')') 


#-------------------------------------------------------------------------------
# finish
#-------------------------------------------------------------------------------
def Finish():
    return Cmd('$finish') 


#-------------------------------------------------------------------------------
# bond step
#-------------------------------------------------------------------------------
def BoundStep(step):
    checkInstance("step", step, RealOp)
    return Cmd('$bound_step(' + str(step) + ')') 


#-------------------------------------------------------------------------------
# last time a signal crossed a treshold
# Parameters
# signal - RealOp class representing the signal
# threshold - RealOp class representing the threshold that must be crossed
# edge - It can be rising, falling or both
#-------------------------------------------------------------------------------
def lastCrossing(signal, threshold, edge = 'both'):
    checkInstance("signal", signal, RealOp)
    checkInstance("threshold", threshold, RealOp)
    checkType("edge", edge, str)
    mapping = {'rising': '1', 'falling': '-1', 'both': '0'}  
    assert edge in mapping.keys()
    cross = "last_crossing(" + str(signal) + " - " + str(threshold) + ", " + \
            mapping[edge] +")" 
    return RealOp(cross) 


#-------------------------------------------------------------------------------
# random number generators
#-------------------------------------------------------------------------------
def random(seed):
    checkInstance("seed", seed, IntegerVar)
    return IntegerOp('$random(' + str(seed) + ')')

def uDist(seed, start, end):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("start", start, IntegerOp)
    checkInstance("end", end, IntegerOp)
    return IntegerOp('$dist_uniform(' + str(seed) + ', ' + str(start) + ', ' + \
                      str(end) + ')')
        
def uDistInt(seed, start, end):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("start", start, IntegerOp)
    checkInstance("end", end, IntegerOp)
    return IntegerOp('$dist_uniform(' + str(seed) + ', ' + str(start) + ', ' + \
                      str(end) + ')')
        
def uDistReal(seed, start, end):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("start", start, RealOp)
    checkInstance("end", end, RealOp)
    return RealOp('$rdist_uniform(' + str(seed) + ', ' + str(start) + ', ' + \
                  str(end) + ')')

def gaussDistInt(seed, mean, std):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("mean", mean, IntegerOp)
    checkInstance("std", std, IntegerOp)
    return IntegerOp('$dist_normal(' + str(seed) + ', ' + str(mean) + ', ' + \
                      str(std) + ')')
        
def gaussDistReal(seed, mean, std):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("mean", mean, RealOp)
    checkInstance("std", std, RealOp)
    return RealOp('$rdist_normal(' + str(seed) + ', ' + str(mean) + ', ' + \
                  str(std) + ')')

def expDistInt(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("mean", mean, IntegerOp)
    return IntegerOp('$dist_exponential(' + str(seed) + ', ' + str(mean) + ')')

def expDistReal(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("mean", mean, RealOp)
    return RealOp('$rdist_exponential(' + str(seed) + ', ' + str(mean) + ')')

def poissonDistInt(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("mean", mean, IntegerOp)
    return IntegerOp('$dist_poisson(' + str(seed) + ', ' + str(mean) + ')')

def poissonDistReal(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    checkInstance("mean", mean, RealOp)
    return RealOp('$rdist_poisson(' + str(seed) + ', ' + str(mean) + ')')


#-------------------------------------------------------------------------------
# Constants for tasks that represents numbers
#-------------------------------------------------------------------------------
temp = RealOp("$temperature")
abstime = RealOp("$abstime")
vt = RealOp("$vt")


#-------------------------------------------------------------------------------
# math functions
#-------------------------------------------------------------------------------
def exp(x):
    checkInstance("x", x, RealOp)
    return RealOp("exp(" + str(x) + ")")

def limexp(x):
    checkInstance("x", x, RealOp)
    return RealOp("limexp(" + str(x) + ")")

def absDelay(x, delay):
    checkInstance("x", x, RealOp)
    checkInstance("delay", delay, RealOp)
    return RealOp("absdelay(" + str(x) + ", " + str(delay) + ")")

def transition(x, 
               delay = Real(0), 
               riseTime = Real(1e-6), 
               fallTime = Real(1e-6)):
    checkInstance("x", x, RealOp)
    checkInstance("delay", delay, RealOp)
    checkInstance("riseTime", riseTime, RealOp)
    checkInstance("fallTime", fallTime, RealOp)
    return RealOp("transition(" + str(x) + ", " + str(delay) + ", " + \
                  str(riseTime) + ", " + str(fallTime) + ")")

def ternary(test, op1, op2):
    assert isinstance(op1, IntegerOp) and \
           isinstance(op2, IntegerOp) or  \
           isinstance(op1, RealOp)    and \
           isinstance(op2, RealOp)    or  \
           isinstance(op1, BoolOp)    and \
           isinstance(op2, BoolOp), "op1 and op2 must have compatible types"
    checkInstance("test", test, BoolOp)
    Type = RealOp if isinstance(op1, RealOp) else \
           BoolOp if isinstance(op1, BoolOp) else \
           IntegerOp
    return Type(str(test) + " ? ( " + str(op1) + " ) : ( " + str(op2) + " )")    

def slew(x, riseSlope = Real(10e-6), fallSlope = Real(10e-6)):
    checkInstance("x", x, RealOp)
    checkInstance("riseSlope", riseSlope, RealOp)
    checkInstance("fallSlope", fallSlope, RealOp)
    return RealOp("slew(" + \
                  str(x) + ", " + \
                  str(riseSlope) + ", " + \
                  str(fallSlope) + ")")

def ddt(x):
    checkInstance("x", x, RealOp)
    return RealOp("ddt(" + str(x) + ")")
    
def idt(x, start = Real(0)):
    checkInstance("x", x, RealOp)
    checkInstance("start", start, RealOp)
    return RealOp("idt(" + str(x) + ", " + str(start) + ")")

def ceil(x):
    checkInstance("x", x, RealOp)
    return IntegerOp("ceil(" + str(x) + ")")
        
def floor(x):
    checkInstance("x", x, RealOp)
    return IntegerOp("floor(" + str(x) + ")")

def ln(x):
    checkInstance("x", x, RealOp)
    return RealOp("ln(" + str(x) + ")")

def log(x):
    checkInstance("x", x, RealOp)
    return RealOp("log(" + str(x) + ")")

def sqrt(x):
    checkInstance("x", x, RealOp)
    return RealOp("sqrt(" + str(x) + ")")

def sin(x):
    checkInstance("x", x, RealOp)
    return RealOp("sin(" + str(x) + ")")

def cos(x):
    checkInstance("x", x, RealOp)
    return RealOp("cos(" + str(x) + ")")

def tan(x):
    checkInstance("x", x, RealOp)
    return RealOp("tan(" + str(x) + ")")

def asin(x):
    checkInstance("x", x, RealOp)
    return RealOp("asin(" + str(x) + ")")

def acos(x):
    checkInstance("x", x, RealOp)
    return RealOp("acos(" + str(x) + ")")

def atan(x):
    checkInstance("x", x, RealOp)
    return RealOp("atan(" + str(x) + ")")

def atan2(x, y):
    checkInstance("x", x, RealOp)
    checkInstance("y", y, RealOp)
    return RealOp("atan2(" + str(x) + ", " + str(y) + ")")

def hypot(x, y):
    checkInstance("x", x, RealOp)
    checkInstance("y", y, RealOp)
    return RealOp("hypot(" + str(x) + ", " + str(y) + ")")

def sinh(x):
    checkInstance("x", x, RealOp)
    return RealOp("sinh(" + str(x) + ")")

def cosh(x):
    checkInstance("x", x, RealOp)
    return RealOp("cosh(" + str(x) + ")")

def tanh(x):
    checkInstance("x", x, RealOp)
    return RealOp("tanh(" + str(x) + ")")

def asinh(x):
    checkInstance("x", x, RealOp)
    return RealOp("asinh(" + str(x) + ")")

def acosh(x):
    checkInstance("x", x, RealOp)
    return RealOp("acosh(" + str(x) + ")")

def atanh(x):
    checkInstance("x", x, RealOp)
    return RealOp("atanh(" + str(x) + ")")


#-------------------------------------------------------------------------------
# Class of electrical signals
#-------------------------------------------------------------------------------
class Electrical():

    #---------------------------------------------------------------------------
    # constructor
    # Parameters:
    # name - name of the electrical signal
    #---------------------------------------------------------------------------
    def __init__(self, name):
        checkType("name", name, str)
        self.name = name
        self.v = RealOp("V(" + name + ")") 
        self.i = RealOp("I(" + name + ")") 
        
    #---------------------------------------------------------------------------
    # Return electrical name
    #---------------------------------------------------------------------------
    def getName(self):
        return self.name

    #---------------------------------------------------------------------------
    # Return a command representing voltage contribution
    # Parameters:
    # value - A RealOp representing the value
    #---------------------------------------------------------------------------
    def vCont(self, value):
        checkInstance("value", value, RealOp)
        return Cmd('V(' + self.name + ') <+ ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing curruent contribution
    # Parameters:
    # value - A RealOp representing the value
    #---------------------------------------------------------------------------
    def iCont(self, value):
        checkInstance("value", value, RealOp)
        return Cmd('I(' + self.name + ') <+ ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing voltage attribution
    # Parameters:
    # value - A RealOp representing the value
    #---------------------------------------------------------------------------
    def vAttr(self, value):
        checkInstance("value", value, RealOp)
        return Cmd('V(' + self.name + ') = ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing current attribution
    # Parameters:
    # value - A RealOp representing the value
    #---------------------------------------------------------------------------
    def iAttr(self, value):
        checkInstance("value", value, RealOp)
        return Cmd('I(' + self.name + ') = ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing voltage indirect assigment
    # Parameters:
    # value - A BoolOp representing the value
    #---------------------------------------------------------------------------
    def vInd(self, value):
        checkInstance("value", value, BoolOp)
        return Cmd('V(' + self.name + ') : ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing current indirect assigment
    # Parameters:
    # value - A BoolOp representing the value
    #---------------------------------------------------------------------------
    def iInd(self, value):
        checkInstance("value", value, BoolOp)
        return Cmd('I(' + self.name + ') : ' + str(value))
 

#-------------------------------------------------------------------------------
# Branch class
#-------------------------------------------------------------------------------
class Branch(Electrical):

    #---------------------------------------------------------------------------
    # constructor
    # Parameters:
    # node1 - electrical signal representing the first node
    # node2 - electrical signal representing the second node
    #---------------------------------------------------------------------------
    def __init__(self, node1, node2):
        checkInstance("node1", node1, Electrical)
        checkInstance("node2", node2, Electrical)
        checkNotInstance("node1", node1, Branch)
        checkNotInstance("node2", node2, Branch)
        super(Branch, self).__init__(node1.getName() + ", " + node2.getName())


#-------------------------------------------------------------------------------
# verilogA class
#-------------------------------------------------------------------------------
class Module:

    #---------------------------------------------------------------------------
    # constructor
    # Parameters:
    # moduleName - name of the module (the first word after module in the va)
    #---------------------------------------------------------------------------
    def __init__(self, moduleName):
        checkType("moduleName", moduleName, str)
        self.moduleName = moduleName   
        self.nameCount  = 0
        self.nameSpace  = []
        self.nodes      = []
        self.ports      = []
        self.parameters = []
        self.variables  = []
        self.cmds       = []
        self.endCmds    = []
        self.beginningCmds = []

    #---------------------------------------------------------------------------
    # return module name
    #---------------------------------------------------------------------------
    def getModuleName(self):
        return self.moduleName

    #---------------------------------------------------------------------------
    # If name is an empty string, get the next name available in the namespace.
    # If name isn't empty, check if the name is available in the verilogA 
    # namespace and raise an exception if it doesn't
    # Parameters: 
    # name - name to be checked
    #---------------------------------------------------------------------------
    def fixName(self, name):
        checkType("name", name, str)
        if name == "":
            self.nameCount = self.nameCount + 1
            name = "_$" + str(self.nameCount)
        assert not name in self.nameSpace, name + " is already taken"
        self.nameSpace.append(name)
        return name

    #---------------------------------------------------------------------------
    # Add variable to the module
    # Parameters: 
    # name - name of the parameter
    # value - the variable created will be the same type as value
    #---------------------------------------------------------------------------
    def var(self, value = Integer(0), name = ""):
        name = self.fixName(name)
        if isinstance(value, IntegerOp):
            vType = "integer"
            ans   = IntegerVar(name)
        elif isinstance(value, BoolOp):
            vType = "integer"
            ans   = BoolVar(name)
        elif isinstance(value, RealOp):
            vType = "real"
            ans   = RealVar(name)
        else:
            raise TypeError("value must be IntegerOp, RealOp, or BoolOp but "+\
                            "a " + str(type(value)) + " was given") 
        self.variables.append((name, vType)) 
        return ans

    #---------------------------------------------------------------------------
    # Add parameter to the module
    # Parameters: 
    # name - name of the parameter
    # value - the variable created will be the same type as value
    #---------------------------------------------------------------------------
    def par(self, value, name):
        name = self.fixName(name)
        if isinstance(value, IntegerOp):
            pType = "integer"
            ans   = IntegerOp(name)
        elif isinstance(value, RealOp):
            pType = "real"
            ans   = RealOp(name)
        else:
            raise TypeError("value must be IntegerOp or RealOp, but a "+\
                            str(type(value)) + " was given") 
        self.parameters.append((name, pType, str(value))) 
        return ans

    #---------------------------------------------------------------------------
    # Add commands to the analog block
    # Parameters:
    # *args - variable number of cmd arguments
    #---------------------------------------------------------------------------
    def analog(self, *args):
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd) and \
                   "cmd[" + str(i) + "] must be an instance of Cmd and but a" +\
                   str(type(arg)) + " was given instead"
            i = i + 1
            self.cmds.append(arg)

    def beginningAnalog(self, *args):
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd) and \
                   "cmd[" + str(i) + "] must be an instance of Cmd and but a" +\
                   str(type(arg)) + " was given instead"
            i = i + 1
            self.beginningCmds.append(arg)

    def endAnalog(self, *args):
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd) and \
                   "cmd[" + str(i) + "] must be an instance of Cmd and but a" +\
                   str(type(arg)) + " was given instead"
            i = i + 1
            self.endCmds.append(arg)


    #---------------------------------------------------------------------------
    # Add port
    # Parameters:
    # name - name of the electrical signal
    # width - width of the electrical signal
    # direction - direction of the signal. It can be internal, input, output, or
    #             inout
    #---------------------------------------------------------------------------
    def addPort(self, name, width, direction):
        checkType("width", width, int)
        assert width > 0, "width must be greather than 0"
        checkType("direction", direction, str)
        assert direction in ["input", "output", "inout", "internal"], \
               "direction must be input, output, inout, or internal"
        name = self.fixName(name)
        if direction != "internal":
            self.ports.append((name, width, direction))
        self.nodes.append((name, width)) 
        return name

    #---------------------------------------------------------------------------
    # Return electrical class
    # Parameters:
    # name - name of the electrical signal
    # width - width of the electrical signal
    # direction - direction of the signal. It can be internal, input, output, or
    #             inout
    #---------------------------------------------------------------------------
    def electrical(self, name = "", width = 1, direction = "internal"):
        name = self.addPort(name, width, direction)
        if width == 1:
            return Electrical(name)
        else:
            vector = list()
            for i in range(0, width):
                vector.append(Electrical(name + "[" + str(i) + "]"))
            return vector

    #---------------------------------------------------------------------------
    # Return the VA verilog command
    #---------------------------------------------------------------------------
    def getVA(self):
        #-----------------------------------------------------------------------
        # Header
        #-----------------------------------------------------------------------
        comment = "Module: " + self.moduleName + "\n"
        comment = comment + "Date: " + str(date.today())
        result = blockComment(0, comment, align = "left")

        #-----------------------------------------------------------------------
        # Includes
        #-----------------------------------------------------------------------
        result = result + '`include "constants.vams"\n'        
        result = result + '`include "disciplines.vams"\n' 

        #-----------------------------------------------------------------------
        # Module declaration
        #-----------------------------------------------------------------------
        result = result + "\n" + blockComment(0, "Module declaration")
        result = result + "module " + self.moduleName + "("
        padding = ",\n        " + " "*len(self.moduleName)
        first = True
        for pin in self.ports:
            if first:   
                first = False
                result = result + pin[0]
            else:
                result = result + padding + pin[0]
        result = result + ');\n' 

        #-----------------------------------------------------------------------
        # Print all ports
        #-----------------------------------------------------------------------
        if not first:
            result = result + '\n' + blockComment(0, "Ports")
        for pin in self.ports:
            result = result + pin[2] + " "
            if pin[1] > 1:
                result = result + "[" + str(pin[1]-1) + ":0] " 
            result = result + pin[0] + ";\n"
 
        #-----------------------------------------------------------------------
        # Print all electrical
        #-----------------------------------------------------------------------
        if len(self.nodes) > 0:
            result = result + '\n' + blockComment(0, "Disciplines")
        for node in self.nodes:
            result = result + "electrical "
            if node[1] > 1:
                result = result + "[" + str(int(node[1])-1) + ":0] " 
            result = result + node[0] + ";\n"

        #-----------------------------------------------------------------------
        # Print all parameters
        #-----------------------------------------------------------------------
        if len(self.parameters) > 0:
            result = result + '\n' + blockComment(0, "Parameters")
        for parameter in self.parameters:
            result = result + "parameter " + parameter[1] + " " +\
                     parameter[0] + " = " + parameter[2] + ";\n"

        #-----------------------------------------------------------------------
        # Print all variables
        #-----------------------------------------------------------------------
        if len(self.variables) > 0:
            result = result + '\n' + blockComment(0, "Variables")
        for variable in self.variables:
            result = result +  variable[1] + " " + variable[0] + ";\n"

        #-----------------------------------------------------------------------
        # Analog
        #-----------------------------------------------------------------------
        result = result + '\n' + blockComment(0, "Analog block")
        result = result + "analog begin\n"
        for cmd in self.beginningCmds + self.cmds + self.endCmds:
            result = result + cmd.getVA(1)
        
        #-----------------------------------------------------------------------
        # End module
        #-----------------------------------------------------------------------
        result = result + "end\nendmodule"

        return result

        
