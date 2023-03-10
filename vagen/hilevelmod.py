## @package tbveriloga
#  Test benches in veriloga
#   
#  @author  Rodrigo Pedroso Mendes
#  @version V1.0
#  @date    14/02/23 13:37:31
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
# Create a child class of command.
# This class of commands are responsible for marking a specific event
#-------------------------------------------------------------------------------
class Mark(Cmd):

    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # cmd - command
    #---------------------------------------------------------------------------
    def __init__(self, cmd):
        checkInstance("cmd", cmd, Cmd)
        self.cmd = cmd

    #---------------------------------------------------------------------------
    # return the command
    #---------------------------------------------------------------------------
    def getCmd(self):
        return self.cmd

    #---------------------------------------------------------------------------
    # Dummy method
    #---------------------------------------------------------------------------        
    def __str__(self):
        #TODO: Find a better way to fix this
        raise Exception("Mark doesn't have string representation")

    #---------------------------------------------------------------------------
    # Dummy method
    #---------------------------------------------------------------------------        
    def getVA(self, padding):
        #TODO: Find a better way to fix this
        raise Exception("Mark can't be outside seq")


#-------------------------------------------------------------------------------
# Marker class. 
# Responsible for flipping the state of one variable to mark events and 
# generates cadance equations that return the time of the events
#-------------------------------------------------------------------------------
class Marker():

    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # name - name of the marker
    # riseFall - rise and fall times of the marker pin
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, riseFall):
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        riseFall = parseReal("riseFall", riseFall)
        self.name = name
        self.markList = []
        self.markerPin  = hiLevelMod.electrical("MARK_" + name, \
                                               direction = "output")
        self.markSt     = hiLevelMod.var(Bool(False), "_$markSt_" + name)         
        hiLevelMod.endAnalog(
            self.markerPin.vCont(transition(Real(self.markSt), 0, riseFall, 
                                                                  riseFall))
        )
        
    #---------------------------------------------------------------------------
    # return the  name of the marker
    #---------------------------------------------------------------------------
    def getName(self):
        return self.name
        
    #---------------------------------------------------------------------------
    # mark a particular event by flipping the  internal variable
    # Parameters:
    # name - name of the event
    #---------------------------------------------------------------------------
    def mark(self, name):
        checkType("name", name, str)
        self.markList.append(name)
        return Mark(self.markSt.toggle())

    #---------------------------------------------------------------------------
    # Force the internal variable low. You shouldn't use because it will 
    # break the synchronism between the cadence equations and the events. 
    # It was implemented for usage in specific power down conditions only.
    #---------------------------------------------------------------------------
    def low(self): 
        return Mark(self.markSt.eq(False))

    #---------------------------------------------------------------------------
    # Force the internal variable high. You shouldn't use because it will 
    # break the synchronism between the cadence equations and the events. 
    # It was implemented for usage in specific power down conditions only.
    #---------------------------------------------------------------------------
    def high(self, name):
        return Mark(self.markSt.eq(True))

    #---------------------------------------------------------------------------
    # Return a list with the cadence equations for the marker     
    # Not implemented yet
    #---------------------------------------------------------------------------
    def getEqs(self):
        ans = {}
        for i in range(0, len(self.markList)):
            ans[self.markList[i]] = 'cross(getData("/MARK_' + self.name + '" '+\
                                    '?result "tran") 0.5 ' +\
                                    '{:d} "either" nil nil)'.format(i + 1)
        return ans
        

#-------------------------------------------------------------------------------
# Create a child class of command.
# This class of commands are responsible for wating a specific signal before
# going to next state of the test sequence state machine 
#-------------------------------------------------------------------------------
class WaitSignal(Cmd):

    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # evnt - event to be waited for
    #---------------------------------------------------------------------------
    def __init__(self, evnt):
        checkInstance("evnt", evnt, Event)
        self.evnt = evnt
        super(WaitSignal, self).__init__("")

    #---------------------------------------------------------------------------
    # return the event that triggers the next state
    #---------------------------------------------------------------------------
    def getEvnt(self):
        return self.evnt
        
    #---------------------------------------------------------------------------
    # Dummy method
    #---------------------------------------------------------------------------        
    def __str__(self):
        #TODO: Find a better way to fix this
        raise Exception("Wait doesn't have string representation")

    #---------------------------------------------------------------------------
    # Dummy method
    #---------------------------------------------------------------------------        
    def getVA(self, padding):
        #TODO: Find a better way to fix this
        raise Exception("Wait can't be outside seq")


