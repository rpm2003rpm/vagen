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
import math as m

#-------------------------------------------------------------------------------
## Check if the type of variable matches the Type. Raise an assertion error if
#  it doesn't.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @param Type Type that the variable should match.
#  @return None.
#
#-------------------------------------------------------------------------------
def checkType(param, var, Type):
    """Check if the type of variable matches the specified Type.

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.
        Type (type): Expected type.

    Returns:
        None; An AssertionError is raised.
    """
    assert type(var) == Type, \
    f"{param} must be a {Type} but a {type(var)} was given instead"


#-------------------------------------------------------------------------------
## Check if the variable is an instance of Type. Raise an assertion error if 
#  it doesn't. 
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @param Type Type that the variable should match.
#  @return None.
#
#-------------------------------------------------------------------------------
def checkInstance(param, var, Type):
    """Check if the variable is an instance of the specified Type.

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.
        Type (type): Expected type.

    Returns:
        None; An AssertionError is raised.
    """
    assert isinstance(var, Type), \
           (f"{param} must be an instance of {Type} but a {type(var)} was given"
             " instead")


#-------------------------------------------------------------------------------
## Check if the variable isn't an instance of Type. Raise an assertion error if 
#  it doesn't. 
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @param Type Type that the variable should match.
#  @return None.
#
#-------------------------------------------------------------------------------
def checkNotInstance(param, var, Type):
    """Check that the variable is not an instance of the specified Type.

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.
        Type (type): Type that must not match.

    Returns:
        None; An AssertionError is raised.
    """
    assert not isinstance(var, Type), f"{param} can't be an instance of {Type}"

#-------------------------------------------------------------------------------
## Return a Real instance.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return Real object.
#
#-------------------------------------------------------------------------------
def parseReal(param, var):
    """Return a Real instance constructed from var.

    Args:
        param (str): Name of the variable.
        var (any): Variable to be parsed.

    Returns:
        Real: The parsed Real object.

    Raises:
        Exception: If var is not an instance of Real, float, or int.
    """
    if isinstance(var, (Real, float, int)):
        return Real(var)
    else:
        raise Exception( (f"{param} must be an instance of 'Real', 'float', "
                          f"'int', or 'bool' but a '{type(var).__name__}' was "
                           "given instead") )


#-------------------------------------------------------------------------------
## Check if the var is Real or it can be parsed to Real.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return None.
#
#-------------------------------------------------------------------------------
def checkReal(param, var):
    """Check if the variable is of type Real (or compatible with Real).

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.

    Returns:
        None; An AssertionError is raised.
    """
    assert isinstance(var, (Real, float, int)), \
           (f"{param} must be an instance of 'Real', 'float', 'int', or 'bool'"
            f" but a '{type(var).__name__}' was given instead")


#-------------------------------------------------------------------------------
## Return an Integer instance 
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return Integer object.
#
#-------------------------------------------------------------------------------
def parseInteger(param, var):
    """Return an Integer instance constructed from var.

    Args:
        param (str): Name of the variable.
        var (any): Variable to be parsed.

    Returns:
        Integer: The parsed Integer object.

    Raises:
        Exception: If var is not an instance of Integer or int.
    """
    if isinstance(var, (Integer, int)):
        return Integer(var)
    else:
        raise Exception( (f"{param} must be an instance of 'Integer', 'int', or"
                          f" 'bool' but a '{type(var).__name__}' was given "
                           "instead") )
                 
                 
#-------------------------------------------------------------------------------
## Check if the variable is Integer or can be parsed to Integer.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return None.
#
#-------------------------------------------------------------------------------
def checkInteger(param, var):
    """Check if the variable is of type Integer (or compatible with Integer).

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.

    Returns:
        None; An AssertionError is raised.
    """
    assert isinstance(var, (Integer, int)), \
           (f"{param} must be an instance of 'Integer', 'int', or 'bool' but a "
            f"'{type(var).__name__}' was given instead")


#-------------------------------------------------------------------------------
## Return a Bool instance.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return Bool object.
#
#-------------------------------------------------------------------------------
def parseBool(param, var):
    """Return a Bool instance constructed from var.

    Args:
        param (str): Name of the variable.
        var (any): Variable to be parsed.

    Returns:
        Bool: The parsed Bool object.

    Raises:
        Exception: If var is not an instance of Bool or bool.
    """
    if isinstance(var, (Bool, bool)):
        return Bool(var)
    else:
        raise Exception( (f"{param} must be an instance of 'Bool' or 'bool' "
                          f"but a '{type(var).__name__}' was given instead") )
                        
                        
#-------------------------------------------------------------------------------
## Check if the variable is Bool or can be parsed to Bool.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return None.
#
#-------------------------------------------------------------------------------
def checkBool(param, var):
    """Check if the variable is of type Bool (or compatible with Bool).

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.

    Returns:
        None; An AssertionError is raised.
    """
    assert isinstance(var, (Bool, bool)), \
           (f"{param} must be an instance of 'Bool' or 'bool' but a "
            f"'{type(var).__name__}' was given instead")


#-------------------------------------------------------------------------------
## Return a Real, Integer or Boolean instance.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return Real, Integer or Bool instance.
#
#-------------------------------------------------------------------------------                        
def parseNumber(param, var):
    """Return a Real, Integer, or Bool instance constructed from var.

    Args:
        param (str): Name of the variable.
        var (any): Variable to be parsed.

    Returns:
        Real, Integer, or Bool: The parsed numeric object.

    Raises:
        Exception: If var is not of a compatible type.
    """
    if isinstance(var, (Bool, bool)):
        return Bool(var)
    elif isinstance(var, (Integer, int)):
        return Integer(var)
    elif isinstance(var, (Real, float)):
        return Real(var)    
    else:
        raise Exception( (f"{param} must be an instance of 'Bool', 'bool', " 
                          f"'Real', 'float', 'Integer' or 'int' but a "
                          f"'{type(var).__name__}' was given instead") ) 
           

#-------------------------------------------------------------------------------
## Check if the variable is a number or can be parsed to Bool.
#  @param param String representing the name of the variable.
#  @param var Variable.
#  @return None.
#
#-------------------------------------------------------------------------------                        
def checkNumber(param, var):
    """Check if the variable is a numeric type (Real, Integer, or Bool).

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.

    Returns:
        None; An AssertionError is raised.
    """
    assert isinstance(var, (Real, Integer, Bool, float, int, bool)), \
           (f"{param} must be an instance of 'Bool', 'bool', 'Real', 'float', "
            f"'Integer' or 'int' but a '{type(var).__name__}' was given instead")
           

#-------------------------------------------------------------------------------
## Creates a comment block
#  @param message String representing the comment
#  @param padding Number of tabs by which the text will be shifted left align
#         center, left or right 
#  @return The comment block.
#
#-------------------------------------------------------------------------------
def blockComment(padding, message, align = "center"):
    """Creates a formatted comment block.

    Args:
        padding (int): Number of tabs for left alignment.
        message (str): The comment text.
        align (str, optional): Alignment of the text 
            ('center', 'left', or 'right'). Defaults to "center".

    Returns:
        str: The formatted comment block.
    """
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
## precedence
#
#-------------------------------------------------------------------------------         
#opPrecedence = {'unary'   : {'+'  : 0, '-'  : 0, '!'  : 0, '~'  : 0},
#                'binary'  : {'*'  : 1, '/'  : 1, '%' : 1,
#                             '+'  : 2, '-'  : 2,
#                             '>>' : 3, '<<' : 3,
#                             '<=' : 4, '>=' : 4, '>' :4, '<' : 4,
#                             '==' : 5, '!=' : 5,
#                             '&'  : 6,
#                             '^'  : 7,
#                             '|'  : 8,
#                             '&&' : 9,
#                             '||' : 10},
#                'ternary' : {'?'  : 11 }}
 
 
#-------------------------------------------------------------------------------
## unary function (local use inside veriloga.py only)
#  @param Type Real, Integer, or Bool
#  @param op1 any Bool, Real, Integer, int, float or bool that represents the 
#         expression when test is true
#  @return Bool, Real or Inteter representing the binary operatation
#
#-------------------------------------------------------------------------------
def unary(Type, op1, operator):
    """Generate a unary expression of the form: operator(op1).

    Args:
        Type (type): The type constructor (Real, Integer, or Bool).
        op1 (any): Operand for the unary operation.
        operator (str): String representing the unary operator.

    Returns:
        An instance of Type representing the unary operation.
    """
    return Type(f"{operator}( {op1} )")
    
 
#-------------------------------------------------------------------------------
## binary function (local use inside veriloga.py only)
#  @param Type Real, Integer, or Bool
#  @param op1 any Bool, Real, Integer, int, float or bool that represents the 
#         expression when test is true
#  @param op2 any Bool, Real, Integer, int, float or bool that represents the 
#         expression when test is false
#  @param operator string representing the operator
#  @return Bool, Real or Inteter representing the binary operatation
#
#-------------------------------------------------------------------------------
def binary(Type, op1, op2, operator):
    """Generate a binary expression combining op1 and op2 with the given 
    operator.

    Args:
        Type (type): The type constructor (Real, Integer, or Bool).
        op1 (any): The left-hand operand.
        op2 (any): The right-hand operand.
        operator (str): The binary operator as a string.

    Returns:
        An instance of Type representing the binary operation.
    """
    return Type(f"( {op1} ){operator}( {op2} )")
    
 
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
    """Generate a ternary expression based on a test condition.

    Args:
        test (Bool or bool): The test condition.
        op1 (any): Expression if test is true.
        op2 (any): Expression if test is false.

    Returns:
        An instance (Real, Integer, or Bool) representing the ternary operation.

    Raises:
        Exception: If op1 and op2 are not of compatible types.
    """
    test = parseBool("test", test)
    if isinstance(op1, (Bool, bool) ) and \
       isinstance(op2, (Bool, bool) ):
       op1 = parseBool("op1", op1)
       op2 = parseBool("op2", op2)
    elif isinstance(op1, (Integer, int) ) and \
         isinstance(op2, (Integer, int) ):
       op1 = parseInteger("op1", op1)
       op2 = parseInteger("op2", op2)
    elif isinstance(op1, (Real, float, int) ) and\
         isinstance(op2, (Real, float, int) ):
       op1 = parseReal("op1", op1)
       op2 = parseReal("op2", op2)
    else:
        raise Exception( ("op1 and op2 must be Integer, Real, Bool, bool, "
                          "float, or int with compatible types but got "
                         f"{type(op1)} and {type(op2)} instead") )
    Type = Real if isinstance(op1, Real) else \
           Bool if isinstance(op1, Bool) else \
           Integer
    return Type(f"{test} ? {op1} : {op2}")        
         

