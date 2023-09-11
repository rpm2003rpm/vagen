## @file hilevelmod.py
#  Hi level modeling.
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
from vagen.veriloga import *


#-------------------------------------------------------------------------------
## Mark command class
#
#  This class of commands are responsible for storing the command thar marks
#  an specific event
#
#-------------------------------------------------------------------------------
class Mark(Cmd):

    #---------------------------------------------------------------------------
    ## Construtor
    #
    #  @param self The object pointer.
    #  @param cmd Command to be added to the marker.
    #
    #---------------------------------------------------------------------------
    def __init__(self, cmd):
        checkInstance("cmd", cmd, Cmd)
        self.cmd = cmd

    #---------------------------------------------------------------------------
    ## Return the command
    #
    #  @param self The object pointer.
    #  @return Command passed to the constructor.
    #
    #---------------------------------------------------------------------------
    def getCmd(self):
        return self.cmd

    #---------------------------------------------------------------------------
    ## Dummy method.
    #  Raise exception when runned.
    #
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------        
    def __str__(self):
        #TODO: Find a better way to fix this
        raise Exception("Mark doesn't have string representation")

    #---------------------------------------------------------------------------
    ## Dummy method.
    #  Raise exception when runned.
    #
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------        
    def getVA(self, padding):
        #TODO: Find a better way to fix this
        raise Exception("Mark can't be outside seq")


#-------------------------------------------------------------------------------
## Marker class. 
#
#  Responsible for flipping the state of one variable to mark events and 
#  generates cadence equations that calculate the time of the events
#
#-------------------------------------------------------------------------------
class Marker():

    #---------------------------------------------------------------------------
    ## Construtor.
    # 
    # @param self The object pointer.
    # @param hiLeveMod  Hi level model in which the analog command will be added
    # @param name Name of the marker.
    # @param riseFall Rise and fall times of the marker pin.
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, riseFall):
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
        
    #---------------------------------------------------------------------------
    ## Return the  name of the Marker.
    # 
    #  @param self The object pointer.
    #  @return Name of the Marker.
    #
    #---------------------------------------------------------------------------
    def getName(self):
        return self.name
        
    #---------------------------------------------------------------------------
    ## Mark a particular event by flipping the internal variable.
    # 
    #  @param self The object pointer.
    #  @param name Name of the event.
    #  @return The Mark command.
    #
    #---------------------------------------------------------------------------
    def mark(self, name):
        checkType("name", name, str)
        self.markList.append(name)
        return Mark(self.markSt.toggle())

    #---------------------------------------------------------------------------
    ## Force the internal variable low. 
    #
    #  You shouldn't use because it will break the synchronism between the 
    #  cadence equations and the events. 
    #  It was implemented for usage in specific power down conditions only.
    # 
    #  @param self The object pointer.
    #  @return The Mark command.
    #
    #---------------------------------------------------------------------------
    def low(self): 
        return Mark(self.markSt.eq(False))

    #---------------------------------------------------------------------------
    ## Force the internal variable high. 
    #
    #  You shouldn't use because it will break the synchronism between the 
    #  cadence equations and the events. 
    #  It was implemented for usage in specific power down conditions only.
    # 
    #  @param self The object pointer.
    #  @return The Mark command.
    #
    #---------------------------------------------------------------------------
    def high(self):
        return Mark(self.markSt.eq(True))

    #---------------------------------------------------------------------------
    ## Return a dictionay with the cadence equations for the marker     
    # 
    #  @param self The object pointer.
    #  @return The dictionary with the cadence equations.
    #
    #---------------------------------------------------------------------------
    def getEqs(self):
        ans = {}
        for i in range(0, len(self.markList)):
            ans[self.markList[i]] = (f'cross(getData("/MARK_{self.name}" '
                                     f'?result "tran") 0.5 {i+1} "either" '
                                     f'nil nil)')
        return ans
        

#-------------------------------------------------------------------------------
## WaitSignal command class
# 
#  This class of commands are responsible for wating a specific Event before
#  allowing a test sequence to continue 
#
#-------------------------------------------------------------------------------
class WaitSignal(Cmd):

    #---------------------------------------------------------------------------
    ## Construtor.
    # 
    #  @param self The object pointer.
    #  @param evnt Event to be waited for.
    #
    #---------------------------------------------------------------------------
    def __init__(self, evnt):
        checkInstance("evnt", evnt, Event)
        self.evnt = evnt
        super(WaitSignal, self).__init__("")

    #---------------------------------------------------------------------------
    ## Return the event that triggers the next state.
    #
    #  @param self The object pointer.
    #  @return Event passed to the constructor.
    #
    #---------------------------------------------------------------------------
    def getEvnt(self):
        return self.evnt
        
    #---------------------------------------------------------------------------
    ## Dummy method.
    #  Raise exception when runned.
    #
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------         
    def __str__(self):
        #TODO: Find a better way to fix this
        raise Exception("Wait doesn't have string representation")

    #---------------------------------------------------------------------------
    ## Dummy method.
    #  Raise exception when runned.
    #
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------      
    def getVA(self, padding):
        #TODO: Find a better way to fix this
        raise Exception("Wait can't be outside seq")


