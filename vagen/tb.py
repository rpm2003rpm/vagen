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
# Marker class. 
# Responsible for flipping the state of one variable to mark events and 
# generates cadance equations that return the time of the events
#-------------------------------------------------------------------------------
class Marker():

    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # name - name of the marker
    # var - Boolen variable to be fliped at the events
    #---------------------------------------------------------------------------
    def __init__(self, name, var):
        checkType("name", name, str)
        checkInstance("var", var, BoolVar)
        self.name = name
        self.markList = []
        self.var = var

    #---------------------------------------------------------------------------
    # mark a particular event by flipping the  internal variable
    # Parameters:
    # name - name of the event
    #---------------------------------------------------------------------------
    def mark(self, name):
        checkType("name", name, str)
        self.markList.append(name)
        return self.var.equal(~self.var)

    #---------------------------------------------------------------------------
    # Force the internal variable low. You shouldn't use because it will 
    # break the synchronism between the cadence equations and the events. 
    # It was implemented for usage in specific power down conditions only.
    #---------------------------------------------------------------------------
    def low(self): 
        return self.var.equal(Bool(0))

    #---------------------------------------------------------------------------
    # Force the internal variable high. You shouldn't use because it will 
    # break the synchronism between the cadence equations and the events. 
    # It was implemented for usage in specific power down conditions only.
    #---------------------------------------------------------------------------
    def high(self, name):
        return self.var.equal(Bool(1))

    #---------------------------------------------------------------------------
    # Return a list with the cadence equations for the marker     
    # Not implemented yet
    #---------------------------------------------------------------------------
    def getCds(self):
        pass
        

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
    # Return the VA verilog command
    # Parameters:
    # padding - dummy for consistency 
    #---------------------------------------------------------------------------        
    def getVA(self, padding):
        #TODO: Find a better way to fix this
        raise Exception("You can't add WaitSignal inside command blocks!")


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
        checkInstance("delay", delay, RealOp)
        self.delay = delay
        super(WaitUs, self).__init__("")

    #---------------------------------------------------------------------------
    # return the delay expression
    #---------------------------------------------------------------------------
    def getDelay(self):
        return self.delay
        
    #---------------------------------------------------------------------------
    # Return the VA verilog command
    # Parameters:
    # padding - dummy for consistency 
    #---------------------------------------------------------------------------        
    def getVA(self, padding):
        #TODO: Find a better way to fix this
        raise Exception("You can't add WaitUs inside command blocks!")


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
    # tb - test bench in which the model will be added
    # name - name of the voltage source electrical pin
    # value - real expression holding the inital voltage
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def __init__(self, tb, name, value, rise, fall): 
        checkInstance("tb", tb, Tb)
        checkType("name", name, str)
        checkInstance("value", value, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        super(Vdc, self).__init__(name)
        self.volt = tb.var(value)
        self.rise = tb.var(rise)
        self.fall = tb.var(fall)
        tb.endAnalog(
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
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        return CmdList(
            self.rise.equal(rise),
            self.fall.equal(fall)
        )

    #---------------------------------------------------------------------------
    # Change the value of the voltage source
    # Parameters:
    # value - real expression holding the votlage.
    #---------------------------------------------------------------------------
    def applyV(self, value):
        checkInstance("value", value, RealOp)
        return self.volt.equal(value)


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
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
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
        checkInstance("value", value, RealOp)
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
    # tb - test bench in which the model will be added
    # name - name of the current source electrical pin
    # value - real expression holding the inital current
    # rise - real expression holding the initial rise time
    # fall - real expression holding the initial fall time
    #---------------------------------------------------------------------------
    def __init__(self, tb, name, value, rise, fall): 
        checkInstance("tb", tb, Tb)
        checkType("name", name, str)
        checkInstance("value", value, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        super(Idc, self).__init__(name)
        self.cur  = tb.var(value)
        self.rise = tb.var(rise)
        self.fall = tb.var(fall)
        tb.endAnalog(
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
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        return CmdList(
            self.rise.equal(rise),
            self.fall.equal(fall)
        )

    #---------------------------------------------------------------------------
    # Change the value of the current source
    # Parameters:
    # value - real expression holding the current
    #---------------------------------------------------------------------------
    def applyI(self, value):
        checkInstance("value", value, RealOp)
        return self.cur.equal(value)


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
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
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
        checkInstance("value", value, RealOp)
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
    # tb - test bench in which the model will be added
    # name - name of the current source electrical pin
    # volt - real expression holding the inital voltage
    # minCur - real expression holding the inital minimum current
    # maxCur - real expression holding the inital maximum current
    # res - real expression holding the resitance
    #---------------------------------------------------------------------------
    def __init__(self, tb, name, volt, minCur, maxCur, res): 
        checkInstance("tb", tb, Tb)
        checkType("name", name, str)
        checkInstance("volt", volt, RealOp)
        checkInstance("minCur", minCur, RealOp)
        checkInstance("maxCur", maxCur, RealOp)
        checkInstance("res", res, RealOp)
        super(Smu, self).__init__(name)
        self.volt     = tb.var(volt)
        self.maxCur   = tb.var(maxCur)
        self.minCur   = tb.var(minCur)
        self.res      = tb.var(res)
        self.vDelay   = tb.var(Real(0))
        self.iDelay   = tb.var(Real(0))
        self.rDelay   = tb.var(Real(0))
        self.riseFall = tb.var(Real(1e-6))
        voltTran      = tb.var(Real(0)) 
        maxCurTran    = tb.var(Real(0))
        minCurTran    = tb.var(Real(0))
        resTran       = tb.var(Real(0))
        tb.endAnalog(
            voltTran.equal(
                transition(
                    self.volt, 
                    self.vDelay,
                    self.riseFall, 
                    self.riseFall
                )
            ), 
            maxCurTran.equal(
                transition(
                    self.maxCur, 
                    self.iDelay,
                    self.riseFall, 
                    self.riseFall
                )
            ),
            minCurTran.equal(
                transition(
                    self.minCur, 
                    self.iDelay,
                    self.riseFall, 
                    self.riseFall
                )
            ),
            resTran.equal(
                transition(
                    self.res, 
                    self.rDelay,
                    self.riseFall, 
                    self.riseFall)),
            self.iCont(
                tanh(Real(50)*(self.v - voltTran))*
                Real(0.5)*(maxCurTran - minCurTran) + 
                Real(0.5)*(maxCurTran + minCurTran)
            ),
            self.iCont(self.v/resTran),
            self.iCont(Real(1e-12)*ddt(self.v))
        ) 
    
    #---------------------------------------------------------------------------
    # Configure the smu as current limited voltage source and apply the desired
    # voltage.
    # Parameters:
    # value - real expression holding the voltage to be applied
    # limit - real expression holding the current limit
    #---------------------------------------------------------------------------
    def applyV(self, value, limit):
        checkInstance("value", value, RealOp)
        checkInstance("limit", limit, RealOp)
        return CmdList(
            self.volt.equal(value),
            self.maxCur.equal(abs(limit)),
            self.minCur.equal(-abs(limit)),
            self.res.equal(Real(1e4)/(abs(limit) + Real(1e-9))),
            self.vDelay.equal(Real(0)),
            self.iDelay.equal(Real(1e-6)),
            self.rDelay.equal(Real(1e-6)),
            self.riseFall.equal(Real(1e-6))
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
        checkInstance("value", value, RealOp)
        checkInstance("limit", limit, RealOp)
        return CmdList(
            self.volt.equal(limit),
            self.maxCur.equal(Real(0.5)*(value + abs(value))),
            self.minCur.equal(Real(0.5)*(value - abs(value))),
            self.res.equal(Real(1e4)/(abs(value) + Real(1e-9))),
            self.vDelay.equal(Real(1e-6)),
            self.iDelay.equal(Real(0)),
            self.rDelay.equal(Real(0)),
            self.riseFall.equal(Real(1e-6))
        )

    #---------------------------------------------------------------------------
    # Configure the resistive load.
    # Parameters:
    # value - real expression holding the value of the resistor
    #---------------------------------------------------------------------------
    def applyR(self, value):
        checkInstance("value", value, RealOp)
        return CmdList(
            self.volt.equal(Real(0)),
            self.maxCur.equal(Real(0)),
            self.minCur.equal(Real(0)),
            self.res.equal(value),
            self.vDelay.equal(Real(1e-6)),
            self.iDelay.equal(Real(0)),
            self.rDelay.equal(Real(0)),
            self.riseFall.equal(Real(1e-6))
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
        checkInstance("value", value, RealOp)
        checkInstance("limit", limit, RealOp)
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
        checkInstance("value", value, RealOp)
        checkInstance("limit", limit, RealOp)
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
        checkInstance("value", value, RealOp)
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
    # tb - test bench in which the model will be added
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
    def __init__(self, tb, name, state, domain, inCap, serRes, rise, fall): 
        checkInstance("tb", tb, Tb)
        checkType("name", name, str)
        checkInstance("state", state, BoolOp)
        checkInstance("domain", domain, Electrical)
        checkInstance("serRes", serRes, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        super(DigOut, self).__init__(name)
        self.st = tb.var(state)
        self.serRes = tb.var(serRes)
        self.rise = tb.var(rise)
        self.fall = tb.var(fall)
        tb.endAnalog(
            self.vCont(
                domain.v*transition(
                    ternary(self.st, Real(1), Real(0)), 
                    Real(0), 
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
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        return CmdList(
            self.rise.equal(rise),
            self.fall.equal(fall)
        )

    #---------------------------------------------------------------------------
    # Write a state to the digital output
    # Parameters:
    # value - boolean expression representing the state to be written
    #---------------------------------------------------------------------------
    def write(self, value):
        checkInstance("value", value, BoolOp)
        return self.st.equal(value)


#-------------------------------------------------------------------------------
# DigIn class. Child of Electrical implementing aditional features in order to 
# work as a digital input pin
#-------------------------------------------------------------------------------
class DigIn(Electrical):
    
    #---------------------------------------------------------------------------
    # tb - test bench in which the model will be added
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
    def __init__(self, tb, name, state, domain, inCap, serRes, rise, fall): 
        checkInstance("tb", tb, Tb)
        checkType("name", name, str)
        checkInstance("domain", domain, Electrical)
        checkInstance("inCap", inCap, RealOp)
        super(DigIn, self).__init__(name)
        self.domain = domain
        self.inCap = tb.var(inCap)
        tb.endAnalog(
            self.iCont(ddt(self.v)*self.inCap)
        ) 
    
    def read(self):
        return self.v > self.domain.v/Real(2)


#-------------------------------------------------------------------------------
# DigInOut class. Child of Electrical implementing aditional features in order to 
# work as a digital input/output pin
#-------------------------------------------------------------------------------
class DigInOut(DigIn, DigOut):
    
    #---------------------------------------------------------------------------
    # Construtor
    # Parameters:
    # tb - test bench in which the model will be added
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
    def __init__(self, tb, name, state, domain, inCap, serRes, rise, fall): 
        checkInstance("tb", tb, Tb)
        checkType("name", name, str)
        checkInstance("state", state, BoolOp)
        checkInstance("domain", domain, Electrical)
        checkInstance("inCap", inCap, RealOp)
        checkInstance("serRes", serRes, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        super(DigOut, self).__init__(name)
        self.st = tb.var(state)
        self.inCap = tb.var(inCap)
        self.serRes = tb.var(serRes)
        self.res = tb.var(serRes)
        self.rise = tb.var(rise)
        self.fall = tb.var(fall)
        self.domain = domain
        pin = tb.electrical()
        conn = Branch(pin, self)
        tb.endAnalog(
            pin.vCont(
                domain.v*transition(
                    ternary(self.st, Real(1), Real(0)), 
                    Real(0), 
                    self.rise, 
                    self.fall
                )
            ),
            conn.vCont(
                conn.i*transition(self.res, Real(0), self.rise, self.fall)
            ),
            self.iCont(ddt(self.v)*self.inCap)
        ) 

    #---------------------------------------------------------------------------
    # Set the pins at hiz in order to use the read function
    #---------------------------------------------------------------------------
    def hiZ(self):
        return self.res.equal(Real(1e12))

    #---------------------------------------------------------------------------
    # Set the pins to low impedance in order to use the write function
    #---------------------------------------------------------------------------
    def lowZ(self):
        return self.res.equal(self.serRes)

               
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
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
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
        checkInstance("value", value, IntegerOp)
        ans = CmdList()
        i = 1
        for pin in self:
            ans.append(pin.write((value & Integer(i)).toBool()))
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
    def read(self):
        ans = self[0].read().toInteger()*Integer(1)
        i = 2
        for pin in self[(len(self)-1):1]:
            ans = IntegerOp(str(ans) + "\n") + pin.read().toInteger()*Integer(i)
            i = i << 1
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
    
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # tb - test bench in which the model will be added
    # pin1 - first node
    # pin2 - second node
    # cond - Real expression representing the initial switch conductance
    # rise - Real expression representing the rise time for changes in the 
    #        conductance
    # fall - Real expression representing the fall time for changes in the 
    #        conductance
    #---------------------------------------------------------------------------
    def __init__(self, tb, pin1, pin2, cond, rise, fall):
        checkInstance("tb", tb, Tb)
        checkInstance("pin1", pin1, Electrical)
        checkInstance("pin2", pin2, Electrical)
        checkInstance("cond", cond, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        self.cond = tb.var(cond)
        self.rise = tb.var(rise)
        self.fall = tb.var(fall)
        self.branch = Branch(pin1, pin2)
        tb.endAnalog(
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
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
        return CmdList(
            self.rise.equal(rise),
            self.fall.equal(fall)
        )

    #---------------------------------------------------------------------------
    # Set the conductance
    # Parameters:
    # cond - new value for the conductance
    #---------------------------------------------------------------------------
    def setCond(self, cond):
        checkInstance("cond", cond, RealOp)
        return self.cond.equal(cond)

#-------------------------------------------------------------------------------
# Clock using a digital pin 
#-------------------------------------------------------------------------------
class Clock():
    
    #---------------------------------------------------------------------------
    # Constructor
    # Parameters:
    # tb - test bench in which the model will be added
    # pin - digital output or inout pin
    #---------------------------------------------------------------------------
    def __init__(self, tb, pin):
        checkInstance("tb", tb, Tb)
        checkInstance("pin", pin, DigOut)
        out = tb.var(pin.st)
        self.isOn = tb.var(Bool(0))
        self.halfPeriod = tb.var(Real(1000000))
        self.time = tb.var(Real(1000000))
        self.at = CmdList(
                      out.equal(~out),
                      pin.write(out),
                      If(self.isOn | out)(
                          self.time.equal(abstime + self.halfPeriod)
                      )
                  )
               
        if isinstance(tb.timeTol, RealOp):
            tb.analog(
                At(Timer(self.time, Real(0), tb.timeTol))(
                    self.at
                )
            )
        elif isinstance(tb.timeTol, type(None)):
            tb.analog(
                At(Timer(self.time))(
                   self.at
                )
            )

    #---------------------------------------------------------------------------
    # Turn the clock generator on
    #---------------------------------------------------------------------------
    def on(self, frequency):
        checkInstance("frequency", frequency, RealOp)
        return CmdList(
                   self.halfPeriod.equal(Real(0.5)/frequency),
                   self.isOn.equal(Bool(1)),
                   self.time.equal(abstime + Real(1e-9))
               )

    #---------------------------------------------------------------------------
    # Turn the clock generator off
    #---------------------------------------------------------------------------
    def off(self):
        return self.isOn.equal(Bool(0))


#-------------------------------------------------------------------------------
# Child of the module class in the veriloA module. It provides aditional
# methods for dealing with digital bus, current sources, voltage sources, 
# clocks and switches
#-------------------------------------------------------------------------------
class Tb(Module):
  
    #---------------------------------------------------------------------------
    # Constructor 
    # Parameters:
    # tbName - name of the test bench
    # timeTol - time tolerances for the timer
    #---------------------------------------------------------------------------
    def __init__(self, tbName, timeTol = None):
        super(Tb, self).__init__(tbName)
        self.dcCmdList  = CmdList() 
        self.testSeq    = self.par(Integer(0), "TEST_SEQ_PARAM")
        self.markerPin  = self.electrical("MARK", direction = "output")
        self.time       = self.var(Real(10e-9), "_$evntTime") 
        self.state      = self.var(Integer(0), "_$state") 
        self.markStReal = self.var(Real(0), "_$markStReal") 
        self.markSt     = self.var(Bool(0), "_$markSt") 
        self.markers    = []
        self.nSeq       = 1
        self.tSeqList   = []
        self.evntList   = []
        self.timerCase  = Case(self.testSeq)() 
        self.timeTol = timeTol
        self.beginningAnalog(
            If(analysis("static"))(
                self.dcCmdList
            ),
            At(InitialStep("tran"))(
                self.dcCmdList
            ),
        )
        if isinstance(self.timeTol, RealOp):
            self.beginningAnalog(
                At(Timer(self.time, Real(0), self.timeTol))(
                    self.timerCase
                )
            )
        elif isinstance(self.timeTol, type(None)):
            self.beginningAnalog(
                At(Timer(self.time))(
                    self.timerCase
                )
            )
        else:
            raise TypeError("timeTol must be RealOp or None") 
        self.endAnalog(
            self.markStReal.equal(self.markSt), 
            self.markerPin.vCont(transition(self.markStReal, \
                                            Real(0), 
                                            Real(1e-12), 
                                            Real(1e-12)))
        )
                    
    #---------------------------------------------------------------------------
    # Add variable to the module. Also, the intial value of the variable will 
    # be set during the static analysis and the initial step of transient.
    # Parameters:
    # name - name of the variable
    # value - Initial value
    #---------------------------------------------------------------------------
    def var(self, value = Integer(0), name = ""):
        ans = super(Tb, self).var(value, name)           
        self.dcCmdList.append(ans.equal(value))
        return ans

    #---------------------------------------------------------------------------
    # Return a marker object
    # Parameters: 
    # name - name of the marker
    #---------------------------------------------------------------------------
    def marker(self, name):
        markerObj = Marker(name, self.markSt)
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
            value = Integer(0),
            inCap = Real(1e-12), 
            serRes = Real(100), 
            rise = Real(1e-12),
            fall = Real(1e-12)):
        #Check the inputs
        checkInstance("domain", domain, Electrical)
        checkInstance("value", value, IntegerOp)
        checkInstance("inCap", inCap, RealOp)
        checkInstance("serRes", serRes, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
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
                           value.toBool(), 
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
                                   (value & Integer(j)).toBool(),
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
        checkInstance("cond", cond, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
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
    # tb - test bench in which the model will be added
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
            volt = Real(0), 
            minCur = Real(0), 
            maxCur = Real(0), 
            res = Real(1e12)): 
        checkInstance("volt", volt, RealOp)
        checkInstance("minCur", minCur, RealOp)
        checkInstance("maxCur", maxCur, RealOp)
        checkInstance("res", res, RealOp)
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
            value = Real(0),
            rise = Real(0),
            fall = Real(0)):
        checkInstance("value", value, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
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
            value = Real(0),
            rise = Real(0),
            fall = Real(0)):
        checkInstance("value", value, RealOp)
        checkInstance("rise", rise, RealOp)
        checkInstance("fall", fall, RealOp)
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
    # *cmds - variable number of commands
    #---------------------------------------------------------------------------
    def seq(self, *cmds):
        nState = 0
        ans = CmdList()
        i = 1
        for cmd in cmds:
            assert isinstance(cmd, Cmd) and \
                   not isinstance(cmd, WaitAnalogEvent), "Command " + str(i) +\
                   " must be an instance of Cmd and can't be and instance of "+\
                   "WaitAnalogEvent"
            i = i + 1
            ans.append(cmd)
        ans = ans.flat()
        pTimerCase = Case(self.state)()
        self.timerCase.append((Integer(self.nSeq), pTimerCase))
        pCase = pTimerCase
        cmds = CmdList()
        caseList = []
        evntList = []
        for cmd in ans:
            #Found a WaitUs. Update timer event and go to next state
            if isinstance(cmd, WaitUs):
                cmds.append(self.state.equal(self.state + Integer(1)))
                cmds.append(self.time.equal(abstime + 
                                            Real(1e-6)*cmd.getDelay()))
                pCase.append((Integer(nState), cmds))
                cmds = CmdList()
                pCase = pTimerCase
                nState = nState + 1
            #Found a WaitSignal. Update signal events and go to next state
            elif isinstance(cmd, WaitSignal):
                cmds.append(self.state.equal(self.state + Integer(1)))
                pCase.append((Integer(nState), cmds))
                cmds = CmdList()
                evnt = cmd.getEvnt()
                #The event was already used for this sequence
                if evnt in evntList:
                    i = evntList.index(evnt)
                    pCase = caseList[i]
                #The event wasn't used already in this sequence, but it
                #has been used before in another sequence
                elif evnt in self.evntList:
                    i = self.evntList.index(evnt)
                    tSeqCase = self.tSeqList[i]
                    pCase = Case(self.state)()
                    tSeqCase.append((Integer(self.nSeq), pCase))
                    evntList.append(evnt)    
                    caseList.append(pCase)    
                #Fist reference to this signal event in all sequences
                else:
                    tSeqCase = Case(self.testSeq)()
                    pCase = Case(self.state)()
                    tSeqCase.append((Integer(self.nSeq), pCase))
                    self.evntList.append(evnt)    
                    self.tSeqList.append(tSeqCase)    
                    evntList.append(evnt)    
                    caseList.append(pCase)    
                    self.beginningAnalog(
                        At(evnt)(
                            tSeqCase
                        )
                    )
                nState = nState + 1
            #Not a wait command. Add it to the list of commands for the current
            #state
            else:
                cmds.append(cmd)
        #Add a finish command
        cmds.append(Finish()) 
        #Add the last state 
        pCase.append((Integer(nState), cmds))
        #Go to the next sequence
        self.nSeq = self.nSeq + 1
            
    #---------------------------------------------------------------------------
    # Return cds equations
    #---------------------------------------------------------------------------
    def getCDS(self):
        return ""  
            


