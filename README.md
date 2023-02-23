# vagen

## What is vagen?

vagen is a verilogA test bench generator that can be used for transient verification of complex analog IPs in the context of VLSI design.
It provides a wide range of basic models with voltage sources, current sources, digital interface, clock, switches, and source measure units. 

Mutiple sequences for different tests can be created and selected during simulation time with the parameter TEST_SEQ_PARAM. 



## How to run

You can run an example of the verilogA test bench generator by typing the following command in a terminal:

```
    python3 example.py
```

## TODO

Although usable, the current development status is beta. There are several things that still needs to be done:

* Create test benches for the code.
* Modify the code so integer, float, and boolean values can be recognized without the need for an explicity declaration (ex. Real(1))
* Modify the code so WaitUs and WaitSignal can be used inside While, If, Case, Repeat and For when these conditions are inside a sequence.
* Implement the automatic generation of cadence equations for the markers.
* Write a documentation for the module.
