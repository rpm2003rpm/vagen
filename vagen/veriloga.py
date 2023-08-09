## @file veriloga.py
#  VerilogA modeling
#
#  @section license_main License
#
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    05/02/23 22:36:08
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
## Imports
#
#-------------------------------------------------------------------------------
from datetime import date
import re

#-------------------------------------------------------------------------------
## Check if the type of variable matches the Type. Raise an assertion error if
#  it doesn't.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @param Type Type that the variable should match.
#  @return True if it matches the type or False otherwise.
#
#-------------------------------------------------------------------------------
def checkType(param, var, Type):
    assert type(var) == Type, \
           param + " must be a " + str(Type) + " but a " + \
           str(type(var)) + " was given"


#-------------------------------------------------------------------------------
## Check if the variable is an instance of Type. Raise an assertion error if 
#  it doesn't. 
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @param Type Type that the variable should match.
#  @return True if it is an instance or False otherwise.
#
#-------------------------------------------------------------------------------
def checkInstance(param, var, Type):
    assert isinstance(var, Type), \
           param + " must be a " + str(Type) + " but a " + \
           str(type(var)) + " was given"


#-------------------------------------------------------------------------------
## Check if the variable isn't an instance of Type. Raise an assertion error if 
#  it doesn't. 
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @param Type Type that the variable should match.
#  @return False if it is an instance or True otherwise.
#
#-------------------------------------------------------------------------------
def checkNotInstance(param, var, Type):
    assert not isinstance(var, Type), \
           param + " can't be a " + str(Type)


#-------------------------------------------------------------------------------
## Return a Real instance.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return Real object.
#
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
## Check if the var is Real or it can be parsed to Real.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return True if it can be parsed to Real or False otherwise.
#
#-------------------------------------------------------------------------------
def checkReal(param, var):
    assert isinstance(var, Real) or type(var) == float or type(var) == int, \
           param + " must be a Real or float but a " + str(type(var)) +\
           " was given"   


#-------------------------------------------------------------------------------
## Return an Integer instance 
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return Integer object.
#
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
## Check if the variable is Integer or can be parsed to Integer.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return True if it can be parsed to Integer or False otherwise.
#
#-------------------------------------------------------------------------------
def checkInteger(param, var):
    assert isinstance(var, Integer) or type(var) == int, \
           param + " must be a Integer or int but a " + str(type(var)) +\
           " was given"


#-------------------------------------------------------------------------------
## Return a Bool instance.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return Bool object.
#
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
## Check if the variable is Bool or can be parsed to Bool.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return True if it can be parsed to Bool or False otherwise.
#
#-------------------------------------------------------------------------------
def checkBool(param, var):
    assert isinstance(var, Bool) or type(var) == bool, \
           param + " must be a Bool or bool but a " + str(type(var)) +\
           " was given"


#-------------------------------------------------------------------------------
## Return a Real, Integer or Boolean instance.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return Real, Integer or Bool instance.
#
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
## Check if the variable is a number or can be parsed to Bool.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return True if it can be parsed to number or False otherwise.
#
#-------------------------------------------------------------------------------                        
def checkNumber(param, var):
    assert isinstance(var, Integer) or isinstance(var, Bool) or  \
           isinstance(var, Real) or type(var) == float or \
           type(var) == int or type(var) == bool, str(param) + " must be " +\
           "Integer, Real, Bool, int, float, or bool, but a "+str(type(value))+\
           " was given instead" 
           