#-------------------------------------------------------------------------------
## WaitUs command class.
# 
#  This class of commands are responsible for wating a specific delay before
#  allowing a test sequence to continue.
#
#-------------------------------------------------------------------------------
class WaitUs(Cmd):

    #---------------------------------------------------------------------------
    ## Construtor.
    # 
    #  @param self The object pointer.
    #  @param delay Delay to be waited for.
    #
    #---------------------------------------------------------------------------
    def __init__(self, delay):
        checkReal("delay", delay)
        self.delay = delay
        super(WaitUs, self).__init__("")

    #---------------------------------------------------------------------------
    ## Return the delay that triggers the next state.
    #
    #  @param self The object pointer.
    #  @return Delay passed to the constructor.
    #
    #---------------------------------------------------------------------------
    def getDelay(self):
        return self.delay
        
    #---------------------------------------------------------------------------
    ## Dummy method.
    #  Raise exception when runned.
    #
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------       
    def __str__(self):
        #TODO: Find a better way to fix this
        raise Exception("Wait doesn't have string representation")

    #---------------------------------------------------------------------------
    ## Dummy method.
    #  Raise exception when runned.
    #
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------      
    def getVA(self, padding):
        #TODO: Find a better way to fix this
        raise Exception("Wait can't be outside seq")


#-------------------------------------------------------------------------------
## Bus class. Child of a list. 
#  It implements aditional methods to deal with read and write operations to 
#  a bus. It also overrides the slice method, so it works similar to a slice 
#  of a bus in verilog.
#
#-------------------------------------------------------------------------------
class Bus(list):

    #---------------------------------------------------------------------------
    ## Constructor
    #
    #  @param self The object pointer.
    #  @param Type Type of the bus elements
    #  @param busType Type of the bus
    #
    #---------------------------------------------------------------------------
    def __init__(self, Type, busType):
        super(Bus, self).__init__()
        self.Type = Type
        self.busType = busType
    
    #---------------------------------------------------------------------------
    ## Slice override.
    #  Override the slice operator, so it will be in the format  [msb:lsb:step]
    #  @param self The object pointer.
    #  @param key Key can be an slice or index
    #  @return Another bus or an element.
    #
    #---------------------------------------------------------------------------
    def __getitem__(self, key):
        if isinstance(key, slice):
            msb = key.start
            lsb = key.stop
            i = key.step
            if i == None:
                i = 1
            assert lsb != None, "lsb Index can't be empty" 
            assert msb != None, "msb Index can't be empty" 
            assert lsb >= 0 and lsb < len(self), "lsb Index is out of range" 
            assert msb >= 0 and msb < len(self), "msb Index is out of range" 
            assert i > 0, "step must be greather than 0" 
            vBus = self.busType()
            if lsb > msb:
                i = -i  
            while lsb <= msb and i > 0 or lsb >= msb and i < 0:
                vBus.append(super(Bus, self).__getitem__(lsb))
                lsb = lsb + i
            return vBus    
        return super(Bus, self).__getitem__(key)

    #---------------------------------------------------------------------------
    ## Append override
    #  @param self The object pointer.
    #  @param item Item to be appended to the bus
    #
    #---------------------------------------------------------------------------
    def append(self, item):
        checkInstance("item", item, self.Type)
        super(Bus, self).append(item)
        
        
#-------------------------------------------------------------------------------
## Vdc class. 
#  Child of Electrical implementing aditional features in order to work as a 
#  voltage source.
#
#-------------------------------------------------------------------------------
class Vdc(Electrical):
    
    #---------------------------------------------------------------------------
    ## Construtor.
    #  @param self The object pointer.
    #  @param hiLeveMod Hi level model in which the analog command will be added.
    #  @param name Name of the voltage source electrical pin.
    #  @param value Real expression holding the inital voltage.
    #  @param gnd Electrical representing the ground reference.
    #  @param rise Real expression holding the initial rise time.
    #  @param fall Real expression holding the initial fall time.
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, value, gnd, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        if gnd != None:
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
        if gnd == None:
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
    
    #---------------------------------------------------------------------------
    ## Set the rise and the fall times for changes in the voltage.
    #  @param self The object pointer.
    #  @param rise Real expression holding the rise time for changes in the 
    #         voltage.
    #  @param fall Real expression holding the fall time for changes in the 
    #         voltage.
    #  @return The commands to change the rise and fall times.
    #
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    #---------------------------------------------------------------------------
    ## Change the value of the voltage source.
    #  @param self The object pointer.
    #  @param value Real expression holding the voltage.
    #  @return The commands to change the voltage.
    #  
    #---------------------------------------------------------------------------
    def applyV(self, value):
        checkReal("value", value)
        return self.volt.eq(value)


