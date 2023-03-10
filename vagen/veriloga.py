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
import re

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
# Return a Real instance 
# Parameters:
# param - string representing the name of the variable
# var - variable
#-------------------------------------------------------------------------------
def parseReal(param, var):
    if isinstance(var, Real):
        return var
    elif type(var) == float or type(var) == int:
        return Real(var)
    else:
        raise Exception(param + " must be a Real, float or int but a " +\
                        str(type(var)) + " was given")


#-------------------------------------------------------------------------------
# Check if the var is Real or can be parsed to Real
# Parameters:
# param - string representing the name of the variable
# var - variable
#-------------------------------------------------------------------------------
def checkReal(param, var):
    assert isinstance(var, Real) or type(var) == float or type(var) == int, \
           param + " must be a Real or float but a " + str(type(var)) +\
           " was given"   


#-------------------------------------------------------------------------------
# Return a Integer instance 
# Parameters:
# param - string representing the name of the variable
# var - variable
#-------------------------------------------------------------------------------
def parseInteger(param, var):
    if isinstance(var, Integer):
        return var
    elif type(var) == int:
        return Integer(var)
    else:
        raise Exception(param + " must be a Integer or int but a " +\
                        str(type(var)) + " was given")
                 
                 
#-------------------------------------------------------------------------------
# Check if the variable is boolean 
# Parameters:
# param - string representing the name of the variable
# var - variable
#-------------------------------------------------------------------------------
def checkInteger(param, var):
    assert isinstance(var, Integer) or type(var) == int, \
           param + " must be a Integer or int but a " + str(type(var)) +\
           " was given"


#-------------------------------------------------------------------------------
# Return a Bool instance 
# Parameters:
# param - string representing the name of the variable
# var - variable
#-------------------------------------------------------------------------------
def parseBool(param, var):
    if isinstance(var, Bool):
        return var
    elif type(var) == bool:
        return Bool(var)
    else:
        raise Exception(param + " must be a Bool or bool but a " +\
                        str(type(var)) + " was given")
                        
                        
#-------------------------------------------------------------------------------
# Check if the variable is boolean 
# Parameters:
# param - string representing the name of the variable
# var - variable
#-------------------------------------------------------------------------------
def checkBool(param, var):
    assert isinstance(var, Bool) or type(var) == bool, \
           param + " must be a Bool or bool but a " + str(type(var)) +\
           " was given"


#-------------------------------------------------------------------------------
# Return a Real, Integer or Boolean instance 
# Parameters:
# param - string representing the name of the variable
# var - variable
#-------------------------------------------------------------------------------                        
def parseNumber(param, var):
    if isinstance(var, Bool)    or \
       isinstance(var, Integer) or \
       isinstance(var, Real):
        return var
    elif type(var) == bool:
        return Bool(var)
    elif type(var) == int:
        return Integer(var)
    elif type(var) == float:
        return Real(var)    
    else:
        raise Exception(param + " must be Integer, Real, Bool, int, float, or"+\
                        " bool, but a "+str(type(value))+ " was given instead")
                        
           
#-------------------------------------------------------------------------------
# Check if the variable is a number 
# Parameters:
# param - string representing the name of the variable
# var - variable
#-------------------------------------------------------------------------------                        
def checkNumber(param, var):
    assert isinstance(var, Integer) or isinstance(var, Bool) or  \
           isinstance(var, Real) or type(var) == float or \
           type(var) == int or type(var) == bool, str(param) + " must be " +\
           "Integer, Real, Bool, int, float, or bool, but a "+str(type(value))+\
           " was given instead" 
           
                                               
