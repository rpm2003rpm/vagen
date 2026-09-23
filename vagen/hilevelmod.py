"""High-level Verilog-A testbench and stimulus modeling."""

from vagen.functions import (
    InitialStep,
    Timer,
    Event,
    analysis,
    abstime,
    transition,
    tanh,
    ddt,
    smooth
)

from vagen.commands import (
    Cmd,
    CmdList, 
    If,
    At,
    Case,
    While,
    Cond,
    WaitAnalogEvent,
    RepeatLoop,
    WhileLoop,
    ForLoop,
    CaseClass
)

from vagen.disciplines import (
    Electrical,
    Branch
)

from vagen.module import (
    Module
)

from vagen.types import (
    Integer,
    Real,
    Bool
)

from vagen.exceptions import VagenSequenceError, VagenTypeError, VagenValueError

from vagen.validation import (
    checkInteger,
    checkBool,
    checkReal,
    checkInstance,
    checkNotInstance,
    checkType,
    parseBool,
    parseReal,
    parseNumber
)

class Mark(Cmd):
    """Mark command class.
    
    This class is used to store a command that marks a specific event.
    """

    def __init__(self, cmd):
        """Initialize a Mark instance.

        Args:
            cmd (Cmd): The command to be stored as a marker.
        """
        checkInstance("cmd", cmd, Cmd)
        self.cmd = cmd

    def getCmd(self):
        """Return the stored command.

        Returns:
            Cmd: The command stored in this marker.
        """
        return self.cmd

    def __str__(self):
        raise VagenSequenceError(
            "Mark cannot be emitted outside mod.seq(...); use it only directly inside a sequence"
        )

    def getVA(self, padding):
        raise VagenSequenceError(
            "Mark cannot be emitted outside mod.seq(...); use it only directly inside a sequence"
        )


class Marker():
    """Marker class.

    Responsible for toggling a variable to mark events and generating cadence equations
    that compute the event times.
    """

    def __init__(self, hiLevelMod, name, riseFall):
        """Initialize a Marker.

        Args:
            hiLevelMod (HiLevelMod): The high-level model where the analog command is added.
            name (str): The marker name.
            riseFall (Real, float, or int): The rise/fall time for the marker pin.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        riseFall = parseReal("riseFall", riseFall)
        self.name = name
        self.markList = []
        self.markerPin = hiLevelMod.electrical(name = f"MARK_{name}",
                                               direction = "output")
        self.markSt = hiLevelMod.var(Bool(False), f"_$markSt_{name}")
        hiLevelMod.endAnalog(
            self.markerPin.vCont(smooth(self.markSt, 0, riseFall, riseFall))
        )
        
    def getName(self):
        """Return the marker's name.

        Returns:
            str: The marker name.
        """
        return self.name
        
    def mark(self, name):
        """Mark an event by toggling the internal variable.

        Args:
            name (str): The name of the event.

        Returns:
            Mark: A Mark command representing the event mark.
        """
        checkType("name", name, str)
        self.markList.append(name)
        return Mark(self.markSt.toggle())

    def low(self):
        """Force the internal variable low.

        Returns:
            Mark: A Mark command forcing the marker state to low.
        """
        return Mark(self.markSt.eq(False))

    def high(self):
        """Force the internal variable high.

        Returns:
            Mark: A Mark command forcing the marker state to high.
        """
        return Mark(self.markSt.eq(True))

    def getEqs(self):
        """Return a dictionary containing the cadence equations for each marked event.

        Returns:
            dict: Keys are event names, and values are cadence equations.
        """
        ans = {}
        for i in range(0, len(self.markList)):
            ans[self.markList[i]] = (f'cross(getData("/MARK_{self.name}" '
                                     f'?result "tran") 0.5 {i+1} "either" '
                                     f'nil nil)')
        return ans
        

class WaitSignal(Cmd):
    """WaitSignal command class.

    This class is used to wait for a specific event before continuing a test sequence.
    """

    def __init__(self, evnt):
        """Initialize a WaitSignal instance.

        Args:
            evnt (Event): The event to wait for.
        """
        checkInstance("evnt", evnt, Event)
        self.evnt = evnt
        super(WaitSignal, self).__init__("")

    def getEvnt(self):
        """Return the event that triggers the next state.

        Returns:
            Event: The event stored in this WaitSignal.
        """
        return self.evnt
        
    def __str__(self):
        raise VagenSequenceError(
            "Mark cannot be emitted outside mod.seq(...); use it only directly inside a sequence"
        )

    def getVA(self, padding):
        raise VagenSequenceError(
            "Mark cannot be emitted outside mod.seq(...); use it only directly inside a sequence"
        )


class WaitUs(Cmd):
    """WaitUs command class.

    This command waits for a specific delay (in microseconds) before continuing.
    """

    def __init__(self, delay):
        """Initialize a WaitUs instance.

        Args:
            delay (Real, float, or int): The delay time.
        """
        checkReal("delay", delay)
        self.delay = delay
        super(WaitUs, self).__init__("")

    def getDelay(self):
        """Return the delay value.

        Returns:
            Real, float, or int: The delay.
        """
        return self.delay
        
    def __str__(self):
        raise VagenSequenceError(
            "Mark cannot be emitted outside mod.seq(...); use it only directly inside a sequence"
        )

    def getVA(self, padding):
        raise VagenSequenceError(
            "Mark cannot be emitted outside mod.seq(...); use it only directly inside a sequence"
        )

class Bus(list):
    """Bus class.

    A list-based class representing a bus. It supports read/write operations and
    custom slicing similar to a Verilog bus.
    """

    def __init__(self, Type, busType):
        """Initialize a Bus instance.

        Args:
            Type (type): The expected type of the bus elements.
            busType (type): The type used for the bus itself.
        """
        super(Bus, self).__init__()
        self.Type = Type
        self.busType = busType

    def __getitem__(self, key):
        """Override slicing to return a bus slice in the format [msb:lsb:step].

        Args:
            key (slice or int): The index or slice.

        Returns:
            Bus or element: A new Bus if a slice is given, else a single element.
        """
        if isinstance(key, slice):
            msb = key.start
            lsb = key.stop
            i = key.step
            if i is None:
                i = 1
            if lsb is None:
                raise VagenValueError("lsb index can't be empty")
            if msb is None:
                raise VagenValueError("msb index can't be empty")
            if lsb < 0 or lsb >= len(self):
                raise VagenValueError("lsb index is out of range")
            if msb < 0 or msb >= len(self):
                raise VagenValueError("msb index is out of range")
            if i <= 0:
                raise VagenValueError("step must be greater than 0")
            vBus = self.busType()
            if lsb > msb:
                i = -i  
            while lsb <= msb and i > 0 or lsb >= msb and i < 0:
                vBus.append(super(Bus, self).__getitem__(lsb))
                lsb = lsb + i
            return vBus    
        return super(Bus, self).__getitem__(key)

    def append(self, item):
        """Append an item to the bus with type checking.

        Args:
            item: The item to append (must be an instance of self.Type).
        """
        checkInstance("item", item, self.Type)
        super(Bus, self).append(item)
        
class Vdc(Electrical):
    """Vdc class.

    A subclass of Electrical that implements extra features for a voltage source.
    """

    def __init__(self, hiLevelMod, name, value, gnd, rise, fall):
        """Initialize a Vdc instance.

        Args:
            hiLevelMod (HiLevelMod): High-level model for adding analog commands.
            name (str): Name of the voltage source pin.
            value (Real, float, or int): The initial voltage.
            gnd (Electrical or None): Ground reference signal.
            rise (Real, float, or int): Initial rise time.
            fall (Real, float, or int): Initial fall time.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        if not (gnd is None):
            checkType("gnd", gnd, Electrical)
            checkNotInstance("gnd", gnd, Branch)
        checkType("name", name, str)
        value = parseReal("value", value)
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        super(Vdc, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$").replace(", ", "_")
        self.volt = hiLevelMod.var(value, f"{prefix}_$value$")
        self.rise = hiLevelMod.var(rise,  f"{prefix}_$rise$")
        self.fall = hiLevelMod.var(fall,  f"{prefix}_$fall$")
        if gnd is None:
            out = self
        else:
            out = Branch(self, gnd)
        self.dv = out.v
        self.di = out.i
        hiLevelMod.endAnalog(
            out.vCont(
                transition(self.volt, Real(0), self.rise, self.fall)
            )
        ) 
    
    def setRiseFall(self, rise, fall):
        """Set the rise and fall times for voltage changes.

        Args:
            rise (Real, float, or int): The new rise time.
            fall (Real, float, or int): The new fall time.

        Returns:
            CmdList: A list of commands to update rise and fall times.
        """
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    def applyV(self, value):
        """Change the voltage value of the source.

        Args:
            value (Real, float, or int): The new voltage value.

        Returns:
            Cmd: A command to update the voltage.
        """
        checkReal("value", value)
        return self.volt.eq(value)

class VdcBus(Bus):
    """VdcBus class.

    A bus of Vdc elements with additional methods for handling voltage source operations.
    """

    def __init__(self):
        """Initialize a VdcBus instance."""
        super(VdcBus, self).__init__(Vdc, VdcBus)
        
    def setRiseFall(self, rise, fall):
        """Set the rise and fall times for all Vdc elements in the bus.

        Args:
            rise (Real, float, or int): The new rise time.
            fall (Real, float, or int): The new fall time.

        Returns:
            CmdList: A list of commands to update the rise and fall times.
        """
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    def applyV(self, value):
        """Change the voltage value for all Vdc elements in the bus.

        Args:
            value (Real, float, or int): The new voltage value.

        Returns:
            CmdList: A list of commands to update the voltage.
        """
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyV(value))
        return ans
        