#-------------------------------------------------------------------------------
# Create a child class of command.
# This class of commands are responsible for wating a delay before
# going to next state of the test sequence state machine 
#-------------------------------------------------------------------------------
class WaitUs(Cmd):

    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # delay - real expression holding the delay to be waited for
    #---------------------------------------------------------------------------
    def __init__(self, delay):
        checkReal("delay", delay)
        self.delay = delay
        super(WaitUs, self).__init__("")

    #---------------------------------------------------------------------------
    # return the delay expression
    #---------------------------------------------------------------------------
    def getDelay(self):
        return self.delay
        
    #---------------------------------------------------------------------------
    # Dummy method
    #---------------------------------------------------------------------------        
    def __str__(self):
        #TODO: Find a better way to fix this
        raise Exception("Wait doesn't have string representation")

    #---------------------------------------------------------------------------
    # Dummy method
    #---------------------------------------------------------------------------        
    def getVA(self, padding):
        #TODO: Find a better way to fix this
        raise Exception("Wait can't be outside seq")


#-------------------------------------------------------------------------------
# DigBus. Child of a list. It implements aditional methods to deal with
# read and write operations to a bus. It also overrides the slice method, so
# it works similar to a slice of a bus in verilog
#-------------------------------------------------------------------------------
class Bus(list):

    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # digType - type of the digital pin
    # digBusType - type of the bus
    #---------------------------------------------------------------------------
    def __init__(self, Type, busType):
        super(Bus, self).__init__()
        self.Type = Type
        self.busType = busType
    
    #---------------------------------------------------------------------------
    # slice override
    # Parameters:
    # key - key can be an slice or index
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
    # Append override
    # Parameters:
    # item - item to be appended to the bus
    #---------------------------------------------------------------------------
    def append(self, item):
        checkInstance("item", item, self.Type)
        super(Bus, self).append(item)
        
        
#-------------------------------------------------------------------------------
# VDC class. Child of Electrical implementing aditional features in order to 
# work as a voltage source.
#-------------------------------------------------------------------------------
class Vdc(Electrical):
    
    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # name - name of the voltage source electrical pin
    # value - real expression holding the inital voltage
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, value, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        value = parseReal("value", value)
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        super(Vdc, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$")
        self.volt = hiLevelMod.var(value, prefix + "_$value$")
        self.rise = hiLevelMod.var(rise, prefix + "_$rise$")
        self.fall = hiLevelMod.var(fall, prefix + "_$fall$")
        hiLevelMod.endAnalog(
            self.vCont(
                transition(self.volt, Real(0), self.rise, self.fall)
            )
        ) 
    
    #---------------------------------------------------------------------------
    # Set the rise and the fall times for changes in the voltage
    # Parameters:
    # rise - real expression holding the rise time for changes in the voltage
    # fall - real expression holding the fall time for changes in the voltage
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    #---------------------------------------------------------------------------
    # Change the value of the voltage source
    # Parameters:
    # value - real expression holding the votlage.
    #---------------------------------------------------------------------------
    def applyV(self, value):
        checkReal("value", value)
        return self.volt.eq(value)


#-------------------------------------------------------------------------------
# VdcBus. Child of a list. It implements aditional methods to deal with
# read and write operations to a bus. It also overrides the slice method, so
# it works similar to a slice of a bus in verilog
#-------------------------------------------------------------------------------
class VdcBus(Bus):

    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self):
        super(VdcBus, self).__init__(Vdc, VdcBus)
        
    #---------------------------------------------------------------------------
    # Set the rise and the fall times for all pins in the Bus
    # Parameters:
    # rise - real expression holding the rise time
    # fall - real expression holding the fall time
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    #---------------------------------------------------------------------------
    # Change the value of the voltage source for the entire bus
    # Parameters:
    # value - real expression holding the voltage
    #---------------------------------------------------------------------------
    def applyV(self, value):
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyV(value))
        return ans
        
        