#-------------------------------------------------------------------------------
## VdcBus class. Child of a list. 
#  It implements aditional methods to deal with read and write operations to 
#  a bus. It also overrides the slice method, so it works similar to a slice 
#  of a bus in verilog.
#
#-------------------------------------------------------------------------------
class VdcBus(Bus):

    #---------------------------------------------------------------------------
    ## Constructor.
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def __init__(self):
        super(VdcBus, self).__init__(Vdc, VdcBus)
        
    #---------------------------------------------------------------------------
    ## Set the rise and the fall times for changes in the voltage.
    #  @param self The object pointer.
    #  @param rise Real expression holding the rise time for changes in the 
    #         voltage.
    #  @param fall Real expression holding the fall time for changes in the 
    #         voltage.
    #  @return The commands to change the rise and fall times.
    #
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    #---------------------------------------------------------------------------
    ## Change the value of the voltage source.
    #  @param self The object pointer.
    #  @param value Real expression holding the voltage.
    #  @return The commands to change the voltage.
    #  
    #---------------------------------------------------------------------------
    def applyV(self, value):
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyV(value))
        return ans
        
        
#-------------------------------------------------------------------------------
## Idc class. 
#  Child of Electrical implementing aditional features in order to work as a 
#  current source.
#
#-------------------------------------------------------------------------------
class Idc(Electrical):
    
    #---------------------------------------------------------------------------
    ## Construtor.
    #  @param self The object pointer.
    #  @param hiLeveMod Hi level model in which the analog command will be added.
    #  @param name Name of the current source electrical pin.
    #  @param value Real expression holding the inital voltage.
    #  @param gnd Electrical representing the ground reference.
    #  @param rise Real expression holding the initial rise time.
    #  @param fall Real expression holding the initial fall time.
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, value, gnd, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        value = parseReal("value", value)
        if gnd != None:
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
    
    #---------------------------------------------------------------------------
    ## Set the rise and the fall times for changes in the voltage.
    #  @param self The object pointer.
    #  @param rise Real expression holding the rise time for changes in the 
    #         current.
    #  @param fall Real expression holding the fall time for changes in the 
    #         current.
    #  @return The commands to change the rise and fall times.
    #
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    #---------------------------------------------------------------------------
    ## Change the value of the current source.
    #  @param self The object pointer.
    #  @param value Teal expression holding the current.
    #  @return The commands to change the current.
    #  
    #---------------------------------------------------------------------------
    def applyI(self, value):
        checkReal("value", value)
        return self.cur.eq(value)


#-------------------------------------------------------------------------------
## IdcBus class. Child of a list. 
#  It implements aditional methods to deal with read and write operations to 
#  a bus. It also overrides the slice method, so it works similar to a slice 
#  of a bus in verilog.
#
#-------------------------------------------------------------------------------
class IdcBus(Bus):

    #---------------------------------------------------------------------------
    ## Constructor.
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def __init__(self):
        super(IdcBus, self).__init__(Idc, IdcBus)
        
    #---------------------------------------------------------------------------
    ## Set the rise and the fall times for changes in the voltage.
    #  @param self The object pointer.
    #  @param rise Real expression holding the rise time for changes in the 
    #         current.
    #  @param fall Real expression holding the fall time for changes in the 
    #         current.
    #  @return The commands to change the rise and fall times.
    #
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    #---------------------------------------------------------------------------
    ## Change the value of the current source.
    #  @param self The object pointer.
    #  @param value Real expression holding the current.
    #  @return The commands to change the current.
    #  
    #---------------------------------------------------------------------------
    def applyI(self, value):
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyI(value))
        return ans
        

