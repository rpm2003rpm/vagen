"""Verilog-A module definition and code generation."""

from datetime import date
import re

from vagen.commands import Cmd
from vagen.disciplines import Electrical
from vagen.enums import PortDirection
from vagen.exceptions import VagenNameError, VagenTypeError, VagenValueError
from vagen.types import Bool, BoolVar, Integer, IntegerVar, Real, RealVar
from vagen.util import blockComment
from vagen.validation import checkType, parseInteger, parseReal

class Module:
    """Class representing a Verilog-A module."""

    def __init__(self, moduleName, ignoreHiddenStates = False):
        """Initialize a Module instance.

        Args:
            moduleName (str): The module's name.
            ignoreHiddenStates (bool): Pragma will be added if True
        """
        checkType("moduleName", moduleName, str)
        self.moduleName = moduleName   
        self.nameCount  = 0
        self.nameSpace  = []
        self.nodes      = []
        self.ports      = []
        self.parameters = []
        self.variables  = []
        self.cmds       = []
        self.endCmds    = []
        self.beginningCmds = []
        self.ignoreHiddenStates = ignoreHiddenStates

    def getModuleName(self):
        """Return the module's name.

        Returns:
            str: The module name.
        """
        return self.moduleName

    def _fixName(self, name):
        """Fix or generate a unique name in the module's namespace.

        Args:
            name (str): The proposed name.

        Returns:
            str: A valid, unique name.
        """
        checkType("name", name, str)
        if name == "":
            self.nameCount = self.nameCount + 1
            name = f"_${self.nameCount}"
        if not re.match(r"[_a-zA-Z][_a-zA-Z$0-9]*", name):
            raise VagenNameError(f"{name} isn't a valid verilogA identifier")
        if name in self.nameSpace:
            raise VagenNameError(f"{name} is already taken")
        self.nameSpace.append(name)
        return name

    def var(self, vType = Integer, name = ""):
        """Add a variable to the module.

        Args:
            vType (type, optional): The variable type (Integer, Bool, or Real). 
                Defaults to Integer.
            name (str, optional): The variable's name. Defaults to "".

        Returns:
            An instance of IntegerVar, BoolVar, or RealVar.
        """
        name = self._fixName(name)
        if vType == Integer:
            vType = "integer"
            ans   = IntegerVar(name)
        elif vType == Bool:
            vType = "integer"
            ans   = BoolVar(name)
        elif vType == Real:
            vType = "real"
            ans   = RealVar(name)
        else:
            raise VagenTypeError(
                f"vType must be Integer, Real, or Bool but a {vType} was given")
        self.variables.append((name, vType)) 
        return ans

    def par(self, value, name):
        """Add a parameter to the module.

        Args:
            value (Real, Integer, int, or float): The parameter's initial value.
            name (str): The parameter's name.

        Returns:
            RealVar or IntegerVar: The parameter variable.
        """
        name = self._fixName(name)
        if isinstance(value, bool):
            raise VagenTypeError(
                "value must be Integer or Real, but a bool was given")
        if isinstance(value, (Integer, int)):
            value = parseInteger("value", value)
            pType = "integer"
            ans   = Integer(name)
        elif isinstance(value, (Real, float)):
            value = parseReal("value", value)
            pType = "real"
            ans   = Real(name)
        else:
            raise VagenTypeError(
                f"value must be Integer or Real, but a {type(value)} was given")
        self.parameters.append((name, pType, str(value))) 
        return ans

    def analog(self, *args):
        """Add commands to the analog block.

        Args:
            *args: Variable number of commands.
        """
        i = 1
        for arg in args:
            if not isinstance(arg, Cmd):
                raise VagenTypeError(
                   f"cmd[{i}] must be an instance of Cmd and but a {type(arg)}"
                    f" was given instead")
            i = i + 1
            self.cmds.append(arg)

    def beginningAnalog(self, *args):
        """Add commands to the beginning of the analog block.

        Args:
            *args: Variable number of commands.
        """
        i = 1
        for arg in args:
            if not isinstance(arg, Cmd):
                raise VagenTypeError(
                   f"cmd[{i}] must be an instance of Cmd and but a {type(arg)}"
                    f" was given instead")
            i = i + 1
            self.beginningCmds.append(arg)

    def endAnalog(self, *args):
        """Add commands to the end of the analog block.

        Args:
            *args: Variable number of commands.
        """
        i = 1
        for arg in args:
            if not isinstance(arg, Cmd):
                raise VagenTypeError(
                   f"cmd[{i}] must be an instance of Cmd and but a {type(arg)}"
                    f" was given instead")
            i = i + 1
            self.endCmds.append(arg)

    def addNode(self, name, width, direction):
        """Add a node to the module.

        Args:
            name (str): The node name.
            width (int): The node width (must be > 0).
            direction (str): The node direction ("internal", "input", "output", or "inout").

        Returns:
            str: The unique node name.
        """
        checkType("width", width, int)
        if width <= 0:
            raise VagenValueError("width must be greater than 0")
        checkType("direction", direction, str)
        if isinstance(direction, PortDirection):
            direction = direction.value
        if direction not in PortDirection.values():
            raise VagenValueError(
               "direction must be input, output, inout, or internal")
        name = self._fixName(name)
        if direction != "internal":
            self.ports.append((name, width, direction))
        self.nodes.append((name, width)) 
        return name

    def electrical(self, name = "", width = 1, direction = "internal"):
        """Return an Electrical signal or a vector of Electrical signals.

        Args:
            name (str, optional): The base name for the signal. Defaults to "".
            width (int, optional): The width of the signal. Defaults to 1.
            direction (str, optional): The signal direction. Defaults to "internal".

        Returns:
            Electrical or list[Electrical]: The Electrical signal(s).
        """
        name = self.addNode(name, width, direction)
        if width == 1:
            return Electrical(name)
        else:
            vector = list()
            for i in range(0, width):
                vector.append(Electrical(f"{name}[{i}]"))
            return vector

    def getVA(self, header_date=None):
        """Return the complete Verilog-A code for the module.

        Args:
            header_date (date, optional): Fixed date for the generated header.
                Defaults to today's date.

        Returns:
            str: The generated Verilog-A code.
        """
        #-----------------------------------------------------------------------
        # Header
        #-----------------------------------------------------------------------
        comment = "Module: " + self.moduleName + "\n"
        comment = comment + "Date: " + str(header_date if header_date is not None else date.today())
        result = blockComment(0, comment, align = "left")

        result = result + '`include "constants.vams"\n'        
        result = result + '`include "disciplines.vams"\n' 

        result = result + "\n" + blockComment(0, "Module declaration")
        if self.ignoreHiddenStates:
            result = result + "(*ignore_hidden_state*)\n"
        result = result + "module " + self.moduleName + "("
        padding = ",\n        " + " "*len(self.moduleName)
        first = True
        for pin in self.ports:
            if first:   
                first = False
                result = result + pin[0]
            else:
                result = result + padding + pin[0]
        result = result + ');\n' 

        if not first:
            result = result + '\n' + blockComment(0, "Ports")
        for pin in self.ports:
            result = result + pin[2] + " "
            if pin[1] > 1:
                result = result + "[" + str(pin[1]-1) + ":0] " 
            result = result + pin[0] + ";\n"
 
        if len(self.nodes) > 0:
            result = result + '\n' + blockComment(0, "Disciplines")
        for node in self.nodes:
            result = result + "electrical "
            if node[1] > 1:
                result = result + "[" + str(int(node[1])-1) + ":0] " 
            result = result + node[0] + ";\n"

        #-----------------------------------------------------------------------
        # Build in analog function
        #-----------------------------------------------------------------------
        result = result + '\n' + blockComment(0, "Build-in functions")
        result = result + ("analog function integer _rtoi;\n"
                           "input in;\n"
                           "real in;\n"
                           "begin\n"
                           "    _rtoi = floor(in + 0.5);\n"
                           "end\n"
                           "endfunction\n")

        #-----------------------------------------------------------------------
        # Print all parameters
        #-----------------------------------------------------------------------
        if len(self.parameters) > 0:
            result = result + '\n' + blockComment(0, "Parameters")
        for parameter in self.parameters:
            result = result + "parameter " + parameter[1] + " " +\
                     parameter[0] + " = " + parameter[2] + ";\n"

        #-----------------------------------------------------------------------
        # Print all variables
        #-----------------------------------------------------------------------
        if len(self.variables) > 0:
            result = result + '\n' + blockComment(0, "Variables")
        for variable in self.variables:
            result = result +  variable[1] + " " + variable[0] + ";\n"

        #-----------------------------------------------------------------------
        # Analog
        #-----------------------------------------------------------------------
        result = result + '\n' + blockComment(0, "Analog block")
        result = result + "analog begin\n"
        for cmd in self.beginningCmds + self.cmds + self.endCmds:
            result = result + cmd.getVA(1)
        
        #-----------------------------------------------------------------------
        # End module
        #-----------------------------------------------------------------------
        result = result + "end\nendmodule"

        return result

    def writeVa(self, path, header_date=None, encoding="utf-8"):
        """Write generated Verilog-A source to a file.

        Args:
            path (str): Output file path.
            header_date (date, optional): Fixed date for the generated header.
            encoding (str, optional): File encoding. Defaults to UTF-8.
        """
        with open(path, "w", encoding=encoding) as file:
            file.write(self.getVA(header_date=header_date))