class Idc(Electrical):
    """Idc class.

    A subclass of Electrical that implements features for a current source.
    """

    def __init__(self, hiLevelMod, name, value, gnd, rise, fall):
        """Initialize an Idc instance.

        Args:
            hiLevelMod (HiLevelMod): High-level model for adding analog commands.
            name (str): Name of the current source pin.
            value (Real, float, or int): The initial current value.
            gnd (Electrical or None): Ground reference signal.
            rise (Real, float, or int): Initial rise time.
            fall (Real, float, or int): Initial fall time.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        value = parseReal("value", value)
        if not (gnd is None):
            checkType("gnd", gnd, Electrical)
            checkNotInstance("gnd", gnd, Branch)
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        super(Idc, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$").replace(", ", "_")
        self.cur  = hiLevelMod.var(value, f"{prefix}_$value$")
        self.rise = hiLevelMod.var(rise,  f"{prefix}_$rise$")
        self.fall = hiLevelMod.var(fall,  f"{prefix}_$fall$")
        if gnd == None:
            out = self
        else:
            out = Branch(self, gnd)
        self.dv = out.v
        self.di = out.i
        hiLevelMod.endAnalog(
            out.iCont(
                transition(self.cur, Real(0), self.rise, self.fall)
            )
        ) 
    
    def setRiseFall(self, rise, fall):
        """Set the rise and fall times for current changes.

        Args:
            rise (Real, float, or int): New rise time.
            fall (Real, float, or int): New fall time.

        Returns:
            CmdList: A list of commands to update the rise and fall times.
        """
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    def applyI(self, value):
        """Change the current value of the source.

        Args:
            value (Real, float, or int): The new current value.

        Returns:
            Cmd: A command to update the current.
        """
        checkReal("value", value)
        return self.cur.eq(value)

class IdcBus(Bus):
    """IdcBus class.

    A bus of Idc elements with additional methods to handle read and write operations,
    including custom slicing similar to a Verilog bus.
    """

    def __init__(self):
        """Initialize an IdcBus instance."""
        super(IdcBus, self).__init__(Idc, IdcBus)
        
    def setRiseFall(self, rise, fall):
        """Set the rise and fall times for all Idc elements in the bus.

        Args:
            rise (Real, float, or int): The new rise time.
            fall (Real, float, or int): The new fall time.

        Returns:
            CmdList: A list of commands to update the rise and fall times.
        """
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    def applyI(self, value):
        """Change the current value for all Idc elements in the bus.

        Args:
            value (Real, float, or int): The new current value.

        Returns:
            CmdList: A list of commands to update the current.
        """
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyI(value))
        return ans
        
class Smu(Electrical):
    """Smu class.

    A subclass of Electrical that implements additional features to work as a 
    Source Measure Unit (SMU).
    """

    def __init__(self, hiLevelMod, name, volt, minCur, maxCur, res, gnd): 

        """Initialize a Smu instance.

        Args:
            hiLeveMod (HiLevelMod): High-level model where analog commands are added.
            name (str): Name of the SMU pin.
            volt (Real, float, or int): Initial voltage.
            minCur (Real, float, or int): Initial minimum current.
            maxCur (Real, float, or int): Initial maximum current.
            res (Real, float, or int): Resistance value.
            gnd (Electrical or None): Ground reference signal.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        volt = parseReal("volt", volt)
        minCur = parseReal("minCur", minCur)
        maxCur = parseReal("maxCur", maxCur)
        res = parseReal("res", res)
        if not (gnd is None):
            checkType("gnd", gnd, Electrical)
            checkNotInstance("gnd", gnd, Branch)
        super(Smu, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$").replace(", ", "_")
        self.volt     = hiLevelMod.var(volt, f"{prefix}_$volt$")
        self.maxCur   = hiLevelMod.var(maxCur, f"{prefix}_$maxCur")
        self.minCur   = hiLevelMod.var(minCur, f"{prefix}_$minCur$")
        self.res      = hiLevelMod.var(res, f"{prefix}_$res$")
        self.vDelay   = hiLevelMod.var(0.0, f"{prefix}_$vDelay$")
        self.iDelay   = hiLevelMod.var(0.0, f"{prefix}_$iDelay$")
        self.rDelay   = hiLevelMod.var(0.0, f"{prefix}_$rDelay$")
        self.riseFall = hiLevelMod.var(100e-9, f"{prefix}_$riseFall$")
        voltTran      = hiLevelMod.var(0.0, f"{prefix}_$voltTran$") 
        maxCurTran    = hiLevelMod.var(0.0, f"{prefix}_$maxCurTran$")
        minCurTran    = hiLevelMod.var(0.0, f"{prefix}_$minCurTran$")
        resTran       = hiLevelMod.var(0.0, f"{prefix}_$resTran$")
        if gnd == None:
            out = self
        else:
            out = Branch(self, gnd)
        self.dv = out.v
        self.di = out.i
        hiLevelMod.endAnalog(
            voltTran.eq(
                transition(
                    self.volt, 
                    self.vDelay,
                    self.riseFall, 
                    self.riseFall
                )
            ), 
            maxCurTran.eq(
                transition(
                    self.maxCur, 
                    self.iDelay,
                    self.riseFall, 
                    self.riseFall
                )
            ),
            minCurTran.eq(
                transition(
                    self.minCur, 
                    self.iDelay,
                    self.riseFall, 
                    self.riseFall
                )
            ),
            resTran.eq(
                transition(
                    self.res, 
                    self.rDelay,
                    self.riseFall, 
                    self.riseFall)),
            out.iCont(
                tanh(50*(out.v - voltTran))*
                0.5*(maxCurTran - minCurTran) + 
                0.5*(maxCurTran + minCurTran)
            ),
            out.iCont(out.v/resTran),
            out.iCont(1e-12*ddt(out.v))
        ) 

    def applyV(self, value, limit):
        """Configure the SMU as a current-limited voltage source and apply a voltage.

        Args:
            value (Real, float, or int): Voltage to be applied.
            limit (Real, float, or int): Current limit.

        Returns:
            CmdList: A list of commands to configure the SMU in voltage mode.
        """
        checkReal("value", value)
        checkReal("limit", limit)
        return CmdList(
            self.volt.eq(value),
            self.maxCur.eq(abs(limit)),
            self.minCur.eq(-abs(limit)),
            self.res.eq(1e4/(abs(limit) + 1e-9)),
            self.vDelay.eq(0),
            self.iDelay.eq(100e-9),
            self.rDelay.eq(100e-9),
        )

    def applyI(self, value, limit):
        """Configure the SMU as a voltage-limited current source and apply a current.

        Args:
            value (Real, float, or int): Current to be applied.
            limit (Real, float, or int): Voltage limit.

        Returns:
            CmdList: A list of commands to configure the SMU in current mode.
        """
        checkReal("value", value)
        checkReal("limit", limit)
        return CmdList(
            self.volt.eq(limit),
            self.maxCur.eq(0.5*(value + abs(value))),
            self.minCur.eq(0.5*(value - abs(value))),
            self.res.eq(1e4/(abs(value) + 1e-9)),
            self.vDelay.eq(100e-9),
            self.iDelay.eq(0),
            self.rDelay.eq(0),
        )

    def applyR(self, value):
        """Configure the SMU as a resistive load.

        Args:
            value (Real, float, or int): The resistor value.

        Returns:
            CmdList: A list of commands to configure the SMU in resistance mode.
        """
        checkReal("value", value)
        return CmdList(
            self.volt.eq(0),
            self.maxCur.eq(0),
            self.minCur.eq(0),
            self.res.eq(value),
            self.vDelay.eq(100e-9),
            self.iDelay.eq(0),
            self.rDelay.eq(0),
        )

class SmuBus(Bus):
    """SmuBus class.

    A bus of Smu elements with additional methods for handling SMU operations.
    """
    def __init__(self):
        """Initialize a SmuBus instance."""
        super(SmuBus, self).__init__(Smu, SmuBus)
      

    def applyI(self, value, limit):
        """Apply a current command to all SMU elements in the bus.

        Args:
            value (Real, float, or int): The current value.
            limit (Real, float, or int): The voltage limit.

        Returns:
            CmdList: A list of commands to update each SMU in current mode.
        """
        checkReal("value", value)
        checkReal("limit", limit)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyI(value, limit))
        return ans

    def applyV(self, value, limit):
        """Apply a voltage command to all SMU elements in the bus.

        Args:
            value (Real, float, or int): The voltage value.
            limit (Real, float, or int): The current limit.

        Returns:
            CmdList: A list of commands to update each SMU in voltage mode.
        """
        checkReal("value", value)
        checkReal("limit", limit)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyV(value, limit))
        return ans

    def applyR(self, value):
        """Apply a resistive load command to all SMU elements in the bus.

        Args:
            value (Real, float, or int): The resistor value.

        Returns:
            CmdList: A list of commands to configure each SMU in resistance mode.
        """
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyR(value))
        return ans
         