#-------------------------------------------------------------------------------
## Class of Real operators
#
#-------------------------------------------------------------------------------
class Real():
    """Real operator class representing a Real expression."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self The object pointer.
    #  @param value String representing a Real expression, an Integer, a Bool,
    #  or a value that can be converted to Real.
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        """Initialize a Real instance.

        Args:
            value (str, Real, Integer, Bool, or numeric): 
            The value to convert into a Real expression.
        """
        if isinstance(value, Bool):
            value = f"{ternary(value, 1.0, 0.0)}"
        elif isinstance(value, (Real, Integer)):
            value = f"{value}"
        elif not isinstance(value, str):
            try:
                value = "{:e}".format(value)
            except:
                raise TypeError(f"Can't convert {value} to Real")
        self.value = value
            
    #---------------------------------------------------------------------------
    ## Return the operator value.
    #  @param self The object pointer.
    #  @return String representing the Real expression.
    #
    #---------------------------------------------------------------------------
    def getValue(self):
        """Return the Real expression as a string.

        Returns:
            str: The expression stored in this Real instance.
        """
        return self.value
    
    #---------------------------------------------------------------------------
    ## Addition override.
    #  @param self The object pointer.
    #  @param other expression to be added.
    #  @return expression representing the addition.
    #
    #---------------------------------------------------------------------------
    def __add__(self, other):
        """Override the addition operator for Real objects.

        Args:
            other (Real, int, float): The operand to add.

        Returns:
            Real: A new Real instance representing the addition.
        """
        other = parseReal("other", other)
        return binary(Real, self, other, "+")

    #---------------------------------------------------------------------------
    ## Subtraction override.
    #  @param self Minuend object pointer.
    #  @param other Subtrahend. 
    #  @return expression representing the subtraction.
    #
    #---------------------------------------------------------------------------
    def __sub__(self, other):
        """Override the subtraction operator for Real objects.

        Args:
            other (Real, int, float): The operand to subtract.

        Returns:
            Real: A new Real instance representing the subtraction.
        """
        other = parseReal("other", other)
        return binary(Real, self, other, "-")
        
    #---------------------------------------------------------------------------
    ## Multiplication override.
    #  @param self Multiplicand object pointer.
    #  @param other Multiplier. 
    #  @return expression representing the multiplication.
    #
    #---------------------------------------------------------------------------
    def __mul__(self, other):
        """Override the multiplication operator for Real objects.

        Args:
            other (Real, int, float): The operand to multiply.

        Returns:
            Real: A new Real instance representing the multiplication.
        """
        other = parseReal("other", other)
        return binary(Real, self, other, "*")

    #---------------------------------------------------------------------------
    ## Division override.
    #  @param self Dividend object pointer.
    #  @param other Quotient. 
    #  @return expression representing the division.
    #
    #---------------------------------------------------------------------------
    def __truediv__(self, other):
        """Override the division operator for Real objects.

        Args:
            other (Real, int, float): The divisor.

        Returns:
            Real: A new Real instance representing the division.
        """
        other = parseReal("other", other)
        return binary(Real, self, other, "/")

    #---------------------------------------------------------------------------
    ## Pow override.
    #  @param self Base object pointer.
    #  @param other Exponent. 
    #  @return expression representing the power.
    #
    #---------------------------------------------------------------------------
    def __pow__(self, other):
        """Override the power operator for Real objects.

        Args:
            other (Real, int, float): The exponent.

        Returns:
            Real: A new Real instance representing the power operation.
        """
        other = parseReal("other", other)
        return Real(f'pow({self}, {other})')

    #---------------------------------------------------------------------------
    ## Greater than override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __gt__(self, other):
        """Override the greater-than operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, ">")

    #---------------------------------------------------------------------------
    ## Less than override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __lt__(self, other):
        """Override the less-than operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, "<")

    #---------------------------------------------------------------------------
    ## Less than equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __le__(self, other):
        """Override the less-than-or-equal operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, "<=")

    #---------------------------------------------------------------------------
    ## Greater than equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ge__(self, other):
        """Override the greater-than-or-equal operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, ">=")

    #---------------------------------------------------------------------------
    ## Equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        """Override the equality operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the equality result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, "==")

    #---------------------------------------------------------------------------
    ## Not equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        """Override the inequality operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the inequality result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, "!=")
        
    #---------------------------------------------------------------------------
    ## Reverse addition override
    #  @param self The object pointer.
    #  @param other expression to be added.
    #  @return expression representing the addition.
    #
    #---------------------------------------------------------------------------
    def __radd__(self, other):
        """Override the reverse addition operator for Real objects.

        Args:
            other (Real, int, float): The left-hand operand.

        Returns:
            Real: A new Real instance representing the addition.
        """
        other = parseReal("other", other)
        return binary(Real, other, self, "+")

    #---------------------------------------------------------------------------
    ## Reverse subtraction override
    #  @param self Subtrahend object pointer.
    #  @param other Minuend. 
    #  @return expression representing the subtraction.
    #
    #---------------------------------------------------------------------------
    def __rsub__(self, other):
        """Override the reverse subtraction operator for Real objects.

        Args:
            other (Real, int, float): The left-hand operand.

        Returns:
            Real: A new Real instance representing the subtraction.
        """
        other = parseReal("other", other)
        return binary(Real, other, self, "-")

    #---------------------------------------------------------------------------
    ## Reverse multiplication override.
    #  @param self Multiplier object pointer.
    #  @param other Multiplicand.
    #  @return expression representing the multiplication.
    #
    #---------------------------------------------------------------------------
    def __rmul__(self, other):
        """Override the reverse multiplication operator for Real objects.

        Args:
            other (Real, int, float): The left-hand operand.

        Returns:
            Real: A new Real instance representing the multiplication.
        """
        other = parseReal("other", other)
        return binary(Real, other, self, "*")

    #---------------------------------------------------------------------------
    ## Reverse division override.
    #  @param self Quotient object pointer.
    #  @param other Dividend. 
    #  @return expression representing the division.
    #
    #---------------------------------------------------------------------------
    def __rtruediv__(self, other):
        """Override the reverse division operator for Real objects.

        Args:
            other (Real, int, float): The left-hand operand.

        Returns:
            Real: A new Real instance representing the division.
        """
        other = parseReal("other", other)
        return binary(Real, other, self, "/")

    #---------------------------------------------------------------------------
    ## Pow override.
    #  @param self Exponent object pointer.
    #  @param other Base. 
    #  @return expression representing the power.
    #
    #---------------------------------------------------------------------------
    def __rpow__(self, other):
        """Override the reverse power operator for Real objects.

        Args:
            other (Real, int, float): The base.

        Returns:
            Real: A new Real instance representing the power.
        """
        other = parseReal("other", other)
        return Real(f'pow({other}, {self})')
        
    #---------------------------------------------------------------------------
    ## negation override
    #  @param self Object pointer.
    #  @return expression representing negation.
    #
    #---------------------------------------------------------------------------
    def __neg__(self):
        """Override the unary negation operator for Real objects.

        Returns:
            Real: A new Real instance representing the negated expression.
        """
        return unary(Real, self, "-") 
    
    #---------------------------------------------------------------------------
    ## pos override
    #  @param self Object pointer.
    #  @return copy of the same object.
    #
    #---------------------------------------------------------------------------
    def __pos__(self):
        """Override the unary plus operator for Real objects.

        Returns:
            Real: A new Real instance that is a copy of this object.
        """
        return unary(Real, self, "+") 

    #---------------------------------------------------------------------------
    ## abs override
    #  @param self Object pointer.
    #  @return expression representing absolute value.
    #
    #---------------------------------------------------------------------------
    def __abs__(self):
        """Override the abs() function for Real objects.

        Returns:
            Real: A new Real instance representing the absolute value.
        """
        return Real(f"abs({self})") 

    #---------------------------------------------------------------------------
    ## str override
    #  @param self Object pointer.
    #  @return string representing the expression
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        """Return the string representation of the Real expression.

        Returns:
            str: The Real expression as a string.
        """
        return self.value


