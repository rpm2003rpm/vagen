"""Verilog-A type classes for expressions and variables."""

from vagen.exceptions import VagenTypeError, VagenValueError
from vagen.util import unary, binary
from vagen.validation import (
    parseInteger, 
    parseBool, 
    parseReal, 
    checkType,
    checkBool  
)
   
class Real():
    """Real operator class representing a Real expression."""

    def __init__(self, value):
        """Initialize a Real instance.

        Args:
            value (str, Real, Integer, Bool, or numeric): 
            The value to convert into a Real expression.
        """
        if isinstance(value, Bool):
            value = "{:s} ? {:e} : {:e}".format(str(value), 1,0)
        elif isinstance(value, (Real, Integer)):
            value = f"{value}"
        elif not isinstance(value, str):
            try:
                value = "{:e}".format(value)
            except (TypeError, ValueError):
                raise VagenTypeError(f"Can't convert {value} to Real")
        self.value = value
            
    def getValue(self):
        """Return the Real expression as a string.

        Returns:
            str: The expression stored in this Real instance.
        """
        return self.value
    
    def __add__(self, other):
        """Override the addition operator for Real objects.

        Args:
            other (Real, int, float): The operand to add.

        Returns:
            Real: A new Real instance representing the addition.
        """
        other = parseReal("other", other)
        return binary(Real, self, other, "+")

    def __sub__(self, other):
        """Override the subtraction operator for Real objects.

        Args:
            other (Real, int, float): The operand to subtract.

        Returns:
            Real: A new Real instance representing the subtraction.
        """
        other = parseReal("other", other)
        return binary(Real, self, other, "-")
        
    def __mul__(self, other):
        """Override the multiplication operator for Real objects.

        Args:
            other (Real, int, float): The operand to multiply.

        Returns:
            Real: A new Real instance representing the multiplication.
        """
        other = parseReal("other", other)
        return binary(Real, self, other, "*")

    def __truediv__(self, other):
        """Override the division operator for Real objects.

        Args:
            other (Real, int, float): The divisor.

        Returns:
            Real: A new Real instance representing the division.
        """
        other = parseReal("other", other)
        return binary(Real, self, other, "/")

    def __pow__(self, other):
        """Override the power operator for Real objects.

        Args:
            other (Real, int, float): The exponent.

        Returns:
            Real: A new Real instance representing the power operation.
        """
        other = parseReal("other", other)
        return Real(f'pow({self}, {other})')

    def __gt__(self, other):
        """Override the greater-than operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, ">")

    def __lt__(self, other):
        """Override the less-than operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, "<")

    def __le__(self, other):
        """Override the less-than-or-equal operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, "<=")

    def __ge__(self, other):
        """Override the greater-than-or-equal operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, ">=")

    def __eq__(self, other):
        """Override the equality operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the equality result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, "==")

    def __ne__(self, other):
        """Override the inequality operator for Real objects.

        Args:
            other (Real, int, float): The operand to compare.

        Returns:
            Bool: A Bool instance representing the inequality result.
        """
        other = parseReal("other", other)
        return binary(Bool, self, other, "!=")
        
    def __radd__(self, other):
        """Override the reverse addition operator for Real objects.

        Args:
            other (Real, int, float): The left-hand operand.

        Returns:
            Real: A new Real instance representing the addition.
        """
        other = parseReal("other", other)
        return binary(Real, other, self, "+")

    def __rsub__(self, other):
        """Override the reverse subtraction operator for Real objects.

        Args:
            other (Real, int, float): The left-hand operand.

        Returns:
            Real: A new Real instance representing the subtraction.
        """
        other = parseReal("other", other)
        return binary(Real, other, self, "-")

    def __rmul__(self, other):
        """Override the reverse multiplication operator for Real objects.

        Args:
            other (Real, int, float): The left-hand operand.

        Returns:
            Real: A new Real instance representing the multiplication.
        """
        other = parseReal("other", other)
        return binary(Real, other, self, "*")

    def __rtruediv__(self, other):
        """Override the reverse division operator for Real objects.

        Args:
            other (Real, int, float): The left-hand operand.

        Returns:
            Real: A new Real instance representing the division.
        """
        other = parseReal("other", other)
        return binary(Real, other, self, "/")

    def __rpow__(self, other):
        """Override the reverse power operator for Real objects.

        Args:
            other (Real, int, float): The base.

        Returns:
            Real: A new Real instance representing the power.
        """
        other = parseReal("other", other)
        return Real(f'pow({other}, {self})')
        
    def __neg__(self):
        """Override the unary negation operator for Real objects.

        Returns:
            Real: A new Real instance representing the negated expression.
        """
        return unary(Real, self, "-") 
    
    def __pos__(self):
        """Override the unary plus operator for Real objects.

        Returns:
            Real: A new Real instance that is a copy of this object.
        """
        return unary(Real, self, "+") 

    def __abs__(self):
        """Override the abs() function for Real objects.

        Returns:
            Real: A new Real instance representing the absolute value.
        """
        return Real(f"abs({self})") 

    def __str__(self):
        """Return the string representation of the Real expression.

        Returns:
            str: The Real expression as a string.
        """
        return self.value


class Bool():
    """Bool operator class representing a Boolean expression."""

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
            except (TypeError, ValueError):
                raise VagenTypeError(f"Can't convert {value} to Bool")
        self.value = value

    def getValue(self):
        """Return the Bool expression as a string.

        Returns:
            str: The expression stored in this Bool instance.
        """
        return self.value

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
                
    def __invert__(self):
        """Override the bitwise inversion operator for Bool objects.

        Returns:
            Bool: A new Bool instance representing the logical NOT of the 
                operand.
        """
        return unary(Bool, self, "!")
        
    def __str__(self):
        """Return the string representation of the Bool expression.

        Returns:
            str: The Bool expression as a string.
        """
        return self.value

    def __eq__(self, other):
        """Override the equality operator for Bool objects.

        Args:
            other (Bool or bool): The operand to compare.

        Returns:
            Bool: A new Bool instance representing the equality result.
        """
        other = parseBool("other", other)
        return binary(Bool, self, other, "==") 

    def __ne__(self, other):
        """Override the inequality operator for Bool objects.

        Args:
            other (Bool or bool): The operand to compare.

        Returns:
            Bool: A new Bool instance representing the inequality result.
        """
        other = parseBool("other", other)
        return binary(Bool, self, other, "!=")
        
        
class Integer():
    """Integer operator class representing an Integer expression."""

    def __init__(self, value):
        """Initialize an Integer instance.

        Args:
            value (str, Integer, Real, Bool, or convertible type): The value to 
                convert into an Integer expression.
        """
        if isinstance(value, Bool):
            value = f"{value} ? 1 : 0"
        elif isinstance(value, Real):
            value = f"_rtoi({value})"
        elif isinstance(value, Integer):
            value = f"{value}"            
        elif not isinstance(value, str):
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise VagenTypeError(f"Can't convert {value} to Integer")
            if not (-2147483648 <= value <= 2147483647):
                raise VagenValueError(
                    f"Can't convert {value} to integer, because it is outside of"
                    " the range [-2147483648, 2147483647]"
                ) 
        self.value = f"{value}"
        
    def getValue(self):
        """Return the Integer expression as a string.

        Returns:
            str: The expression stored in this Integer instance.
        """
        return self.value

    def __add__(self, other):
        """Override the addition operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to add.

        Returns:
            Integer: A new Integer instance representing the addition.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "+")
        
    def __radd__(self, other):
        """Override the reverse addition operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the addition.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "+")
        
    def __sub__(self, other):
        """Override the subtraction operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to subtract.

        Returns:
            Integer: A new Integer instance representing the subtraction.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "-")
        
    def __rsub__(self, other):
        """Override the reverse subtraction operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the subtraction.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "-")

    def __mul__(self, other):
        """Override the multiplication operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to multiply.

        Returns:
            Integer: A new Integer instance representing the multiplication.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "*")
        
    def __rmul__(self, other):
        """Override the reverse multiplication operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the multiplication.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "*")

    def __truediv__(self, other):
        """Override the division operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The divisor.

        Returns:
            Integer: A new Integer instance representing the division.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "/")

    def __rtruediv__(self, other):
        """Override the reverse division operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the division.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "/")
        
    def __mod__(self, other):
        """Override the modulus operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The divisor.

        Returns:
            Integer: A new Integer instance representing the modulus.
        """
        other = parseInteger("other", other)
        return binary(Integer, self, other, "%")
        
    def __rmod__(self, other):
        """Override the reverse modulus operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the modulus.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "%")

    def __pow__(self, other):
        """Override the power operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The exponent.

        Returns:
            Integer: A new Integer instance representing the power operation.
        """
        other = parseInteger("other", other)
        return Integer(f'_rtoi(pow({self}, {other}))')
        
    def __rpow__(self, other):
        """Override the reverse power operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The base.

        Returns:
            Integer: A new Integer instance representing the power operation.
        """
        other = parseInteger("other", other)
        return Integer(f'_rtoi(pow({other}, {self}))')
        
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

    def __rrshift__(self, other):
        """Override the reverse right shift operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the right shift.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, ">>")
        
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
        
    def __rlshift__(self, other):
        """Override the reverse left shift operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the left shift.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "<<")
        
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

    def __rand__(self, other):
        """Override the reverse bitwise AND operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the bitwise AND.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "&")
        
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
        
    def __ror__(self, other):
        """Override the reverse bitwise OR operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the bitwise OR.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "|")

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
        
    def __rxor__(self, other):
        """Override the reverse bitwise XOR operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The left-hand operand.

        Returns:
            Integer: A new Integer instance representing the bitwise XOR.
        """
        other = parseInteger("other", other)
        return binary(Integer, other, self, "^")
        
    def __lt__(self, other):
        """Override the less-than operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, "<")
    
    def __gt__(self, other):
        """Override the greater-than operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, ">")

    def __le__(self, other):
        """Override the less-than-or-equal operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, "<=")

    def __ge__(self, other):
        """Override the greater-than-or-equal operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the comparison.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, ">=")

    def __eq__(self, other):
        """Override the equality operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the equality.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, "==")

    def __ne__(self, other):
        """Override the inequality operator for Integer objects.

        Args:
            other (Integer, int, or convertible type): The operand to compare.

        Returns:
            Bool: A Bool instance representing the inequality.
        """
        other = parseInteger("other", other)
        return binary(Bool, self, other, "!=")
        
    def __neg__(self):
        """Override the unary negation operator for Integer objects.

        Returns:
            Integer: A new Integer instance representing the negated expression.
        """
        return unary(Integer, self, "-")
    
    def __abs__(self):
        """Override the abs() function for Integer objects.

        Returns:
            Integer: A new Integer instance representing the absolute value.
        """
        return Integer(f"abs({self})") 

    def __pos__(self):
        """Override the unary plus operator for Integer objects.

        Returns:
            Integer: A new Integer instance that is a copy of this object.
        """
        return unary(Integer, self, "+")

    def __invert__(self):
        """Override the bitwise inversion operator for Integer objects.

        Returns:
            Integer: A new Integer instance representing the bitwise NOT of the 
                operand.
        """
        return unary(Integer, self, "~")
        
    def __str__(self):
        """Return the string representation of the Integer expression.

        Returns:
            str: The Integer expression as a string.
        """
        return self.value

        
class IntegerVar(Integer):
    """Class representing an Integer variable with additional operations."""

    def __init__(self, value):
        """Initialize an IntegerVar instance.

        Args:
            value (str): A string representing the value.
        """
        checkType("value", value, str)
        super(IntegerVar, self).__init__(value)

    def inc(self):
        """Generate a command to increment the IntegerVar.

        Returns:
            Cmd: A command representing the increment operation.
        """
        from vagen.commands import Cmd
        return Cmd(f"{self} = {self} + 1")  
        
    def dec(self):
        """Generate a command to decrement the IntegerVar.

        Returns:
            Cmd: A command representing the decrement operation.
        """
        from vagen.commands import Cmd
        return Cmd(f"{self} = {self} - 1")    
                     
    def eq(self, value):
        """Generate a command to assign a new value to the IntegerVar.

        Args:
            value (Integer, int, or convertible type): The value to assign.

        Returns:
            Cmd: A command representing the assignment.
        """
        from vagen.commands import Cmd
        value = parseInteger("value", value)
        return Cmd(f"{self} = {value}")        
    

class RealVar(Real):
    """Class representing a Real variable with additional operations."""

    def __init__(self, value):
        """Initialize a RealVar instance.

        Args:
            value (str): A string representing the value.
        """
        checkType("value", value, str)
        super(RealVar, self).__init__(value)

    def eq(self, value):
        """Generate a command to assign a new value to the RealVar.

        Args:
            value (Real, float, int, or convertible type): The value to assign.

        Returns:
            Cmd: A command representing the assignment.
        """
        from vagen.commands import Cmd
        value = parseReal("value", value)
        return Cmd(f"{self} = {value}")     
        
        
class BoolVar(Bool):
    """Class representing a Boolean variable with additional operations."""

    def __init__(self, value):
        """Initialize a BoolVar instance.

        Args:
            value (str): A string representing the value.
        """
        checkType("value", value, str)
        super(BoolVar, self).__init__(value)

    def toggle(self):
        """Generate a command to toggle the Boolean variable.

        Returns:
            Cmd: A command representing the toggle operation.
        """
        from vagen.commands import Cmd
        return Cmd(f"{self} = !{self}")  
        
    def eq(self, value):
        """Generate a command to assign a new value to the BoolVar.

        Args:
            value (Bool, bool, or convertible type): The value to assign.

        Returns:
            Cmd: A command representing the assignment.
        """
        from vagen.commands import Cmd
        value = parseBool("value", value)
        return Cmd(f"{self} = {value}")