#-------------------------------------------------------------------------------
## Creates a comment block
#  @param message String representing the comment
#  @param padding Number of tabs by which the text will be shifted left align
#         center, left or right 
#  @return The comment block.
#
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
## Class of Real operators
#
#-------------------------------------------------------------------------------
class Real():

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self The object pointer.
    #  @param value String representing a Real expression, an Integer, a Bool,
    #  or a value that can be converted to Real.
    #
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
    ## Return the operator value.
    #  @param self The object pointer.
    #  @return String representing the Real expression.
    #
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value
    
    #---------------------------------------------------------------------------
    ## Addition override.
    #  @param self The object pointer.
    #  @param other expression to be added.
    #  @return expression representing the addition.
    #
    #---------------------------------------------------------------------------
    def __add__(self, other):
        other = parseReal("other", other)
        return Real("( " + str(self) + ' ) + ( ' + str(other) + " )")

    #---------------------------------------------------------------------------
    ## Subtraction override.
    #  @param self Minuend object pointer.
    #  @param other Subtrahend. 
    #  @return expression representing the subtraction.
    #
    #---------------------------------------------------------------------------
    def __sub__(self, other):
        other = parseReal("other", other)
        return Real("( " + str(self) + ' ) - ( ' + str(other) + " )")

    #---------------------------------------------------------------------------
    ## Multiplication override.
    #  @param self Multiplicand object pointer.
    #  @param other Multiplier. 
    #  @return expression representing the multiplication.
    #
    #---------------------------------------------------------------------------
    def __mul__(self, other):
        other = parseReal("other", other)
        return Real('( '+ str(self) + ' )*( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Division override.
    #  @param self Dividend object pointer.
    #  @param other Quotient. 
    #  @return expression representing the division.
    #
    #---------------------------------------------------------------------------
    def __truediv__(self, other):
        other = parseReal("other", other)
        return Real('( '+ str(self) + ' )/( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Pow override.
    #  @param self Base object pointer.
    #  @param other Exponent. 
    #  @return expression representing the power.
    #
    #---------------------------------------------------------------------------
    def __pow__(self, other):
        other = parseReal("other", other)
        return Real('pow('+ str(self) + ', ' + str(other) + ')')

    #---------------------------------------------------------------------------
    ## Greater than override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __gt__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) > ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Less than override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __lt__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) < ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Less than equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __le__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) <= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Greater than equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ge__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) >= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) == ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Not equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        other = parseReal("other", other)
        return Bool('( '+ str(self) + ' ) != ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    ## Reverse addition override
    #  @param self The object pointer.
    #  @param other expression to be added.
    #  @return expression representing the addition.
    #
    #---------------------------------------------------------------------------
    def __radd__(self, other):
        other = parseReal("other", other)
        return Real("( " + str(other) + ' ) + ( ' + str(self) + " )")

    #---------------------------------------------------------------------------
    ## Reverse subtraction override
    #  @param self Subtrahend object pointer.
    #  @param other Minuend. 
    #  @return expression representing the subtraction.
    #
    #---------------------------------------------------------------------------
    def __rsub__(self, other):
        other = parseReal("other", other)
        return Real("( " + str(other) + ' ) - ( ' + str(self) + " )")

    #---------------------------------------------------------------------------
    ## Reverse multiplication override.
    #  @param self Multiplier object pointer.
    #  @param other Multiplicand.
    #  @return expression representing the multiplication.
    #
    #---------------------------------------------------------------------------
    def __rmul__(self, other):
        other = parseReal("other", other)
        return Real('( '+ str(other) + ' )*( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    ## Reverse division override.
    #  @param self Quotient object pointer.
    #  @param other Dividend. 
    #  @return expression representing the division.
    #
    #---------------------------------------------------------------------------
    def __rtruediv__(self, other):
        other = parseReal("other", other)
        return Real('( '+ str(other) + ' )/( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    ## Pow override.
    #  @param self Exponent object pointer.
    #  @param other Base. 
    #  @return expression representing the power.
    #
    #---------------------------------------------------------------------------
    def __rpow__(self, other):
        other = parseReal("other", other)
        return Real('pow('+ str(other) + ', ' + str(self) + ')')
        
    #---------------------------------------------------------------------------
    ## negation override
    #  @param self Object pointer.
    #  @return expression representing negation.
    #
    #---------------------------------------------------------------------------
    def __neg__(self):
        return Real('-( '+ str(self) + ' )')
    
    #---------------------------------------------------------------------------
    ## pos override
    #  @param self Object pointer.
    #  @return copy of the same object.
    #
    #---------------------------------------------------------------------------
    def __pos__(self):
        return Real(str(self))

    #---------------------------------------------------------------------------
    ## abs override
    #  @param self Object pointer.
    #  @return expression representing absolute value.
    #
    #---------------------------------------------------------------------------
    def __abs__(self):
        return Real('abs( '+ str(self) + ' )')

    #---------------------------------------------------------------------------
    ## str override
    #  @param self Object pointer.
    #  @return string representing the expression
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value


#-------------------------------------------------------------------------------
## Class of Bool operators
#
#-------------------------------------------------------------------------------
class Bool():

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param Self The object pointer.
    #  @param Value String representing a Real expression, an Integer, a Bool,
    #  or a value that can be converted to Bool.
    #
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
    ## Return the operator value.
    #  @param Self The object pointer.
    #  @return String representing the Bool expression.
    #
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value

    #---------------------------------------------------------------------------
    ## And logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the and operation.
    #
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
    ## Reverse and logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the and operation.
    #
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
    ## Or logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the or operation.
    #
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
    ## Reverse or logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the or operation.
    #
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
    ## Xor logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the exclusive or operation.
    #
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
    ## Reverse xor logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the exclusive or operation.
    #
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
    ## Inversion override
    #  @param Self Object pointer.
    #  @return Expression representing inversion.
    #
    #---------------------------------------------------------------------------
    def __invert__(self):
        return Bool('!( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    ## str override
    #  @param Self Object pointer.
    #  @return String representing the expression
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value

    #---------------------------------------------------------------------------
    ## Equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        other = parseBool("other", other)
        return Bool('( '+ str(self) + ' ) == ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Not equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        other = parseBool("other", other)
        return Bool('( '+ str(self) + ' ) != ( ' + str(other) + ' )')
        
#-------------------------------------------------------------------------------
## Class of Integer operators
#
#-------------------------------------------------------------------------------
class Integer():

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param Self The object pointer.
    #  @param Value String representing a Real expression, an Integer, a Bool,
    #  or a value that can be converted to Integer.
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        if isinstance(value, Bool):
            value = str(ternary(value, Integer('1'), Integer('0')))
        elif isinstance(value, Real):
            value = str(ceil(value)) 
        elif isinstance(value, Integer):
            value = str(value)
        elif type(value) != str:
            try:
                if isinstance(value, int):
                    assert value > -2147483648 and value < 2147483647, "Can't " +\
                    "convert " +str(value)+ " to integer, because it is outside"+\
                    " the range [-2147483648, 2147483647]" 
                value = str(int(value))
            except:
                raise TypeError("Can't convert " + str(value) + " to integer")
        self.value = value
    
    #---------------------------------------------------------------------------
    ## Return the operator value.
    #  @param Self The object pointer.
    #  @return String representing the Bool expression.
    #
    #---------------------------------------------------------------------------
    def getValue(self):
        return self.value

    #---------------------------------------------------------------------------
    ## Addition override.
    #  @param self The object pointer.
    #  @param other expression to be added.
    #  @return expression representing the addition.
    #
    #---------------------------------------------------------------------------
    def __add__(self, other):
        other = parseInteger("other", other)
        return Integer("( " + str(self) + ' ) + ( ' + str(other) + " )")
        
    #---------------------------------------------------------------------------
    ## Reverse addition override
    #  @param self The object pointer.
    #  @param other expression to be added.
    #  @return expression representing the addition.
    #
    #---------------------------------------------------------------------------
    def __radd__(self, other):
        other = parseInteger("other", other)
        return Integer("( " + str(other) + ' ) + ( ' + str(self) + " )")
        
    #---------------------------------------------------------------------------
    ## Subtraction override.
    #  @param self Minuend object pointer.
    #  @param other Subtrahend. 
    #  @return expression representing the subtraction.
    #
    #---------------------------------------------------------------------------
    def __sub__(self, other):
        other = parseInteger("other", other)
        return Integer("( " + str(self) + ' ) - ( ' + str(other) + " )")
        
    #---------------------------------------------------------------------------
    ## Reverse subtraction override
    #  @param self Subtrahend object pointer.
    #  @param other Minuend. 
    #  @return expression representing the subtraction.
    #
    #--------------------------------------------------------------------------- 
    def __rsub__(self, other):
        other = parseInteger("other", other)
        return Integer("( " + str(other) + ' ) - ( ' + str(self) + " )")

    #---------------------------------------------------------------------------
    ## Multiplication override.
    #  @param self Multiplicand object pointer.
    #  @param other Multiplier. 
    #  @return expression representing the multiplication.
    #
    #---------------------------------------------------------------------------
    def __mul__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' )*( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    ## Reverse multiplication override.
    #  @param self Multiplier object pointer.
    #  @param other Multiplicand.
    #  @return expression representing the multiplication.
    #
    #---------------------------------------------------------------------------
    def __rmul__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' )*( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    ## Division override.
    #  @param self Dividend object pointer.
    #  @param other Quotient. 
    #  @return expression representing the division.
    #
    #---------------------------------------------------------------------------
    def __truediv__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' )/( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Reverse division override.
    #  @param self Quotient object pointer.
    #  @param other Dividend. 
    #  @return expression representing the division.
    #
    #---------------------------------------------------------------------------
    def __rtruediv__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' )/( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    ## module override
    #  @param self Dividend.
    #  @param other Quotient. 
    #  @return expression representing the mdule.
    #
    #---------------------------------------------------------------------------
    def __mod__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) % ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    ## reverse module override
    #  @param self Quotient. 
    #  @param other Dividend.
    #  @return expression representing the mdule.
    #
    #---------------------------------------------------------------------------
    def __rmod__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) % ( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    ## Pow override.
    #  @param self Base object pointer.
    #  @param other Exponent. 
    #  @return expression representing the power.
    #
    #---------------------------------------------------------------------------
    def __pow__(self, other):
        other = parseInteger("other", other)
        return Integer('pow(' + str(self) + ', ' + str(other) + ')')
        
    #---------------------------------------------------------------------------
    ## Reverse pow override.
    #  @param self Exponent object pointer.
    #  @param other Base. 
    #  @return expression representing the power.
    #
    #---------------------------------------------------------------------------
    def __rpow__(self, other):
        other = parseInteger("other", other)
        return Integer('pow(' + str(other) + ', ' + str(self) + ')')
        
    #---------------------------------------------------------------------------
    ## right shift override.
    #  @param self Integer to be shifted.
    #  @param other number of times the number will be shifted.
    #  @return expression representing the shift.
    #
    #---------------------------------------------------------------------------
    def __rshift__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) >> ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Reverse right shift override.
    #  @param self number of times the number will be shifted.
    #  @param other Integer to be shifted.
    #  @return expression representing the shift.
    #
    #---------------------------------------------------------------------------
    def __rrshift__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) >> ( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    ## left shift override.
    #  @param self Integer to be shifted.
    #  @param other number of times the number will be shifted.
    #  @return expression representing the shift.
    #
    #---------------------------------------------------------------------------
    def __lshift__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) << ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    ## Reverse left shift override.
    #  @param self number of times the number will be shifted.
    #  @param other Integer to be shifted.
    #  @return expression representing the shift.
    #
    #---------------------------------------------------------------------------
    def __rlshift__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) << ( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    ## Bitwise and logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __and__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) & ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Reverse bitwise and logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __rand__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) & ( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    ## Bitwise or logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __or__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) | ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    ## Reverse bitwise or logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __ror__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) | ( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    ## Bitwise xor logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __xor__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(self) + ' ) ^ ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    ## Reverse bitwise xor logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __rxor__(self, other):
        other = parseInteger("other", other)
        return Integer('( ' + str(other) + ' ) ^ ( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    ## Less than override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __lt__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) < ( ' + str(other) + ' )')
    
    #---------------------------------------------------------------------------
    ## Greater than override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __gt__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) > ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Less than equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __le__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) <= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Greater than equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ge__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) >= ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) == ( ' + str(other) + ' )')

    #---------------------------------------------------------------------------
    ## Not equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        other = parseInteger("other", other)
        return Bool('( ' + str(self) + ' ) != ( ' + str(other) + ' )')
        
    #---------------------------------------------------------------------------
    ## negation override
    #  @param self Object pointer.
    #  @return expression representing negation.
    #
    #---------------------------------------------------------------------------
    def __neg__(self):
        return Integer('-( ' + str(self) + ' )')
    
    #---------------------------------------------------------------------------
    ## abs override
    #  @param self Object pointer.
    #  @return expression representing absolute value.
    #
    #---------------------------------------------------------------------------
    def __abs__(self):
        return Integer('abs( ' + str(self) + ' )')

    #---------------------------------------------------------------------------
    ## pos override
    #  @param self Object pointer.
    #  @return copy of the same object.
    #
    #---------------------------------------------------------------------------
    def __pos__(self):
        return Integer(str(self))

    #---------------------------------------------------------------------------
    ## invert override
    #  @param self Object pointer.
    #  @return expression representing bitwise not in all bits
    #
    #---------------------------------------------------------------------------
    def __invert__(self):
        return Integer('~( ' + str(self) + ' )')
        
    #---------------------------------------------------------------------------
    ## str override
    #  @param self Object pointer.
    #  @return string representing the expression
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value

        
#-------------------------------------------------------------------------------
## Integer variable class
#
#-------------------------------------------------------------------------------
class IntegerVar(Integer):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param value string representing the value
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        super(IntegerVar, self).__init__(value)

    #---------------------------------------------------------------------------
    ## Increment
    #  @param self object pointer
    #  @return command representing the increment
    #
    #---------------------------------------------------------------------------
    def inc(self):
        return Cmd(self.getValue() + ' = ' + self.getValue() + " + 1")  
        
    #---------------------------------------------------------------------------
    ## Decrement
    #  @param self object pointer
    #  @return command representing the decrement
    #
    #---------------------------------------------------------------------------
    def dec(self):
        return Cmd(self.getValue() + ' = ' + self.getValue() + " - 1")     
                     
    #---------------------------------------------------------------------------
    ## Atribution
    #  @param self object pointer
    #  @param value A number representing the value
    #  @return Return a command representing the attribution to a variable
    #
    #---------------------------------------------------------------------------
    def eq(self, value):
        value = parseInteger("value", value)
        return Cmd(self.getValue() + ' = ' + str(value))         
    

#-------------------------------------------------------------------------------
## Real variable class
#
#-------------------------------------------------------------------------------
class RealVar(Real):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param value string representing the value
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        super(RealVar, self).__init__(value)

    #---------------------------------------------------------------------------
    ## Atribution
    #  @param self object pointer
    #  @param value A number representing the value
    #  @return Return a command representing the attribution to a variable
    #
    #---------------------------------------------------------------------------
    def eq(self, value):
        value = parseReal("value", value)
        return Cmd(self.getValue() + ' = ' + str(value))      
        
        
#-------------------------------------------------------------------------------
## Boolean variable class
#
#-------------------------------------------------------------------------------
class BoolVar(Bool):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param value string representing the value
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        super(BoolVar, self).__init__(value)

    #---------------------------------------------------------------------------
    ## Toogle
    #  @param self object pointer
    #  @return  Return a command representing the state toggle
    #
    #---------------------------------------------------------------------------
    def toggle(self):
        return Cmd(self.getValue() + ' = !' + self.getValue())  
        
    #---------------------------------------------------------------------------
    ## Atribution
    #  @param self object pointer
    #  @param value A number representing the value
    #  @return Return a command representing the attribution to a variable
    #
    #---------------------------------------------------------------------------
    def eq(self, value):
        value = parseBool("value", value)
        return Cmd(self.getValue() + ' = ' + str(value))  
        
       
#-------------------------------------------------------------------------------
## Class of events
#
#-------------------------------------------------------------------------------
class Event():

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param value string representing the event
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        checkType("value", value, str)
        self.value = value

    #---------------------------------------------------------------------------
    ## or logic override
    #  @param self object pointer
    #  @param other pointer to another Event object
    #  @return Return an Event representing the or logic between the two
    #
    #---------------------------------------------------------------------------
    def __or__(self, other):
        checkInstance("other", other, Event)
        return Event(str(self) + ' or ' + str(other))

    #---------------------------------------------------------------------------
    ## string representation
    #  @param self object pointer
    #  @param other pointer to another Event object
    #  @return The string representation of the Event
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.value
               
               
#-------------------------------------------------------------------------------
## Command class
#
#-------------------------------------------------------------------------------
class Cmd:
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param cmd command to be added to the va
    #
    #---------------------------------------------------------------------------
    def __init__(self, cmd):
        checkType("cmd", cmd, str)
        self.cmd = cmd

    #---------------------------------------------------------------------------
    ## Return string representation
    #  @param self object pointer
    #  @return string representation
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        return self.cmd

    #---------------------------------------------------------------------------
    ## Return the VA verilog command
    #  @param self object pointer
    #  @param padding padding number of tabs by which the text will be right 
    #         shifted
    #  @return verilog command
    #  
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
## Command List class
#
#-------------------------------------------------------------------------------
class CmdList(list, Cmd):
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param cmds commands to be added to the va
    #
    #---------------------------------------------------------------------------
    def __init__(self, *cmds):
        super(CmdList, self).__init__()
        self.append(*cmds)
        
    #---------------------------------------------------------------------------
    ## Return string representation
    #  @param self object pointer
    #  @return string representation
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        return ", ".join([str(x) for x in self])
        
    #---------------------------------------------------------------------------
    ## Return a flat command list Fatten
    #  @param self object pointer
    #  @return flat command list. Only imediate CmdLists will be open.
    #
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
    ## append override 
    #  @param self object pointer
    #
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
    ## Return the VA verilog command
    #  @param self object pointer
    #  @param padding number of tabs by which the text will be right shifted
    #  @return verilog command
    #  
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        result = ""
        for item in self:
            result = result + item.getVA(padding)
        return result


#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to an analog event
#  @param header header of the block
#  @return pointer to a function that creates a block object
#
#-----------------------------------------------------------------------------
def block(header):
    def func (*cmds):
        return Block(header, *cmds)
    return func
    
    
#-------------------------------------------------------------------------------
## Command Block Class
#
#-------------------------------------------------------------------------------
class Block(CmdList):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param header header of the command block
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, header, *cmds):
        checkType("header", header, str)
        self.header  = header
        super(Block, self).__init__(*cmds)
        
    #---------------------------------------------------------------------------
    ## Return the header of a block command
    #  @param self object pointer
    #  @return header o the block 
    # 
    #---------------------------------------------------------------------------
    def getHeader(self):
        return self.header
                
    #---------------------------------------------------------------------------
    ## Return the VA verilog command
    #  @param self object pointer
    #  @param padding number of tabs by which the text will be right shifted
    #  @return verilog command
    #  
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
## Returns the pointer to a function that add commands to an analog event
#  @param event instance of the Event class representing the analog event
#  @return function pointer
#
#-------------------------------------------------------------------------------
def At(event):
    def func (*cmds):
        return WaitAnalogEvent(event, *cmds)
    return func
    
    
#-------------------------------------------------------------------------------
## Wait analog event class
#
#-------------------------------------------------------------------------------
class WaitAnalogEvent(Block):
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param event Event to be waited for
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, event, *cmds):
        checkInstance("event", event, Event)
        super(WaitAnalogEvent, self).__init__('@( ' + str(event) + ' )', *cmds)
        

#-------------------------------------------------------------------------------
## Cross Class
#
#-------------------------------------------------------------------------------
class Cross(Event):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param exp Real class or build-in real representing the expression
    #  @param edge It can be rising, falling or both
    #  @param *pars optional Real or build-in real parameters timeTol and expTol
    #         in this order
    #
    #---------------------------------------------------------------------------
    def __init__(self, expr, edge, *pars):
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        expr = parseReal("expr", expr)
        checkType("edge", edge, str)
        mapping = {'rising': '1', 'falling': '-1', 'both': '0'}  
        assert edge in mapping.keys(), "Wrong value for edge"
        params = [str(mapping[edge])]

        for par in pars:
            par = parseReal("timeTol or expTol", par)
            params.append(str(par))
        
        evnt = "cross(" + str(expr) + ", " + ", ".join(params) + ")" 
        super(Cross, self).__init__(evnt)


#-------------------------------------------------------------------------------
## Above Class
#
#-------------------------------------------------------------------------------
class Above(Event):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param expr Real class or build-in real representing the expression
    #  @param *pars optional Real or build-in real parameters timeTol and expTol
    #         in this order
    #
    #---------------------------------------------------------------------------
    def __init__(self, expr, *pars):
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        expr = parseReal("expr", expr)
        params = [str(expr)] 

        for par in pars:
            par = parseReal("timeTol or expTol", par)
            params.append(str(par))

        evnt = "above(" + ", ".join(params) + ")" 
        super(Above, self).__init__(evnt)


#-------------------------------------------------------------------------------
## Timer Class
#
#-------------------------------------------------------------------------------
class Timer(Event):
    
    #----------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param startTime Real or build-in real representing the time tolerance
    #  @param *pars optional Real or build-in real parameters timeTol and expTol
    #         in this order
    #
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
## types of analysis
#
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
## Unfold variable number of simulation types
#  @param list of simulation types
#  @result string with the unfolded simulation types
#
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
## InitialStep class
#
#-------------------------------------------------------------------------------
class InitialStep(Event):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param *simTypes optional parameters representing the simulation type
    #
    #---------------------------------------------------------------------------
    def __init__(self, *simTypes):
        ans = "initial_step"
        simTypes = unfoldSimTypes(*simTypes)
        if simTypes != "":
            ans = ans + '(' + simTypes + ')'
        super(InitialStep, self).__init__(ans)
                                          

#-------------------------------------------------------------------------------
## FinalStep class
#
#-------------------------------------------------------------------------------
class FinalStep(Event):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param *simTypes optional parameters representing the simulation type
    #
    #---------------------------------------------------------------------------
    def __init__(self, *simTypes):
        ans = "final_step"
        simTypes = unfoldSimTypes(*simTypes)
        if simTypes != "":
            ans = ans + '(' + simTypes + ')'
        super(FinalStep, self).__init__(ans)
  
   
#-------------------------------------------------------------------------------
## Type of analysis
#  @param *simTypes optional parameters representing the simulation type
#  @return Bool expression representing the analysis type test
#
#-------------------------------------------------------------------------------
def analysis(*simTypes):
    if simTypes == "":
        raise Exception("At least one simulation type must be specified")
    return Bool('analysis(' + unfoldSimTypes(*simTypes) + ')')


#-------------------------------------------------------------------------------
## ac stimulus
#  @param mag Real class or build-in real representing the magnitude
#  @param phase Real class or build-in representing the phase (default it 0)
#  @param simType string representing the simulation type (default is "ac")
#  @return Real expression representing the ac stimulus command
#
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
## Returns the pointer to a function that add commands to an Repeat block
#  @param n Integer class or int representing the number of times the 
#         sequence must be repeated
#  @return pointer to a function that returns a RepeatLoop class
#
#-------------------------------------------------------------------------------
def Repeat(n):
    def func (*cmds):
        return RepeatLoop(n, *cmds)
    return func


#-------------------------------------------------------------------------------
## RepeatLoop class  
#
#-------------------------------------------------------------------------------
class RepeatLoop(Block):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param n Integer class or int representing the number of times the block 
    #         of commands must be repeated
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, n, *cmds):
        n = parseInteger("n", n)
        self.n = n
        super(RepeatLoop, self).__init__("repeat( " + str(n) + " )", *cmds)  
        
    #---------------------------------------------------------------------------
    ## Return the repeat count
    #  @param self object pointer
    #  @return Integer class representing the number of times the block of 
    #          commands will be repeated
    #
    #---------------------------------------------------------------------------
    def getN(self):
        return self.n
        

#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to a While loop 
#  @param cond Bool class or build-in bool representing the condition that must 
#         be satisfied in order repeat the sequence of commands in the block
#  @return pointer to a function that returns a WhileLoop class
# 
#-------------------------------------------------------------------------------
def While(cond):
    def func (*cmds):
        return WhileLoop(cond, *cmds)
    return func


#-------------------------------------------------------------------------------
## WhileLoop class
#
#-------------------------------------------------------------------------------
class WhileLoop(Block):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param cond Bool class or build-in bool representing the condition that 
    #         must be satisfied in order repeat the sequence of commands in the 
    #         block
    #  @param *cmds variable number of Cmd or CmdList to be added  
    # 
    #---------------------------------------------------------------------------
    def __init__(self, cond, *cmds):
        cond = parseBool("cond", cond)
        self.cond = cond
        super(WhileLoop, self).__init__("while( " + str(cond) + " )", *cmds)  
        
    #---------------------------------------------------------------------------
    ## Return the while loop condition
    #  @param self object pointer
    #  @return Bool class representing the condition that must be satisfied in 
    #          order repeat the sequence of commands in the block
    #
    #---------------------------------------------------------------------------
    def getCond(self):
        return self.cond   
    
    
#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to a ForLoop
#  @param start command executed at the beggining
#  @param cond condition that must be satisfied in order repeat the sequence of 
#         commands in the block
#  @param inc command executed at the end of each step
#  @return pointer to a function that returns a ForLoop class
#
#-------------------------------------------------------------------------------
def For(start, cond, inc):
    def func (*cmds):
        return ForLoop(start, cond, inc, *cmds)
    return func
    
    
#-------------------------------------------------------------------------------
## ForLoop class
#
#-------------------------------------------------------------------------------
class ForLoop(Block):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param start command executed at the beggining
    #  @param cond condition that must be satisfied in order repeat the sequence
    #         of commands in the block
    #  @param inc command executed at the end of each step
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
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
    ## Return the Forloop condition
    #  @param self object pointer
    #  @return Bool class representing the condition that must be satisfied in 
    #          order repeat the sequence of commands in the block
    #
    #---------------------------------------------------------------------------
    def getCond(self):
        return self.cond
        
    #---------------------------------------------------------------------------
    ## Return the Forloop start
    #  @param self object pointer
    #  @return Cmd class representing the initial command run by the loop
    #
    #---------------------------------------------------------------------------
    def getStart(self):
        return self.start  
        
    #---------------------------------------------------------------------------
    ## Return the Forloop increment
    #  @param self object pointer
    #  @return Cmd class representing the increment command run at each 
    #          iteraction
    #
    #---------------------------------------------------------------------------
    def getInc(self):
        return self.inc   
        
        
#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to a Cond Class
#  @param cond condition that must be satisfied in order to run the sequence of 
#         commands in the block
#  @return pointer to a function that returns a Cmd class
#
#-------------------------------------------------------------------------------
def If(cond):
    def ifFunc (*cmds):
        ans = Cond(cond, *cmds)
        return ans
    return ifFunc    


#-------------------------------------------------------------------------------
## Condition Class. It is used inside the function If in order to provide an If
#  and else structure
#
#-------------------------------------------------------------------------------
class Cond(Cmd):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param cond condition that must be satisfied in order to run the sequence 
    #         of commands in the block
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, cond, *cmds):
        cond = parseBool("cond", cond)
        trueHead  = "if( " + str(cond) + " )"
        falseHead = "else"
        self.cond = cond
        self.cmdDict = {True:Block(trueHead, *cmds), \
                        False:Block(falseHead)}

    #---------------------------------------------------------------------------
    ## Return the Cond condition
    #  @param self object pointer
    #  @return Bool class representing the condition that must be satisfied in 
    #          order run the sequence of commands in the block
    #
    #---------------------------------------------------------------------------
    def getCond(self):
        return self.cond
        
    #---------------------------------------------------------------------------
    ## Return the block of commands for a given state
    #  @param self object pointer
    #  @param state true or false
    #  @return block of commands for True and False conditions
    #
    #---------------------------------------------------------------------------
    def getBlock(self, state = True):
        checkType("state", state, bool)
        return self.cmdDict[state]
                
    #---------------------------------------------------------------------------
    ## Add command
    #  @param self object pointer
    #  @param state true or false 
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def append(self, state, *cmds):
        checkType("state", state, bool)
        self.cmdDict[state].append(*cmds)

    #---------------------------------------------------------------------------
    ## List of commands to be run when condition is false
    #  @param self object pointer
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #  @return pointer to self
    # 
    #---------------------------------------------------------------------------
    def Else(self, *cmds):
        self.cmdDict[False].append(*cmds)
        return self

    #---------------------------------------------------------------------------
    ## Return the VA verilog command
    #  @param self object pointer
    #  @param padding number of tabs by which the text will be right shifted
    #  @return verilog command
    #  
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        result = self.cmdDict[True].getVA(padding)
        if len(self.cmdDict[False]) > 0:
            result = result + self.cmdDict[False].getVA(padding)
        return result


