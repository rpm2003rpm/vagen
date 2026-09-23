"""Built-in Verilog-A functions and system variables."""

import math as m
from vagen.enums import CrossEdge
from vagen.exceptions import VagenTypeError, VagenValueError
from vagen.types import Bool, Integer, Real, IntegerVar
from vagen.validation import (
    checkBool,
    checkInstance,
    checkReal,
    parseInteger,
    parseReal,
    parseBool,
    checkType
)

def random(seed):
    """Return a random Integer generated using the given seed.

    Args:
        seed (IntegerVar): The seed for the random generator.

    Returns:
        Integer: A random integer.
    """
    checkInstance("seed", seed, IntegerVar)
    return Integer(f'$random({seed})')


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


temp = Real("$temperature")
abstime = Real("$abstime")
vt = Real("$vt")


def exp(x):
    """Return a Real expression for the exponential of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing exp(x).
    """
    x = parseReal("x", x)
    return Real(f"exp({x})")


def limexp(x):
    """Return a Real expression for the limited exponential function of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing limexp(x).
    """
    x = parseReal("x", x)
    return Real(f"limexp({x})")


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


def ddt(x):
    """Return a Real expression representing the differential function of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing ddt(x).
    """
    x = parseReal("x", x)
    return Real(f"ddt({x})")
 
 
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


def ceil(x):
    """Return a Real expression representing the ceiling of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing ceil(x).
    """
    x = parseReal("x", x)
    return Real(f"ceil({x})")
      

def floor(x):
    """Return a Real expression representing the floor of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing floor(x).
    """
    x = parseReal("x", x)
    return Real(f"floor({x})")


def ln(x):
    """Return a Real expression representing the natural logarithm of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing ln(x).
    """
    x = parseReal("x", x)
    return Real(f"ln({x})")

def log(x):
    """Return a Real expression representing the log of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing log(x).
    """
    x = parseReal("x", x)
    return Real(f"log({x})")


def sqrt(x):
    """Return a Real expression representing the square root of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing sqrt(x).
    """
    x = parseReal("x", x)
    return Real(f"sqrt({x})")


def sin(x):
    """Return a Real expression representing the sine of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing sin(x).
    """
    x = parseReal("x", x)
    return Real(f"sin({x})")


def cos(x):
    """Return a Real expression representing the cosine of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing cos(x).
    """
    x = parseReal("x", x)
    return Real(f"cos({x})")


def tan(x):
    """Return a Real expression representing the tangent of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing tan(x).
    """
    x = parseReal("x", x)
    return Real(f"tan({x})")


def asin(x):
    """Return a Real expression representing the arcsine of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing asin(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"asin({x})")


def acos(x):
    """Return a Real expression representing the arccosine of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing acos(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"acos({x})")


def atan(x):
    """Return a Real expression representing the arctangent of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing atan(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"atan({x})")


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


def sinh(x):
    """Return a Real expression representing the hyperbolic sine of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing sinh(x).
    """
    x = parseReal("x", x)
    return Real(f"sinh({x})")


def cosh(x):
    """Return a Real expression representing the hyperbolic cosine of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing cosh(x).
    """
    x = parseReal("x", x)
    return Real(f"cosh({x})")


def tanh(x):
    """Return a Real expression representing the hyperbolic tangent of x.

    Args:
        x (Real, float, or int): Angle in radians.

    Returns:
        Real: An expression representing tanh(x).
    """
    x = parseReal("x", x)
    return Real(f"tanh({x})")


def asinh(x):
    """Return a Real expression representing the inverse hyperbolic sine of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing asinh(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"asinh({x})")