#-------------------------------------------------------------------------------
# break long line
#-------------------------------------------------------------------------------                        
def breakLongLines(text):
    checkType("text", text, str)
    div = '),'
    i = 0
    k = 0
    ans = ''
    for j in range(0, len(text)):
        if text[j] == '\n':
            ans = ans + text[i:(j+1)]
            i = j + 1
            k = k + 1
        else:
            if text[j] in div:
                k = j + 1
            if (j - i) > 80 and j < (len(text) - 1) and k > i:
                ans = ans + text[i:k] + '\n'
                i = k  
    ans = ans + text[i:len(text)]
    return ans


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
class Real():

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        if isinstance(value, Bool):
            value = str(ternary(value, Real('1.0'), Real('0.0')))
        elif isinstance(value, Real) or isinstance(value, Integer):
            value = str(value)
        elif type(value) != str:
            try:
                value = "{:e}".format(value)
            except:
                raise TypeError("Can't convert " + str(value) + " to Real")
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
        other = parseReal("other", other)
        return Real("( " + str(self) + ' ) + ( ' + str(other) + " )")

    #---------------------------------------------------------------------------
    # subtraction override
    #---------------------------------------------------------------------------
    def __sub__(self, other):
        other = parseReal("other", other)
        return Real("( " + str(self) + ' ) - ( ' + str(other) + " )")

    #---------------------------------------------------------------------------
    # multiplication override
    #---------------------------------------------------------------------------
    def __mul__(self, other):
        other = parseReal("other", other)
        return Real('( '+ str(self) + ' )*( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # true division override
    #---------------------------------------------------------------------------
    def __truediv__(self, other):
        other = parseReal("other", other)
        return Real('( '+ str(self) + ' )/( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # power override
    #---------------------------------------------------------------------------
    def __pow__(self, other):
        other = parseReal("other", other)
        return Real('pow('+ str(self) + ', ' + str(other) + ')')

    #---------------------------------------------------------------------------
    # greater than override
    #---------------------------------------------------------------------------
    def __gt__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) > ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # less than override
    #---------------------------------------------------------------------------
    def __lt__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) < ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # less than equal override
    #---------------------------------------------------------------------------
    def __le__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) <= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # greater than equal override
    #---------------------------------------------------------------------------
    def __ge__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) >= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) == ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # not equal override
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) != ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    # adition override
    #---------------------------------------------------------------------------
    def __radd__(self, other):
        other = parseReal("other", other)
        return Real("( " + str(other) + ' ) + ( ' + str(self) + " )")

    #---------------------------------------------------------------------------
    # subtraction override
    #---------------------------------------------------------------------------
    def __rsub__(self, other):
        other = parseReal("other", other)
        return Real("( " + str(other) + ' ) - ( ' + str(self) + " )")

    #---------------------------------------------------------------------------
    # multiplication override
    #---------------------------------------------------------------------------
    def __rmul__(self, other):
        other = parseReal("other", other)
        return Real('( '+ str(other) + ' )*( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    # true division override
    #---------------------------------------------------------------------------
    def __rtruediv__(self, other):
        other = parseReal("other", other)
        return Real('( '+ str(other) + ' )/( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    # power override
    #---------------------------------------------------------------------------
    def __rpow__(self, other):
        other = parseReal("other", other)
        return Real('pow('+ str(other) + ', ' + str(self) + ')')
        
    #---------------------------------------------------------------------------
    # negation override
    #---------------------------------------------------------------------------
    def __neg__(self):
        return Real('-( '+ str(self) + ' )')
    
    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __pos__(self):
        return Real(str(self))

    #---------------------------------------------------------------------------
    # abs override
    #---------------------------------------------------------------------------
    def __abs__(self):
        return Real('abs( '+ str(self) + ' )')

    #---------------------------------------------------------------------------
    # String representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value


#-------------------------------------------------------------------------------
# class of binary operators
#-------------------------------------------------------------------------------
class Bool():

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        if isinstance(value, Real):
            value = str(value != 0.0)
        elif isinstance(value, Integer):
            value = str(value != 0)
        elif isinstance(value, Bool):
            value = str(value)
        elif type(value) != str:
            try:
                value = str(int(bool(value)))
            except:
                raise TypeError("Can't convert " + str(value) + " to bool")
        self.value = value
    
    #---------------------------------------------------------------------------
    # Return the operator value
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value

    #---------------------------------------------------------------------------
    # and logic override
    #---------------------------------------------------------------------------
    def __and__(self, other):
        checkBool("other", other)
        if isinstance(other, Bool):
            return Bool('( ' + str(self) + ' ) && ( ' + str(other) + ' )')
        else:
            if other:
                return Bool(str(self))
            else:  
                return False

    #---------------------------------------------------------------------------
    # and logic override
    #---------------------------------------------------------------------------
    def __rand__(self, other):
        checkBool("other", other)
        if isinstance(other, Bool):
            return Bool('( ' + str(other) + ' ) && ( ' + str(self) + ' )')
        else:
            if other:
                return Bool(str(self))
            else:  
                return False
        
    #---------------------------------------------------------------------------
    # or logic override
    #---------------------------------------------------------------------------
    def __or__(self, other):
        checkBool("other", other)
        if isinstance(other, Bool):
            return Bool('( ' + str(self) + ' ) || ( ' + str(other) + ' )')
        else:
            if other:
                return True
            else:  
                return Bool(str(self))
        
    #---------------------------------------------------------------------------
    # or logic override
    #---------------------------------------------------------------------------
    def __ror__(self, other):
        checkBool("other", other)
        if isinstance(other, Bool):
            return Bool('( ' + str(other) + ' ) || ( ' + str(self) + ' )')
        else:
            if other:
                return True
            else:  
                return Bool(str(self))
        
    #---------------------------------------------------------------------------
    # xor logic override
    #---------------------------------------------------------------------------
    def __xor__(self, other):
        checkBool("other", other)
        if isinstance(other, Bool):
            return (self & ~other) | (~self & other)
        else:
            if other:
                return Bool(str(~self))
            else:  
                return Bool(str(self))

    #---------------------------------------------------------------------------
    # xor logic override
    #---------------------------------------------------------------------------
    def __rxor__(self, other):
        checkBool("other", other)
        if isinstance(other, Bool):
            return (other & ~self) | (~other & self)
        else:
            if other:
                return Bool(str(~self))
            else:  
                return Bool(str(self))
                
    #---------------------------------------------------------------------------
    # iversion override
    #---------------------------------------------------------------------------
    def __invert__(self):
        return Bool('!( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # String representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value

    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        other = parseBool("other", other)
        return Bool('( '+ str(self) + ' ) == ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # not equal override
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        other = parseBool("other", other)
        return Bool('( '+ str(self) + ' ) != ( ' + str(other) + ' )')
        
#-------------------------------------------------------------------------------
# class of integer operators
#-------------------------------------------------------------------------------
class Integer():

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        if isinstance(value, Bool):
            value = str(ternary(value, Integer('1'), Integer('0')))
        elif isinstance(value, Real):
            value = str(ceil(value)) 
        elif isinstance(value, Integer):
            assert value > -2147483648 and value < 2147483647,                +\
            "Can't convert " +str(value)+ " to integer, because it is outside"+\
            " the range [-2147483648, 2147483647]" 
            value = str(value)
        elif type(value) != str:
            try:
                value = str(int(value))
            except:
                raise TypeError("Can't convert " + str(value) + " to integer")
        self.value = value
    
    #---------------------------------------------------------------------------
    # return the operator value
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value

    #---------------------------------------------------------------------------
    # adition override
    #---------------------------------------------------------------------------
    def __add__(self, other):
        other = parseInteger("other", other)
        return Integer("( " + str(self) + ' ) + ( ' + str(other) + " )")
        
    #---------------------------------------------------------------------------
    # adition override
    #---------------------------------------------------------------------------
    def __radd__(self, other):
        other = parseInteger("other", other)
        return Integer("( " + str(other) + ' ) + ( ' + str(self) + " )")

    #---------------------------------------------------------------------------
    # subtraction override
    #---------------------------------------------------------------------------
    def __sub__(self, other):
        other = parseInteger("other", other)
        return Integer("( " + str(self) + ' ) - ( ' + str(other) + " )")
        
    #---------------------------------------------------------------------------
    # subtraction override
    #---------------------------------------------------------------------------
    def __rsub__(self, other):
        other = parseInteger("other", other)
        return Integer("( " + str(other) + ' ) - ( ' + str(self) + " )")

    #---------------------------------------------------------------------------
    # multiplication override
    #---------------------------------------------------------------------------
    def __mul__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' )*( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    # multiplication override
    #---------------------------------------------------------------------------
    def __rmul__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' )*( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    # true division override
    #---------------------------------------------------------------------------
    def __truediv__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' )/( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # true division override
    #---------------------------------------------------------------------------
    def __rtruediv__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' )/( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # module override
    #---------------------------------------------------------------------------
    def __mod__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) % ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    # module override
    #---------------------------------------------------------------------------
    def __rmod__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) % ( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    # power override
    #---------------------------------------------------------------------------
    def __pow__(self, other):
        other = parseInteger("other", other)
        return Integer('pow(' + str(self) + ', ' + str(other) + ')')
        
    #---------------------------------------------------------------------------
    # power override
    #---------------------------------------------------------------------------
    def __rpow__(self, other):
        other = parseInteger("other", other)
        return Integer('pow(' + str(other) + ', ' + str(self) + ')')
        
    #---------------------------------------------------------------------------
    # right shift override
    #---------------------------------------------------------------------------
    def __rshift__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) >> ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # right shift override
    #---------------------------------------------------------------------------
    def __rrshift__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) >> ( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # left shift override
    #---------------------------------------------------------------------------
    def __lshift__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) << ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    # left shift override
    #---------------------------------------------------------------------------
    def __rlshift__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) << ( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # and logic override
    #---------------------------------------------------------------------------
    def __and__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) & ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # and logic override
    #---------------------------------------------------------------------------
    def __rand__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) & ( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # or logic override
    #---------------------------------------------------------------------------
    def __or__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) | ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    # or logic override
    #---------------------------------------------------------------------------
    def __ror__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) | ( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    # xor logic override
    #---------------------------------------------------------------------------
    def __xor__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) ^ ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    # xor logic override
    #---------------------------------------------------------------------------
    def __rxor__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) ^ ( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # less than override
    #---------------------------------------------------------------------------
    def __lt__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) < ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # greater than override
    #---------------------------------------------------------------------------
    def __gt__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) > ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # less than equal override
    #---------------------------------------------------------------------------
    def __le__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) <= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # greater than equal override
    #---------------------------------------------------------------------------
    def __ge__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) >= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) == ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    # not equal override
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) != ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    # negation override
    #---------------------------------------------------------------------------
    def __neg__(self):
        return Integer('-( ' + str(self) + ' )')
    
    #---------------------------------------------------------------------------
    # abs override
    #---------------------------------------------------------------------------
    def __abs__(self):
        return Integer('abs( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    # equal override
    #---------------------------------------------------------------------------
    def __pos__(self):
        return Integer(str(self))

    #---------------------------------------------------------------------------
    # iversion override
    #---------------------------------------------------------------------------
    def __invert__(self):
        return Integer('~( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    # String representation
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value

        
#-------------------------------------------------------------------------------
# Integer variable class
#-------------------------------------------------------------------------------
class IntegerVar(Integer):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        super(IntegerVar, self).__init__(value)

    #---------------------------------------------------------------------------
    # Return a command representing the increment of the variable
    #---------------------------------------------------------------------------
    def inc(self):
        return Cmd(self.getValue() + ' = ' + self.getValue() + " + 1")  
        
    #---------------------------------------------------------------------------
    # Return a command representing the decrement of the variable
    #---------------------------------------------------------------------------
    def dec(self):
        return Cmd(self.getValue() + ' = ' + self.getValue() + " - 1")     
                     
    #---------------------------------------------------------------------------
    # Return a command representing the attribution to a variable
    # Parameters:
    # value - A number representing the value
    #---------------------------------------------------------------------------
    def eq(self, value):
        value = parseInteger("value", value)
        return Cmd(self.getValue() + ' = ' + str(value))         
    
    
#-------------------------------------------------------------------------------
# Real variable class
#-------------------------------------------------------------------------------
class RealVar(Real):
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        super(RealVar, self).__init__(value)

    #---------------------------------------------------------------------------
    # Return a command representing the attribution to a variable
    # Parameters:
    # value - A number representing the value
    #---------------------------------------------------------------------------
    def eq(self, value):
        value = parseReal("value", value)
        return Cmd(self.getValue() + ' = ' + str(value))      
        
        
#-------------------------------------------------------------------------------
# Boolean variable class
#-------------------------------------------------------------------------------
class BoolVar(Bool):
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # value - string representing the value
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        super(BoolVar, self).__init__(value)

    #---------------------------------------------------------------------------
    # Return a command representing the state toggle
    #---------------------------------------------------------------------------
    def toggle(self):
        return Cmd(self.getValue() + ' = !' + self.getValue())  
        
    #---------------------------------------------------------------------------
    # Return a command representing the attribution to a variable
    # Parameters:
    # value - A number representing the value
    #---------------------------------------------------------------------------
    def eq(self, value):
        value = parseBool("value", value)
        return Cmd(self.getValue() + ' = ' + str(value))  
        
       
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
        i = 0
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
# Returns the pointer to a function that add commands to an analog event
# Parameters:
# header - header of the block
#-----------------------------------------------------------------------------
def block(header):
    def func (*cmds):
        return Block(header, *cmds)
    return func
    
    
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
    # Return the header of a block command
    #---------------------------------------------------------------------------
    def getHeader(self):
        return self.header
                
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
# Returns the pointer to a function that add commands to an analog event
# Parameters:
# event - instance of the Event class representing the analog event
#-------------------------------------------------------------------------------
def At(event):
    def func (*cmds):
        return WaitAnalogEvent(event, *cmds)
    return func
    
    
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
# Cross Class
#-------------------------------------------------------------------------------
class Cross(Event):

    #---------------------------------------------------------------------------
    # Constructor
    # signal crossing function
    # Parameters:
    # signal - Real class representing the signal
    # threshold - Real class representing the threshold that must be crossed
    # edge: It can be rising, falling or both
    # *pars - optional parameters in order: timeTol and expTol both Real
    #---------------------------------------------------------------------------
    def __init__(self, signal, threshold, edge, *pars):
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        signal = parseReal("signal", signal)
        threshold = parseReal("threshold", threshold)
        checkType("edge", edge, str)
        mapping = {'rising': '1', 'falling': '-1', 'both': '0'}  
        assert edge in mapping.keys(), "Wrong value for edge"
        params = [str(mapping[edge])]

        for par in pars:
            par = parseReal("timeTol or expTol", par)
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
    # signal - Real class representing the signal
    # threshold - Real class representing the threshold that must be crossed
    # *pars - optional parameters in order: timeTol and expTol both Real
    #---------------------------------------------------------------------------
    def __init__(self, signal, threshold, *pars):
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        signal = parseReal("signal", signal)
        threshold = parseReal("threshold", threshold)
        params = [str(signal) + " - " + str(threshold)] 

        for par in pars:
            par = parseReal("timeTol or expTol", par)
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
    # startTime - Real class representing the time tolerance
    # *pars - optional parameters in order: period and timeTol both Real
    #----------------------------------------------------------------------------
    def __init__(self, startTime, *pars):
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        startTime = parseReal("startTime", startTime)
        params = [str(startTime)] 

        for par in pars:
            par = parseReal("period or timeTol", par)
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
# type of analysis
#-------------------------------------------------------------------------------
def analysis(*simTypes):
    if simTypes == "":
        raise Exception("At least one simulation type must be specified")
    return Bool('analysis(' + unfoldSimTypes(*simTypes) + ')')


#-------------------------------------------------------------------------------
# ac stimulus
#-------------------------------------------------------------------------------
def acStim(mag, phase = 0, simType = "ac"):
    assert simType in anaTypes, \
           "simType must be of of the following: " + str(anaTypes)
    mag = parseReal("mag", mag)
    phase = parseReal("phase", phase)
    return Real('ac_stim("' + str(simType) + '", ' + \
                              str(mag)     + ', ' + \
                              str(phase) + ')')
    
                   
#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to an Block 
# Parameters:
# n - number of times the sequence of commands must be repeated
#-------------------------------------------------------------------------------
def Repeat(n):
    def func (*cmds):
        return RepeatLoop(n, *cmds)
    return func


#-------------------------------------------------------------------------------
# Repeat loop class
#-------------------------------------------------------------------------------
class RepeatLoop(Block):
    #---------------------------------------------------------------------------
    # Returns the pointer to a function that add commands to an Block 
    # Parameters:
    # n - number of times the sequence of commands must be repeated
    #---------------------------------------------------------------------------
    def __init__(self, n, *cmds):
        n = parseInteger("n", n)
        self.n = n
        super(RepeatLoop, self).__init__("repeat( " + str(n) + " )", *cmds)  
        
    #---------------------------------------------------------------------------
    # Return the repeat count
    #---------------------------------------------------------------------------
    def getN(self):
        return self.n
        

#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to a While loop 
# Parameters:
# cond - condition that must be satisfied in order repeat the sequence of 
#        commands in the block
#-------------------------------------------------------------------------------
def While(cond):
    def func (*cmds):
        return WhileLoop(cond, *cmds)
    return func


#-------------------------------------------------------------------------------
# While loop class
#-------------------------------------------------------------------------------
class WhileLoop(Block):
    #---------------------------------------------------------------------------
    # Returns the pointer to a function that add commands to an Block 
    # Parameters:
    # cond - condition that must be satisfied in order repeat the sequence of 
    #        commands in the block
    # *cmds - variable number of commands to be added
    #---------------------------------------------------------------------------
    def __init__(self, cond, *cmds):
        cond = parseBool("cond", cond)
        self.cond = cond
        super(WhileLoop, self).__init__("while( " + str(cond) + " )", *cmds)  
        
    #---------------------------------------------------------------------------
    # Return the while loop condition
    #---------------------------------------------------------------------------
    def getCond(self):
        return self.cond   
    
    
#-------------------------------------------------------------------------------
# Returns the pointer to a function that add commands to a ForLoop
# Parameters:
# start - command executed at the beggining
# cond - condition that must be satisfied in order repeat the sequence of 
#        commands in the block
# inc - command executed at the end of each step
#-------------------------------------------------------------------------------
def For(start, cond, inc):
    def func (*cmds):
        return ForLoop(start, cond, inc, *cmds)
    return func
    
    
#-------------------------------------------------------------------------------
# For loop class
#-------------------------------------------------------------------------------
class ForLoop(Block):
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # start - command executed at the beggining
    # cond - condition that must be satisfied in order repeat the sequence of 
    #        commands in the block
    # inc - command executed at the end of each step
    # *cmds - variable number of commands to be added
    #---------------------------------------------------------------------------
    def __init__(self, start, cond, inc, *cmds):
        cond = parseBool("cond", cond)
        assert type(start) == Cmd or type(start) == CmdList, +\
               "start must be Cmd or CmdList but a " + str(type(start)) +\
               " was given instead"
        assert type(inc) == Cmd or type(inc) == CmdList, +\
               "start must be Cmd or CmdList but a " + str(type(inc)) +\
               " was given instead"
        head = "for( " + str(start) + "; " + str(cond) + "; " + str(inc) + " )"
        self.cond = cond
        self.start = start
        self.inc = inc 
        super(ForLoop, self).__init__(head, *cmds)

    #---------------------------------------------------------------------------
    # Return the for loop condition
    #---------------------------------------------------------------------------
    def getCond(self):
        return self.cond
        
    #---------------------------------------------------------------------------
    # Return the for loop start commands
    #---------------------------------------------------------------------------
    def getStart(self):
        return self.start  
        
    #---------------------------------------------------------------------------
    # Return the for loop increment commands
    #---------------------------------------------------------------------------
    def getInc(self):
        return self.inc   
        
        
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
    # cond - condition that must be satisfied in order repeat the sequence of 
    #        commands in the block
    # *cmds - variable number of commands to be added
    #---------------------------------------------------------------------------
    def __init__(self, cond, *cmds):
        cond = parseBool("cond", cond)
        trueHead  = "if( " + str(cond) + " )"
        falseHead = "else"
        self.cond = cond
        self.cmdDict = {True:Block(trueHead, *cmds), \
                        False:Block(falseHead)}

    #---------------------------------------------------------------------------
    # Return the Cond condition
    #---------------------------------------------------------------------------
    def getCond(self):
        return self.cond
        
    #---------------------------------------------------------------------------
    # Return the block of commands for a given state
    #---------------------------------------------------------------------------
    def getBlock(self, state = True):
        checkType("state", state, bool)
        return self.cmdDict[state]
                
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
        self.test = parseNumber("test", test)
        self.cmds = []
        self.append(*cmds)

    #---------------------------------------------------------------------------
    # Return the block of commands for a given state
    #---------------------------------------------------------------------------
    def getBlockList(self):
        return self.cmds
                      
    #---------------------------------------------------------------------------
    # Add command
    # Parameters:
    # *cmd - variable number of tuples with case conditions and command objects
    #---------------------------------------------------------------------------
    def append(self, *cmds):
        i = 0
        for tup in cmds:
            assert type(tup) == tuple, "cmds[" + str(i) + "] must be tuple"
            assert len(tup) > 1, "cmds[" + str(i) + "] length must > 1"
            if not isinstance(tup[0], type(None)):
                if isinstance(self.test, Integer) and \
                   (isinstance(tup[0], Integer) or type(tup[0]) == int):
                   test = parseInteger("cmds[" + str(i) + "][0]", tup[0])
                elif isinstance(self.test, Real)  and \
                     (isinstance(tup[0], Real) or type(tup[0]) == float or\
                      type(tup[0]) == int):
                   test = parseReal("cmds[" + str(i) + "][0]", tup[0])
                elif isinstance(self.test, Bool)  and \
                     (isinstance(tup[0], Bool) or type(tup[0]) == bool):
                   test = parseBool("cmds[" + str(i) + "][0]", tup[0])
                else:
                    raise Exception( "cmds[" + str(i) + "][0] must be " +\
                          " compatible with " + str(type(self.test))    +\
                          " but a " + str(type(tup[0])) + " was given " +\
                          "instead.")
                blockCmd = Block(str(test) + ":")
            else:
                blockCmd = Block("default:")  
            j = 1
            for cmd in tup[1:]:
                assert isinstance(cmd, Cmd) and \
                       not isinstance(cmd, WaitAnalogEvent), "cmds[" + str(i) +\
                   "][" +str(j)+ "] must be an instance of Cmd and can't be " +\
                   "an instance of WaitAnalogEvent, but a " + str(type(cmd))  +\
                   " was given instead"
                blockCmd.append(cmd)
                j = j + 1
            self.cmds.append(blockCmd)
            i = i + 1

    #---------------------------------------------------------------------------
    # Return the VA verilog command
    # Parameters:
    # padding number of tabs by which the text will be right shifted
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        result = "    "*padding + "case( " + str(self.test) + " )\n"
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
        param = parseNumber("param[" + str(i) + "]", param)
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
    return Integer('$fopen("' + msg + '")') 


#-------------------------------------------------------------------------------
# Fwrite
#-------------------------------------------------------------------------------
def Fclose(desc):
    desc = parseInteger("desc", desc)
    return Cmd('$fclose(' + str(desc) + ')') 


#-------------------------------------------------------------------------------
# Fstrobe
#-------------------------------------------------------------------------------
def Fstrobe(desc, msg, *params):
    desc = parseInteger("desc", desc)
    checkType("msg", msg, str)
    return Cmd('$fstrobe(' + str(desc) + ', "' + \
                         msg + '"' + \
                         unfoldParams(*params) + ")")


#-------------------------------------------------------------------------------
# Fwrite
#-------------------------------------------------------------------------------
def Fwrite(desc, msg, *params):
    desc = parseInteger("desc", desc)
    checkType("msg", msg, str)
    return Cmd('$fwrite(' + str(desc) + ', "' + \
                         msg + '"' + \
                         unfoldParams(*params) + ")")
                         

#-------------------------------------------------------------------------------
# discontinuity
#-------------------------------------------------------------------------------
def Discontinuity(degree = 0):
    degree = parseInteger("degree", degree)
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
    step = parseReal("step", step)
    return Cmd('$bound_step(' + str(step) + ')') 


#-------------------------------------------------------------------------------
# last time a signal crossed a treshold
# Parameters
# signal - Real class representing the signal
# threshold - Real class representing the threshold that must be crossed
# edge - It can be rising, falling or both
#-------------------------------------------------------------------------------
def lastCrossing(signal, threshold, edge = 'both'):
    signal = parseReal("signal", signal)
    threshold = parseReal("threshold", threshold)
    checkType("edge", edge, str)
    mapping = {'rising': '1', 'falling': '-1', 'both': '0'}  
    assert edge in mapping.keys()
    cross = "last_crossing(" + str(signal) + " - " + str(threshold) + ", " + \
            mapping[edge] +")" 
    return Real(cross) 


#-------------------------------------------------------------------------------
# random number generators
#-------------------------------------------------------------------------------
def random(seed):
    checkInstance("seed", seed, IntegerVar)
    return Integer('$random(' + str(seed) + ')')
        
def uDistInt(seed, start, end):
    checkInstance("seed", seed, IntegerVar)
    start = parseInteger("start", start)
    end = parseInteger("end", end)
    return Integer('$dist_uniform(' + str(seed) + ', ' + str(start) + ', ' + \
                      str(end) + ')')
        
def uDistReal(seed, start, end):
    checkInstance("seed", seed, IntegerVar)
    start = parseReal("start", start)
    end = parseReal("end", end)
    return Real('$rdist_uniform(' + str(seed) + ', ' + str(start) + ', ' + \
                  str(end) + ')')

def gaussDistInt(seed, mean, std):
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    std = parseInteger("std", std)
    return Integer('$dist_normal(' + str(seed) + ', ' + str(mean) + ', ' + \
                      str(std) + ')')
        
def gaussDistReal(seed, mean, std):
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    std = parseReal("std", std)
    return Real('$rdist_normal(' + str(seed) + ', ' + str(mean) + ', ' + \
                  str(std) + ')')

def expDistInt(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    return Integer('$dist_exponential(' + str(seed) + ', ' + str(mean) + ')')

def expDistReal(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    return Real('$rdist_exponential(' + str(seed) + ', ' + str(mean) + ')')

def poissonDistInt(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    return Integer('$dist_poisson(' + str(seed) + ', ' + str(mean) + ')')

def poissonDistReal(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    return Real('$rdist_poisson(' + str(seed) + ', ' + str(mean) + ')')


#-------------------------------------------------------------------------------
# Constants for tasks that represents numbers
#-------------------------------------------------------------------------------
temp = Real("$temperature")
abstime = Real("$abstime")
vt = Real("$vt")


#-------------------------------------------------------------------------------
# math functions
#-------------------------------------------------------------------------------
def exp(x):
    x = parseReal("x", x)
    return Real("exp(" + str(x) + ")")

def limexp(x):
    x = parseReal("x", x)
    return Real("limexp(" + str(x) + ")")

def absDelay(x, delay):
    x = parseReal("x", x)
    delay = parseReal("delay", delay)
    return Real("absdelay(" + str(x) + ", " + str(delay) + ")")

def transition(x, 
               delay = 0, 
               riseTime = 1e-6, 
               fallTime = 1e-6):
    x = parseReal("x", x)
    delay = parseReal("delay", delay)
    riseTime = parseReal("riseTime", riseTime)
    fallTime = parseReal("fallTime", fallTime)
    return Real("transition(" + str(x) + ", " + str(delay) + ", " + \
                  str(riseTime) + ", " + str(fallTime) + ")")

def ternary(test, op1, op2):
    test = parseBool("test", test)
    if (isinstance(op1, Integer) or type(op1) == int) and \
       (isinstance(op2, Integer) or type(op2) == int):
       op1 = parseInteger("op1", op1)
       op2 = parseInteger("op2", op2)
    elif (isinstance(op1, Bool) or type(op1) == bool) and \
         (isinstance(op2, Bool) or type(op2) == bool):
       op1 = parseBool("op1", op1)
       op2 = parseBool("op2", op2)
    elif (isinstance(op1, Real) or type(op1) == float or type(op1) == int) and\
         (isinstance(op2, Real) or type(op2) == float or type(op2) == int):
       op1 = parseReal("op1", op1)
       op2 = parseReal("op2", op2)
    else:
        raise Exception("op1 and op2 must be Integer, Real, Bool, bool, " +\
                        "float or int with compatible types but got " +\
                        str(type(op1)) + " and " + str(type(op2)) +\
                        " instead")
    Type = Real if isinstance(op1, Real) else \
           Bool if isinstance(op1, Bool) else \
           Integer
    return Type(str(test) + " ? ( " + str(op1) + " ) : ( " + str(op2) + " )")    

def slew(x, riseSlope = 10e-6, fallSlope = 10e-6):
    x = parseReal("x", x)
    riseSlope = parseReal("riseSlope", riseSlope)
    fallSlope = parseReal("fallSlope", fallSlope)
    return Real("slew(" + \
                  str(x) + ", " + \
                  str(riseSlope) + ", " + \
                  str(fallSlope) + ")")

def ddt(x):
    x = parseReal("x", x)
    return Real("ddt(" + str(x) + ")")
    
def idt(x, start = Real(0)):
    x = parseReal("x", x)
    start = parseReal("start", start)
    return Real("idt(" + str(x) + ", " + str(start) + ")")

def ceil(x):
    x = parseReal("x", x)
    return Integer("ceil(" + str(x) + ")")
        
def floor(x):
    x = parseReal("x", x)
    return Integer("floor(" + str(x) + ")")

def ln(x):
    x = parseReal("x", x)
    return Real("ln(" + str(x) + ")")

def log(x):
    x = parseReal("x", x)
    return Real("log(" + str(x) + ")")

def sqrt(x):
    x = parseReal("x", x)
    return Real("sqrt(" + str(x) + ")")

def sin(x):
    x = parseReal("x", x)
    return Real("sin(" + str(x) + ")")

def cos(x):
    x = parseReal("x", x)
    return Real("cos(" + str(x) + ")")

def tan(x):
    x = parseReal("x", x)
    return Real("tan(" + str(x) + ")")

def asin(x):
    x = parseReal("x", x)
    return Real("asin(" + str(x) + ")")

def acos(x):
    x = parseReal("x", x)
    return Real("acos(" + str(x) + ")")

def atan(x):
    x = parseReal("x", x)
    return Real("atan(" + str(x) + ")")

def atan2(x, y):
    x = parseReal("x", x)
    y = parseReal("y", y)
    return Real("atan2(" + str(x) + ", " + str(y) + ")")

def hypot(x, y):
    x = parseReal("x", x)
    y = parseReal("y", y)
    return Real("hypot(" + str(x) + ", " + str(y) + ")")

def sinh(x):
    x = parseReal("x", x)
    return Real("sinh(" + str(x) + ")")

def cosh(x):
    x = parseReal("x", x)
    return Real("cosh(" + str(x) + ")")

def tanh(x):
    x = parseReal("x", x)
    return Real("tanh(" + str(x) + ")")

def asinh(x):
    x = parseReal("x", x)
    return Real("asinh(" + str(x) + ")")

def acosh(x):
    x = parseReal("x", x)
    return Real("acosh(" + str(x) + ")")

def atanh(x):
    x = parseReal("x", x)
    return Real("atanh(" + str(x) + ")")


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
        self.v = Real("V(" + name + ")") 
        self.i = Real("I(" + name + ")") 
        
    #---------------------------------------------------------------------------
    # Return electrical name
    #---------------------------------------------------------------------------
    def getName(self):
        return self.name

    #---------------------------------------------------------------------------
    # Return a command representing voltage contribution
    # Parameters:
    # value - A Real representing the value
    #---------------------------------------------------------------------------
    def vCont(self, value):
        value = parseReal("value", value)
        return Cmd('V(' + self.name + ') <+ ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing curruent contribution
    # Parameters:
    # value - A Real representing the value
    #---------------------------------------------------------------------------
    def iCont(self, value):
        value = parseReal("value", value)
        return Cmd('I(' + self.name + ') <+ ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing voltage attribution
    # Parameters:
    # value - A Real representing the value
    #---------------------------------------------------------------------------
    def vAttr(self, value):
        value = parseReal("value", value)
        return Cmd('V(' + self.name + ') = ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing current attribution
    # Parameters:
    # value - A Real representing the value
    #---------------------------------------------------------------------------
    def iAttr(self, value):
        value = parseReal("value", value)
        return Cmd('I(' + self.name + ') = ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing voltage indirect assigment
    # Parameters:
    # value - A Bool representing the value
    #---------------------------------------------------------------------------
    def vInd(self, value):
        value = parseBool("value", value)
        return Cmd('V(' + self.name + ') : ' + str(value))

    #---------------------------------------------------------------------------
    # Return a command representing current indirect assigment
    # Parameters:
    # value - A Bool representing the value
    #---------------------------------------------------------------------------
    def iInd(self, value):
        value = parseBool("value", value)
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
        assert re.match(r"[_a-zA-Z][_a-zA-Z$0-9]*", name), str(name) +\
               " isn't a valid verilogA identifier"
        assert not name in self.nameSpace, name + " is already taken"
        self.nameSpace.append(name)
        return name

    #---------------------------------------------------------------------------
    # Add variable to the module
    # Parameters: 
    # name - name of the parameter
    # value - the variable created will be the same type as value
    #---------------------------------------------------------------------------
    def var(self, vType = Integer, name = ""):
        name = self.fixName(name)
        if vType == Integer:
            vType = "integer"
            ans   = IntegerVar(name)
        elif vType == Bool:
            vType = "integer"
            ans   = BoolVar(name)
        elif vType == Real:
            vType = "real"
            ans   = RealVar(name)
        else:
            raise TypeError("vType be Integer, Real, or Bool but "+\
                            "a " + str(vType) + " was given") 
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
        if isinstance(value, Integer) or type(value) == int:
            value = parseInteger("value", value)
            pType = "integer"
            ans   = Integer(name)
        elif isinstance(value, Real) or type(value) == float:
            value = parseReal("value", value)
            pType = "real"
            ans   = Real(name)
        else:
            raise TypeError("value must be Integer or Real, but a "+\
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

        