#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to a Block 
#  @param variable under test of the case structure
#  @return pointer to a function that returns a CaseClass
#  
#-------------------------------------------------------------------------------
def Case(test):
    def caseFunc(*cmds):
        return CaseClass(test, *cmds)
    return caseFunc


#-------------------------------------------------------------------------------
## Condition Class. It is used by the function Case in order to provide the case
#  structure
#
#-------------------------------------------------------------------------------
class CaseClass(Cmd):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param test Must be Integer, Bool, or Real
    #  @param *cmds variable number of tupples containing a condition and a 
    #         command
    #
    #---------------------------------------------------------------------------
    def __init__(self, test, *cmds):
        self.test = parseNumber("test", test)
        self.cmds = []
        self.append(*cmds)

    #---------------------------------------------------------------------------
    ## Return the list of block of commands 
    #  @param self object pointer
    #  @return a list of block of commands
    #
    #---------------------------------------------------------------------------
    def getBlockList(self):
        return self.cmds
                      
    #---------------------------------------------------------------------------
    ## Add command
    #  @param self object pointer
    #  @param *cmds variable number of tupples containing a condition and a 
    #         command
    #
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
    ## Return the VA verilog command
    #  @param self object pointer
    #  @param padding number of tabs by which the text will be right shifted
    #  @return verilog command
    #  
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        checkType("padding", padding, int)
        result = "    "*padding + "case( " + str(self.test) + " )\n"
        for item in self.cmds:
            result = result + item.getVA(padding + 1)
        result = result + "    "*padding + "endcase\n"
        return result