#-------------------------------------------------------------------------------
## Smu class. Child of Electrical implementing aditional features in order to 
#  work as a Source Measure Unit
#
#-------------------------------------------------------------------------------
class Smu(Electrical):

    #---------------------------------------------------------------------------
    ## Construtor.
    #  @param self The object pointer.
    #  @param hiLeveMod Hi level model in which the analog command will be added.
    #  @param name Name of the smu electrical pin.
    #  @param volt Real expression holding the inital voltage.
    #  @param minCur Real expression holding the inital minimum current.
    #  @param maxCur Real expression holding the inital maximum current.
    #  @param res Real expression holding the resitance.
    #  @param gnd Electrical representing the ground reference.
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, volt, minCur, maxCur, res, gnd): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        volt = parseReal("volt", volt)
        minCur = parseReal("minCur", minCur)
        maxCur = parseReal("maxCur", maxCur)
        res = parseReal("res", res)
        if gnd != None:
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
    
    #---------------------------------------------------------------------------
    ## Configure the smu as current limited voltage source and apply the desired
    #  voltage.
    #  @param self The object pointer.
    #  @param value Real expression holding the voltage to be applied.
    #  @param limit Real expression holding the current limit.
    #  @return The commands to configure the Smu in voltage mode.
    #
    #---------------------------------------------------------------------------
    def applyV(self, value, limit):
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

    #---------------------------------------------------------------------------
    ## Configure the smu as voltage limited current source and apply the desired
    # current. Positive currents are sink current sources. The limit corresponds 
    # to the uppper voltage when value < 0 and to the lower voltage when value > 
    # 0.
    #  @param self The object pointer.
    #  @param value Real expression holding the current to be applied.
    #  @param limit Real expression holding the voltage limit.
    #  @return The commands to configure the Smu in current mode.
    # 
    #---------------------------------------------------------------------------
    def applyI(self, value, limit):
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

    #---------------------------------------------------------------------------
    ## Configure the resistive load.
    #  @param self The object pointer.
    #  @param value Real expression holding the value of the resistor.
    #  @return The commands to configure the Smu in resistance mode.
    # 
    #---------------------------------------------------------------------------
    def applyR(self, value):
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


#-------------------------------------------------------------------------------
## SmuBus class. Child of a list. 
#  It implements aditional methods to deal with read and write operations to 
#  a bus. It also overrides the slice method, so it works similar to a slice 
#  of a bus in verilog.
#
#-------------------------------------------------------------------------------
class SmuBus(Bus):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def __init__(self):
        super(SmuBus, self).__init__(Smu, SmuBus)
      

    #---------------------------------------------------------------------------
    ## Configure the smu as voltage limited current source and apply the desired
    # current. Positive currents are sink current sources. The limit corresponds 
    # to the uppper voltage when value < 0 and to the lower voltage when value > 
    # 0.
    #  @param self The object pointer.
    #  @param value Real expression holding the current to be applied.
    #  @param limit Real expression holding the voltage limit.
    #  @return The commands to configure the Smu in current mode.
    # 
    #---------------------------------------------------------------------------
    def applyI(self, value, limit):
        checkReal("value", value)
        checkReal("limit", limit)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyI(value, limit))
        return ans
        
    #---------------------------------------------------------------------------
    ## Configure the smu as current limited voltage source and apply the desired
    #  voltage.
    #  @param self The object pointer.
    #  @param value Real expression holding the voltage to be applied.
    #  @param limit Real expression holding the current limit.
    #  @return The commands to configure the Smu in voltage mode.
    #
    #---------------------------------------------------------------------------
    def applyV(self, value, limit):
        checkReal("value", value)
        checkReal("limit", limit)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyV(value, limit))
        return ans
        
    #---------------------------------------------------------------------------
    ## Configure the resistive load.
    #  @param self The object pointer.
    #  @param value Real expression holding the value of the resistor.
    #  @return The commands to configure the Smu in resistance mode.
    # 
    #---------------------------------------------------------------------------
    def applyR(self, value):
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyR(value))
        return ans
         
                
#-------------------------------------------------------------------------------
## DigOut class. Child of Electrical implementing aditional features in order to 
#  work as a digital output pin.
#
#-------------------------------------------------------------------------------
class DigOut(Electrical):
    
    #---------------------------------------------------------------------------
    ## Construtor
    #  @param self The object pointer
    #  @param hiLeveMod Hi level model in which the analog command will be added.
    #  @param name Name of the electrical pin.
    #  @param state Boolean expression holding the intial state of the digital 
    #         pin.
    #  @param domain electrical pin. The voltage across the digial pins will be
    #         equal to the domain when the logical state is 1.
    #  @param inCap Dummy parameter for consistency.  
    #  @param serRes Real expression holding the value of the series resistance.
    #         This value will be set at the beggining of the simulation and 
    #         can't be changed afterwards.
    #  @param gnd Electrical representing the ground reference.
    #  @param delay Real expression holding the initial delay time.
    #  @param rise Real expression holding the initial rise time.
    #  @param fall Real expression holding the initial fall time.
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, gnd, 
                 delay, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        state = parseBool("state", state)
        serRes = parseReal("serRes", serRes)
        if gnd != None:
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
        if gnd == None:
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

    #---------------------------------------------------------------------------
    ## Set the delay times of the digital output pin.
    #  @param self The object pointer.
    #  @param delay Real expression holding the delay time.
    #  @return The commands to change the delay.
    #
    #---------------------------------------------------------------------------
    def setDelay(self, delay):
        checkReal("delay", delay)
        return self.delay.eq(delay)
           
    #---------------------------------------------------------------------------
    ## Set the rise and the fall times of the digital output pin.
    #  @param self The object pointer.
    #  @param Rise Real expression holding the rise time.
    #  @param Fall Real expression holding the fall time.
    #  @return The commands to change the rise and fall times.
    #
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    #---------------------------------------------------------------------------
    ## Write a state to the digital output.
    #  @param self The object pointer.
    #  @param value Boolean expression representing the state to be written.
    #  @return The commands to change the stare of a digital pin.
    #
    #---------------------------------------------------------------------------
    def write(self, value):
        checkBool("value", value)
        return self.st.eq(value)
        
    #---------------------------------------------------------------------------
    ## Return the state of the digital output.
    #  @param self The object pointer.
    #  @return The commands to change the stare of a digital pin.
    #
    #---------------------------------------------------------------------------
    def getST(self):
        return self.st

    #---------------------------------------------------------------------------
    ## Toogle the state to the digital output.
    #  @param self The object pointer.
    #  @return The commands to change the stare of a digital pin.
    #
    #---------------------------------------------------------------------------
    def toggle(self):
        return self.st.toggle()