#-------------------------------------------------------------------------------
# IDC class. Child of Electrical implementing aditional features in order to 
# work as a current source.
#-------------------------------------------------------------------------------
class Idc(Electrical):
    
    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # name - name of the current source electrical pin
    # value - real expression holding the inital current
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, value, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        value = parseReal("value", value)
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        super(Idc, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$")
        self.cur = hiLevelMod.var(value, prefix + "_$value$")
        self.rise = hiLevelMod.var(rise, prefix + "_$rise$")
        self.fall = hiLevelMod.var(fall, prefix + "_$fall$")
        hiLevelMod.endAnalog(
            self.iCont(
                transition(self.cur, Real(0), self.rise, self.fall)
            )
        ) 
    
    #---------------------------------------------------------------------------
    # Set the rise and the fall times for changes in the current
    # Parameters:
    # rise - real expression holding the rise time for changes in the current
    # fall - real expression holding the fall time for changes in the current
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    #---------------------------------------------------------------------------
    # Change the value of the current source
    # Parameters:
    # value - real expression holding the current
    #---------------------------------------------------------------------------
    def applyI(self, value):
        checkReal("value", value)
        return self.cur.eq(value)


#-------------------------------------------------------------------------------
# IdcBus. Child of a list. It implements aditional methods to deal with
# read and write operations to a bus. It also overrides the slice method, so
# it works similar to a slice of a bus in verilog
#-------------------------------------------------------------------------------
class IdcBus(Bus):

    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self):
        super(IdcBus, self).__init__(Idc, IdcBus)
        
    #---------------------------------------------------------------------------
    # Set the rise and the fall times for all pins in the Bus
    # Parameters:
    # rise - real expression holding the rise time
    # fall - real expression holding the fall time
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    #---------------------------------------------------------------------------
    # Change the value of the current source for the entire bus
    # Parameters:
    # value - real expression holding the current
    #---------------------------------------------------------------------------
    def applyI(self, value):
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyI(value))
        return ans
        

#-------------------------------------------------------------------------------
# SMU class. Child of Electrical implementing aditional features in order to 
# work as a Source Measure Unit
#-------------------------------------------------------------------------------
class Smu(Electrical):
    
    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # name - name of the current source electrical pin
    # volt - real expression holding the inital voltage
    # minCur - real expression holding the inital minimum current
    # maxCur - real expression holding the inital maximum current
    # res - real expression holding the resitance
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, volt, minCur, maxCur, res): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        volt = parseReal("volt", volt)
        minCur = parseReal("minCur", minCur)
        maxCur = parseReal("maxCur", maxCur)
        res = parseReal("res", res)
        super(Smu, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$")
        self.volt     = hiLevelMod.var(volt, prefix + "_$volt$")
        self.maxCur   = hiLevelMod.var(maxCur, prefix + "_$maxCur")
        self.minCur   = hiLevelMod.var(minCur, prefix + "_$minCur$")
        self.res      = hiLevelMod.var(res, prefix + "_$res$")
        self.vDelay   = hiLevelMod.var(Real(0), prefix + "_$vDelay$")
        self.iDelay   = hiLevelMod.var(Real(0), prefix + "_$iDelay$")
        self.rDelay   = hiLevelMod.var(Real(0), prefix + "_$rDelay$")
        self.riseFall = hiLevelMod.var(Real(1e-6), prefix + "_$riseFall$")
        voltTran      = hiLevelMod.var(Real(0), prefix + "_$voltTran$") 
        maxCurTran    = hiLevelMod.var(Real(0), prefix + "_$maxCurTran$")
        minCurTran    = hiLevelMod.var(Real(0), prefix + "_$minCurTran$")
        resTran       = hiLevelMod.var(Real(0), prefix + "_$resTran$")
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
            self.iCont(
                tanh(50*(self.v - voltTran))*
                0.5*(maxCurTran - minCurTran) + 
                0.5*(maxCurTran + minCurTran)
            ),
            self.iCont(self.v/resTran),
            self.iCont(1e-12*ddt(self.v))
        ) 
    
    #---------------------------------------------------------------------------
    # Configure the smu as current limited voltage source and apply the desired
    # voltage.
    # Parameters:
    # value - real expression holding the voltage to be applied
    # limit - real expression holding the current limit
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
            self.iDelay.eq(1e-6),
            self.rDelay.eq(1e-6),
            self.riseFall.eq(1e-6)
        )

    #---------------------------------------------------------------------------
    # Configure the smu as voltage limited current source and apply the desired
    # current. Positive currents are sink current sources. The limit corresponds 
    # to the uppper voltage when value < 0 and to the lower voltage when value > 
    # 0.
    # Parameters:
    # value - real expression holding the current to be applied
    # limit - real expression holding the voltage limit
    #---------------------------------------------------------------------------
    def applyI(self, value, limit):
        checkReal("value", value)
        checkReal("limit", limit)
        return CmdList(
            self.volt.eq(limit),
            self.maxCur.eq(0.5*(value + abs(value))),
            self.minCur.eq(0.5*(value - abs(value))),
            self.res.eq(1e4/(abs(value) + 1e-9)),
            self.vDelay.eq(1e-6),
            self.iDelay.eq(0),
            self.rDelay.eq(0),
            self.riseFall.eq(1e-6)
        )

    #---------------------------------------------------------------------------
    # Configure the resistive load.
    # Parameters:
    # value - real expression holding the value of the resistor
    #---------------------------------------------------------------------------
    def applyR(self, value):
        checkReal("value", value)
        return CmdList(
            self.volt.eq(0),
            self.maxCur.eq(0),
            self.minCur.eq(0),
            self.res.eq(value),
            self.vDelay.eq(1e-6),
            self.iDelay.eq(0),
            self.rDelay.eq(0),
            self.riseFall.eq(1e-6)
        )