#-------------------------------------------------------------------------------
## Unfold variable number of parameters
#  @param *params variable number of parameters
#  @return string representing the parameters separeted by comma
#
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
## Strobe
#  @param msg message to be printed
#  @param *params variable number of parameters
#  @return Cmd representing the strobe
#
#-------------------------------------------------------------------------------
def Strobe(msg, *params):
    checkType("msg", msg, str)
    return Cmd('$strobe("' + msg + '"' + unfoldParams(*params) + ")")


#-------------------------------------------------------------------------------
## Write
#  @param msg message to be printed
#  @param *params variable number of parameters
#  @return Cmd representing the Write
#
#-------------------------------------------------------------------------------
def Write(msg, *params):
    checkType("msg", msg, str)
    return Cmd('$write("' + msg + '"' + unfoldParams(*params) + ")")


#-------------------------------------------------------------------------------
## Fopen
#  @param fileName name of the file
#  @return Integer representing the file descriptor
#
#-------------------------------------------------------------------------------
def Fopen(fileName):
    checkType("msg", fileName, str)
    return Integer('$fopen("' + fileName + '")') 


#-------------------------------------------------------------------------------
## Fclose
#  @param desc Integer or int representing the file descriptor
#  @return Cmd to close the file
#
#-------------------------------------------------------------------------------
def Fclose(desc):
    desc = parseInteger("desc", desc)
    return Cmd('$fclose(' + str(desc) + ')') 