#-------------------------------------------------------------------------------
## Class of Bool operators
#
#-------------------------------------------------------------------------------
class Bool():
    """Bool operator class representing a Boolean expression."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param Self The object pointer.
    #  @param Value String representing a Real expression, an Integer, a Bool,
    #  or a value that can be converted to Bool.
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        """Initialize a Bool instance.

        Args:
            value (str, Real, Integer, Bool, or any convertible type): 
            The value to convert into a Bool expression.
        """
        if isinstance(value, (Real, Integer)):
            value = f"{value != 0}"
        elif isinstance(value, Bool):
            value = f"{value}"
        elif not isinstance(value, str):
            try:
                value = f"{int(bool(value))}"
            except:
                raise TypeError(f"Can't convert {value} to Bool")
        self.value = value

    #---------------------------------------------------------------------------
    ## Return the operator value.
    #  @param Self The object pointer.
    #  @return String representing the Bool expression.
    #
    #---------------------------------------------------------------------------
    def getValue(self):
        """Return the Bool expression as a string.

        Returns:
            str: The expression stored in this Bool instance.
        """
        return self.value

    #---------------------------------------------------------------------------
    ## And logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the and operation.
    #
    #---------------------------------------------------------------------------
    def __and__(self, other):
        """Override the logical AND operator for Bool objects.

        Args:
            other (Bool or bool): The operand for the AND operation.

        Returns:
            Bool: A new Bool instance representing the result of the AND 
                operation.
        """
        checkBool("other", other)
        if isinstance(other, Bool):
            return binary(Bool, self, other, "&&")
        else:
            if other:
                return Bool(self)
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
        """Override the reverse logical AND operator for Bool objects.

        Args:
            other (Bool or bool): The left-hand operand for the AND operation.

        Returns:
            Bool: A new Bool instance representing the result of the AND 
                operation.
        """
        checkBool("other", other)
        if isinstance(other, Bool):
            return binary(Bool, other, self, "&&")
        else:
            if other:
                return Bool(self)
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
        """Override the logical OR operator for Bool objects.

        Args:
            other (Bool or bool): The operand for the OR operation.

        Returns:
            Bool: A new Bool instance representing the result of the OR 
                operation.
        """
        checkBool("other", other)
        if isinstance(other, Bool):
            return binary(Bool, self, other, "||")
        else:
            if other:
                return True
            else:  
                return Bool(self)
        
    #---------------------------------------------------------------------------
    ## Reverse or logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the or operation.
    #
    #---------------------------------------------------------------------------
    def __ror__(self, other):
        """Override the reverse logical OR operator for Bool objects.

        Args:
            other (Bool or bool): The left-hand operand for the OR operation.

        Returns:
            Bool: A new Bool instance representing the result of the OR 
                 operation.
        """
        checkBool("other", other)
        if isinstance(other, Bool):
            return binary(Bool, other, self, "||")
        else:
            if other:
                return True
            else:  
                return Bool(self)
        
    #---------------------------------------------------------------------------
    ## Xor logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the exclusive or operation.
    #
    #---------------------------------------------------------------------------
    def __xor__(self, other):
        """Override the logical XOR operator for Bool objects.

        Args:
            other (Bool or bool): The operand for the XOR operation.

        Returns:
            Bool: A new Bool instance representing the result of the XOR 
                operation.
        """
        checkBool("other", other)
        if isinstance(other, Bool):
            return (self & ~other) | (~self & other)
        else:
            if other:
                return ~self
            else:  
                return Bool(self)

    #---------------------------------------------------------------------------
    ## Reverse xor logic override
    #  @param Self First operand object pointer.
    #  @param Other Second operand.
    #  @return Result of the exclusive or operation.
    #
    #---------------------------------------------------------------------------
    def __rxor__(self, other):
        """Override the reverse logical XOR operator for Bool objects.

        Args:
            other (Bool or bool): The left-hand operand for the XOR operation.

        Returns:
            Bool: A new Bool instance representing the result of the XOR 
                operation.
        """
        checkBool("other", other)
        if isinstance(other, Bool):
            return (other & ~self) | (~other & self)
        else:
            if other:
                return ~self
            else:  
                return Bool(self)
                
    #---------------------------------------------------------------------------
    ## Inversion override
    #  @param Self Object pointer.
    #  @return Expression representing inversion.
    #
    #---------------------------------------------------------------------------
    def __invert__(self):
        """Override the bitwise inversion operator for Bool objects.

        Returns:
            Bool: A new Bool instance representing the logical NOT of the 
                operand.
        """
        return unary(Bool, self, "!")
        
    #---------------------------------------------------------------------------
    ## str override
    #  @param Self Object pointer.
    #  @return String representing the expression
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        """Return the string representation of the Bool expression.

        Returns:
            str: The Bool expression as a string.
        """
        return self.value

    #---------------------------------------------------------------------------
    ## Equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        """Override the equality operator for Bool objects.

        Args:
            other (Bool or bool): The operand to compare.

        Returns:
            Bool: A new Bool instance representing the equality result.
        """
        other = parseBool("other", other)
        return binary(Bool, self, other, "==") 

    #---------------------------------------------------------------------------
    ## Not equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        """Override the inequality operator for Bool objects.

        Args:
            other (Bool or bool): The operand to compare.

        Returns:
            Bool: A new Bool instance representing the inequality result.
        """
        other = parseBool("other", other)
        return binary(Bool, self, other, "!=")
        
        
#-------------------------------------------------------------------------------
## Class of Integer operators
#
#-------------------------------------------------------------------------------
class Integer():
    """Integer operator class representing an Integer expression."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param Self The object pointer.
    #  @param Value String representing a Real expression, an Integer, a Bool,
    #  or a value that can be converted to Integer.
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        """Initialize an Integer instance.

        Args:
            value (str, Integer, Real, Bool, or convertible type): The value to 
                convert into an Integer expression.
        """
        if isinstance(value, Bool):
            value = f"{ternary(value, 1, 0)}"
        elif isinstance(value, Real):
            value = f"_rtoi({value})"
        elif isinstance(value, Integer):
            value = f"{value}"            
        elif not isinstance(value, str):
            if isinstance(value, int):
                assert value > -2147483648 and value < 2147483647, \
                (f"Can't convert {value} to integer, because it is outside of"
                  "the range [-2147483648, 2147483647]") 
            try:
                value = f"{int(value)}"
            except:
                raise TypeError(f"Can't convert {value} to Integer")
        self.value = value
        
    #---------------------------------------------------------------------------
    ## Return the operator value.
    #  @param Self The object pointer.
    #  @return String representing the Bool expression.
    #
    #---------------------------------------------------------------------------
    def getValue(self):
        """Return the Integer expression as a string.

        Returns:
            str: The expression stored in this Integer instance.
        """
        return self.value

    #---------------------------------------------------------------------------
    ## Addition override.
    #  @param self The object pointer.
    #  @param other expression to be added.
    #  @return expression representing the addition.
    #
    #---------------------------------------------------------------------------
    def __add__(self, other):
        """Override the addition operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to add.

        Returns:
            Integer: A new Integer instance representing the addition.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "+")
        
    #---------------------------------------------------------------------------
    ## Reverse addition override
    #  @param self The object pointer.
    #  @param other expression to be added.
    #  @return expression representing the addition.
    #
    #---------------------------------------------------------------------------
    def __radd__(self, other):
        """Override the reverse addition operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the addition.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "+")
        
    #---------------------------------------------------------------------------
    ## Subtraction override.
    #  @param self Minuend object pointer.
    #  @param other Subtrahend. 
    #  @return expression representing the subtraction.
    #
    #---------------------------------------------------------------------------
    def __sub__(self, other):
        """Override the subtraction operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to subtract.

        Returns:
            Integer: A new Integer instance representing the subtraction.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "-")
        
    #---------------------------------------------------------------------------
    ## Reverse subtraction override
    #  @param self Subtrahend object pointer.
    #  @param other Minuend. 
    #  @return expression representing the subtraction.
    #
    #--------------------------------------------------------------------------- 
    def __rsub__(self, other):
        """Override the reverse subtraction operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the subtraction.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "-")

    #---------------------------------------------------------------------------
    ## Multiplication override.
    #  @param self Multiplicand object pointer.
    #  @param other Multiplier. 
    #  @return expression representing the multiplication.
    #
    #---------------------------------------------------------------------------
    def __mul__(self, other):
        """Override the multiplication operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to multiply.

        Returns:
            Integer: A new Integer instance representing the multiplication.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "*")
        
    #---------------------------------------------------------------------------
    ## Reverse multiplication override.
    #  @param self Multiplier object pointer.
    #  @param other Multiplicand.
    #  @return expression representing the multiplication.
    #
    #---------------------------------------------------------------------------
    def __rmul__(self, other):
        """Override the reverse multiplication operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the multiplication.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "*")

    #---------------------------------------------------------------------------
    ## Division override.
    #  @param self Dividend object pointer.
    #  @param other Quotient. 
    #  @return expression representing the division.
    #
    #---------------------------------------------------------------------------
    def __truediv__(self, other):
        """Override the division operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The divisor.

        Returns:
            Integer: A new Integer instance representing the division.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "/")

    #---------------------------------------------------------------------------
    ## Reverse division override.
    #  @param self Quotient object pointer.
    #  @param other Dividend. 
    #  @return expression representing the division.
    #
    #---------------------------------------------------------------------------
    def __rtruediv__(self, other):
        """Override the reverse division operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the division.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "/")
        
    #---------------------------------------------------------------------------
    ## module override
    #  @param self Dividend.
    #  @param other Quotient. 
    #  @return expression representing the module.
    #
    #---------------------------------------------------------------------------
    def __mod__(self, other):
        """Override the modulus operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The divisor.

        Returns:
            Integer: A new Integer instance representing the modulus.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "%")
        
    #---------------------------------------------------------------------------
    ## reverse module override
    #  @param self Quotient. 
    #  @param other Dividend.
    #  @return expression representing the module.
    #
    #---------------------------------------------------------------------------
    def __rmod__(self, other):
        """Override the reverse modulus operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the modulus.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "%")

    #---------------------------------------------------------------------------
    ## Pow override.
    #  @param self Base object pointer.
    #  @param other Exponent. 
    #  @return expression representing the power.
    #
    #---------------------------------------------------------------------------
    def __pow__(self, other):
        """Override the power operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The exponent.

        Returns:
            Integer: A new Integer instance representing the power operation.
        """
        other = parseInteger("other", other)
        return Integer(f'_rtoi(pow({self}, {other}))')
        
    #---------------------------------------------------------------------------
    ## Reverse pow override.
    #  @param self Exponent object pointer.
    #  @param other Base. 
    #  @return expression representing the power.
    #
    #---------------------------------------------------------------------------
    def __rpow__(self, other):
        """Override the reverse power operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The base.

        Returns:
            Integer: A new Integer instance representing the power operation.
        """
        other = parseInteger("other", other)
        return Integer(f'_rtoi(pow({other}, {self}))')
        
    #---------------------------------------------------------------------------
    ## right shift override.
    #  @param self Integer to be shifted.
    #  @param other number of times the number will be shifted.
    #  @return expression representing the shift.
    #
    #---------------------------------------------------------------------------
    def __rshift__(self, other):
        """Override the right shift operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The number of times to 
                shift.

        Returns:
            Integer: A new Integer instance representing the right shift.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, ">>")

    #---------------------------------------------------------------------------
    ## Reverse right shift override.
    #  @param self number of times the number will be shifted.
    #  @param other Integer to be shifted.
    #  @return expression representing the shift.
    #
    #---------------------------------------------------------------------------
    def __rrshift__(self, other):
        """Override the reverse right shift operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the right shift.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, ">>")
        
    #---------------------------------------------------------------------------
    ## left shift override.
    #  @param self Integer to be shifted.
    #  @param other number of times the number will be shifted.
    #  @return expression representing the shift.
    #
    #---------------------------------------------------------------------------
    def __lshift__(self, other):
        """Override the left shift operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The number of times to 
                shift.

        Returns:
            Integer: A new Integer instance representing the left shift.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "<<")
        
    #---------------------------------------------------------------------------
    ## Reverse left shift override.
    #  @param self number of times the number will be shifted.
    #  @param other Integer to be shifted.
    #  @return expression representing the shift.
    #
    #---------------------------------------------------------------------------
    def __rlshift__(self, other):
        """Override the reverse left shift operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the left shift.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "<<")
        
    #---------------------------------------------------------------------------
    ## Bitwise and logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __and__(self, other):
        """Override the bitwise AND operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand for the AND 
                operation.

        Returns:
            Integer: A new Integer instance representing the bitwise AND.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "&")

    #---------------------------------------------------------------------------
    ## Reverse bitwise and logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __rand__(self, other):
        """Override the reverse bitwise AND operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the bitwise AND.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "&")
        
    #---------------------------------------------------------------------------
    ## Bitwise or logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __or__(self, other):
        """Override the bitwise OR operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand for the OR 
                operation.

        Returns:
            Integer: A new Integer instance representing the bitwise OR.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "|")
        
    #---------------------------------------------------------------------------
    ## Reverse bitwise or logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __ror__(self, other):
        """Override the reverse bitwise OR operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the bitwise OR.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "|")

    #---------------------------------------------------------------------------
    ## Bitwise xor logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __xor__(self, other):
        """Override the bitwise XOR operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand for the XOR 
                operation.

        Returns:
            Integer: A new Integer instance representing the bitwise XOR.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "^")
        
    #---------------------------------------------------------------------------
    ## Reverse bitwise xor logic
    #  @param self first operator.
    #  @param other second operator.
    #  @return expression representing the bitwise and.
    #
    #---------------------------------------------------------------------------
    def __rxor__(self, other):
        """Override the reverse bitwise XOR operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the bitwise XOR.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "^")
        
    #---------------------------------------------------------------------------
    ## Less than override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __lt__(self, other):
        """Override the less-than operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, "<")
    
    #---------------------------------------------------------------------------
    ## Greater than override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __gt__(self, other):
        """Override the greater-than operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, ">")

    #---------------------------------------------------------------------------
    ## Less than equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __le__(self, other):
        """Override the less-than-or-equal operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, "<=")

    #---------------------------------------------------------------------------
    ## Greater than equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ge__(self, other):
        """Override the greater-than-or-equal operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, ">=")

    #---------------------------------------------------------------------------
    ## Equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __eq__(self, other):
        """Override the equality operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the equality.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, "==")

    #---------------------------------------------------------------------------
    ## Not equal override
    #  @param self Left operand object pointer.
    #  @param other Right operand. 
    #  @return expression representing the comparison.
    #
    #---------------------------------------------------------------------------
    def __ne__(self, other):
        """Override the inequality operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the inequality.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, "!=")
        
    #---------------------------------------------------------------------------
    ## negation override
    #  @param self Object pointer.
    #  @return expression representing negation.
    #
    #---------------------------------------------------------------------------
    def __neg__(self):
        """Override the unary negation operator for Integer objects.

        Returns:
            Integer: A new Integer instance representing the negated expression.
        """
        return unary(Integer, self, "-")
    
    #---------------------------------------------------------------------------
    ## abs override
    #  @param self Object pointer.
    #  @return expression representing absolute value.
    #
    #---------------------------------------------------------------------------
    def __abs__(self):
        """Override the abs() function for Integer objects.

        Returns:
            Integer: A new Integer instance representing the absolute value.
        """
        return Integer(f"abs({self})") 

    #---------------------------------------------------------------------------
    ## pos override
    #  @param self Object pointer.
    #  @return copy of the same object.
    #
    #---------------------------------------------------------------------------
    def __pos__(self):
        """Override the unary plus operator for Integer objects.

        Returns:
            Integer: A new Integer instance that is a copy of this object.
        """
        return unary(Integer, self, "+")

    #---------------------------------------------------------------------------
    ## invert override
    #  @param self Object pointer.
    #  @return expression representing bitwise not in all bits
    #
    #---------------------------------------------------------------------------
    def __invert__(self):
        """Override the bitwise inversion operator for Integer objects.

        Returns:
            Integer: A new Integer instance representing the bitwise NOT of the 
                operand.
        """
        return unary(Integer, self, "~")
        
    #---------------------------------------------------------------------------
    ## str override
    #  @param self Object pointer.
    #  @return string representing the expression
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        """Return the string representation of the Integer expression.

        Returns:
            str: The Integer expression as a string.
        """
        return self.value

        
#-------------------------------------------------------------------------------
## Integer variable class
#
#-------------------------------------------------------------------------------
class IntegerVar(Integer):
    """Class representing an Integer variable with additional operations."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param value string representing the value
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        """Initialize an IntegerVar instance.

        Args:
            value (str): A string representing the value.
        """
        checkType("value", value, str)
        super(IntegerVar, self).__init__(value)

    #---------------------------------------------------------------------------
    ## Increment
    #  @param self object pointer
    #  @return command representing the increment
    #
    #---------------------------------------------------------------------------
    def inc(self):
        """Generate a command to increment the IntegerVar.

        Returns:
            Cmd: A command representing the increment operation.
        """
        return Cmd(f"{self} = {self} + 1")  
        
    #---------------------------------------------------------------------------
    ## Decrement
    #  @param self object pointer
    #  @return command representing the decrement
    #
    #---------------------------------------------------------------------------
    def dec(self):
        """Generate a command to decrement the IntegerVar.

        Returns:
            Cmd: A command representing the decrement operation.
        """
        return Cmd(f"{self} = {self} - 1")    
                     
    #---------------------------------------------------------------------------
    ## Atribution
    #  @param self object pointer
    #  @param value A number representing the value
    #  @return Return a command representing the attribution to a variable
    #
    #---------------------------------------------------------------------------
    def eq(self, value):
        """Generate a command to assign a new value to the IntegerVar.

        Args:
            value (Integer, int, or convertible type): The value to assign.

        Returns:
            Cmd: A command representing the assignment.
        """
        value = parseInteger("value", value)
        return Cmd(f"{self} = {value}")        
    

#-------------------------------------------------------------------------------
## Real variable class
#
#-------------------------------------------------------------------------------
class RealVar(Real):
    """Class representing a Real variable with additional operations."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param value string representing the value
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        """Initialize a RealVar instance.

        Args:
            value (str): A string representing the value.
        """
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
        """Generate a command to assign a new value to the RealVar.

        Args:
            value (Real, float, int, or convertible type): The value to assign.

        Returns:
            Cmd: A command representing the assignment.
        """
        value = parseReal("value", value)
        return Cmd(f"{self} = {value}")     
        
        