#-------------------------------------------------------------------------------
# SmuBus. Child of a list. It implements aditional methods to deal with
# read and write operations to a bus. It also overrides the slice method, so
# it works similar to a slice of a bus in verilog
#-------------------------------------------------------------------------------
class SmuBus(Bus):

    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self):
        super(SmuBus, self).__init__(Smu, SmuBus)
      

    #---------------------------------------------------------------------------
    # Change the value of the current source for the entire bus
    # Parameters:
    # value - real expression holding the current to be applied
    # limit - real expression holding the voltage limit
    #---------------------------------------------------------------------------
    def applyI(self, value, limit):
        checkReal("value", value)
        checkReal("limit", limit)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyI(value, limit))
        return ans
        
    #---------------------------------------------------------------------------
    # Change the value of the current source for the entire bus
    # Parameters:
    # value - real expression holding the voltage to be applied
    # limit - real expression holding the current limit
    #---------------------------------------------------------------------------
    def applyV(self, value, limit):
        checkReal("value", value)
        checkReal("limit", limit)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyV(value, limit))
        return ans
        
    #---------------------------------------------------------------------------
    # Change the value of the current source for the entire bus
    # Parameters:
    # value - real expression holding the current
    #---------------------------------------------------------------------------
    def applyR(self, value):
        checkReal("value", value)
        ans = CmdList()
        for pin in self:
            ans.append(pin.applyR(value))
        return ans
         
                