#-------------------------------------------------------------------------------
## Fstrobe
#  @param desc Integer or int representing the file descriptor
#  @param msg message to be written
#  @param *params variable number of parameters
#  @return Cmd representing the Fstrobe
#
#-------------------------------------------------------------------------------
def Fstrobe(desc, msg, *params):
    desc = parseInteger("desc", desc)
    checkType("msg", msg, str)
    return Cmd('$fstrobe(' + str(desc) + ', "' + \
                         msg + '"' + \
                         unfoldParams(*params) + ")")


#-------------------------------------------------------------------------------
## Fwrite
#  @param desc Integer or int representing the file descriptor
#  @param msg message to be written
#  @param *params variable number of parameters
#  @return Cmd representing the FWrite
#
#-------------------------------------------------------------------------------
def Fwrite(desc, msg, *params):
    desc = parseInteger("desc", desc)
    checkType("msg", msg, str)
    return Cmd('$fwrite(' + str(desc) + ', "' + \
                         msg + '"' + \
                         unfoldParams(*params) + ")")
                         

#-------------------------------------------------------------------------------
## discontinuity
#  @param degree Integer or int representing the degree of the derivative with
#         discontinuity
#  @return Cmd representing the discontinuity
#
#-------------------------------------------------------------------------------
def Discontinuity(degree = 0):
    degree = parseInteger("degree", degree)
    return Cmd('$discontinuity(' + str(degree) + ')') 