#-------------------------------------------------------------------------------
## Boolean variable class
#
#-------------------------------------------------------------------------------
class BoolVar(Bool):
    """Class representing a Boolean variable with additional operations."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param value string representing the value
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        """Initialize a BoolVar instance.

        Args:
            value (str): A string representing the value.
        """
        checkType("value", value, str)
        super(BoolVar, self).__init__(value)

    #---------------------------------------------------------------------------
    ## Toggle
    #  @param self object pointer
    #  @return  Return a command representing the state toggle
    #
    #---------------------------------------------------------------------------
    def toggle(self):
        """Generate a command to toggle the Boolean variable.

        Returns:
            Cmd: A command representing the toggle operation.
        """
        return Cmd(f"{self} = !{self}")  
        
    #---------------------------------------------------------------------------
    ## Atribution
    #  @param self object pointer
    #  @param value A number representing the value
    #  @return Return a command representing the attribution to a variable
    #
    #---------------------------------------------------------------------------
    def eq(self, value):
        """Generate a command to assign a new value to the BoolVar.

        Args:
            value (Bool, bool, or convertible type): The value to assign.

        Returns:
            Cmd: A command representing the assignment.
        """
        value = parseBool("value", value)
        return Cmd(f"{self} = {value}") 
        
       
#-------------------------------------------------------------------------------
## Class of events
#
#-------------------------------------------------------------------------------
class Event():
    """Class representing an event in the system."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param value string representing the event
    #
    #---------------------------------------------------------------------------
    def __init__(self, value):
        """Initialize an Event instance.

        Args:
            value (str): A string representing the event.
        """
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
        """Override the logical OR operator for Event objects.

        Args:
            other (Event): Another Event instance.

        Returns:
            Event: A new Event instance representing the logical OR of the 
                events.
        """
        checkInstance("other", other, Event)
        return Event(f"{self} or {other}")

    #---------------------------------------------------------------------------
    ## string representation
    #  @param self object pointer
    #  @return The string representation of the Event
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        """Return the string representation of the Event.

        Returns:
            str: The event as a string.
        """
        return self.value
               
               
#-------------------------------------------------------------------------------
## Command class
#
#-------------------------------------------------------------------------------
class Cmd:
    """Class representing a command in the system."""
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param cmd command to be added to the va
    #
    #---------------------------------------------------------------------------
    def __init__(self, cmd):
        """Initialize a Cmd instance.

        Args:
            cmd (str): The command string.
        """
        checkType("cmd", cmd, str)
        self.cmd = cmd

    #---------------------------------------------------------------------------
    ## Return string representation
    #  @param self object pointer
    #  @return string representation
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        """Return the string representation of the command.

        Returns:
            str: The command as a string.
        """
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
        """Return the VA Verilog command with the specified padding.

        Args:
            padding (int): The number of tabs for right shift.

        Returns:
            str: The formatted Verilog command.
        """
        checkType("padding", padding, int)
        chunks = self.cmd.split("\n")
        result = '\n'.join([f"{'    '*padding}{l}" for l in chunks])
        result = f"{result};\n"
        return result


#-------------------------------------------------------------------------------
## Command List class
#
#-------------------------------------------------------------------------------
class CmdList(list, Cmd):
    """Command list class that combines list behavior with Cmd functionality."""
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param cmds commands to be added to the va
    #
    #---------------------------------------------------------------------------
    def __init__(self, *cmds):
        """Initialize a CmdList instance and append the provided commands.

        Args:
            *cmds: Variable number of commands to add.
        """
        super(CmdList, self).__init__()
        self.append(*cmds)
        
    #---------------------------------------------------------------------------
    ## Return string representation
    #  @param self object pointer
    #  @return string representation
    #
    #---------------------------------------------------------------------------
    def __str__(self):
        """Return a comma-separated string representation of the command list.

        Returns:
            str: The string representation.
        """
        return ", ".join([str(x) for x in self])
        
    #---------------------------------------------------------------------------
    ## Return a flat command list Fatten
    #  @param self object pointer
    #  @return flat command list. Only immediate CmdLists will be open.
    #
    #---------------------------------------------------------------------------
    def flat(self):
        """Return a flat list of commands, recursively flattening any CmdList 
        items.

        Returns:
            list: A flat list of commands.
        """
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
        """Override the append method to add commands with type checking.

        Args:
            *cmds: Variable number of commands to append.
        """
        i = 0
        for cmd in cmds:
            checkInstance(f"cmds[{i}]", cmd, Cmd)
            checkNotInstance(f"cmds[{i}]", cmd, WaitAnalogEvent)
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
        """Return the concatenated VA Verilog commands with the specified 
        padding.

        Args:
            padding (int): Number of indentation tabs.

        Returns:
            str: The formatted Verilog command string.
        """
        checkType("padding", padding, int)
        return "".join([f"{l.getVA(padding)}" for l in self])


#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to an analog event
#  @param header header of the block
#  @return pointer to a function that creates a block object
#
#-----------------------------------------------------------------------------
def block(header):
    """Return a function that creates a Block with the given header.

    Args:
        header (str): The header for the block.

    Returns:
        function: A function that accepts commands and returns a Block.
    """
    def func(*cmds):
        return Block(header, *cmds)
    return func
    
    
#-------------------------------------------------------------------------------
## Command Block Class
#
#-------------------------------------------------------------------------------
class Block(CmdList):
    """Command Block class for grouping commands under a header."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param header header of the command block
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, header, *cmds):
        """Initialize a Block instance with a header and commands.

        Args:
            header (str): Header of the block.
            *cmds: Variable number of commands or CmdLists.
        """
        checkType("header", header, str)
        self.header = header
        super(Block, self).__init__(*cmds)
        
    #---------------------------------------------------------------------------
    ## Return the header of a block command
    #  @param self object pointer
    #  @return header of the block 
    # 
    #---------------------------------------------------------------------------
    def getHeader(self):
        """Return the header of the block.

        Returns:
            str: The block header.
        """
        return self.header
                
    #---------------------------------------------------------------------------
    ## Return the VA verilog command
    #  @param self object pointer
    #  @param padding number of tabs by which the text will be right shifted
    #  @return verilog command
    #  
    #---------------------------------------------------------------------------
    def getVA(self, padding):
        """Return the formatted VA Verilog command for the block with padding.

        Args:
            padding (int): Number of indentation tabs.

        Returns:
            str: The formatted Verilog command string.
        """
        checkType("padding", padding, int)
        length = len(self.flat())
        if length > 1:
            result = (f"{'    '*padding}{self.header} begin\n"
                      f"{super(Block, self).getVA(padding + 1)}"
                      f"{'    '*padding}end\n")
        elif length == 1:
            result = (f"{'    '*padding}{self.header}\n"
                      f"{super(Block, self).getVA(padding + 1)}")     
        else:
            result = f"{'    '*padding}{self.header};\n"
        return result


#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to an analog event
#  @param event instance of the Event class representing the analog event
#  @return function pointer
#
#-------------------------------------------------------------------------------
def At(event):
    """Return a function that creates a WaitAnalogEvent for the given event.

    Args:
        event (Event): An Event instance representing the analog event.

    Returns:
        function: A function that accepts commands and returns a WaitAnalogEvent.
    """
    def func(*cmds):
        return WaitAnalogEvent(event, *cmds)
    return func
    
    
#-------------------------------------------------------------------------------
## Wait analog event class
#
#-------------------------------------------------------------------------------
class WaitAnalogEvent(Block):
    """Class representing a wait for an analog event."""
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param event Event to be waited for
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, event, *cmds):
        """Initialize a WaitAnalogEvent instance.

        Args:
            event (Event): The event to wait for.
            *cmds: Variable number of commands or CmdLists.
        """
        checkInstance("event", event, Event)
        super(WaitAnalogEvent, self).__init__(f'@( {event} )', *cmds)
        

#-------------------------------------------------------------------------------
## Cross Class
#
#-------------------------------------------------------------------------------
class Cross(Event):
    """Class representing a cross event."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param expr Real class or build-in real representing the expression
    #  @param edge It can be rising, falling or both
    #  @param *pars optional Real or build-in real parameters timeTol and expTol
    #         in this order
    #
    #---------------------------------------------------------------------------
    def __init__(self, expr, edge, *pars):
        """Initialize a Cross event instance.

        Args:
            expr (Real or numeric): The expression for the cross event.
            edge (str): The edge type ('rising', 'falling', or 'both').
            *pars: Optional parameters (timeTol and expTol).

        Raises:
            AssertionError: If an invalid edge value is provided or wrong number 
                of parameters.
        """
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        expr = parseReal("expr", expr)
        checkType("edge", edge, str)
        mapping = {'rising': '1', 'falling': '-1', 'both': '0'}  
        assert edge in mapping.keys(), "Wrong value for edge"
        params = [mapping[edge]]

        for par in pars:
            par = parseReal("timeTol or expTol", par)
            params.append(str(par))
        
        evnt = f"cross({expr}, {', '.join(params)})" 
        super(Cross, self).__init__(evnt)


#-------------------------------------------------------------------------------
## Above Class
#
#-------------------------------------------------------------------------------
class Above(Event):
    """Class representing an above event."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param expr Real class or build-in real representing the expression
    #  @param *pars optional Real or build-in real parameters timeTol and expTol
    #         in this order
    #
    #---------------------------------------------------------------------------
    def __init__(self, expr, *pars):
        """Initialize an Above event instance.

        Args:
            expr (Real or numeric): The expression for the above event.
            *pars: Optional parameters (timeTol and expTol).
        """
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        expr = parseReal("expr", expr)
        params = [str(expr)] 

        for par in pars:
            par = parseReal("timeTol or expTol", par)
            params.append(str(par))

        evnt = f"above({', '.join(params)})" 
        super(Above, self).__init__(evnt)


#-------------------------------------------------------------------------------
## Timer Class
#
#-------------------------------------------------------------------------------
class Timer(Event):
    """Class representing a timer event."""
    
    #----------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param startTime Real or build-in real representing the time tolerance
    #  @param *pars optional Real or build-in real parameters timeTol and expTol
    #         in this order
    #
    #----------------------------------------------------------------------------
    def __init__(self, startTime, *pars):
        """Initialize a Timer event instance.

        Args:
            startTime (Real or numeric): The start time for the timer.
            *pars: Optional parameters (period or timeTol, expTol).

        Raises:
            AssertionError: If wrong number of parameters is provided.
        """
        assert len(pars) >= 0 and len(pars) <= 2, "Wrong number of parameters"
        startTime = parseReal("startTime", startTime)
        params = [str(startTime)] 

        for par in pars:
            par = parseReal("period or timeTol", par)
            params.append(str(par))

        evnt = f"timer({', '.join(params)})" 
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
    """Unfold a variable number of simulation types into a comma-separated string.

    Args:
        *simTypes: Simulation type strings.

    Returns:
        str: A comma-separated string of simulation types enclosed in quotes.

    Raises:
        AssertionError: If any provided simulation type is not in anaTypes.
    """
    ans = []
    i = 1
    for simType in simTypes:
        assert simType in anaTypes, \
               f"simType[{i}] must be of of the following: {anaTypes}"
        i = i + 1
        ans.append(f'"{simType}"')
    return ", ".join(ans)


#-------------------------------------------------------------------------------
## InitialStep class
#
#-------------------------------------------------------------------------------
class InitialStep(Event):
    """Class representing an initial step event."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param *simTypes optional parameters representing the simulation type
    #
    #---------------------------------------------------------------------------
    def __init__(self, *simTypes):
        """Initialize an InitialStep event.

        Args:
            *simTypes: Optional simulation type parameters.
        """
        ans = "initial_step"
        simTypes = unfoldSimTypes(*simTypes)
        if simTypes != "":
            ans = f"{ans}({simTypes})"
        super(InitialStep, self).__init__(ans)
                                          