#-------------------------------------------------------------------------------
# DigOut class. Child of Electrical implementing aditional features in order to 
# work as a digital output pin
#-------------------------------------------------------------------------------
class DigOut(Electrical):
    
    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # name - name of the electrical pin
    # state - boolean expression holding the intial state of the digital pin
    # domain - electrical pin. The voltage across the domain will be equal
    #          the voltage in the digial pins when the logical state is 1.
    # inCap - dummy parameter for consistency  
    # serRes - real expression holding the value of the series resistance. This
    #       value will be set at the beggining of the simulation and can't be
    #       changed afterwards
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        state = parseBool("state", state)
        serRes = parseReal("serRes", serRes)
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        super(DigOut, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$")
        self.st = hiLevelMod.var(state, prefix + "_$state$")
        self.serRes = hiLevelMod.var(serRes, prefix + "_$serRes$")
        self.rise = hiLevelMod.var(rise, prefix + "_$rise")
        self.fall = hiLevelMod.var(fall, prefix + "_$fall$")
        hiLevelMod.endAnalog(
            self.vCont(
                domain.v*transition(
                    ternary(self.st, 1.0, 0.0), 
                    0, 
                    self.rise, 
                    self.fall
                )
            ),
            self.vCont(self.i*self.serRes)
        ) 
   
    #---------------------------------------------------------------------------
    # Set the rise and the fall times of the digital output pin
    # Parameters:
    # rise - real expression holding the rise time
    # fall - real expression holding the fall time
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    #---------------------------------------------------------------------------
    # Write a state to the digital output
    # Parameters:
    # value - boolean expression representing the state to be written
    #---------------------------------------------------------------------------
    def write(self, value):
        checkBool("value", value)
        return self.st.eq(value)


#-------------------------------------------------------------------------------
# DigIn class. Child of Electrical implementing aditional features in order to 
# work as a digital input pin
#-------------------------------------------------------------------------------
class DigIn(Electrical):
    
    #---------------------------------------------------------------------------
    # hiLeveMod - Hi level model in which the model will be added
    # name - name of the electrical pin
    # state - dummy parameter for consistency
    # domain - electrical pin. The voltage across the domain will be equal
    #          the voltage in the digial pins when the logical state is 1.
    # inCap - real expression holding the value of the input capacitance. This
    #       value will be set at the beggining of the simulation and can't be
    #       changed afterwards
    # serRes - dummy parameter for consistency
    # rise - dummy parameter for consistency
    # fall - dummy parameter for consistency
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        inCap = parseReal("inCap", inCap)
        super(DigIn, self).__init__(name)
        self.domain = domain
        prefix = name.replace("[", "_$").replace("]", "$")
        self.inCap = hiLevelMod.var(inCap, prefix + "_$inCap$")
        hiLevelMod.endAnalog(
            self.iCont(ddt(self.v)*self.inCap)
        ) 
    
    def read(self):
        return self.v > self.domain.v/2


#-------------------------------------------------------------------------------
# DigInOut class. Child of Electrical implementing aditional features in order to 
# work as a digital input/output pin
#-------------------------------------------------------------------------------
class DigInOut(DigIn, DigOut):
    
    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # name - name of the electrical pin
    # state - boolean expression holding the intial state of the digital pin
    # domain - electrical pin. The voltage across the domain will be equal
    #          the voltage in the digial pins when the logical state is 1.
    # inCap - real expression holding the value of the input capacitance. This
    #       value will be set at the beggining of the simulation and can't be
    #       changed afterwards
    # serRes - real expression holding the value of the series resistance. This
    #       value will be set at the beggining of the simulation and can't be
    #       changed afterwards
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, name, state, domain, inCap, serRes, rise, fall): 
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        state = parseBool("state", state)
        serRes = parseReal("serRes", serRes)
        inCap = parseReal("inCap", inCap)        
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        super(DigOut, self).__init__(name)
        prefix = name.replace("[", "_$").replace("]", "$")
        self.st = hiLevelMod.var(state, prefix + "_$state$")
        self.serRes = hiLevelMod.var(serRes, prefix + "_$serRes$")
        self.inCap = hiLevelMod.var(inCap, prefix + "_$inCap$")
        self.res = hiLevelMod.var(serRes, prefix + "_$res$")
        self.rise = hiLevelMod.var(rise, prefix + "_$rise")
        self.fall = hiLevelMod.var(fall, prefix + "_$fall$")
        self.domain = domain
        pin = hiLevelMod.electrical()
        conn = Branch(pin, self)
        hiLevelMod.endAnalog(
            pin.vCont(
                domain.v*transition(
                    ternary(self.st, 1.0, 0.0), 
                    0, 
                    self.rise, 
                    self.fall
                )
            ),
            conn.vCont(
                conn.i*transition(self.res, 0, self.rise, self.fall)
            ),
            self.iCont(ddt(self.v)*self.inCap)
        ) 

    #---------------------------------------------------------------------------
    # Set the pins at hiz in order to use the read function
    #---------------------------------------------------------------------------
    def hiZ(self):
        return self.res.eq(1e12)

    #---------------------------------------------------------------------------
    # Set the pins to low impedance in order to use the write function
    #---------------------------------------------------------------------------
    def lowZ(self):
        return self.res.eq(self.serRes)

               
#-------------------------------------------------------------------------------
# DigBuOut. Child of a list. It implements aditional methods to deal with
# read and write operations to a bus. It also overrides the slice method, so
# it works similar to a slice of a bus in verilog
#-------------------------------------------------------------------------------
class DigBusOut(Bus):

    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self):
        super(DigBusOut, self).__init__(DigOut, DigBusOut)
        
    #---------------------------------------------------------------------------
    # Set the rise and the fall times for all pins in the Bus
    # Parameters:
    # rise - real expression holding the rise time
    # fall - real expression holding the fall time
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        ans = CmdList()
        for pin in self:
            ans.append(pin.setRiseFall(rise, fall))
        return ans

    #---------------------------------------------------------------------------
    # Convert the value to binary and write it to the bus
    # Parameters:
    # value - integer expression representing the value
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