#-------------------------------------------------------------------------------
## finish
#  @return Cmd representing the finish
#
#-------------------------------------------------------------------------------
def Finish():
    return Cmd('$finish') 


#-------------------------------------------------------------------------------
## error
#  @param msg message to be printed
#  @param *params variable number of parameters
#  @return Cmd representing the error
#
#-------------------------------------------------------------------------------
def Error(msg, *params):
    checkType("msg", msg, str)
    return Cmd('$error("' + msg + '"' + unfoldParams(*params) + ")")

#-------------------------------------------------------------------------------
## fatal
#  @param msg message to be printed
#  @param *params variable number of parameters
#  @return Cmd representing the error
#
#-------------------------------------------------------------------------------
def Fatal(msg, *params):
    checkType("msg", msg, str)
    return Cmd('$fatal(0, "' + msg + '"' + unfoldParams(*params) + ")")

#-------------------------------------------------------------------------------
## bond step
#  @param step Real, float or int representing the step
#  @return Cmd representing the BondStep
#
#-------------------------------------------------------------------------------
def BoundStep(step):
    step = parseReal("step", step)
    return Cmd('$bound_step(' + str(step) + ')') 


#-------------------------------------------------------------------------------
## last time a signal crossed a treshold
#  @param signal Real, float or int representing the signal
#  @param threshold Real, float or int representing the threshold that must be 
#         crossed
#  @param edge It can be one the strings "rising", "falling" or "both"
#  @return Real class representing the last crossing.
#
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
## random number generator
#  @param seed IntegerVar with the seed
#  @return random Integer
#
#-------------------------------------------------------------------------------
def random(seed):
    checkInstance("seed", seed, IntegerVar)
    return Integer('$random(' + str(seed) + ')')


#-------------------------------------------------------------------------------
## Uniforme distribution random number generator
#  @param seed IntegerVar with the seed
#  @param start Integer or int representing the start of the range
#  @param end Integer or int representing the end of the range
#  @return random Integer
#
#-------------------------------------------------------------------------------        
def uDistInt(seed, start, end):
    checkInstance("seed", seed, IntegerVar)
    start = parseInteger("start", start)
    end = parseInteger("end", end)
    return Integer('$dist_uniform(' + str(seed) + ', ' + str(start) + ', ' + \
                      str(end) + ')')
            
                      
#-------------------------------------------------------------------------------
## Uniforme distribution random number generator
#  @param seed IntegerVar with the seed
#  @param start Real, float or int representing the start of the range
#  @param end Real, float or int representing the end of the range
#  @return random Real
#
#-------------------------------------------------------------------------------       
def uDistReal(seed, start, end):
    checkInstance("seed", seed, IntegerVar)
    start = parseReal("start", start)
    end = parseReal("end", end)
    return Real('$rdist_uniform(' + str(seed) + ', ' + str(start) + ', ' + \
                  str(end) + ')')


#-------------------------------------------------------------------------------
## Gaussian distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Integer or int representing the start of the range
#  @param std Integer or int representing the end of the range
#  @return random Integer
#
#-------------------------------------------------------------------------------   
def gaussDistInt(seed, mean, std):
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    std = parseInteger("std", std)
    return Integer('$dist_normal(' + str(seed) + ', ' + str(mean) + ', ' + \
                      str(std) + ')')
        
        
#-------------------------------------------------------------------------------
## Gaussian distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Real, float or int representing the start of the range
#  @param std Real, float or int representing the end of the range
#  @return random Real
#
#------------------------------------------------------------------------------- 
def gaussDistReal(seed, mean, std):
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    std = parseReal("std", std)
    return Real('$rdist_normal(' + str(seed) + ', ' + str(mean) + ', ' + \
                  str(std) + ')')

