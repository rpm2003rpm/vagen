"""Type and value validation helpers for Verilog-A modeling."""

from vagen.exceptions import VagenTypeError

def checkType(param, var, Type):
    """Check if the type of variable matches the specified Type.

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.
        Type (type): Expected type.

    Raises:
        VagenTypeError: If the type does not match.
    """
    if not isinstance(var, Type):
        raise VagenTypeError(
            f"{param} must be a {Type} but a {type(var)} was given instead")


def checkInstance(param, var, Type):
    """Check if the variable is an instance of the specified Type.

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.
        Type (type): Expected type.

    Returns:
        None; An AssertionError is raised.
    """
    if not isinstance(var, Type):
        raise VagenTypeError(
            f"{param} must be an instance of {Type} but a {type(var)} was given"
            " instead")


def checkNotInstance(param, var, Type):
    """Check that the variable is not an instance of the specified Type.

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.
        Type (type): Type that must not match.

    Returns:
        None; An AssertionError is raised.
    """
    if isinstance(var, Type):
        raise VagenTypeError(f"{param} can't be an instance of {Type}")
        
        
def checkReal(param, var):
    """Check if the variable is of type Real (or compatible with Real).

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.

    Returns:
        None; An AssertionError is raised.
    """
    from vagen.types import Real
    if not isinstance(var, (Real, float, int)):
        raise VagenTypeError(
            f"{param} must be an instance of 'Real', 'float', 'int', or 'bool'"
            f" but a '{type(var).__name__}' was given instead")
            
def checkInteger(param, var):
    """Check if the variable is of type Integer (or compatible with Integer).

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.

    Returns:
        None; An AssertionError is raised.
    """
    from vagen.types import Integer
    if not isinstance(var, (Integer, int)):
        raise VagenTypeError(
            f"{param} must be an instance of 'Integer', 'int', or 'bool' but a "
            f"'{type(var).__name__}' was given instead")
            
def checkBool(param, var):
    """Check if the variable is of type Bool (or compatible with Bool).

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.

    Returns:
        None; An AssertionError is raised.
    """
    from vagen.types import Bool
    if not isinstance(var, (Bool, bool)):
        raise VagenTypeError(
            f"{param} must be an instance of 'Bool' or 'bool' but a "
            f"'{type(var).__name__}' was given instead")
           
           
def checkNumber(param, var):
    """Check if the variable is a numeric type (Real, Integer, or Bool).

    Args:
        param (str): Name of the variable.
        var (any): Variable to check.

    Returns:
        None; An AssertionError is raised.
    """
    from vagen.types import Real, Integer, Bool
    if not isinstance(var, (Real, Integer, Bool, float, int, bool)):
        raise VagenTypeError(
            f"{param} must be an instance of 'Bool', 'bool', 'Real', 'float', "
            f"'Integer' or 'int' but a '{type(var).__name__}' was given instead")
            
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
    from vagen.types import Real
    if isinstance(var, (Real, float, int)):
        return Real(var)
    else:
        raise VagenTypeError( (f"{param} must be an instance of 'Real', 'float', "
                          f"'int', or 'bool' but a '{type(var).__name__}' was "
                           "given instead") )

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
    from vagen.types import Integer
    if isinstance(var, (Integer, int)):
        return Integer(var)
    else:
        raise VagenTypeError( (f"{param} must be an instance of 'Integer', 'int', or"
                          f" 'bool' but a '{type(var).__name__}' was given "
                           "instead") )
                 
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
    from vagen.types import Bool
    if isinstance(var, (Bool, bool)):
        return Bool(var)
    else:
        raise VagenTypeError( (f"{param} must be an instance of 'Bool' or 'bool' "
                          f"but a '{type(var).__name__}' was given instead") )
                          

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
    from vagen.types import Real, Integer, Bool
    if isinstance(var, (Bool, bool)):
        return Bool(var)
    elif isinstance(var, (Integer, int)):
        return Integer(var)
    elif isinstance(var, (Real, float)):
        return Real(var)    
    else:
        raise VagenTypeError( (f"{param} must be an instance of 'Bool', 'bool', " 
                          f"'Real', 'float', 'Integer' or 'int' but a "
                          f"'{type(var).__name__}' was given instead") )