#-------------------------------------------------------------------------------
# DigBuIn. Child of a list. It implements aditional methods to deal with
# read and write operations to a bus. It also overrides the slice method, so
# it works similar to a slice of a bus in verilog
#-------------------------------------------------------------------------------
class DigBusIn(Bus):

    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self):  
        super(DigBusIn, self).__init__(DigIn, DigBusIn)
            
    #---------------------------------------------------------------------------
    # Returns an Integer expression representing the convertion of binary 
    # inputs to Unsigned Integer
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
# DigBuInOut. Child of a list. It implements aditional methods to deal with
# read and write operations to a bus. It also overrides the slice method, so
# it works similar to a slice of a bus in verilog
#-------------------------------------------------------------------------------
class DigBusInOut(DigBusIn, DigBusOut):
 
    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self):   
        super(DigBusOut, self).__init__(DigInOut, DigBusInOut)

    #---------------------------------------------------------------------------
    # Set the pins at hiz in order to use the read function
    #---------------------------------------------------------------------------
    def hiZ(self):
        ans = CmdList()
        for pin in self:
            ans.append(pin.hiZ())
        return ans

    #---------------------------------------------------------------------------
    # Set the pins to low impedance in order to use the write function
    #---------------------------------------------------------------------------
    def lowZ(self):
        ans = CmdList()
        for pin in self:
            ans.append(pin.lowZ())
        return ans


#-------------------------------------------------------------------------------
# Switch between two nodes. 
#-------------------------------------------------------------------------------
class Sw():

    swCount = 1
    
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # pin1 - first node
    # pin2 - second node
    # cond - Real expression representing the initial switch conductance
    # rise - Real expression representing the rise time for changes in the 
    #        conductance
    # fall - Real expression representing the fall time for changes in the 
    #        conductance
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, pin1, pin2, cond, rise, fall):
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkInstance("pin1", pin1, Electrical)
        checkInstance("pin2", pin2, Electrical)
        cond = parseReal("cond", cond)
        rise = parseReal("rise", rise)
        fall = parseReal("fall", fall)
        prefix = "sw" + str(self.swCount)
        self.swCount = self.swCount + 1
        self.cond = hiLevelMod.var(cond, prefix + "_$cond$")
        self.rise = hiLevelMod.var(rise, prefix + "_$rise")
        self.fall = hiLevelMod.var(fall, prefix + "_$fall$")
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
    # Set the rise and the fall times of the digital output pin
    # Parameters:
    # rise - real expression holding the rise time
    # fall - real expression holding the fall time
    #---------------------------------------------------------------------------
    def setRiseFall(self, rise, fall):
        checkReal("rise", rise)
        checkReal("fall", fall)
        return CmdList(
            self.rise.eq(rise),
            self.fall.eq(fall)
        )

    #---------------------------------------------------------------------------
    # Set the conductance
    # Parameters:
    # cond - new value for the conductance
    #---------------------------------------------------------------------------
    def setCond(self, cond):
        checkReal("cond", cond)
        return self.cond.eq(cond)


#-------------------------------------------------------------------------------
# Clock using a digital pin 
#-------------------------------------------------------------------------------
class Clock():
    
    clockCount = 1
    
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # pin - digital output or inout pin
    #---------------------------------------------------------------------------
    def __init__(self, hiLevelMod, pin):
        checkInstance("hiLevelMod", hiLevelMod, HiLevelMod)
        checkInstance("pin", pin, DigOut)
        prefix = "clk" + str(self.clockCount)
        self.clockCount = self.clockCount + 1
        out = hiLevelMod.var(Bool(str(pin.st)), prefix + "_$out$")
        self.isOn = hiLevelMod.var(Bool(0), prefix + "_$isOn$")
        self.halfPeriod = hiLevelMod.var(Real(1000000), prefix + "_$halfPeriod$")
        self.time = hiLevelMod.var(Real(1000000), prefix + "_$time$")
        self.at = CmdList(
                      out.toggle(),
                      pin.write(out),
                      If(self.isOn | out)(
                          self.time.eq(abstime + self.halfPeriod)
                      )
                  )
               
        hiLevelMod.analog(
           At(Timer(*([self.time] + hiLevelMod.timeArgs)))(
               self.at
           )
        )

    #---------------------------------------------------------------------------
    # Turn the clock generator on
    #---------------------------------------------------------------------------
    def on(self, frequency):
        checkReal("frequency", frequency)
        return CmdList(
                   self.halfPeriod.eq(0.5/frequency),
                   self.isOn.eq(True),
                   self.time.eq(abstime + 1e-9)
               )

    #---------------------------------------------------------------------------
    # Turn the clock generator off
    #---------------------------------------------------------------------------
    def off(self):
        return self.isOn.eq(Bool(0))