class DigOut(Electrical):
    """DigOut class.

    A subclass of Electrical that represents a digital output pin.
    """

    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, gnd, 
                 delay, rise, fall): 
        """Initialize a DigOut instance.

        Args:
            hiLeveMod (HiLevelMod): The high-level model.
            name (str): The pin name.
            state (Bool or bool): The initial state.
            domain (Electrical): The voltage domain.
            inCap: Dummy parameter for consistency.
            serRes (Real, float, or int): Series resistance.
            gnd (Electrical or None): Ground reference.
            delay (Real, float, or int): Initial delay.
            rise (Real, float, or int): Initial rise time.
            fall (Real, float, or int): Initial fall time.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        state = parseBool("state", state)
        serRes = parseReal("serRes", serRes)
        if not (gnd is None):
            checkType("gnd", gnd, Electrical)
            checkNotInstance("gnd", gnd, Branch)
        delay = parseReal("delay", delay) 
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        super(DigOut, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$").replace(", ", "_")
        self.st = hiLevelMod.var(state, f"{prefix}_$state$")
        self.serRes = hiLevelMod.var(serRes, f"{prefix}_$serRes$")
        self.delay = hiLevelMod.var(delay, f"{prefix}_$delay$")
        self.rise = hiLevelMod.var(rise, f"{prefix}_$rise$")
        self.fall = hiLevelMod.var(fall, f"{prefix}_$fall$")
        if gnd is None:
            out = self
            dm  = domain
        else:
            out = Branch(self, gnd)
            dm  = Branch(domain, gnd)
        self.dv = out.v
        self.di = out.i
        self.diffHalfDomain = self.dv - dm.v/2
        hiLevelMod.endAnalog(
            out.vCont(
                dm.v*smooth(
                    self.st, 
                    self.delay, 
                    self.rise, 
                    self.fall
                )
            ),
            out.vCont(out.i*self.serRes)
        ) 

    def setDelay(self, delay):
        """Set the delay for the digital output pin.

        Args:
            delay (Real, float, or int): The new delay time.

        Returns:
            Cmd: A command to update the delay.
        """
        checkReal("delay", delay)
        return self.delay.eq(delay)

    def setRiseFall(self, rise, fall):
        """Set the rise and fall times for the digital output pin.

        Args:
            rise (Real, float, or int): New rise time.
            fall (Real, float, or int): New fall time.

        Returns:
            CmdList: A list of commands to update the rise and fall times.
        """
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    def write(self, value):
        """Write a new state to the digital output pin.

        Args:
            value (Bool or bool): The state to write.

        Returns:
            Cmd: A command to update the state.
        """
        checkBool("value", value)
        return self.st.eq(value)

    def getST(self):
        """Return the current state of the digital output pin.

        Returns:
            Bool: The state.
        """
        return self.st

    def toggle(self):
        """Toggle the state of the digital output pin.

        Returns:
            Cmd: A command to toggle the state.
        """
        return self.st.toggle()


class DigIn(Electrical):
    """DigIn class.

    A subclass of Electrical representing a digital input pin.
    """

    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, gnd, 
                 delay, rise, fall): 
        """Initialize a DigIn instance.

        Args:
            hiLeveMod (HiLevelMod): The high-level model.
            name (str): The pin name.
            state: Dummy parameter (not used).
            domain (Electrical): The voltage domain.
            inCap (Real, float, or int): Input capacitance.
            serRes: Dummy parameter.
            gnd (Electrical or None): Ground reference.
            delay, rise, fall: Dummy parameters.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        inCap = parseReal("inCap", inCap)
        if not (gnd is None):
            checkType("gnd", gnd, Electrical)
            checkNotInstance("gnd", gnd, Branch)
        super(DigIn, self).__init__(name)
        self.domain = domain
        self.gnd = gnd
        prefix = name.replace("[", "_$").replace("]", "$").replace(", ", "_")
        self.inCap = hiLevelMod.var(inCap, f"{prefix}_$inCap$")
        if self.gnd is None:
            out = self
            dm  = self.domain
        else:
            out = Branch(self, gnd)
            dm  = Branch(self.domain, gnd)
        self.dv = out.v
        self.di = out.i
        self.diffHalfDomain = self.dv - dm.v/2
        hiLevelMod.endAnalog(
            out.iCont(ddt(out.v)*self.inCap)
        ) 
 
    def read(self):
        """Read the digital input state.

        Returns:
            Bool: An expression indicating whether the digital input is high.
        """
        return self.diffHalfDomain > 0