#-------------------------------------------------------------------------------
## DigIn class. Child of Electrical implementing aditional features in order to 
#  work as a digital input pin
#
#-------------------------------------------------------------------------------
class DigIn(Electrical):
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self The object pointer.
    #  @param hiLeveMod Hi level model in which the analog command will be added.
    #  @param name Name of the electrical pin.
    #  @param state Dummy parameter for consistency.
    #  @param domain Electrical pin. The voltage across the domain will be equal
    #         the voltage in the digial pins when the logical state is 1.
    #  @param inCap Real expression holding the value of the input capacitance. 
    #         This value will be set at the beggining of the simulation and can't 
    #         be changed afterwards.
    #  @param serRes Dummy parameter for consistency.
    #  @param gnd Electrical representing the ground reference.
    #  @param delay Dummy parameter for consistency.
    #  @param rise Dummy parameter for consistency.
    #  @param fall Dummy parameter for consistency.
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, gnd, 
                 delay, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        inCap = parseReal("inCap", inCap)
        if gnd != None:
            checkType("gnd", gnd, Electrical)
            checkNotInstance("gnd", gnd, Branch)
        super(DigIn, self).__init__(name)
        self.domain = domain
        self.gnd = gnd
        prefix = name.replace("[", "_$").replace("]", "$").replace(", ", "_")
        self.inCap = hiLevelMod.var(inCap, f"{prefix}_$inCap$")
        if self.gnd == None:
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
 
    #---------------------------------------------------------------------------
    ## Read a state from the digital input.
    #  @param self The object pointer.
    #  @return The commands to read the stare of a digital pin.
    #
    #---------------------------------------------------------------------------   
    def read(self):
        return self.diffHalfDomain > 0


#-------------------------------------------------------------------------------
## DigInOut class. Child of Electrical implementing aditional features in order 
#  to work as a digital input/output pin
#
#-------------------------------------------------------------------------------
class DigInOut(DigIn, DigOut):
    
    #---------------------------------------------------------------------------
    ## Construtor
    #  @param self The object pointer.
    #  @param hiLeveMod Hi level model in which the analog command will be added.
    #  @param name Name of the electrical pin.
    #  @param state Boolean expression holding the intial state of the digital 
    #         pin.
    #  @param domain electrical pin. The voltage across the digial pins will be
    #         equal to the domain when the logical state is 1.
    #  @param inCap Real expression holding the value of the input capacitance. 
    #         This value will be set at the beggining of the simulation and can't 
    #         be changed afterwards.
    #  @param serRes Real expression holding the value of the series resistance.
    #         This value will be set at the beggining of the simulation and 
    #         can't be changed afterwards.
    #  @param gnd Electrical representing the ground reference.
    #  @param delay Real expression holding the initial delay time.
    #  @param rise Real expression holding the initial rise time.
    #  @param fall Real expression holding the initial fall time.
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, gnd, 
                 delay, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        state = parseBool("state", state)
        serRes = parseReal("serRes", serRes)
        inCap = parseReal("inCap", inCap) 
        if gnd != None:
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
        if gnd == None:
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

    #---------------------------------------------------------------------------
    ## Set the pin at hiz in order to use the read function.
    #  @param self The object pointer.
    #  @return The commands to change the inOut pin to hiZ (input).
    #
    #---------------------------------------------------------------------------
    def hiZ(self):
        return self.res.eq(1e12)

    #---------------------------------------------------------------------------
    ## Set the pin to low impedance in order to use the write function
    #  @param self The object pointer.
    #  @return The commands to change the inOut pin to lowZ (output).
    #
    #---------------------------------------------------------------------------
    def lowZ(self):
        return self.res.eq(self.serRes)

               