#-------------------------------------------------------------------------------
## FinalStep class
#
#-------------------------------------------------------------------------------
class FinalStep(Event):
    """Class representing a final step event."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param *simTypes optional parameters representing the simulation type
    #
    #---------------------------------------------------------------------------
    def __init__(self, *simTypes):
        """Initialize a FinalStep event.

        Args:
            *simTypes: Optional simulation type parameters.
        """
        ans = "final_step"
        simTypes = unfoldSimTypes(*simTypes)
        if simTypes != "":
            ans = f"{ans}({simTypes})"
        super(FinalStep, self).__init__(ans)
  
   
#-------------------------------------------------------------------------------
## Type of analysis
#  @param *simTypes optional parameters representing the simulation type
#  @return Bool expression representing the analysis type test
#
#-------------------------------------------------------------------------------
def analysis(*simTypes):
    """Return a Bool expression that tests for the specified analysis type(s).

    Args:
        *simTypes: One or more simulation type strings.

    Returns:
        Bool: A Bool expression representing the analysis test.

    Raises:
        Exception: If no simulation type is specified.
    """
    if simTypes == "":
        raise Exception("At least one simulation type must be specified")
    return Bool(f'analysis({unfoldSimTypes(*simTypes)})')


#-------------------------------------------------------------------------------
## ac stimulus
#  @param mag Real class or build-in real representing the magnitude
#  @param phase Real class or build-in representing the phase (default it 0)
#  @param simType string representing the simulation type (default is "ac")
#  @return Real expression representing the ac stimulus command
#
#-------------------------------------------------------------------------------
def acStim(mag, phase=0, simType="ac"):
    """Return a Real expression representing an AC stimulus command.

    Args:
        mag (Real or numeric): The magnitude.
        phase (Real or numeric, optional): The phase (default is 0).
        simType (str, optional): The simulation type (default is "ac").

    Returns:
        Real: A Real expression for the AC stimulus command.

    Raises:
        AssertionError: If simType is not in the list of allowed analysis types.
    """
    assert simType in anaTypes, \
           f"simType must be of of the following: {anaTypes}"
    mag = parseReal("mag", mag)
    phase = parseReal("phase", phase)
    return Real(f'ac_stim("{simType}", {mag}, {phase})')
    
                   
#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to an Repeat block
#  @param n Integer class or int representing the number of times the 
#         sequence must be repeated
#  @return pointer to a function that returns a RepeatLoop class
#
#-------------------------------------------------------------------------------
def Repeat(n):
    """Return a function that creates a RepeatLoop with the specified repeat count.

    Args:
        n (Integer, int, or convertible type): Number of times to repeat.

    Returns:
        function: A function that accepts commands and returns a RepeatLoop.
    """
    def func(*cmds):
        return RepeatLoop(n, *cmds)
    return func


#-------------------------------------------------------------------------------
## RepeatLoop class  
#
#-------------------------------------------------------------------------------
class RepeatLoop(Block):
    """Class representing a loop that repeats a block of commands."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param n Integer class or int representing the number of times the block 
    #         of commands must be repeated
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, n, *cmds):
        """Initialize a RepeatLoop instance.

        Args:
            n (Integer, int, or convertible type): The repeat count.
            *cmds: Variable number of commands or CmdLists.
        """
        n = parseInteger("n", n)
        self.n = n
        super(RepeatLoop, self).__init__(f"repeat( {n} )", *cmds)  
        
    #---------------------------------------------------------------------------
    ## Return the repeat count
    #  @param self object pointer
    #  @return Integer class representing the number of times the block of 
    #          commands will be repeated
    #
    #---------------------------------------------------------------------------
    def getN(self):
        """Return the repeat count.

        Returns:
            Integer: The number of repetitions.
        """
        return self.n
        

#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to a While loop 
#  @param cond Bool class or build-in bool representing the condition that must 
#         be satisfied in order repeat the sequence of commands in the block
#  @return pointer to a function that returns a WhileLoop class
# 
#-------------------------------------------------------------------------------
def While(cond):
    """Return a function that creates a WhileLoop with the given condition.

    Args:
        cond (Bool or bool): The condition for the while loop.

    Returns:
        function: A function that accepts commands and returns a WhileLoop.
    """
    def func(*cmds):
        return WhileLoop(cond, *cmds)
    return func

#-------------------------------------------------------------------------------
## WhileLoop class
#
#-------------------------------------------------------------------------------
class WhileLoop(Block):
    """Class representing a while loop block."""

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
        """Initialize a WhileLoop instance.

        Args:
            cond (Bool or bool): The condition to control the loop.
            *cmds: Variable number of commands or command lists to execute.
        """
        cond = parseBool("cond", cond)
        self.cond = cond
        super(WhileLoop, self).__init__(f"while( {cond} )", *cmds)  
        
    #---------------------------------------------------------------------------
    ## Return the while loop condition
    #  @param self object pointer
    #  @return Bool class representing the condition that must be satisfied in 
    #          order repeat the sequence of commands in the block
    #
    #---------------------------------------------------------------------------
    def getCond(self):
        """Return the loop condition.

        Returns:
            Bool: The condition controlling the while loop.
        """
        return self.cond   
    
    
#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to a ForLoop
#  @param start command executed at the beginning
#  @param cond condition that must be satisfied in order repeat the sequence of 
#         commands in the block
#  @param inc command executed at the end of each step
#  @return pointer to a function that returns a ForLoop class
#
#-------------------------------------------------------------------------------
def For(start, cond, inc):
    """Return a function that creates a ForLoop instance.

    Args:
        start (Cmd or CmdList): The initialization command.
        cond (Bool or bool): The loop condition.
        inc (Cmd or CmdList): The increment command.

    Returns:
        function: A function that accepts commands and returns a ForLoop.
    """
    def func(*cmds):
        return ForLoop(start, cond, inc, *cmds)
    return func
    
    
#-------------------------------------------------------------------------------
## ForLoop class
#
#-------------------------------------------------------------------------------
class ForLoop(Block):
    """Class representing a for loop block."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param start command executed at the beginning
    #  @param cond condition that must be satisfied in order repeat the sequence
    #         of commands in the block
    #  @param inc command executed at the end of each step
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, start, cond, inc, *cmds):
        """Initialize a ForLoop instance.

        Args:
            start (Cmd or CmdList): The initialization command.
            cond (Bool or bool): The loop condition.
            inc (Cmd or CmdList): The increment command.
            *cmds: Additional commands to execute inside the loop.
        """
        cond = parseBool("cond", cond)
        assert type(start) == Cmd or type(start) == CmdList, \
               (f"start must be Cmd or CmdList but a {type(start)} was given "
                 "instead")
        assert type(inc) == Cmd or type(inc) == CmdList, \
               (f"start must be Cmd or CmdList but a {type(inc)} was given "
                 "instead")
        head = f"for( {start}; {cond}; {inc} )"
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
        """Return the for loop condition.

        Returns:
            Bool: The condition controlling the for loop.
        """
        return self.cond
        
    #---------------------------------------------------------------------------
    ## Return the Forloop start
    #  @param self object pointer
    #  @return Cmd class representing the initial command run by the loop
    #
    #---------------------------------------------------------------------------
    def getStart(self):
        """Return the for loop's start command.

        Returns:
            Cmd or CmdList: The initialization command.
        """
        return self.start
        
    #---------------------------------------------------------------------------
    ## Return the Forloop increment
    #  @param self object pointer
    #  @return Cmd class representing the increment command run at each 
    #          iteration
    #
    #---------------------------------------------------------------------------
    def getInc(self):
        """Return the for loop's increment command.

        Returns:
            Cmd or CmdList: The increment command.
        """
        return self.inc   
        
        
#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to a Cond Class
#  @param cond condition that must be satisfied in order to run the sequence of 
#         commands in the block
#  @return pointer to a function that returns a Cmd class
#
#-------------------------------------------------------------------------------
def If(cond):
    """Return a function that creates a conditional block.

    Args:
        cond (Bool or bool): The condition for the 'if' structure.

    Returns:
        function: A function that accepts commands and returns a Cond instance.
    """
    def ifFunc(*cmds):
        ans = Cond(cond, *cmds)
        return ans
    return ifFunc


#-------------------------------------------------------------------------------
## Condition Class. It is used inside the function If in order to provide an If
#  and else structure
#
#-------------------------------------------------------------------------------
class Cond(Cmd):
    """Class representing a conditional (if-else) block."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param cond condition that must be satisfied in order to run the sequence 
    #         of commands in the block
    #  @param *cmds variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def __init__(self, cond, *cmds):
        """Initialize a Cond instance.

        Args:
            cond (Bool or bool): The condition for the 'if' branch.
            *cmds: Commands to execute when the condition is true.
        """
        cond = parseBool("cond", cond)
        trueHead  = f"if( {cond} )"
        falseHead = "else"
        self.cond = cond
        self.cmdDict = {True:Block(trueHead, *cmds), \
                        False:Block(falseHead)}

    #---------------------------------------------------------------------------
    ## Return the Cond condition
    #  @param self object pointer
    #  @return Bool class representing the condition that must be satisfied in 
    #          order to run the sequence of commands in the block
    #
    #---------------------------------------------------------------------------
    def getCond(self):
        """Return the condition for the if branch.

        Returns:
            Bool: The condition.
        """
        return self.cond
        
    #---------------------------------------------------------------------------
    ## Return the block of commands for a given state
    #  @param self object pointer
    #  @param state true or false
    #  @return block of commands for True and False conditions
    #
    #---------------------------------------------------------------------------
    def getBlock(self, state=True):
        """Return the command block corresponding to a state.

        Args:
            state (bool, optional): True for 'if', False for 'else'. 
                Defaults to True.

        Returns:
            Block: The command block for the given state.
        """
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
        """Append commands to the block corresponding to the given state.

        Args:
            state (bool): True for 'if' branch, False for 'else' branch.
            *cmds: Commands to append.
        """
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
        """Append commands to the 'else' branch.

        Args:
            *cmds: Commands to append.

        Returns:
            Cond: The current instance.
        """
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
        """Return the VA Verilog command string for the conditional block.

        Args:
            padding (int): Number of indentation tabs.

        Returns:
            str: The formatted Verilog command.
        """
        checkType("padding", padding, int)
        result = f"{self.cmdDict[True].getVA(padding)}" 
        if len(self.cmdDict[False]) > 0:
            result = f"{result}{self.cmdDict[False].getVA(padding)}"
        return result


#-------------------------------------------------------------------------------
## Returns the pointer to a function that add commands to a Block 
#  @param variable under test of the case structure
#  @return pointer to a function that returns a CaseClass
#  
#-------------------------------------------------------------------------------
def Case(test):
    """Return a function that creates a case structure.

    Args:
        test (Integer, Bool, or Real): The variable under test.

    Returns:
        function: A function that accepts command tuples and returns a CaseClass.
    """
    def caseFunc(*cmds):
        return CaseClass(test, *cmds)
    return caseFunc


#-------------------------------------------------------------------------------
## Condition Class. It is used by the function Case in order to provide the case
#  structure
#
#-------------------------------------------------------------------------------
class CaseClass(Cmd):
    """Class representing a case structure with multiple conditional branches."""

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self object pointer
    #  @param test Must be Integer, Bool, or Real
    #  @param *cmds variable number of tuples containing a condition and a 
    #         command
    #
    #---------------------------------------------------------------------------
    def __init__(self, test, *cmds):
        """Initialize a CaseClass instance.

        Args:
            test (Integer, Bool, or Real): The test expression.
            *cmds: Tuples where each tuple contains a condition and corresponding 
                commands.
        """
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
        """Return the list of command blocks for each case branch.

        Returns:
            list: A list of Block instances.
        """
        return self.cmds
                      
    #---------------------------------------------------------------------------
    ## Add command
    #  @param self object pointer
    #  @param *cmds variable number of tuples containing a condition and a 
    #         command
    #
    #---------------------------------------------------------------------------
    def append(self, *cmds):
        """Append tuples of condition and commands to the case structure.

        Args:
            *cmds: Tuples where the first element is the case condition 
                   (or None for default) followed by one or more commands.
        """
        i = 0
        for tup in cmds:
            assert type(tup) == tuple, f"cmds[{i}] must be tuple"
            assert len(tup) > 1, f"cmds[{i}] length must > 1"
            if not isinstance(tup[0], type(None)):
                if isinstance(self.test, Bool)  and \
                   isinstance(tup[0], (Bool, bool)):
                   test = parseBool(f"cmds[{i}][0]", tup[0])
                elif isinstance(self.test, Integer)  and \
                     isinstance(tup[0], (Integer, int)):
                   test = parseInteger(f"cmds[{i}][0]", tup[0])
                elif isinstance(self.test, Real)  and \
                     isinstance(tup[0], (Real, float, int)):
                   test = parseReal(f"cmds[{i}][0]", tup[0])
                else:
                    raise Exception( (f"cmds[{i}][0] must be compatible with "  
                          f"{type(self.test)} but a {type(tup[0])} was given "
                           "instead."))
                blockCmd = Block(f"{test}:")
            else:
                blockCmd = Block("default:")  
            j = 1
            for cmd in tup[1:]:
                checkInstance(f"cmds[{i}][{j}]", cmd, Cmd)
                checkNotInstance(f"cmds[{i}][{j}]", cmd, WaitAnalogEvent)
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
        """Return the VA Verilog command string for the case structure.

        Args:
            padding (int): Number of indentation tabs.

        Returns:
            str: The formatted Verilog command.
        """
        checkType("padding", padding, int)
        result = (f"{'    '*padding}case( {self.test} )\n"
                  f"{''.join([l.getVA(padding+1) for l in self.cmds])}"
                  f"{'    '*padding}endcase\n")
        return result