#-------------------------------------------------------------------------------
# Child of the module class in the veriloA module. It provides aditional
# methods for dealing with digital bus, current sources, voltage sources, 
# clocks and switches
#-------------------------------------------------------------------------------
class HiLevelMod(Module):
  
    #---------------------------------------------------------------------------
    # Constructor 
    # Parameters:
    # tbName - name of the test bench
    # timeTol - time tolerances for the timer
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
    # Add variable to the module. Also, the intial value of the variable will 
    # be set during the static analysis and the initial step of transient.
    # Parameters:
    # name - name of the variable
    # value - Initial value
    #---------------------------------------------------------------------------
    def var(self, value = 0, name = ""):
        value = parseNumber("value", value)
        ans = super(HiLevelMod, self).var(type(value), name)           
        self.dcCmdList.append(ans.eq(value))
        return ans

    #---------------------------------------------------------------------------
    # Return a marker object
    # Parameters: 
    # name - name of the marker
    # riseFall - rise and fall times of the marker pin. Default is 10ps
    #---------------------------------------------------------------------------
    def marker(self, name, riseFall = 10e-9):
        markerObj = Marker(self, name, riseFall)
        self.markers.append(markerObj)
        return markerObj
        
    #---------------------------------------------------------------------------
    # Return a DigIn, DigOut, or DigInOut object. A DigBusIn, DigBusOut or
    # DigBusInOut will be returned if width > 0
    # Parameters:
    # domain - electrical pin. The voltage across the domain will be equal
    #          the voltage in the digial pins when the logical state is 1.
    # name - name of the electrical pin
    # value - integer expression holding the intial value of the digital pin
    # width - if width is greather than 1, It returns a list
    # direction - it can be internal, input, output, or inout
    # inCap - real expression holding the value of the input capacitance. This
    #       value will be set at the beggining of the simulation and can't be
    #       changed afterwards
    # serRes - real expression holding the value of the series resistance. This
    #       value will be set at the beggining of the simulation and can't be
    #       changed afterwards
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def dig(self, 
            domain, 
            name = "", 
            width = 1, 
            direction = "internal", 
            value = 0,
            inCap = 1e-12, 
            serRes = 100, 
            rise = 1e-12,
            fall = 1e-12):
        #Check the inputs
        checkInstance("domain", domain, Electrical)
        checkInteger("value", value)
        checkReal("inCap", inCap)
        checkReal("serRes", serRes)
        checkReal("rise", rise)
        checkReal("fall", fall)
        name = self.addPort(name, width, direction)
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
                                   rise, 
                                   fall))
                j = j << 1
            return bus

    #---------------------------------------------------------------------------
    # switch
    # Parameters:
    # pin1 - first node
    # pin2 - second node
    # cond - initial switch conductance. Default is 0S.
    # rise - rise time for changes in the conductance. Default is
    #        1us
    # fall - fall time for changes in the conductance. Default is
    #        1us
    #---------------------------------------------------------------------------
    def sw(self, pin1, pin2, cond = Real(0), rise=Real(1e-6), fall=Real(1e-6)):
        checkInstance("pin1", pin1, Electrical)
        checkInstance("pin2", pin2, Electrical)
        checkReal("cond", cond)
        checkReal("rise", rise)
        checkReal("fall", fall)
        return Sw(self, pin1, pin2, cond, rise, fall)
        
    #---------------------------------------------------------------------------
    # Build a clock model using a digital pin
    # Parameters:
    # pin1 - digital output or inout pin
    #---------------------------------------------------------------------------
    def clock(self, pin):
        checkInstance("pin", pin, DigOut)
        return Clock(self, pin)

    #---------------------------------------------------------------------------
    # Return a smu object or a list of smu objects if width > 0
    # Parameters:
    # hiLeveMod - Hi level model in which the model will be added
    # name - name of the current source electrical pin
    # width - if width is greather than 1, It returns a list
    # direction - it can be internal, input, output, or inout
    # volt - real expression holding the inital voltage
    # minCur - real expression holding the inital minimum current
    # maxCur - real expression holding the inital maximum current
    # res - real expression holding the resitance
    #---------------------------------------------------------------------------
    def smu(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            volt = 0, 
            minCur = 0, 
            maxCur = 0, 
            res = 1e12): 
        checkReal("volt", volt)
        checkReal("minCur", minCur)
        checkReal("maxCur", maxCur)
        checkReal("res", res)
        name = self.addPort(name, width, direction)
        if width == 1:
            return  Smu(self, name, volt, minCur, maxCur, res)
        else:
            vector = SmuBus()
            for i in range(0, width):
                vector.append(
                    Smu(self, 
                        name + "[" + str(i) + "]",
                        volt, 
                        minCur,
                        maxCur,
                        res
                    )
                )
            return vector
        
    #---------------------------------------------------------------------------
    # Return a vdc object or a list of vdc objects if width > 1
    # Parameters:
    # name - name of the voltage source
    # width - if width is greather than 1, It returns a list
    # direction - it can be internal, input, output, or inout
    # value - real expression holding the inital value
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def vdc(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            value = 0,
            rise = 0,
            fall = 0):
        checkReal("value", value)
        checkReal("rise", rise)
        checkReal("fall", fall)
        name = self.addPort(name, width, direction)
        if width == 1:
            return  Vdc(self, name, value, rise, fall)
        else:
            vBus = VdcBus()
            for i in range(0, width):
                vBus.append(
                    Vdc(self, 
                        name + "[" + str(i) + "]", 
                        value,
                        rise, 
                        fall
                    )
                )
            return vBus

    #---------------------------------------------------------------------------
    # Return a idc object or a list of idc objects if width > 0
    # Parameters:
    # name - name of the current source
    # width - if width is greather than 1, It returns a list
    # direction - it can be internal, input, output, or inout
    # value - real expression holding the inital value
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def idc(self, 
            name = "", 
            width = 1, 
            direction = "internal", 
            value = 0,
            rise = 0,
            fall = 0):
        checkReal("value", value)
        checkReal("rise", rise)
        checkReal("fall", fall)
        name = self.addPort(name, width, direction)
        if width == 1:
            return  Idc(self, name, value, rise, fall)
        else:
            iBus = IdcBus()
            for i in range(0, width):
                iBus.append(
                    Idc(self, 
                        name + "[" + str(i) + "]", 
                        value,
                        rise, 
                        fall
                    )
                )
            return iBus

    #---------------------------------------------------------------------------
    # Sequence
    # Parameters:
    # cmds - command list
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
                raise Exception("You can't have conditional executed mark" +
                                "or marks inside command lists")

            #The commands doesn't require special handling. Add it to the list.
            else:
                cmds.append(cmd)
                
        return cmds

    #---------------------------------------------------------------------------
    # Sequence
    # Parameters:
    # *args - variable number of commands
    #---------------------------------------------------------------------------
    def seq(self, cond):
        def func(*args):
            self.nState   = 0
            self.time     = self.var(Real(1e6),  "_$evntTime_" + str(self.nSeq)) 
            self.state    = self.var(Integer(0), "_$state_"    + str(self.nSeq)) 
            self.runSt    = self.var(Bool(True), "_$runSt_"    + str(self.nSeq)) 
            self.eventId  = self.var(Integer(0), "_$eventId_"  + str(self.nSeq)) 
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
                       not isinstance(cmd, WaitAnalogEvent), "Command " +str(i)+\
                       " must be an instance of Cmd and can't be and instance "+\
                       "of WaitAnalogEvent"
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
    # Return the equations in a format that can be imported by the maestro view
    #---------------------------------------------------------------------------
    def getEqs(self):
        ans = "Test,Name,Type,Output,Plot,Save,Spec\n"
        for mark in self.markers:
            eqs = mark.getEqs()
            name = mark.getName()
            for key in eqs.keys():
                ans = ans + "{:s},{:s},expr,{:s},t,,\n".format(name, 
                                                               name + "_" + key, 
                                                               eqs[key])
        return ans 
            

    #---------------------------------------------------------------------------
    # Return a ocean script that add equations to the opened session of adexl
    #---------------------------------------------------------------------------
    def getOcn(self):
        ans = "session = axlGetWindowSession()\n"
        for mark in self.markers:
            eqs = mark.getEqs()
            name = mark.getName()
            for key in eqs.keys():
                ans = ans + "axlAddOutputExpr(session " +\
                      '"{:s}" "{:s}" ?expr "{:s}" ?plot t)\n'.format(name, 
                      name + "_" + key, eqs[key].replace('"', '\\"'))
        return ans 