#-------------------------------------------------------------------------------
## DigBusOut class. Child of a list. It implements aditional methods to deal with
#  read and write operations to a bus. It also overrides the slice method, so
#  it works similar to a slice of a bus in verilog
#
#-------------------------------------------------------------------------------
class DigBusOut(Bus):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def __init__(self):
        super(DigBusOut, self).__init__(DigOut, DigBusOut)
 
 
    #---------------------------------------------------------------------------
    ## Set the delay times for all digital output pin.
    #  @param self The object pointer.
    #  @param delay Real expression holding the delay time.
    #  @return The commands to change the delay times.
    #
    #---------------------------------------------------------------------------
    def setDelay(self, delay):
        checkReal("delay", delay)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setDelay(delay))
        return ans
       
    #---------------------------------------------------------------------------
    ## Set the rise and the fall times of all digital output pin.
    #  @param self The object pointer.
    #  @param Rise Real expression holding the rise time.
    #  @param Fall Real expression holding the fall time.
    #  @return The commands to change the rise and fall times.
    #
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    #---------------------------------------------------------------------------
    ## Write a binary to the digital output bus.
    #  @param self The object pointer.
    #  @param value Integer expression representing the value to be written.
    #  @return The commands to write to a digital bus.
    #
    #---------------------------------------------------------------------------
    def write(self, value):
        checkInteger("value", value)
        assert len(self) <= 32 or not isinstance(value, Integer), \
               "Can't write an instance of integer to a bus wider than 32 bit"
        ans = CmdList()
        i = 1
        for pin in self:
            ans.append(pin.write(Bool(value & i)))
            i = i << 1
        return ans

    #---------------------------------------------------------------------------
    ## Toogle all the states of a digital bus
    #  @param self The object pointer.
    #  @return The commands to change the stare of a digital pin.
    #
    #---------------------------------------------------------------------------
    def toggle(self):
        ans = CmdList()
        for pin in self:
            ans.append(pin.toggle())
        return ans
        
#-------------------------------------------------------------------------------
## DigBusIn class. Child of a list. It implements aditional methods to deal with
#  read and write operations to a bus. It also overrides the slice method, so
#  it works similar to a slice of a bus in verilog
#
#-------------------------------------------------------------------------------
class DigBusIn(Bus):

    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def __init__(self):  
        super(DigBusIn, self).__init__(DigIn, DigBusIn)
            
    #---------------------------------------------------------------------------
    ## Read a binary from the digital input bus.
    #  @param self The object pointer.
    #  @param signed Read as signed if True and unsigned otherwise.
    #  @return The commands to read a digital bus as binary.
    #
    #---------------------------------------------------------------------------   
    def read(self, signed = False):
        assert len(self) <= 32, "Can't read a bus wider than 32 bit"
        assert len(self) <= 31 or signed, \
               "Can't read a bus wider than 31 bit as unsigned"
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


#-------------------------------------------------------------------------------
## DigBusInOut class. Child of a list. It implements aditional methods to deal 
#  with read and write operations to a bus. It also overrides the slice method, 
#  so it works similar to a slice of a bus in verilog
#
#-------------------------------------------------------------------------------
class DigBusInOut(DigBusIn, DigBusOut):
 
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def __init__(self):   
        super(DigBusOut, self).__init__(DigInOut, DigBusInOut)

    #---------------------------------------------------------------------------
    ## Set the pins at hiz in order to use the read function.
    #  @param self The object pointer.
    #  @return The commands to change the inOut pin to hiZ (input).
    #
    #---------------------------------------------------------------------------
    def hiZ(self):
        ans = CmdList()
        for pin in self:
            ans.append(pin.hiZ())
        return ans

    #---------------------------------------------------------------------------
    ## Set the pins to low impedance in order to use the write function
    #  @param self The object pointer.
    #  @return The commands to change the inOut pin to lowZ (output).
    #
    #---------------------------------------------------------------------------
    def lowZ(self):
        ans = CmdList()
        for pin in self:
            ans.append(pin.lowZ())
        return ans


#-------------------------------------------------------------------------------
## Sw class. Switch between two nodes. 
#
#-------------------------------------------------------------------------------
class Sw():
    
    #---------------------------------------------------------------------------
    ## Construtor
    #  @param self The object pointer.
    #  @param hiLeveMod Hi level model in which the analog command will be added.
    #  @param pin1 First node
    #  @param pin2 Second node
    #  @param cond Real expression representing the initial switch conductance
    #  @param rise Real expression representing the rise time for changes in the 
    #         conductance
    #  @param fall Real expression representing the fall time for changes in the 
    #         conductance
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, pin1, pin2, cond, rise, fall):
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

    #---------------------------------------------------------------------------
    ## Set the rise and the fall times of all digital output pin.
    #  @param self The object pointer.
    #  @param Rise Real expression holding the rise time.
    #  @param Fall Real expression holding the fall time.
    #  @return The commands to change the rise and fall times.
    #
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    #---------------------------------------------------------------------------
    ## Set the conductance
    #  @param self The object pointer.
    #  @param cond Real expression holding the conductance value.
    #  @return The commands to change the conductance.
    #
    #---------------------------------------------------------------------------
    def setCond(self, cond):
        checkReal("cond", cond)
        return self.cond.eq(cond)