#-------------------------------------------------------------------------------
## Unfold variable number of parameters
#  @param *params variable number of parameters
#  @return string representing the parameters separated by comma
#
#-------------------------------------------------------------------------------
def unfoldParams(*params):
    """Unfold a variable number of parameters into a comma-separated string.

    Args:
        *params: Parameters to be unfolded.

    Returns:
        str: A string with the parameters separated by commas.
    """
    cmd = ""
    i = 0
    for param in params:
        param = parseNumber(f"param[i]", param)
        cmd = f"{cmd}, {param}"
        i = i + 1
    return cmd


#-------------------------------------------------------------------------------
## Strobe
#  @param msg message to be printed
#  @param *params variable number of parameters
#  @return Cmd representing the strobe
#
#-------------------------------------------------------------------------------
def Strobe(msg, *params):
    """Return a command representing a strobe operation.

    Args:
        msg (str): The message to be printed.
        *params: Additional parameters for the strobe.

    Returns:
        Cmd: A command for the strobe.
    """
    checkType("msg", msg, str)
    return Cmd(f'$strobe("{msg}"{unfoldParams(*params)})')


#-------------------------------------------------------------------------------
## Write
#  @param msg message to be printed
#  @param *params variable number of parameters
#  @return Cmd representing the Write
#
#-------------------------------------------------------------------------------
def Write(msg, *params):
    """Return a command representing a write operation.

    Args:
        msg (str): The message to be printed.
        *params: Additional parameters for the write.

    Returns:
        Cmd: A command for the write.
    """
    checkType("msg", msg, str)
    return Cmd(f'$write("{msg}"{unfoldParams(*params)})')


#-------------------------------------------------------------------------------
## Fopen
#  @param fileName name of the file
#  @return Integer representing the file descriptor
#
#-------------------------------------------------------------------------------
def Fopen(fileName):
    """Return an Integer representing the file descriptor from opening a file.

    Args:
        fileName (str): The name of the file.

    Returns:
        Integer: The file descriptor.
    """
    checkType("msg", fileName, str)
    return Integer(f'$fopen("{fileName}")') 


#-------------------------------------------------------------------------------
## Fclose
#  @param desc Integer or int representing the file descriptor
#  @return Cmd to close the file
#
#-------------------------------------------------------------------------------
def Fclose(desc):
    """Return a command to close a file.

    Args:
        desc (Integer or int): The file descriptor.

    Returns:
        Cmd: A command to close the file.
    """
    desc = parseInteger("desc", desc)
    return Cmd(f'$fclose({desc})') 


#-------------------------------------------------------------------------------
## Fstrobe
#  @param desc Integer or int representing the file descriptor
#  @param msg message to be written
#  @param *params variable number of parameters
#  @return Cmd representing the Fstrobe
#
#-------------------------------------------------------------------------------
def Fstrobe(desc, msg, *params):
    """Return a command representing a file strobe operation.

    Args:
        desc (Integer or int): The file descriptor.
        msg (str): The message to be written.
        *params: Additional parameters.

    Returns:
        Cmd: A command for the file strobe.
    """
    desc = parseInteger("desc", desc)
    checkType("msg", msg, str)
    return Cmd(f'$fstrobe({desc}, "{msg}"{unfoldParams(*params)})')


#-------------------------------------------------------------------------------
## Fwrite
#  @param desc Integer or int representing the file descriptor
#  @param msg message to be written
#  @param *params variable number of parameters
#  @return Cmd representing the FWrite
#
#-------------------------------------------------------------------------------
def Fwrite(desc, msg, *params):
    """Return a command representing a file write operation.

    Args:
        desc (Integer or int): The file descriptor.
        msg (str): The message to be written.
        *params: Additional parameters.

    Returns:
        Cmd: A command for the file write.
    """
    desc = parseInteger("desc", desc)
    checkType("msg", msg, str)
    return Cmd(f'$fwrite({desc}, "{msg}"{unfoldParams(*params)})')
                         

#-------------------------------------------------------------------------------
## discontinuity
#  @param degree Integer or int representing the degree of the derivative with
#         discontinuity
#  @return Cmd representing the discontinuity
#
#-------------------------------------------------------------------------------
def Discontinuity(degree=0):
    """Return a command representing a discontinuity in the derivative.

    Args:
        degree (Integer, int, or numeric, optional): The degree of discontinuity. 
            Defaults to 0.

    Returns:
        Cmd: A command for the discontinuity.
    """
    degree = parseInteger("degree", degree)
    return Cmd(f'$discontinuity({degree})')


#-------------------------------------------------------------------------------
## finish
#  @return Cmd representing the finish
#
#-------------------------------------------------------------------------------
def Finish():
    """Return a command representing finish.

    Returns:
        Cmd: A finish command.
    """
    return Cmd('$finish')


#-------------------------------------------------------------------------------
## error
#  @param msg message to be printed
#  @param *params variable number of parameters
#  @return Cmd representing the error
#
#-------------------------------------------------------------------------------
def Error(msg, *params):
    """Return a command representing an error message.

    Args:
        msg (str): The error message.
        *params: Additional parameters.

    Returns:
        Cmd: A command for the error.
    """
    checkType("msg", msg, str)
    return Cmd(f'$error("{msg}"{unfoldParams(*params)})')

#-------------------------------------------------------------------------------
## fatal
#  @param msg message to be printed
#  @param *params variable number of parameters
#  @return Cmd representing the error
#
#-------------------------------------------------------------------------------
def Fatal(msg, *params):
    """Return a command representing a fatal error.

    Args:
        msg (str): The error message.
        *params: Additional parameters.

    Returns:
        Cmd: A command for the fatal error.
    """
    checkType("msg", msg, str)
    return Cmd(f'$fatal(0, "{msg}"{unfoldParams(*params)})')

#-------------------------------------------------------------------------------
## bond step
#  @param step Real, float or int representing the step
#  @return Cmd representing the BondStep
#
#-------------------------------------------------------------------------------
def BoundStep(step):
    """Return a command representing a bond step.

    Args:
        step (Real, float, or int): The step value.

    Returns:
        Cmd: A command for the bond step.
    """
    step = parseReal("step", step)
    return Cmd(f'$bound_step({step})') 


#-------------------------------------------------------------------------------
## last time a signal crossed a threshold
#  @param signal Real, float or int representing the signal
#  @param threshold Real, float or int representing the threshold that must be 
#         crossed
#  @param edge It can be one the strings "rising", "falling" or "both"
#  @return Real class representing the last crossing.
#
#-------------------------------------------------------------------------------
def lastCrossing(signal, threshold, edge='both'):
    """Return a Real expression representing the last time a signal crossed a 
    threshold.

    Args:
        signal (Real, float, or int): The signal value.
        threshold (Real, float, or int): The threshold value.
        edge (str, optional): The edge type ("rising", "falling", or "both"). 
            Defaults to 'both'.

    Returns:
        Real: A Real expression for the last crossing.
    """
    signal = parseReal("signal", signal)
    threshold = parseReal("threshold", threshold)
    checkType("edge", edge, str)
    mapping = {'rising': '1', 'falling': '-1', 'both': '0'}
    assert edge in mapping.keys()
    cross = f"last_crossing({signal} - {threshold}, {mapping[edge]})"
    return Real(cross)


#-------------------------------------------------------------------------------
## random number generator
#  @param seed IntegerVar with the seed
#  @return random Integer
#
#-------------------------------------------------------------------------------
def random(seed):
    """Return a random Integer generated using the given seed.

    Args:
        seed (IntegerVar): The seed for the random generator.

    Returns:
        Integer: A random integer.
    """
    checkInstance("seed", seed, IntegerVar)
    return Integer(f'$random({seed})')


#-------------------------------------------------------------------------------
## Uniforme distribution random number generator
#  @param seed IntegerVar with the seed
#  @param start Integer or int representing the start of the range
#  @param end Integer or int representing the end of the range
#  @return random Integer
#
#-------------------------------------------------------------------------------        
def uDistInt(seed, start, end):
    """Return a random Integer from a uniform distribution.

    Args:
        seed (IntegerVar): The seed for the generator.
        start (Integer, int, or numeric): The start of the range.
        end (Integer, int, or numeric): The end of the range.

    Returns:
        Integer: A random integer from the specified range.
    """
    checkInstance("seed", seed, IntegerVar)
    start = parseInteger("start", start)
    end = parseInteger("end", end)
    return Integer(f'$dist_uniform({seed}, {start}, {end})')
            
                      
#-------------------------------------------------------------------------------
## Uniforme distribution random number generator
#  @param seed IntegerVar with the seed
#  @param start Real, float or int representing the start of the range
#  @param end Real, float or int representing the end of the range
#  @return random Real
#
#-------------------------------------------------------------------------------       
def uDistReal(seed, start, end):
    """Return a random Real from a uniform distribution.

    Args:
        seed (IntegerVar): The seed for the generator.
        start (Real, float, or int): The start of the range.
        end (Real, float, or int): The end of the range.

    Returns:
        Real: A random real number from the specified range.
    """
    checkInstance("seed", seed, IntegerVar)
    start = parseReal("start", start)
    end = parseReal("end", end)
    return Real(f'$rdist_uniform({seed}, {start}, {end})')


#-------------------------------------------------------------------------------
## Gaussian distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Integer or int representing the start of the range
#  @param std Integer or int representing the end of the range
#  @return random Integer
#
#-------------------------------------------------------------------------------   
def gaussDistInt(seed, mean, std):
    """Return a random Integer from a Gaussian distribution.

    Args:
        seed (IntegerVar): The seed for the generator.
        mean (Integer, int, or numeric): The mean value.
        std (Integer, int, or numeric): The standard deviation.

    Returns:
        Integer: A random integer from the Gaussian distribution.
    """
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    std = parseInteger("std", std)
    return Integer(f'$dist_normal({seed}, {mean}, {std})')
        
        
#-------------------------------------------------------------------------------
## Gaussian distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Real, float or int representing the start of the range
#  @param std Real, float or int representing the end of the range
#  @return random Real
#
#------------------------------------------------------------------------------- 
def gaussDistReal(seed, mean, std):
    """Return a random Real from a Gaussian distribution.

    Args:
        seed (IntegerVar): The seed for the generator.
        mean (Real, float, or int): The mean value.
        std (Real, float, or int): The standard deviation.

    Returns:
        Real: A random real number from the Gaussian distribution.
    """
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    std = parseReal("std", std)
    return Real(f'$rdist_normal({seed}, {mean}, {std})')

#-------------------------------------------------------------------------------
## Exponential distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Integer or int representing the start of the range
#  @return random Integer
#
#-------------------------------------------------------------------------------   
def expDistInt(seed, mean):
    """Return a random Integer from an exponential distribution.

    Args:
        seed (IntegerVar): The seed for the generator.
        mean (Integer, int, or numeric): The mean value.

    Returns:
        Integer: A random integer from the exponential distribution.
    """
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    return Integer(f'$dist_exponential({seed}, {mean})')


#-------------------------------------------------------------------------------
## Exponential distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Real, float or int representing the start of the range
#  @return random Real
#
#------------------------------------------------------------------------------- 
def expDistReal(seed, mean):
    """Return a random Real from an exponential distribution.

    Args:
        seed (IntegerVar): The seed for the generator.
        mean (Real, float, or int): The mean value.

    Returns:
        Real: A random real number from the exponential distribution.
    """
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    return Real(f'$rdist_exponential({seed}, {mean})')


#-------------------------------------------------------------------------------
## Poisson distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Integer or int representing the start of the range
#  @return random Integer
#
#-------------------------------------------------------------------------------  
def poissonDistInt(seed, mean):
    """Return a random Integer from a Poisson distribution.

    Args:
        seed (IntegerVar): The seed for the generator.
        mean (Integer, int, or numeric): The mean value.

    Returns:
        Integer: A random integer from the Poisson distribution.
    """
    checkInstance("seed", seed, IntegerVar)
    mean = parseInteger("mean", mean)
    return Integer(f'$dist_poisson({seed}, {mean})')