class DigInOut(DigIn, DigOut):
    """DigInOut class.

    A subclass that combines digital input and output functionalities.
    """

    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, gnd, 
                 delay, rise, fall): 
        """Initialize a DigInOut instance.

        Combines features of digital input and output.
        
        Args:
            hiLeveMod (HiLevelMod): The high-level model.
            name (str): The pin name.
            state (Bool or bool): The initial state.
            domain (Electrical): The voltage domain.
            inCap (Real, float, or int): Input capacitance.
            serRes (Real, float, or int): Series resistance.
            gnd (Electrical or None): Ground reference.
            delay, rise, fall (Real, float, or int): Timing parameters.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        state = parseBool("state", state)
        serRes = parseReal("serRes", serRes)
        inCap = parseReal("inCap", inCap) 
        if not (gnd is None):
            checkType("gnd", gnd, Electrical)
            checkNotInstance("gnd", gnd, Branch)  
        delay = parseReal("delay", delay)     
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        super(DigOut, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$").replace(", ", "_")
        self.st = hiLevelMod.var(state, f"{prefix}_$state$")
        self.serRes = hiLevelMod.var(serRes, f"{prefix}_$serRes$")
        self.inCap = hiLevelMod.var(inCap, f"{prefix}_$inCap$")
        self.res = hiLevelMod.var(serRes, f"{prefix}_$res$")
        self.delay = hiLevelMod.var(delay, f"{prefix}_$delay$")
        self.rise = hiLevelMod.var(rise, f"{prefix}_$rise$")
        self.fall = hiLevelMod.var(fall, f"{prefix}_$fall$")
        self.domain = domain
        pin = hiLevelMod.electrical()
        conn = Branch(pin, self)
        if gnd is None:
            out = self
            dm  = domain
        else:
            out = Branch(self, gnd)
            pin = Branch(pin,  gnd)
            dm  = Branch(domain, gnd)
        self.dv = out.v
        self.di = out.i
        self.diffHalfDomain = self.dv - dm.v/2
        hiLevelMod.endAnalog(
            pin.vCont(
                dm.v*smooth(
                    self.st, 
                    self.delay, 
                    self.rise, 
                    self.fall
                )
            ),
            conn.vCont(
                conn.i*transition(self.res, self.delay, self.rise, self.fall)
            ),
            out.iCont(ddt(out.v)*self.inCap)
        ) 

    def hiZ(self):
        """Set the pin to high impedance (hiZ) for input mode.

        Returns:
            Cmd: A command to set the pin to hiZ.
        """
        return self.res.eq(1e12)

    def lowZ(self):
        """Set the pin to low impedance (lowZ) for output mode.

        Returns:
            Cmd: A command to set the pin to lowZ.
        """
        return self.res.eq(self.serRes)

class DigBusOut(Bus):
    """DigBusOut class.
    
    A bus of digital output pins with additional methods for read/write operations,
    and custom slicing similar to a Verilog bus.
    """

    def __init__(self):
        """Initialize a DigBusOut instance."""
        super(DigBusOut, self).__init__(DigOut, DigBusOut)
 
    def setDelay(self, delay):
        """Set the delay time for all digital output pins in the bus.

        Args:
            delay (Real, float, or int): The delay time.

        Returns:
            CmdList: A list of commands to update the delay times.
        """
        checkReal("delay", delay)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setDelay(delay))
        return ans

    def setRiseFall(self, rise, fall):
        """Set the rise and fall times for all digital output pins in the bus.

        Args:
            rise (Real, float, or int): The new rise time.
            fall (Real, float, or int): The new fall time.

        Returns:
            CmdList: A list of commands to update the rise and fall times.
        """
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    def write(self, value):
        """Write a binary value to the digital output bus.

        Args:
            value (Integer or int): The value to be written.

        Returns:
            CmdList: A list of commands that write the binary value to the bus.
        """
        checkInteger("value", value)
        if len(self) > 32 and isinstance(value, Integer):
            raise VagenValueError(
                "Can't write a dynamic integer value to a bus wider than 32 bits; "
                "use a plain int literal instead"
            )
        ans = CmdList()
        i = 1
        for pin in self:
            ans.append(pin.write(Bool(value & i)))
            i = i << 1
        return ans

    def toggle(self):
        """Toggle the state of all digital output pins in the bus.

        Returns:
            CmdList: A list of commands to toggle each pin.
        """
        ans = CmdList()
        for pin in self:
            ans.append(pin.toggle())
        return ans

class DigBusIn(Bus):
    """DigBusIn class.
    
    A bus of digital input pins with methods to read binary values, and custom slicing
    similar to a Verilog bus.
    """

    def __init__(self):  
        """Initialize a DigBusIn instance."""
        super(DigBusIn, self).__init__(DigIn, DigBusIn)

    def read(self, signed = False):
        if len(self) > 32:
            raise VagenValueError("Can't read a bus wider than 32 bits")
        if len(self) > 31 and not signed:
            raise VagenValueError("Can't read a bus wider than 31 bits as unsigned")
        ans = Integer(self[0].read())
        i = 2
        for j in range(1, len(self) - 1):
            ans = ans + Integer(self[j].read())*i
            i = i << 1
        if len(self) > 1:
            if signed:
                ans = ans - Integer(self[len(self)-1].read())*i
            else:
                ans = ans + Integer(self[len(self)-1].read())*i
        return ans        

class DigBusInOut(DigBusIn, DigBusOut):
    """DigBusInOut class.
    
    A bus of digital input/output pins with methods to set pins to high impedance
    (hiZ) or low impedance (lowZ) for input/output operations.
    """

    def __init__(self):   
        """Initialize a DigBusInOut instance."""
        super(DigBusOut, self).__init__(DigInOut, DigBusInOut)

    def hiZ(self):
        """Set all digital I/O pins to high impedance (hiZ) for input mode.

        Returns:
            CmdList: A list of commands to set each pin to hiZ.
        """
        ans = CmdList()
        for pin in self:
            ans.append(pin.hiZ())
        return ans

    def lowZ(self):
        """Set all digital I/O pins to low impedance (lowZ) for output mode.

        Returns:
            CmdList: A list of commands to set each pin to lowZ.
        """
        ans = CmdList()
        for pin in self:
            ans.append(pin.lowZ())
        return ans

class Sw():
    """Sw class.
    
    Represents a switch between two nodes. It toggles conductance based on
    a transition function.
    """
    
    def __init__(self, hiLevelMod, pin1, pin2, cond, rise, fall):
        """Initialize a Sw instance representing a switch between two nodes.

        Args:
            hiLeveMod (HiLevelMod): The high-level model.
            pin1 (Electrical): The first node.
            pin2 (Electrical): The second node.
            cond (Real, float, or int): Initial conductance.
            rise (Real, float, or int): Rise time for conductance changes.
            fall (Real, float, or int): Fall time for conductance changes.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkInstance("pin1", pin1, Electrical)
        checkInstance("pin2", pin2, Electrical)
        cond = parseReal("cond", cond)
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        hiLevelMod.swCount += 1
        prefix = f"sw{hiLevelMod.swCount}"
        self.cond = hiLevelMod.var(cond, f"{prefix}_$cond$")
        self.rise = hiLevelMod.var(rise, f"{prefix}_$rise$")
        self.fall = hiLevelMod.var(fall, f"{prefix}_$fall$")
        self.branch = Branch(pin1, pin2)
        hiLevelMod.endAnalog(
            self.branch.iCont(
                self.branch.v*transition(
                    self.cond, 
                    Real(0), 
                    self.rise, 
                    self.fall
                )
            )
        )

    def setRiseFall(self, rise, fall):
        """Set the rise and fall times for the switch.

        Args:
            rise (Real, float, or int): New rise time.
            fall (Real, float, or int): New fall time.

        Returns:
            CmdList: A list of commands to update the rise and fall times.
        """
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    def setCond(self, cond):
        """Set the conductance value of the switch.

        Args:
            cond (Real, float, or int): The new conductance.

        Returns:
            Cmd: A command to update the conductance.
        """
        checkReal("cond", cond)
        return self.cond.eq(cond)

