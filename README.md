# vagen

## What is vagen?

vagen was created mainly to generate verilogA stimulus for verification of complex analog IPs. However, it has wrappers for most of the verilogA reserved words, so it also generates verilogA models.

## Instalation 

You can install vagen by typing the command:

```
    pip3 install vagen
```

## Example 1: Stimulus for verification of a DCDC

Let's assume that a stimulus with the following sequence is required:

* VDD must rise from 0 to 5.0V in 10us.
* After 10us, the clock signal (CLK) must start with a frequency of 4MHz. CLK domain is VDD.
* After 1us, RST must rise. RST domain is VDD.
* Wait for the positive edge of the signal READY when it crosses half of the domain voltage. READY domain is VDD. 
* A current of 100mA must be drawn from the in OUT with a rise time of 100ns. 
* After 10us, the bus CONFIG_VOUT[3:0] must be changed from 0 to 5. CONFIG_VOUT[3:0] domain is VDD.
* After 20us, finishes the simulation. 

The python code that generates this stimulus is shown below:

```
import vagen as va

#Create a module     
mod = va.HiLevelMod("DCDC_STML")

#Create pins
VDD = mod.vdc(name = "VDD", width = 1, direction = "inout")
OUT = mod.idc(name = "OUT", width = 1, direction = "inout")
CLK = mod.clock(mod.dig(name = "CLK", domain = VDD, width = 1, direction = "output", rise = 100e-12, fall = 100e-12))
RST = mod.dig(name = "RST", domain = VDD, width = 1, value = 0, direction = "output", rise = 100e-12, fall = 100e-12)
READY = mod.dig(name = "READY", domain = VDD, width = 1, direction = "input")
CONFIG_VOUT = mod.dig(name = "CONFIG_VOUT", domain = VDD, width = 4, value = 0, direction = "output", rise = 100e-12, fall = 100e-12)

#READY positive event
EVNT_READY = va.Cross(READY.diffHalfDomain, "rising")

#Sequence
mod.seq(True)(
    VDD.setRiseFall(10e-6, 10e-6),
    VDD.applyV(5.0),
    va.WaitUs(10), 
    CLK.on(4e6),
    va.WaitUs(1),
    RST.write(True),
    va.WaitSignal(EVNT_READY),
    OUT.setRiseFall(100e-9, 100e-9),
    OUT.applyI(100e-3), #Positive current enters the model
    va.WaitUs(10),
    CONFIG_VOUT.write(5),
    va.WaitUs(20),
    va.Finish()
)

#Save veriloga file
file = open('veriloga.va', 'w')
file.write(mod.getVA())
file.close()
```

## Example 2: More than one sequence in the same veriloga

You can create a veriloga parameter called testSeq

```
seqPar = mod.par(name = "testSeq", value = 0)
```

And then use this parameter to select the sequence depending on the value

```
#sequence 1 
mod.seq(seqPar == 1)(
...
)

#sequence 2
mod.seq(seqPar == 2)(
...
)
```

## Example 3: Model of a configurable resistor

As mentioned before, vagen can be used to generate models. As an example, the code below generates a veriloga model of a configurable resistor.

```
import vagen as va

#Create a module
mod = va.HiLevelMod("CONFIG_RES")

#Create pins
VDD = mod.electrical(name = "VDD", width = 1, direction = "inout")
IN1 = mod.electrical(name = "IN1", width = 1, direction = "inout")
IN2 = mod.electrical(name = "IN2", width = 1, direction = "inout")
CONFIG = mod.dig(name = "CONFIG", domain = VDD, width = 4, inCap = 100e-15, direction = "input")

#Parameters
alfa = mod.par(name = "alfa", value = 10.0)

#Analog block
mod.analog(
    va.Branch(IN1, IN2).vCont(va.Branch(IN1, IN2).i*(va.Real(CONFIG.read(signed = False)) + 1)*alfa)
)

#Save veriloga file
file = open('veriloga.va', 'w')
file.write(mod.getVA())
file.close()
```

# More examples
Extra examples will be added to examples folder