#-------------------------------------------------------------------------------
## Poisson distribution random number generator
#  @param seed IntegerVar with the seed
#  @param mean Real, float or int representing the start of the range
#  @return random Real
#
#-------------------------------------------------------------------------------
def poissonDistReal(seed, mean):
    """Return a random Real from a Poisson distribution.

    Args:
        seed (IntegerVar): The seed for the generator.
        mean (Real, float, or int): The mean value.

    Returns:
        Real: A random real number from the Poisson distribution.
    """
    checkInstance("seed", seed, IntegerVar)
    mean = parseReal("mean", mean)
    return Real(f'$rdist_poisson({seed}, {mean})')


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
    """Return a Real expression for the exponential of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing exp(x).
    """
    x = parseReal("x", x)
    return Real(f"exp({x})")


#-------------------------------------------------------------------------------
## Limited Exponential function
#  @param x Real, float or int input
#  @return Real expressing the limited exponential function
#
#-------------------------------------------------------------------------------
def limexp(x):
    """Return a Real expression for the limited exponential function of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing limexp(x).
    """
    x = parseReal("x", x)
    return Real(f"limexp({x})")


#-------------------------------------------------------------------------------
## Absolute Delay
#  @param x Real, float or int input
#  @param delay Real, float or int delay input
#  @return Real expressing the absolute delay function
#
#-------------------------------------------------------------------------------
def absDelay(x, delay):
    """Return a Real expression for the absolute delay function.

    Args:
        x (Real, float, or int): The input expression.
        delay (Real, float, or int): The delay value.

    Returns:
        Real: An expression representing absdelay(x, delay).
    """
    x = parseReal("x", x)
    delay = parseReal("delay", delay)
    return Real(f"absdelay({x}, {delay})")


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
    """ transition filter
    Args:
        x (Real, float, or int): The input value.
        delay (Real, float, or int, optional): The delay. Defaults to 0.
        riseTime (Real, float, or int, optional): Defaults to 1e-6.
        fallTime (Real, float, or int, optional): Defaults to 1e-6.

    Returns:
        Real: An expression representing the transition filter.
    """
    x = parseReal("x", x)
    delay = parseReal("delay", delay)
    riseTime = parseReal("riseTime", riseTime)
    fallTime = parseReal("fallTime", fallTime)
    return Real(f"transition({x}, {delay}, {riseTime}, {fallTime})") 


#-------------------------------------------------------------------------------
## smooth filter with hyperbolic tangent to avoid discontinuities. It goes from
#         0.0 to 1.0
#  @param x Real, float or int input
#  @param delay Real, float or int delay input
#  @param riseTime Real, float or int rise time from 5% to 95%
#  @param fallTime Real, float or int fall time from 5% to 95%
#  @return Real expressing the smooth filter
#
#-------------------------------------------------------------------------------
def smooth(x, 
           delay = 0, 
           riseTime = 1e-6, 
           fallTime = 1e-6):
    """Return a Real expression for a smooth filter using hyperbolic tangent.

    Args:
        x (Real, float, or int): The input value.
        delay (Real, float, or int, optional): The delay. Defaults to 0.
        riseTime (Real, float, or int, optional): The rise time (5%-95%). 
            Defaults to 1e-6.
        fallTime (Real, float, or int, optional): The fall time (5%-95%). 
            Defaults to 1e-6.

    Returns:
        Real: An expression representing the smooth filter.
    """
    checkBool("x", x)
    checkReal("delay", delay)
    checkReal("riseTime", riseTime)
    checkReal("fallTime", fallTime)
    gain = 6
    minLim = 0.05
    maxLim = 0.95
    cte = 2*m.tanh(gain/2)
    rfCte = gain/(m.atanh(cte*(maxLim - 0.5)) - m.atanh(cte*(minLim - 0.5)))
    riseTime = riseTime*rfCte
    fallTime = fallTime*rfCte
    x = transition(Real(x), delay, riseTime, fallTime)
    return tanh(gain*x - gain/2)/cte + 0.5
    
    
#-------------------------------------------------------------------------------
## slew filter
#  @param x Real, float or int input
#  @param riseSlope Real, float or int delay input
#  @param fallSlope Real, float or int delay input
#  @return Real expressing the slew filter
#
#-------------------------------------------------------------------------------
def slew(x, riseSlope = 10e-6, fallSlope = 10e-6):
    """Return a Real expression for the slew filter.

    Args:
        x (Real, float, or int): The input value.
        riseSlope (Real, float, or int, optional): The rise slope. 
            Defaults to 10e-6.
        fallSlope (Real, float, or int, optional): The fall slope. 
            Defaults to 10e-6.

    Returns:
        Real: An expression representing the slew filter.
    """
    x = parseReal("x", x)
    riseSlope = parseReal("riseSlope", riseSlope)
    fallSlope = parseReal("fallSlope", fallSlope)
    return Real(f"slew({x}, {riseSlope}, {fallSlope})")


#-------------------------------------------------------------------------------
## Differential function
#  @param x Real, float or int input
#  @return Real expressing the differential function
#
#-------------------------------------------------------------------------------
def ddt(x):
    """Return a Real expression representing the differential function of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing ddt(x).
    """
    x = parseReal("x", x)
    return Real(f"ddt({x})")
 
 
#-------------------------------------------------------------------------------
## Integral function
#  @param x Real, float or int input
#  @param start Real, float or int input
#  @return Real expressing the integral function
#
#-------------------------------------------------------------------------------   
def idt(x, start = Real(0)):
    """Return a Real expression representing the integral of x.

    Args:
        x (Real, float, or int): The input value.
        start (Real, float, or int, optional): The starting value. 
            Defaults to Real(0).

    Returns:
        Real: An expression representing idt(x, start).
    """
    x = parseReal("x", x)
    start = parseReal("start", start)
    return Real(f"idt({x}, {start})")


#-------------------------------------------------------------------------------
## Ceil function
#  @param x Real, float or int input
#  @return Integer expressing the ceil function
#
#-------------------------------------------------------------------------------
def ceil(x):
    """Return a Real expression representing the ceiling of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing ceil(x).
    """
    x = parseReal("x", x)
    return Real(f"ceil({x})")
      

#-------------------------------------------------------------------------------
## floor function
#  @param x Real, float or int input
#  @return Integer expressing the floor function
#
#-------------------------------------------------------------------------------  
def floor(x):
    """Return a Real expression representing the floor of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing floor(x).
    """
    x = parseReal("x", x)
    return Real(f"floor({x})")


#-------------------------------------------------------------------------------
## natural log function
#  @param x Real, float or int input
#  @return Real expressing the natural log function
#
#-------------------------------------------------------------------------------
def ln(x):
    """Return a Real expression representing the natural logarithm of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing ln(x).
    """
    x = parseReal("x", x)
    return Real(f"ln({x})")

#-------------------------------------------------------------------------------
## log function
#  @param x Real, float or int input
#  @return Real expressing the log function
#
#-------------------------------------------------------------------------------
def log(x):
    """Return a Real expression representing the log of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing log(x).
    """
    x = parseReal("x", x)
    return Real(f"log({x})")


#-------------------------------------------------------------------------------
## square root function
#  @param x Real, float or int input
#  @return Real expressing the square root function
#
#-------------------------------------------------------------------------------
def sqrt(x):
    """Return a Real expression representing the square root of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing sqrt(x).
    """
    x = parseReal("x", x)
    return Real(f"sqrt({x})")


#-------------------------------------------------------------------------------
## sin function
#  @param x Real, float or int angle in radians
#  @return Real expressing the sin function
#
#-------------------------------------------------------------------------------
def sin(x):
    """Return a Real expression representing the sine of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing sin(x).
    """
    x = parseReal("x", x)
    return Real(f"sin({x})")


#-------------------------------------------------------------------------------
## cos function
#  @param x Real, float or int angle in radians
#  @return Real expressing the cos function
#
#-------------------------------------------------------------------------------
def cos(x):
    """Return a Real expression representing the cosine of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing cos(x).
    """
    x = parseReal("x", x)
    return Real(f"cos({x})")


#-------------------------------------------------------------------------------
## tan function
#  @param x Real, float or int angle in radians
#  @return Real expressing the tan function
#
#-------------------------------------------------------------------------------
def tan(x):
    """Return a Real expression representing the tangent of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing tan(x).
    """
    x = parseReal("x", x)
    return Real(f"tan({x})")


#-------------------------------------------------------------------------------
## arc sin function
#  @param x Real, float or int angle input
#  @return Real expressing the arc sin function in radians
#
#-------------------------------------------------------------------------------
def asin(x):
    """Return a Real expression representing the arcsine of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing asin(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"asin({x})")


#-------------------------------------------------------------------------------
## arc cos function
#  @param x Real, float or int angle input
#  @return Real expressing the arc cos function in radians
#
#-------------------------------------------------------------------------------
def acos(x):
    """Return a Real expression representing the arccosine of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing acos(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"acos({x})")


#-------------------------------------------------------------------------------
## arc tan function
#  @param x Real, float or int angle input
#  @return Real expressing the arc tan function in radians
#
#-------------------------------------------------------------------------------
def atan(x):
    """Return a Real expression representing the arctangent of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing atan(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"atan({x})")


#-------------------------------------------------------------------------------
## arc tanh2 function. Equivalent to atan(x/y)
#  @param x Real, float or int angle input
#  @param x Real, float or int angle input
#  @return Real expressing the arc tan function in radians
#
#-------------------------------------------------------------------------------
def atan2(x, y):
    """Return a Real expression representing the two-argument arctangent.

    Args:
        x (Real, float, or int): The numerator.
        y (Real, float, or int): The denominator.

    Returns:
        Real: An expression representing atan2(x, y) in radians.
    """
    x = parseReal("x", x)
    y = parseReal("y", y)
    return Real(f"atan2({x}, {y})")


#-------------------------------------------------------------------------------
## hypot function. Equivalent to sqrt(x*x + y*y)
#  @param x Real, float or int angle input
#  @param x Real, float or int angle input
#  @return Real expressing the hypot function
#
#-------------------------------------------------------------------------------
def hypot(x, y):
    """Return a Real expression representing the hypotenuse of x and y.

    Args:
        x (Real, float, or int): The first value.
        y (Real, float, or int): The second value.

    Returns:
        Real: An expression representing hypot(x, y) (i.e. sqrt(x*x + y*y)).
    """
    x = parseReal("x", x)
    y = parseReal("y", y)
    return Real(f"hypot({x}, {y})")


#-------------------------------------------------------------------------------
## sinh function
#  @param x Real, float or int angle in radians
#  @return Real expressing the sinh function
#
#-------------------------------------------------------------------------------
def sinh(x):
    """Return a Real expression representing the hyperbolic sine of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing sinh(x).
    """
    x = parseReal("x", x)
    return Real(f"sinh({x})")


#-------------------------------------------------------------------------------
## cosh function
#  @param x Real, float or int angle in radians
#  @return Real expressing the cosh function
#
#-------------------------------------------------------------------------------
def cosh(x):
    """Return a Real expression representing the hyperbolic cosine of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing cosh(x).
    """
    x = parseReal("x", x)
    return Real(f"cosh({x})")


#-------------------------------------------------------------------------------
## tanh function
#  @param x Real, float or int angle in radians
#  @return Real expressing the tanh function
#
#-------------------------------------------------------------------------------
def tanh(x):
    """Return a Real expression representing the hyperbolic tangent of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing tanh(x).
    """
    x = parseReal("x", x)
    return Real(f"tanh({x})")


#-------------------------------------------------------------------------------
## arc sinh function
#  @param x Real, float or int angle input
#  @return Real expressing the arc sinh function in radians
#
#-------------------------------------------------------------------------------
def asinh(x):
    """Return a Real expression representing the inverse hyperbolic sine of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing asinh(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"asinh({x})")


#-------------------------------------------------------------------------------
## arc cosh function
#  @param x Real, float or int angle input
#  @return Real expressing the arc cosh function in radians
#
#-------------------------------------------------------------------------------
def acosh(x):
    """Return a Real expression representing the inverse hyperbolic cosine of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing acosh(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"acosh({x})")


#-------------------------------------------------------------------------------
## arc tanh function
#  @param x Real, float or int angle input
#  @return Real expressing the arc tanh function in radians
#
#-------------------------------------------------------------------------------
def atanh(x):
    """Return a Real expression representing the inverse hyperbolic tangent of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing atanh(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"atanh({x})")