class Clock():
    """Clock class.
    
    Represents a clock generator that toggles a digital output pin at a specified frequency.
    """

    def __init__(self, hiLevelMod, pin):
        """Initialize a Clock instance.

        Args:
            hiLevelMod (HiLevelMod): The high-level model.
            pin (DigOut): A digital output pin used for the clock signal.
        """
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkInstance("pin", pin, DigOut)
        hiLevelMod.clkCount += 1
        prefix = f"clk{hiLevelMod.clkCount}"
        self.pin = pin
        self.isOn = hiLevelMod.var(Bool(0), f"{prefix}_$isOn$")
        self.halfPeriod = hiLevelMod.var(Real(1000000), f"{prefix}_$halfPeriod$")
        self.time = hiLevelMod.var(Real(1000000), f"{prefix}_$time$")
        _at = CmdList(
                self.pin.toggle(),
                If(self.isOn | self.pin.getST())(
                    self.time.eq(abstime + self.halfPeriod)
                )
            )
               
        hiLevelMod.analog(
            At(Timer(*([self.time] + hiLevelMod.timeArgs)))(
                _at
            )
        )

    def on(self, frequency):
        """Turn on the clock generator.

        Args:
            frequency (Real, float, or int): The clock frequency.

        Returns:
            CmdList: A list of commands to start the clock.
        """
        checkReal("frequency", frequency)
        return CmdList(
            self.halfPeriod.eq(0.5/frequency),
            self.isOn.eq(True),
            self.pin.toggle(),
            self.time.eq(abstime + self.halfPeriod)
        )

    def off(self):
        """Turn off the clock generator.

        Returns:
            Cmd: A command to turn off the clock.
        """
        return self.isOn.eq(False)