#-------------------------------------------------------------------------------
## Clock class.
# 
#-------------------------------------------------------------------------------
class Clock():
    
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param self The object pointer.
    #  @param hiLeveMod Hi level model in which the analog command will be added.
    #  @param pin DigIn or DigInOut
    #
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, pin):
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

    #---------------------------------------------------------------------------
    ## Turn the clock generator on
    #  @param self The object pointer.
    #  @param frequency frequency of the clock generator.
    #
    #---------------------------------------------------------------------------
    def on(self, frequency):
        checkReal("frequency", frequency)
        return CmdList(
            self.halfPeriod.eq(0.5/frequency),
            self.isOn.eq(True),
            self.pin.toggle(),
            self.time.eq(abstime + self.halfPeriod)
        )

    #---------------------------------------------------------------------------
    ## Turn the clock generator off
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def off(self):
        return self.isOn.eq(False)


#-------------------------------------------------------------------------------
## HiLevelMod class. Child of the module class in the veriloA module. It 
#  provides aditional methods for dealing with digital bus, current sources, 
#  voltage sources, clocks and switches
#
#-------------------------------------------------------------------------------
class HiLevelMod(Module):
  
    #---------------------------------------------------------------------------
    ## Constructor 
    #  @param self The object pointer.
    #  @param tbName Name of the test bench.
    #  @param timeTol Time tolerances for the timer.
    #
    #---------------------------------------------------------------------------
    def __init__(self, tbName, timeTol = None):
        super(HiLevelMod, self).__init__(tbName)
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
                    
    #---------------------------------------------------------------------------
    ## Add variable to the module. Also, the intial value of the variable will 
    #  be set during the static analysis and the initial step of transient.
    #  The type of the variable will be compatible with the type of the initial
    #  value.
    #  @param self The object pointer.
    #  @param name Name of the variable.
    #  @param value Initial value. Default is 0.
    #  @return a variable class.
    #
    #---------------------------------------------------------------------------
    def var(self, value = 0, name = ""):
        value = parseNumber("value", value)
        ans = super(HiLevelMod, self).var(type(value), name)           
        self.dcCmdList.append(ans.eq(value))
        return ans

    #---------------------------------------------------------------------------
    ## Return a marker object.
    #  @param self The object pointer.
    #  @param name Name of the marker.
    #  @param riseFall Rise and fall times of the marker pin. Default is 100ps.
    #  @return Marker class.
    #
    #---------------------------------------------------------------------------
    def marker(self, name, riseFall = 50e-12):
        markerObj = Marker(self, name, riseFall)
        self.markers.append(markerObj)
        return markerObj
        
    #---------------------------------------------------------------------------
    ## Return a DigIn, DigOut, or DigInOut object. A DigBusIn, DigBusOut or
    #  DigBusInOut will be returned if width > 0.
    #  @param self The object pointer.
    #  @param domain electrical pin. The voltage across the digial pins will be
    #         equal to the domain when the logical state is 1.
    #  @param name Name of the electrical pin.
    #  @param value Integer expression holding the intial value of the digital 
    #         pin.
    #  @param width If width is greather than 1, It returns a bus.
    #  @param direction It can be internal, input, output, or inout.
    #  @param inCap Real expression holding the value of the input capacitance. 
    #         This value will be set at the beggining of the simulation and 
    #         can't be changed afterwards.
    #  @param serRes Real expression holding the value of the series resistance. 
    #         This value will be set at the beggining of the simulation and 
    #         can't be changed afterwards.
    #  @param gnd Electrical representing the ground reference.
    #  @param delay Real expression holding the initial delay time.    
    #  @param rise Real expression holding the initial rise time.
    #  @param fall Real expression holding the initial fall time.
    #  @return DigIn, DigOut, or DigInOut object. A DigBusIn, DigBusOut or
    #          DigBusInOut will be returned if width > 0.
    #
    #---------------------------------------------------------------------------
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

    #---------------------------------------------------------------------------
    ## switch
    #  @param self The object pointer.
    #  @param pin1 First node (Electrical)
    #  @param pin2 Second node (Electrical)
    #  @param cond Initial switch conductance. Default is 0S.
    #  @param rise Rise time for changes in the conductance. Default is 1us.
    #  @param fall Fall time for changes in the conductance. Default is 1us.
    #  @return a Sw class.
    #
    #---------------------------------------------------------------------------
    def sw(self, pin1, pin2, cond = 0.0, rise = 1e-6, fall = 1e-6):
        checkInstance("pin1", pin1, Electrical)
        checkInstance("pin2", pin2, Electrical)
        checkReal("cond", cond)
        checkReal("rise", rise)
        checkReal("fall", fall)
        return Sw(self, pin1, pin2, cond, rise, fall)
        
    #---------------------------------------------------------------------------
    ## Build a clock model using a digital pin
    #  @param self The object pointer.
    #  @param pin DigIn or DigInOut.
    #  @return a Clock class.
    #
    #---------------------------------------------------------------------------
    def clock(self, pin):
        checkInstance("pin", pin, DigOut)
        return Clock(self, pin)

    #---------------------------------------------------------------------------
    ## Return a Smu object or a SmuBus object if width > 1.
    #  @param self The object pointer.
    #  @param name Name of the smu electrical pin.
    #  @param width If width is greather than 1, It returns a SmuBus.
    #  @param direction It can be internal, input, output, or inout.
    #  @param volt Real expression holding the inital voltage.
    #  @param minCur Real expression holding the inital minimum current.
    #  @param maxCur Real expression holding the inital maximum current.
    #  @param res Real expression holding the resitance.
    #  @return Smu or SmuBus depending on the width. 
    #  @param gnd Electrical representing the ground reference. 
    #
    #---------------------------------------------------------------------------
    def smu(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            volt = 0, 
            minCur = 0, 
            maxCur = 0, 
            res = 1e12,
            gnd = None): 
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
        
    #---------------------------------------------------------------------------
    ## Return a Vdc object or a VdcBus object if width > 1.
    #  @param self The object pointer.
    #  @param name Name of the voltage source.
    #  @param width If width is greather than 1, It returns a list.
    #  @param direction It can be internal, input, output, or inout.
    #  @param value Real expression holding the inital value.
    #  @param gnd Electrical representing the ground reference.
    #  @param rise Real expression holding the initial rise time.
    #  @param fall Real expression holding the initial fall time.
    #  @return Vdc or VdcBus depending on the width. 
    #
    #---------------------------------------------------------------------------
    def vdc(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            value = 0,
            gnd = None,
            rise = 1e-6,
            fall = 1e-6):
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

    #---------------------------------------------------------------------------
    ## Return a Idc object or a IdcBus object if width > 1.
    #  @param self The object pointer.
    #  @param name Name of the voltage source.
    #  @param width If width is greather than 1, It returns a list.
    #  @param direction It can be internal, input, output, or inout.
    #  @param value Real expression holding the inital value.
    #  @param gnd Electrical representing the ground reference.
    #  @param rise Real expression holding the initial rise time.
    #  @param fall Real expression holding the initial fall time.
    #  @return Idc or IdcBus depending on the width. 
    #
    #---------------------------------------------------------------------------
    def idc(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            value = 0,
            gnd = None,
            rise = 1e-6,
            fall = 1e-6):
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

    #---------------------------------------------------------------------------
    ## Sequence. Do not use it! Use Seq instead.
    #  @param cmdsIn list of commands to be processed.
    #  @return The list of remaining commands to be processed.
    #
    #---------------------------------------------------------------------------
    def seqNested(self, cmdsIn):
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
                raise Exception("You can't have a Case inside a seq")
                                                       
            #Found a case
            elif isinstance(cmd, Mark):
                raise Exception( ("You can't have conditional executed mark"
                                  "or marks inside command lists") )

            #The commands doesn't require special handling. Add it to the list.
            else:
                cmds.append(cmd)
                
        return cmds

    #---------------------------------------------------------------------------
    ## Sequence
    #  @param cond condition to run the sequence.
    #  @return function that accepts variable number of commands to be added to
    #  the sequence.
    #
    #---------------------------------------------------------------------------
    def seq(self, cond):
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
            assert len(args) > 0, "Sequence can be empty"
            for cmd in args:
                assert isinstance(cmd, Cmd) and \
                       not isinstance(cmd, WaitAnalogEvent), (f"Command {i}"
                       " must be an instance of Cmd and can't be and instance "
                       "of WaitAnalogEvent")
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
            
    #---------------------------------------------------------------------------
    ## Return the equations in a format that can be imported by the maestro view
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def getEqs(self):
        ans = ["Test,Name,Type,Output,Plot,Save,Spec"]
        for mark in self.markers:
            eqs = mark.getEqs()
            name = mark.getName()
            for key in eqs.keys():
                ans.append(f"{name},{name}_{key},expr,{eqs[key]},t,,")
        return "\n".join(ans) 
            

    #---------------------------------------------------------------------------
    ## Return a ocean script that add equations to the opened session of adexl
    #  @param self The object pointer.
    #
    #---------------------------------------------------------------------------
    def getOcn(self):
        ans = ["session = axlGetWindowSession()"]
        for mark in self.markers:
            eqs = mark.getEqs()
            name = mark.getName()
            for key in eqs.keys():
                eq = eqs[key].replace('"', '\\"')
                ans.append( (f"axlAddOutputExpr(session {name} {name}_{key} "
                             f"?expr {eq} ?plot t)") )
        return "\n".join(ans) 