#-------------------------------------------------------------------------------
## Class of Electrical signals
#
#-------------------------------------------------------------------------------
class Electrical():
    """Class representing an electrical signal with voltage and current."""

    #---------------------------------------------------------------------------
    ## constructor
    #  @param self The object pointer.
    #  @param name string representing the name of the Electrical signal
    # 
    #---------------------------------------------------------------------------
    def __init__(self, name):
        """Initialize an Electrical signal.

        Args:
            name (str): The name of the electrical signal.
        """
        checkType("name", name, str)
        self.name = name
        self.v = Real(f"V({name})") 
        self.i = Real(f"I({name})") 
        
    #---------------------------------------------------------------------------
    ## Return Electrical name
    #  @param self The object pointer.
    #  @return string representing the name of the signal
    # 
    #---------------------------------------------------------------------------
    def getName(self):
        """Return the name of the electrical signal.

        Returns:
            str: The signal's name.
        """
        return self.name

    #---------------------------------------------------------------------------
    ## Return a command representing voltage contribution
    #  @param self The object pointer.
    #  @param value Real, float or int representing the value of the contribution
    #  @return a Cmd representing the voltage contribution 
    # 
    #---------------------------------------------------------------------------
    def vCont(self, value):
        """Return a command for a voltage contribution.

        Args:
            value (Real, float, or int): The contribution value.

        Returns:
            Cmd: A command representing the voltage contribution.
        """
        value = parseReal("value", value)
        return Cmd(f'V({self.name}) <+ {value}')

    #---------------------------------------------------------------------------
    ## Return a command representing current contribution
    #  @param self The object pointer.
    #  @param value Real, float or int representing the value of the contribution
    #  @return a Cmd representing the current contribution 
    # 
    #---------------------------------------------------------------------------
    def iCont(self, value):
        """Return a command for a current contribution.

        Args:
            value (Real, float, or int): The contribution value.

        Returns:
            Cmd: A command representing the current contribution.
        """
        value = parseReal("value", value)
        return Cmd(f'I({self.name}) <+ {value}')

    #---------------------------------------------------------------------------
    ## Return a command representing voltage attribution
    #  @param self The object pointer.
    #  @param value Real, float or int representing the value of the attribution
    #  @return a Cmd representing the voltage attribution
    # 
    #---------------------------------------------------------------------------
    def vAttr(self, value):
        """Return a command for a voltage attribution.

        Args:
            value (Real, float, or int): The attribution value.

        Returns:
            Cmd: A command representing the voltage attribution.
        """
        value = parseReal("value", value)
        return Cmd(f'V({self.name}) = {value}')

    #---------------------------------------------------------------------------
    ## Return a command representing current attribution
    #  @param self The object pointer.
    #  @param value Real, float or int representing the value of the attribution
    #  @return a Cmd representing the current attribution
    # 
    #---------------------------------------------------------------------------
    def iAttr(self, value):
        """Return a command for a current attribution.

        Args:
            value (Real, float, or int): The attribution value.

        Returns:
            Cmd: A command representing the current attribution.
        """
        value = parseReal("value", value)
        return Cmd(f'I({self.name}) = {value}')

    #---------------------------------------------------------------------------
    ## Return a command representing voltage indirect assignment (Voltage that
    #  makes value true)
    #  @param self The object pointer.
    #  @param value Bool or bool condition
    #  @return a Cmd representing the voltage indirect assignment 
    #
    #---------------------------------------------------------------------------
    def vInd(self, value):
        """Return a command for a voltage indirect assignment.

        Args:
            value (Bool or bool): The condition for the assignment.

        Returns:
            Cmd: A command representing the voltage indirect assignment.
        """
        value = parseBool("value", value)
        return Cmd(f'V({self.name}) : {value}')

    #---------------------------------------------------------------------------
    ## Return a command representing current indirect assignment (Current that
    #  makes value true)
    #  @param self The object pointer.
    #  @param value Bool or bool condition
    #  @return a Cmd representing the current indirect assignment 
    #
    #---------------------------------------------------------------------------
    def iInd(self, value):
        """Return a command for a current indirect assignment.

        Args:
            value (Bool or bool): The condition for the assignment.

        Returns:
            Cmd: A command representing the current indirect assignment.
        """
        value = parseBool("value", value)
        return Cmd(f'I({self.name}) : {value}')
 

#-------------------------------------------------------------------------------
## Branch class
#
#-------------------------------------------------------------------------------
class Branch(Electrical):
    """Class representing a branch connecting two electrical signals."""

    #---------------------------------------------------------------------------
    ## constructor
    #  @param self The object pointer.
    #  @param node1 Electrical signal representing the first node
    #  @param node2 Electrical signal representing the second node
    #
    #---------------------------------------------------------------------------
    def __init__(self, node1, node2):
        """Initialize a Branch instance connecting two nodes.

        Args:
            node1 (Electrical): The first node.
            node2 (Electrical): The second node.
        """
        checkInstance("node1", node1, Electrical)
        checkInstance("node2", node2, Electrical)
        checkNotInstance("node1", node1, Branch)
        checkNotInstance("node2", node2, Branch)
        super(Branch, self).__init__(f"{node1.getName()}, {node2.getName()}")


#-------------------------------------------------------------------------------
## verilogA class
#
#-------------------------------------------------------------------------------
class Module:
    """Class representing a Verilog-A module."""

    #---------------------------------------------------------------------------
    ## constructor
    #  @param self The object pointer.
    #  @param node1 Electrical signal representing the first node
    #  @param moduleName name of the module (the first word after module in the 
    #         va)
    #  @param ignoreHiddenStates ignore hiddel state pragma will be added if True
    #
    #---------------------------------------------------------------------------
    def __init__(self, moduleName, ignoreHiddenStates = False):
        """Initialize a Module instance.

        Args:
            moduleName (str): The module's name.
            ignoreHiddenStates (bool): Pragma will be added if True
        """
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
        self.ignoreHiddenStates = ignoreHiddenStates 

    #---------------------------------------------------------------------------
    ## return module name
    #  @param self The object pointer
    #  @return string representing the name of the module
    #
    #---------------------------------------------------------------------------
    def getModuleName(self):
        """Return the module's name.

        Returns:
            str: The module name.
        """
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
        """Fix or generate a unique name in the module's namespace.

        Args:
            name (str): The proposed name.

        Returns:
            str: A valid, unique name.
        """
        checkType("name", name, str)
        if name == "":
            self.nameCount = self.nameCount + 1
            name = f"_${self.nameCount}"
        assert re.match(r"[_a-zA-Z][_a-zA-Z$0-9]*", name), \
               f"{name} isn't a valid verilogA identifier"
        assert not name in self.nameSpace, f"{name} is already taken"
        self.nameSpace.append(name)
        return name

    #---------------------------------------------------------------------------
    ## Add variable to the module
    #  @param self The object pointer. 
    #  @param vType it can be Integer, Bool or Real
    #  @param name string representing the name of the variable in the verilogA
    #  @return RealVar, IntegerVar or BoolVar depending on the vType
    #   
    #---------------------------------------------------------------------------
    def var(self, vType = Integer, name = ""):
        """Add a variable to the module.

        Args:
            vType (type, optional): The variable type (Integer, Bool, or Real). 
                Defaults to Integer.
            name (str, optional): The variable's name. Defaults to "".

        Returns:
            An instance of IntegerVar, BoolVar, or RealVar.
        """
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
            raise TypeError( (f"vType be Integer, Real, or Bool but a {vType}"
                               " was given") ) 
        self.variables.append((name, vType)) 
        return ans

    #---------------------------------------------------------------------------
    ## Add parameter to the module
    #  @param self The object pointer. 
    #  @param value Initial value. It can be Real, Integer, int or float.
    #  @param name string representing the name of the parameter in the verilogA
    #  @return RealVar or IntegerVar depending on the initial value
    #
    #---------------------------------------------------------------------------
    def par(self, value, name):
        """Add a parameter to the module.

        Args:
            value (Real, Integer, int, or float): The parameter's initial value.
            name (str): The parameter's name.

        Returns:
            RealVar or IntegerVar: The parameter variable.
        """
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
            raise TypeError( ( "value must be Integer or Real, but a"
                              f"{type(value)} was given" ) ) 
        self.parameters.append((name, pType, str(value))) 
        return ans

    #---------------------------------------------------------------------------
    ## Add commands to the analog block
    #  @param self The object pointer.
    #  @param *args variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def analog(self, *args):
        """Add commands to the analog block.

        Args:
            *args: Variable number of commands.
        """
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd), \
                   (f"cmd[{i}] must be an instance of Cmd and but a {type(arg)}"
                    f" was given instead")
            i = i + 1
            self.cmds.append(arg)

    #---------------------------------------------------------------------------
    ## Add commands to beginning of the analog block
    #  @param self The object pointer.
    #  @param *args variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def beginningAnalog(self, *args):
        """Add commands to the beginning of the analog block.

        Args:
            *args: Variable number of commands.
        """
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd), \
                   (f"cmd[{i}] must be an instance of Cmd and but a {type(arg)}"
                    f" was given instead")
            i = i + 1
            self.beginningCmds.append(arg)

    #---------------------------------------------------------------------------
    ## Add commands to the end of the analog block
    #  @param self The object pointer.
    #  @param *args variable number of Cmd or CmdList to be added 
    #
    #---------------------------------------------------------------------------
    def endAnalog(self, *args):
        """Add commands to the end of the analog block.

        Args:
            *args: Variable number of commands.
        """
        i = 1
        for arg in args:
            assert isinstance(arg, Cmd), \
                   (f"cmd[{i}] must be an instance of Cmd and but a {type(arg)}"
                    f" was given instead")
            i = i + 1
            self.endCmds.append(arg)

    #---------------------------------------------------------------------------
    ## Add node
    #  @param self The object pointer.
    #  @param name string representing the name of the Electrical signal
    #  @param width int representing the width of the Electrical signal
    #  @param direction direction of the signal. It can be one of the strings 
    #         "internal", "input", "output", or "inout"
    #  @return string with the name of the node
    #
    #---------------------------------------------------------------------------
    def addNode(self, name, width, direction):
        """Add a node to the module.

        Args:
            name (str): The node name.
            width (int): The node width (must be > 0).
            direction (str): The node direction ("internal", "input", "output", or "inout").

        Returns:
            str: The unique node name.
        """
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
    ## Return Electrical class
    #  @param self The object pointer.
    #  @param name string representing the name of the Electrical signal
    #  @param width int representing the width of the Electrical signal
    #  @param direction direction of the signal. It can be one of the strings 
    #         "internal", "input", "output", or "inout"
    #  @return list of Electrical classes or an Electrical class depending on 
    #          the width
    #
    #---------------------------------------------------------------------------
    def electrical(self, name = "", width = 1, direction = "internal"):
        """Return an Electrical signal or a vector of Electrical signals.

        Args:
            name (str, optional): The base name for the signal. Defaults to "".
            width (int, optional): The width of the signal. Defaults to 1.
            direction (str, optional): The signal direction. Defaults to "internal".

        Returns:
            Electrical or list[Electrical]: The Electrical signal(s).
        """
        name = self.addNode(name, width, direction)
        if width == 1:
            return Electrical(name)
        else:
            vector = list()
            for i in range(0, width):
                vector.append(Electrical(f"{name}[{i}]"))
            return vector

    #---------------------------------------------------------------------------
    ## Return the VA verilog code
    #  @param self The object pointer.
    #  @return string with the verilogA code
    #
    #---------------------------------------------------------------------------
    def getVA(self):
        """Return the complete Verilog-A code for the module.

        Returns:
            str: The generated Verilog-A code.
        """
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
        if self.ignoreHiddenStates:
            result = result + "(*ignore_hidden_state*)\n"
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
        # Print all Electrical
        #-----------------------------------------------------------------------
        if len(self.nodes) > 0:
            result = result + '\n' + blockComment(0, "Disciplines")
        for node in self.nodes:
            result = result + "electrical "
            if node[1] > 1:
                result = result + "[" + str(int(node[1])-1) + ":0] " 
            result = result + node[0] + ";\n"

        #-----------------------------------------------------------------------
        # Build in analog function
        #-----------------------------------------------------------------------
        result = result + '\n' + blockComment(0, "Build-in functions")
        result = result + ("analog function integer _rtoi;\n"
                           "input in;\n"
                           "real in;\n"
                           "begin\n"
                           "    _rtoi = floor(in + 0.5);\n"
                           "end\n"
                           "endfunction\n")

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
    