class HiLevelMod(Module):
    """
    HiLevelMod class extends the Module class in Verilog-A. 
    It provides additional methods for handling digital buses, 
    current sources, voltage sources, clocks, and switches.
    """

    def __init__(self, tbName, timeTol = None, ignoreHiddenStates = False):
        """
        Initializes the HiLevelMod instance.

        Args:
            tbName (str): Name of the test bench.
            timeTol (float, optional): Time tolerance for the timer.
            ignoreHiddenStates (bool): Pragma will be added if True.
        """
        
        super(HiLevelMod, self).__init__(
            tbName, 
            ignoreHiddenStates = ignoreHiddenStates
        )
        self.dcCmdList  = CmdList()
        self.time       = None 
        self.state      = None
        self.runSt      = None
        self.eventId    = None
        self.evntList   = None
        self.pEventList = []
        self.evntListG  = []
        self.markers    = []
        self.nSeq       = 1
        self.testSeqs   = CmdList()    
        self.var()   
        self.swCount = 0
        self.clkCount = 0

        if not isinstance(timeTol, type(None)):
            self.timeArgs = [0, parseReal("timeTol", timeTol)]
        else:
            self.timeArgs = []
          
        self.beginningAnalog(
            If(analysis("static"))(
                self.dcCmdList
            ),
            At(InitialStep("tran"))(
                self.dcCmdList
            ),
        )
        
        self.analog(
            self.testSeqs
        )

    def var(self, value = 0, name = ""):
        """
        Adds a variable to the module.

        Args:
            value (int, float, optional): Initial value. Default is 0.
            name (str, optional): Name of the variable.
        
        Returns:
            Variable: A variable instance.
        """
        
        value = parseNumber("value", value)
        ans = super(HiLevelMod, self).var(type(value), name)           
        self.dcCmdList.append(ans.eq(value))
        return ans

    def marker(self, name, riseFall = 50e-12):
        """
        Returns a marker object.

        Args:
            name (str): Name of the marker.
            riseFall (float, optional): Rise and fall times of the marker pin. Default is 50ps.
        
        Returns:
            Marker: Marker class instance.
        """
        markerObj = Marker(self, name, riseFall)
        self.markers.append(markerObj)
        return markerObj
        
    def dig(self, 
            domain, 
            name = "", 
            width = 1, 
            direction = "internal", 
            value = 0,
            inCap = 1e-14, 
            serRes = 10e3, 
            gnd = None, 
            delay = 0,
            rise = 100e-12,
            fall = 100e-12):
        """
        Returns a digital pin or a digital bus.

        Args:
            domain (Electrical): Electrical pin that defines the voltage when logical state is 1.
            name (str, optional): Name of the electrical pin.
            width (int, optional): Bus width. If greater than 1, a bus is returned.
            direction (str, optional): Direction (internal, input, output, inout).
            value (int, optional): Initial value of the digital pin.
            inCap (float, optional): Input capacitance.
            serRes (float, optional): Series resistance.
            gnd (Electrical, optional): Ground reference.
            delay (float, optional): Initial delay time.
            rise (float, optional): Initial rise time.
            fall (float, optional): Initial fall time.

        Returns:
            DigIn, DigOut, DigInOut, DigBusIn, DigBusOut, or DigBusInOut: The corresponding digital pin or bus object.
        """
        #Check the inputs
        checkInstance("domain", domain, Electrical)
        checkInteger("value", value)
        checkReal("inCap", inCap)
        checkReal("serRes", serRes)
        checkReal("rise", rise)
        checkReal("fall", fall)
        name = self.addNode(name, width, direction)
        if direction == "input":
            digType = DigIn
            busType = DigBusIn
        elif direction == "output":
            digType = DigOut
            busType = DigBusOut
        else:
            digType = DigInOut
            busType = DigBusInOut
        #Create single pin
        if width == 1:
            return digType(self, 
                           name, 
                           Bool(value), 
                           domain, 
                           inCap, 
                           serRes, 
                           gnd,
                           delay,
                           rise, 
                           fall)
        #Create a bus
        else:
            bus = busType()
            j = 1
            for i in range(0, width):
                bus.append(digType(self, 
                                   name + "[" + str(i) + "]",
                                   Bool(value & j),
                                   domain, 
                                   inCap, 
                                   serRes,
                                   gnd,
                                   delay,
                                   rise, 
                                   fall))
                j = j << 1
            return bus

    def sw(self, pin1, pin2, cond = 0.0, rise = 1e-6, fall = 1e-6):
        checkInstance("pin1", pin1, Electrical)
        checkInstance("pin2", pin2, Electrical)
        checkReal("cond", cond)
        checkReal("rise", rise)
        checkReal("fall", fall)
        return Sw(self, pin1, pin2, cond, rise, fall)

    def clock(self, pin):
        """
        Builds a clock model using a digital pin.

        Args:
            pin (DigOut): Digital output pin.

        Returns:
            Clock: Clock object.
        """
        checkInstance("pin", pin, DigOut)
        return Clock(self, pin)

    def smu(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            volt = 0, 
            minCur = 0, 
            maxCur = 0, 
            res = 1e12,
            gnd = None): 
        """
        Return a Smu object or a SmuBus object if width > 1.

        Args:
            name (str): Name of the smu electrical pin.
            width (int): If width is greater than 1, it returns a SmuBus.
            direction (str): Direction of the signal (internal, input, output, inout).
            volt (float): Real expression holding the initial voltage.
            minCur (float): Real expression holding the initial minimum current.
            maxCur (float): Real expression holding the initial maximum current.
            res (float): Real expression holding the resistance.
            gnd (optional): Electrical reference for the ground.

        Returns:
            Smu or SmuBus: Depending on the width, returns a single Smu or a vector of Smu objects.
        """
        checkReal("volt", volt)
        checkReal("minCur", minCur)
        checkReal("maxCur", maxCur)
        checkReal("res", res)
        name = self.addNode(name, width, direction)
        if width == 1:
            return  Smu(self, name, volt, minCur, maxCur, res, gnd)
        else:
            vector = SmuBus()
            for i in range(0, width):
                vector.append(
                    Smu(self, 
                        name + "[" + str(i) + "]",
                        volt, 
                        minCur,
                        maxCur,
                        res,
                        gnd
                    )
                )
            return vector

    def vdc(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            value = 0,
            gnd = None,
            rise = 1e-6,
            fall = 1e-6):
        """
        Return a Vdc object or a VdcBus object if width > 1.

        Args:
            name (str): Name of the voltage source.
            width (int): If width is greater than 1, it returns a list of Vdc objects.
            direction (str): Direction of the signal (internal, input, output, inout).
            value (float): Real expression holding the initial voltage value.
            gnd (optional): Electrical reference for the ground.
            rise (float): Initial rise time of the voltage.
            fall (float): Initial fall time of the voltage.

        Returns:
            Vdc or VdcBus: Depending on the width, returns a single Vdc or a vector of Vdc objects.
        """
        checkReal("value", value)
        checkReal("rise", rise)
        checkReal("fall", fall)
        name = self.addNode(name, width, direction)
        if width == 1:
            return  Vdc(self, name, value, gnd, rise, fall)
        else:
            vBus = VdcBus()
            for i in range(0, width):
                vBus.append(
                    Vdc(self, 
                        name + "[" + str(i) + "]", 
                        value,
                        gnd,
                        rise, 
                        fall
                    )
                )
            return vBus

    def idc(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            value = 0,
            gnd = None,
            rise = 1e-6,
            fall = 1e-6):
        """
        Return an Idc object or an IdcBus object if width > 1.

        Args:
            name (str): Name of the current source.
            width (int): If width is greater than 1, it returns a list of Idc objects.
            direction (str): Direction of the signal (internal, input, output, inout).
            value (float): Real expression holding the initial current value.
            gnd (optional): Electrical reference for the ground.
            rise (float): Initial rise time of the current.
            fall (float): Initial fall time of the current.

        Returns:
            Idc or IdcBus: Depending on the width, returns a single Idc or a vector of Idc objects.
        """
        checkReal("value", value)
        checkReal("rise", rise)
        checkReal("fall", fall)
        name = self.addNode(name, width, direction)
        if width == 1:
            return  Idc(self, name, value, gnd, rise, fall)
        else:
            iBus = IdcBus()
            for i in range(0, width):
                iBus.append(
                    Idc(self, 
                        name + "[" + str(i) + "]", 
                        value,
                        gnd,
                        rise, 
                        fall
                    )
                )
            return iBus

    def seqNested(self, cmdsIn):
        """
        Sequence. Do not use it! Use Seq instead.

        Args:
            cmdsIn (list): List of commands to be processed.

        Returns:
            CmdList: The list of remaining commands to be processed.
        """
        cmdsIn = cmdsIn.flat()
        cmds = CmdList()
        for cmd in cmdsIn:
        
            #Found a WaitUs. Update timer event and go to next state
            if isinstance(cmd, WaitUs):
                cmds.append(self.eventId.eq(0))
                cmds.append(self.state.eq(self.nState + 1))
                cmds.append(self.time.eq(abstime + 1e-6*cmd.getDelay()))
                self.pCase.append((self.nState, cmds))
                self.nState = self.nState + 1
                cmds = CmdList()
                
            #Found a WaitSignal. Update signal events and go to next state
            elif isinstance(cmd, WaitSignal):
                evnt = cmd.getEvnt()
                #The event was used before
                if evnt in self.evntList:
                    i = self.evntListG.index(evnt)
                    eventId = i + 1  
                #Fist event was used before but not in the current sequence
                elif evnt in self.evntListG:
                    self.evntList.append(evnt)
                    i = self.evntListG.index(evnt)
                    eventId = i + 1  
                    self.pEventList[i].append(
                        If(eventId == self.eventId)(
                            self.runSt.eq(True)
                        )
                    )
                #The event wasn't used in any sequence
                else:
                    eventId = len(self.evntListG) + 1
                    self.evntList.append(evnt)
                    self.evntListG.append(evnt)
                    pEvntCmd = CmdList( 
                        If(eventId == self.eventId)(
                            self.runSt.eq(True)
                        )
                    )
                    self.pEventList.append(pEvntCmd)
                    self.beginningAnalog(
                        At(evnt)(
                            pEvntCmd
                        )
                    )
                cmds.append(self.eventId.eq(eventId))
                cmds.append(self.state.eq(self.nState + 1))
                self.pCase.append((self.nState, cmds))
                self.nState = self.nState + 1
                cmds = CmdList()
                
            #Found a repeat loop
            elif isinstance(cmd, RepeatLoop):
                temp = self.var()
                cmds.append(temp.eq(0))
                cmds.append(self.runSt.eq(True))
                cmds.append(self.state.eq(self.nState + 1))
                self.pCase.append((self.nState, cmds))
                self.nState = self.nState + 1
                nStateTest = self.nState
                self.nState = self.nState + 1
                nStateLoop = self.nState
                cmds = self.seqNested(cmd)
                self.pCase.append(
                    (self.nState, 
                        cmds,
                        temp.inc(),
                        self.runSt.eq(True),
                        self.state.eq(nStateTest)
                    )
                )               
                self.pCase.append(
                    (nStateTest,
                        self.runSt.eq(True),
                        If(temp < cmd.getN())(
                            self.state.eq(nStateLoop),
                        ).Else(
                            self.state.eq(self.nState + 1)    
                        )
                    )
                )  
                self.nState = self.nState + 1  
                cmds = CmdList()           

            #Found a While loop
            elif isinstance(cmd, WhileLoop):
                cmds.append(self.runSt.eq(True))
                cmds.append(self.state.eq(self.nState + 1))
                self.pCase.append((self.nState, cmds))
                self.nState = self.nState + 1
                nStateTest = self.nState
                self.nState = self.nState + 1
                nStateLoop = self.nState
                cmds = self.seqNested(cmd)
                self.pCase.append(
                    (self.nState, 
                        cmds,
                        self.runSt.eq(True),
                        self.state.eq(nStateTest)
                    )
                )               
                self.pCase.append(
                    (nStateTest,
                        self.runSt.eq(True),
                        If(cmd.getCond())(
                            self.state.eq(nStateLoop),
                        ).Else(
                            self.state.eq(self.nState + 1)    
                        )
                    )
                )  
                self.nState = self.nState + 1  
                cmds = CmdList()
                
            #Found a for loop
            elif isinstance(cmd, ForLoop):
                cmds.append(cmd.getStart())
                cmds.append(self.runSt.eq(True))
                cmds.append(self.state.eq(self.nState + 1))
                self.pCase.append((self.nState, cmds))
                self.nState = self.nState + 1
                nStateTest = self.nState
                self.nState = self.nState + 1
                nStateLoop = self.nState
                cmds = self.seqNested(cmd)
                self.pCase.append(
                    (self.nState, 
                        cmds,
                        cmd.getInc(),
                        self.runSt.eq(True),
                        self.state.eq(nStateTest)
                    )
                )               
                self.pCase.append(
                    (nStateTest,
                        self.runSt.eq(True),
                        If(cmd.getCond())(
                            self.state.eq(nStateLoop),
                        ).Else(
                            self.state.eq(self.nState + 1)    
                        )
                    )
                )  
                self.nState = self.nState + 1  
                cmds = CmdList()
                
            #Found a If
            elif isinstance(cmd, Cond):
                nStateTest = self.nState
                self.nState = self.nState + 1
                nStateTrue = self.nState
                cmdsEndTrue = self.seqNested(cmd.getBlock(True))
                nStateEndTrue = self.nState
                self.nState = self.nState + 1
                nStateFalse = self.nState                
                cmdsEndFalse = self.seqNested(cmd.getBlock(False))
                self.pCase.append(
                    (self.nState, 
                        cmdsEndFalse,
                        self.runSt.eq(True),
                        self.state.eq(self.nState + 1)
                    )
                )      
                self.pCase.append(
                    (nStateEndTrue, 
                        cmdsEndTrue,
                        self.runSt.eq(True),
                        self.state.eq(self.nState + 1)
                    )
                )                    
                self.pCase.append(
                    (nStateTest,
                        cmds,
                        self.runSt.eq(True),
                        If(cmd.getCond())(
                            self.state.eq(nStateTrue),
                        ).Else(
                            self.state.eq(nStateFalse)    
                        )
                    )
                )  
                self.nState = self.nState + 1  
                cmds = CmdList()
                
            #Found a case
            elif isinstance(cmd, CaseClass):
                raise VagenSequenceError("You can't have a Case inside a seq")
                                                       
            #Found a case
            elif isinstance(cmd, Mark):
                raise VagenSequenceError(
                    "You can't have conditionally executed marks or marks "
                    "inside command lists"
                )

            #The commands doesn't require special handling. Add it to the list.
            else:
                cmds.append(cmd)
                
        return cmds

    def seq(self, cond):
        """
        Sequence

        Args:
            cond (bool): Condition to run the sequence.

        Returns:
            func: Function that accepts a variable number of commands to be added to the sequence.
        """
        def func(*args):
            self.nState   = 0
            self.time     = self.var(Real(1e-9),  f"_$evntTime_{self.nSeq}") 
            self.state    = self.var(Integer(0),  f"_$state_{self.nSeq}") 
            self.runSt    = self.var(Bool(False), f"_$runSt_{self.nSeq}") 
            self.eventId  = self.var(Integer(0),  f"_$eventId_{self.nSeq}") 
            self.pCase    = Case(self.state)()
            self.cond     = cond
            self.evntList = []
            self.beginningAnalog(
                At(Timer(*([self.time] + self.timeArgs)))(
                    If(self.eventId == 0)(
                        self.runSt.eq(True)
                    )
                )
            )
            self.testSeqs.append(
                If(self.cond)(
                    While(self.runSt)(
                        self.runSt.eq(False),
                        self.pCase
                    )
                )
            )
            cmds = CmdList()
            i = 1
            if len(args) == 0:
                raise VagenValueError("Sequence can't be empty")
            for cmd in args:
                if not isinstance(cmd, Cmd) or isinstance(cmd, WaitAnalogEvent):
                    raise VagenTypeError(
                        f"Command {i} must be an instance of Cmd and can't be "
                        "an instance of WaitAnalogEvent"
                    )
                i = i + 1
                if isinstance(cmd, Mark):
                    cmds.append(cmd.getCmd())
                else:
                    cmds.append(cmd)
            cmds = self.seqNested(cmds)
            #Add a finish command
            #cmds.append(Finish()) 
            #Add the last state 
            if len(cmds) > 0:
                self.pCase.append((Integer(self.nState), cmds))
            #Go to the next sequence
            self.nSeq = self.nSeq + 1
        return func

    def getEqs(self):
        """
        Return the equations in a format that can be imported by the maestro view.

        Returns:
            str: Equations in a string format for the maestro view.
        """
        ans = ["Test,Name,Type,Output,Plot,Save,Spec"]
        for mark in self.markers:
            eqs = mark.getEqs()
            name = mark.getName()
            for key in eqs.keys():
                ans.append(f"{name},{name}_{key},expr,{eqs[key]},t,,")
        return "\n".join(ans) 
            
    def getOcn(self):
        """
        Return an ocean script that adds equations to the opened session of adexl.

        Returns:
            str: Ocean script for adding equations to adexl.
        """
        ans = ["session = axlGetWindowSession()"]
        for mark in self.markers:
            eqs = mark.getEqs()
            name = mark.getName()
            for key in eqs.keys():
                eq = eqs[key].replace('"', '\\"')
                ans.append( (f"axlAddOutputExpr(session {name} {name}_{key} "
                             f"?expr {eq} ?plot t)") )
        return "\n".join(ans) 