#-------------------------------------------------------------------------------
## Exponential distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Integer or int representing the start of the range
#  @return random Integer
#
#-------------------------------------------------------------------------------   
def expDistInt(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    return Integer('$dist_exponential(' + str(seed) + ', ' + str(mean) + ')')


#-------------------------------------------------------------------------------
## Exponential distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Real, float or int representing the start of the range
#  @return random Real
#
#------------------------------------------------------------------------------- 
def expDistReal(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    return Real('$rdist_exponential(' + str(seed) + ', ' + str(mean) + ')')


#-------------------------------------------------------------------------------
## Poisson distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Integer or int representing the start of the range
#  @return random Integer
#
#-------------------------------------------------------------------------------  
def poissonDistInt(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    return Integer('$dist_poisson(' + str(seed) + ', ' + str(mean) + ')')


#-------------------------------------------------------------------------------
## Poisson distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Real, float or int representing the start of the range
#  @return random Real
#
#-------------------------------------------------------------------------------
def poissonDistReal(seed, mean):
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    return Real('$rdist_poisson(' + str(seed) + ', ' + str(mean) + ')')


#-------------------------------------------------------------------------------
## Constants for tasks that represents numbers
#
#-------------------------------------------------------------------------------
temp = Real("$temperature")
abstime = Real("$abstime")
vt = Real("$vt")


#-------------------------------------------------------------------------------
## Exponential function
#  @param x Real, float or int input
#  @return Real expressing the exponential function
#
#-------------------------------------------------------------------------------
def exp(x):
    x = parseReal("x", x)
    return Real("exp(" + str(x) + ")")


#-------------------------------------------------------------------------------
## Limited Exponential function
#  @param x Real, float or int input
#  @return Real expressing the limited exponential function
#
#-------------------------------------------------------------------------------
def limexp(x):
    x = parseReal("x", x)
    return Real("limexp(" + str(x) + ")")


#-------------------------------------------------------------------------------
## Absolute Delay
#  @param x Real, float or int input
#  @param delay Real, float or int delay input
#  @return Real expressing the absolute delay function
#
#-------------------------------------------------------------------------------
def absDelay(x, delay):
    x = parseReal("x", x)
    delay = parseReal("delay", delay)
    return Real("absdelay(" + str(x) + ", " + str(delay) + ")")


#-------------------------------------------------------------------------------
## transition filter
#  @param x Real, float or int input
#  @param delay Real, float or int delay input
#  @param riseTime delay Real, float or int delay input
#  @param fallTime delay Real, float or int delay input
#  @return Real expressing the transition filter
#
#-------------------------------------------------------------------------------
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


#-------------------------------------------------------------------------------
## ternary function
#  @param test Bool or bool representing the test
#  @param op1 any Bool, Real, Integer, int, float or bool that represents the 
#         expression when test is true
#  @param op2 any Bool, Real, Integer, int, float or bool that represents the 
#         expression when test is false
#  @return Bool, Real or Inteter representing the ternary operator
#
#-------------------------------------------------------------------------------
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


#-------------------------------------------------------------------------------
## slew filter
#  @param x Real, float or int input
#  @param riseSlope Real, float or int delay input
#  @param fallSlope Real, float or int delay input
#  @return Real expressing the slew filter
#
#-------------------------------------------------------------------------------
def slew(x, riseSlope = 10e-6, fallSlope = 10e-6):
    x = parseReal("x", x)
    riseSlope = parseReal("riseSlope", riseSlope)
    fallSlope = parseReal("fallSlope", fallSlope)
    return Real("slew(" + \
                  str(x) + ", " + \
                  str(riseSlope) + ", " + \
                  str(fallSlope) + ")")


#-------------------------------------------------------------------------------
## Diferential function
#  @param x Real, float or int input
#  @return Real expressing the diferential function
#
#-------------------------------------------------------------------------------
def ddt(x):
    x = parseReal("x", x)
    return Real("ddt(" + str(x) + ")")
 
 
#-------------------------------------------------------------------------------
## Integral function
#  @param x Real, float or int input
#  @param start Real, float or int input
#  @return Real expressing the integral function
#
#-------------------------------------------------------------------------------   
def idt(x, start = Real(0)):
    x = parseReal("x", x)
    start = parseReal("start", start)
    return Real("idt(" + str(x) + ", " + str(start) + ")")


#-------------------------------------------------------------------------------
## Ceil function
#  @param x Real, float or int input
#  @return Integer expressing the ceil function
#
#-------------------------------------------------------------------------------
def ceil(x):
    x = parseReal("x", x)
    return Integer("ceil(" + str(x) + ")")
      

#-------------------------------------------------------------------------------
## floor function
#  @param x Real, float or int input
#  @return Integer expressing the floor function
#
#-------------------------------------------------------------------------------  
def floor(x):
    x = parseReal("x", x)
    return Integer("floor(" + str(x) + ")")


#-------------------------------------------------------------------------------
## natural log function
#  @param x Real, float or int input
#  @return Real expressing the natural log function
#
#-------------------------------------------------------------------------------
def ln(x):
    x = parseReal("x", x)
    return Real("ln(" + str(x) + ")")


#-------------------------------------------------------------------------------
## log function
#  @param x Real, float or int input
#  @return Real expressing the log function
#
#-------------------------------------------------------------------------------
def log(x):
    x = parseReal("x", x)
    return Real("log(" + str(x) + ")")


#-------------------------------------------------------------------------------
## square root function
#  @param x Real, float or int input
#  @return Real expressing the square root function
#
#-------------------------------------------------------------------------------
def sqrt(x):
    x = parseReal("x", x)
    return Real("sqrt(" + str(x) + ")")


#-------------------------------------------------------------------------------
## sin function
#  @param x Real, float or int angle in radians
#  @return Real expressing the sin function
#
#-------------------------------------------------------------------------------
def sin(x):
    x = parseReal("x", x)
    return Real("sin(" + str(x) + ")")


#-------------------------------------------------------------------------------
## cos function
#  @param x Real, float or int angle in radians
#  @return Real expressing the cos function
#
#-------------------------------------------------------------------------------
def cos(x):
    x = parseReal("x", x)
    return Real("cos(" + str(x) + ")")


#-------------------------------------------------------------------------------
## tan function
#  @param x Real, float or int angle in radians
#  @return Real expressing the tan function
#
#-------------------------------------------------------------------------------
def tan(x):
    x = parseReal("x", x)
    return Real("tan(" + str(x) + ")")


#-------------------------------------------------------------------------------
## arc sin function
#  @param x Real, float or int angle input
#  @return Real expressing the arc sin function in radians
#
#-------------------------------------------------------------------------------
def asin(x):
    x = parseReal("x", x)
    return Real("asin(" + str(x) + ")")


#-------------------------------------------------------------------------------
## arc cos function
#  @param x Real, float or int angle input
#  @return Real expressing the arc cos function in radians
#
#-------------------------------------------------------------------------------
def acos(x):
    x = parseReal("x", x)
    return Real("acos(" + str(x) + ")")


#-------------------------------------------------------------------------------
## arc tan function
#  @param x Real, float or int angle input
#  @return Real expressing the arc tan function in radians
#
#-------------------------------------------------------------------------------
def atan(x):
    x = parseReal("x", x)
    return Real("atan(" + str(x) + ")")


#-------------------------------------------------------------------------------
## arc tanh2 function. Equivalent to atan(x/y)
#  @param x Real, float or int angle input
#  @param x Real, float or int angle input
#  @return Real expressing the arc tan function in radians
#
#-------------------------------------------------------------------------------
def atan2(x, y):
    x = parseReal("x", x)
    y = parseReal("y", y)
    return Real("atan2(" + str(x) + ", " + str(y) + ")")


#-------------------------------------------------------------------------------
## hypot function. Equivalent to sqrt(x*x + y*y)
#  @param x Real, float or int angle input
#  @param x Real, float or int angle input
#  @return Real expressing the hypot function
#
#-------------------------------------------------------------------------------
def hypot(x, y):
    x = parseReal("x", x)
    y = parseReal("y", y)
    return Real("hypot(" + str(x) + ", " + str(y) + ")")


#-------------------------------------------------------------------------------
## sinh function
#  @param x Real, float or int angle in radians
#  @return Real expressing the sinh function
#
#-------------------------------------------------------------------------------
def sinh(x):
    x = parseReal("x", x)
    return Real("sinh(" + str(x) + ")")


#-------------------------------------------------------------------------------
## cosh function
#  @param x Real, float or int angle in radians
#  @return Real expressing the cosh function
#
#-------------------------------------------------------------------------------
def cosh(x):
    x = parseReal("x", x)
    return Real("cosh(" + str(x) + ")")


#-------------------------------------------------------------------------------
## tanh function
#  @param x Real, float or int angle in radians
#  @return Real expressing the tanh function
#
#-------------------------------------------------------------------------------
def tanh(x):
    x = parseReal("x", x)
    return Real("tanh(" + str(x) + ")")


#-------------------------------------------------------------------------------
## arc sinh function
#  @param x Real, float or int angle input
#  @return Real expressing the arc sinh function in radians
#
#-------------------------------------------------------------------------------
def asinh(x):
    x = parseReal("x", x)
    return Real("asinh(" + str(x) + ")")


#-------------------------------------------------------------------------------
## arc cosh function
#  @param x Real, float or int angle input
#  @return Real expressing the arc cosh function in radians
#
#-------------------------------------------------------------------------------
def acosh(x):
    x = parseReal("x", x)
    return Real("acosh(" + str(x) + ")")


#-------------------------------------------------------------------------------
## arc tanh function
#  @param x Real, float or int angle input
#  @return Real expressing the arc tanh function in radians
#
#-------------------------------------------------------------------------------
def atanh(x):
    x = parseReal("x", x)
    return Real("atanh(" + str(x) + ")")


#-------------------------------------------------------------------------------
## Class of electrical signals
#
#-------------------------------------------------------------------------------
class Electrical():

    #---------------------------------------------------------------------------
    ## constructor
    #  @param self The object pointer.
    #  @param name string representing the name of the electrical signal
    # 
    #---------------------------------------------------------------------------
    def __init__(self, name):
        checkType("name", name, str)
        self.name = name
        self.v = Real("V(" + name + ")") 
        self.i = Real("I(" + name + ")") 
        
    #---------------------------------------------------------------------------
    ## Return electrical name
    #  @param self The object pointer.
    #  @return string representing the name of the signal
    # 
    #---------------------------------------------------------------------------
    def getName(self):
        return self.name

    #---------------------------------------------------------------------------
    ## Return a command representing voltage contribution
    #  @param self The object pointer.
    #  @param value Real, float or int representig the value of the contribution
    #  @return a Cmd representing the voltage contribution 
    # 
    #---------------------------------------------------------------------------
    def vCont(self, value):
        value = parseReal("value", value)
        return Cmd('V(' + self.name + ') <+ ' + str(value))

    #---------------------------------------------------------------------------
    ## Return a command representing current contribution
    #  @param self The object pointer.
    #  @param value Real, float or int representig the value of the contribution
    #  @return a Cmd representing the current contribution 
    # 
    #---------------------------------------------------------------------------
    def iCont(self, value):
        value = parseReal("value", value)
        return Cmd('I(' + self.name + ') <+ ' + str(value))

    #---------------------------------------------------------------------------
    ## Return a command representing voltage attribution
    #  @param self The object pointer.
    #  @param value Real, float or int representig the value of the attribution
    #  @return a Cmd representing the voltage attribution
    # 
    #---------------------------------------------------------------------------
    def vAttr(self, value):
        value = parseReal("value", value)
        return Cmd('V(' + self.name + ') = ' + str(value))

    #---------------------------------------------------------------------------
    ## Return a command representing current attribution
    #  @param self The object pointer.
    #  @param value Real, float or int representig the value of the attribution
    #  @return a Cmd representing the current attribution
    # 
    #---------------------------------------------------------------------------
    def iAttr(self, value):
        value = parseReal("value", value)
        return Cmd('I(' + self.name + ') = ' + str(value))

    #---------------------------------------------------------------------------
    ## Return a command representing voltage indirect assigment (Voltage that
    #  makes value true)
    #  @param self The object pointer.
    #  @param value Bool or bool condition
    #  @return a Cmd representing the voltage indirect assigment 
    #
    #---------------------------------------------------------------------------
    def vInd(self, value):
        value = parseBool("value", value)
        return Cmd('V(' + self.name + ') : ' + str(value))

    #---------------------------------------------------------------------------
    ## Return a command representing current indirect assigment (Current that
    #  makes value true)
    #  @param self The object pointer.
    #  @param value Bool or bool condition
    #  @return a Cmd representing the current indirect assigment 
    #
    #---------------------------------------------------------------------------
    def iInd(self, value):
        value = parseBool("value", value)
        return Cmd('I(' + self.name + ') : ' + str(value))
 

#-------------------------------------------------------------------------------
## Branch class
#
#-------------------------------------------------------------------------------
class Branch(Electrical):

    #---------------------------------------------------------------------------
    ## constructor
    #  @param self The object pointer.
    #  @param node1 Electrical signal representing the first node
    #  @param node2 Electrical signal representing the second node
    #
    #---------------------------------------------------------------------------
    def __init__(self, node1, node2):
        checkInstance("node1", node1, Electrical)
        checkInstance("node2", node2, Electrical)
        checkNotInstance("node1", node1, Branch)
        checkNotInstance("node2", node2, Branch)
        super(Branch, self).__init__(node1.getName() + ", " + node2.getName())


#-------------------------------------------------------------------------------
## verilogA class
#
#-------------------------------------------------------------------------------
class Module:

    #---------------------------------------------------------------------------
    ## constructor
    #  @param self The object pointer.
    #  @param node1 Electrical signal representing the first node
    #  @param moduleName name of the module (the first word after module in the 
    #         va)
    #
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
    ## return module name
    #  @param self The object pointer
    #  @return string representing the name of the module
    #
    #---------------------------------------------------------------------------
    def getModuleName(self):
        return self.moduleName

    #---------------------------------------------------------------------------
    ## If name is an empty string, get the next name available in the namespace.
    #  If name isn't empty, check if the name is available in the verilogA 
    #  namespace and raise an exception if it doesn't
    #  @param self The object pointer. 
    #  @param name string to be checked
    #  @return string representing a valid name in the verilogA namespace
    #
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
    ## Add variable to the module
    #  @param self The object pointer. 
    #  @param vType it can be Integer Bool or Real
    #  @param name string representing the name of the variable in the verilogA
    #  @return RealVar, IntegerVar or BoolVar depending on the vType
    #   
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
    ## Add parameter to the module
    #  @param self The object pointer. 
    #  @param value Initial value. It can be Real, Integer, int or float.
    #  @param name string representing the name of the parameter in the verilogA
    #  @return RealVar or RealVar depending on the initial value
    #
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
    ## Add commands to the analog block
    #  @param self The object pointer.
    #  @param *args variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def analog(self, *args):
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd) and \
                   "cmd[" + str(i) + "] must be an instance of Cmd and but a" +\
                   str(type(arg)) + " was given instead"
            i = i + 1
            self.cmds.append(arg)

    #---------------------------------------------------------------------------
    ## Add commands to beginning of the analog block
    #  @param self The object pointer.
    #  @param *args variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def beginningAnalog(self, *args):
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd) and \
                   "cmd[" + str(i) + "] must be an instance of Cmd and but a" +\
                   str(type(arg)) + " was given instead"
            i = i + 1
            self.beginningCmds.append(arg)

    #---------------------------------------------------------------------------
    ## Add commands to the end of the analog block
    #  @param self The object pointer.
    #  @param *args variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def endAnalog(self, *args):
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd) and \
                   "cmd[" + str(i) + "] must be an instance of Cmd and but a" +\
                   str(type(arg)) + " was given instead"
            i = i + 1
            self.endCmds.append(arg)

    #---------------------------------------------------------------------------
    ## Add node
    #  @param self The object pointer.
    #  @param name string representing the name of the electrical signal
    #  @param width int representing the width of the electrical signal
    #  @param direction direction of the signal. It can be on the strings 
    #         "internal", "input", "output", or "inout"
    #  @return string with the name of the node
    #
    #---------------------------------------------------------------------------
    def addNode(self, name, width, direction):
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
    ## Return electrical class
    #  @param self The object pointer.
    #  @param name string representing the name of the electrical signal
    #  @param width int representing the width of the electrical signal
    #  @param direction direction of the signal. It can be on the strings 
    #         "internal", "input", "output", or "inout"
    #  @return list of electrical classes or an electrical class depending on 
    #          the width
    #
    #---------------------------------------------------------------------------
    def electrical(self, name = "", width = 1, direction = "internal"):
        name = self.addNode(name, width, direction)
        if width == 1:
            return Electrical(name)
        else:
            vector = list()
            for i in range(0, width):
                vector.append(Electrical(name + "[" + str(i) + "]"))
            return vector

    #---------------------------------------------------------------------------
    ## Return the VA verilog code
    #  @param self The object pointer.
    #  @return string with the verilogA code
    #
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

        