def acosh(x):
    """Return a Real expression representing the inverse hyperbolic cosine of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing acosh(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"acosh({x})")


def atanh(x):
    """Return a Real expression representing the inverse hyperbolic tangent of x.

    Args:
        x (Real, float, or int): The input value.

    Returns:
        Real: An expression representing atanh(x) in radians.
    """
    x = parseReal("x", x)
    return Real(f"atanh({x})")


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
        raise VagenTypeError(
            "op1 and op2 must be Integer, Real, Bool, bool, float, or int "
            f"with compatible types but got {type(op1)} and {type(op2)} instead"
        )
    Type = Real if isinstance(op1, Real) else \
           Bool if isinstance(op1, Bool) else \
           Integer
    return Type(f"{test} ? {op1} : {op2}") 
    
    
class Event():
    """Class representing an event in the system."""

    def __init__(self, value):
        """Initialize an Event instance.

        Args:
            value (str): A string representing the event.
        """
        checkType("value", value, str)
        self.value = value

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

    def __str__(self):
        """Return the string representation of the Event.

        Returns:
            str: The event as a string.
        """
        return self.value        
        
        
mapping = {CrossEdge.RISING.value: '1',
           CrossEdge.FALLING.value: '-1',
           CrossEdge.BOTH.value: '0'}
           
class Cross(Event):
    """Class representing a cross event."""

    def __init__(self, expr, edge, *pars):
        """Initialize a Cross event instance.

        Args:
            expr (Real or numeric): The expression for the cross event.
            edge (str or CrossEdge): The edge type ('rising', 'falling', or 'both').
            *pars: Optional parameters (timeTol and expTol).

        Raises:
            VagenValueError: If an invalid edge value is provided or wrong number
                of parameters.
        """
        if not (0 <= len(pars) <= 2):
            raise VagenValueError("Wrong number of parameters")
        expr = parseReal("expr", expr)
        if isinstance(edge, CrossEdge):
            edge = edge.value
        checkType("edge", edge, str)
        if edge not in mapping:
            raise VagenValueError("Wrong value for edge")
        params = [mapping[edge]]

        for par in pars:
            par = parseReal("timeTol or expTol", par)
            params.append(str(par))
        
        evnt = f"cross({expr}, {', '.join(params)})" 
        super(Cross, self).__init__(evnt)


class Above(Event):
    """Class representing an above event."""

    def __init__(self, expr, *pars):
        """Initialize an Above event instance.

        Args:
            expr (Real or numeric): The expression for the above event.
            *pars: Optional parameters (timeTol and expTol).
        """
        if not (0 <= len(pars) <= 2):
            raise VagenValueError("Wrong number of parameters")
        expr = parseReal("expr", expr)
        params = [str(expr)] 

        for par in pars:
            par = parseReal("timeTol or expTol", par)
            params.append(str(par))

        evnt = f"above({', '.join(params)})" 
        super(Above, self).__init__(evnt)


class Timer(Event):
    """Class representing a timer event."""
    
    def __init__(self, startTime, *pars):
        """Initialize a Timer event instance.

        Args:
            startTime (Real or numeric): The start time for the timer.
            *pars: Optional parameters (period or timeTol, expTol).

        Raises:
            AssertionError: If wrong number of parameters is provided.
        """
        if not (0 <= len(pars) <= 2):
            raise VagenValueError("Wrong number of parameters")
        startTime = parseReal("startTime", startTime)
        params = [str(startTime)] 

        for par in pars:
            par = parseReal("period or timeTol", par)
            params.append(str(par))

        evnt = f"timer({', '.join(params)})" 
        super(Timer, self).__init__(evnt)


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
        if simType not in anaTypes:
            raise VagenValueError(
               f"simType[{i}] must be of of the following: {anaTypes}")
        i = i + 1
        ans.append(f'"{simType}"')
    return ", ".join(ans)


class InitialStep(Event):
    """Class representing an initial step event."""

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
                                          

class FinalStep(Event):
    """Class representing a final step event."""

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
  
   
def analysis(*simTypes):
    """Return a Bool expression that tests for the specified analysis type(s).

    Args:
        *simTypes: One or more simulation type strings.

    Returns:
        Bool: A Bool expression representing the analysis test.

    Raises:
        Exception: If no simulation type is specified.
    """
    if not simTypes:
        raise VagenTypeError("At least one simulation type must be specified")
    return Bool(f'analysis({unfoldSimTypes(*simTypes)})')


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
    if simType not in anaTypes:
        raise VagenValueError(
           f"simType must be of of the following: {anaTypes}")
    mag = parseReal("mag", mag)
    phase = parseReal("phase", phase)
    return Real(f'ac_stim("{simType}", {mag}, {phase})')
    

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
    if isinstance(edge, CrossEdge):
        edge = edge.value
    checkType("edge", edge, str)
    if edge not in mapping:
        raise VagenValueError("Wrong value for edge")
    cross = f"last_crossing({signal} - {threshold}, {mapping[edge]})"
    return Real(cross)
