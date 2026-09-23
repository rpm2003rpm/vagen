# vagen

**vagen** is a Python library that generates Verilog-A (`.va`) source code for analog IP verification and behavioral modeling. It was created primarily to build transient testbenches for complex analog blocks, but it also wraps most Verilog-A reserved words, so you can use it to generate behavioral models as well.

## Installation

Install the latest release from PyPI:

```bash
pip install vagen
```

For local development, clone the repository and install in editable mode:

```bash
pip install -e .
```

## Quick start

The usual workflow is:

1. Create a `HiLevelMod` (for testbenches) or `Module` (for behavioral models).
2. Declare pins, parameters, and variables.
3. Describe your sequence or model.
4. Export the generated Verilog-A with `mod.getVA()`.

`HiLevelMod` adds high-level primitives such as voltage/current sources, digital pins, clocks, markers, and sequence compilation. Use `Module` when you only need the lower-level Verilog-A building blocks.

## Example 1: DCDC verification stimulus

Suppose a simulation must execute the following sequence:

- Raise `VDD` from 0 V to 5.0 V in 10 µs.
- After 10 µs, start `CLK` at 4 MHz. The clock domain is `VDD`.
- After 1 µs, assert `RST`. Its domain is also `VDD`.
- Wait for the rising edge of `READY`, which is referenced to `VDD`.
- Draw 100 mA from `OUT` with a 100 ns rise time.
- After 10 µs, change `CONFIG_VOUT[3:0]` from 0 to 5.
- After 20 µs, finish the simulation.

The Python code below generates that stimulus.

```python
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
file.write(mod.getVA())
```



## Example 2: Multiple sequences in one module

Create a parameter that selects which sequence to run:

```python
seqPar = mod.par("testSeq", value = 0)
```

Then guard each sequence with that parameter:

```python
mod.seq(seqPar == 1)(
    # sequence 1 commands ...
)

mod.seq(seqPar == 2)(
    # sequence 2 commands ...
)
```

Each call to `mod.seq(...)` adds another compiled state machine to the module.

## Example 3: Configurable resistor model

vagen can also generate behavioral models. The example below builds a configurable resistor:

```python
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

## Sequence limitations

A few constructs are only valid inside `mod.seq(...)`:

- `WaitUs`, `WaitSignal`, and `Mark` cannot be emitted directly to Verilog-A outside a sequence.
- `Case` statements cannot be nested inside a sequence.
- Marks cannot appear inside arbitrary command lists within a sequence.

If you violate these rules, vagen raises `VagenSequenceError`.

## API reference

`HiLevelMod` extends `Module` with helpers for building transient testbenches. 

| Method | Purpose |
|--------|---------|
| `mod.vdc(name, width, ...)` | Voltage source (DC) bus or pin |
| `mod.idc(name, width, ...)` | Current source (DC) bus or pin |
| `mod.smu(name, width, ...)` | Source-measure unit (voltage, current, or resistive mode) |
| `mod.dig(domain, name, width, ...)` | Digital pin or bus referenced to an analog domain |
| `mod.clock(dig_pin)` | Clock wrapper around a digital output pin |
| `mod.sw(pin1, pin2, ...)` | Analog switch between two nodes |
| `mod.marker(name)` | Marker for tagging events in a sequence |
| `mod.electrical(name, width, ...)` | Plain electrical node without an attached source model |

Shared options on `Module` / `HiLevelMod` constructors and helpers:

- `direction` — `"input"`, `"output"`, `"inout"`, or `"internal"` (also available as `va.PortDirection`)
- `ignoreHiddenStates=True` — adds the `(*ignore_hidden_state*)` pragma to the module
- `timeTol` — optional timer tolerance passed to `HiLevelMod` (used by internal sequence timing)

## Exporting Verilog-A

`mod.getVA()` returns the full `.va` source as a string.
`mod.writeVa(path)` writes the generated source to a file using UTF-8 by default.

## Cadence export helpers

For Cadence ADE / Maestro workflows, `HiLevelMod` can export marker timing equations:

- `mod.getEqs()` — CSV suitable for Maestro equation import
- `mod.getOcn()` — Ocean script that registers outputs in an ADE XL session

Cadence and Maestro are trademarks of the Cadence company.
This project is not affiliated with, endorsed by, or sponsored by Cadence.

## Exceptions

vagen raises typed exceptions (all inherit from `VagenError`):

| Exception | When it is raised |
|-----------|-------------------|
| `VagenTypeError` | Wrong argument type (e.g. invalid `par()` value, bad command operand) |
| `VagenValueError` | Valid type but invalid value (e.g. out-of-range integer, bad bus slice) |
| `VagenSequenceError` | Sequence-only construct used outside `mod.seq(...)` |
| `VagenNameError` | Invalid or duplicate Verilog-A identifier |

## More examples

See the `examples/` directory for additional scripts. README Examples 1–3 are exercised by the test suite.

## Development

Install with dev dependencies, then run lint, tests, and coverage from the repository root:

```bash
pip install -e ".[dev]"
python -m ruff check .
python -m unittest discover -s tests -v
python -m coverage run -m unittest discover -s tests
python -m coverage report
python -m mypy vagen
```
