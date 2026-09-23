"""Verilog-A command and control-flow primitives."""

from vagen.exceptions import VagenTypeError, VagenValueError
from vagen.functions import Event
from vagen.types import Bool, Integer, Real
from vagen.validation import (
    checkInstance,
    checkNotInstance,
    checkType,
    parseBool,
    parseInteger,
    parseNumber,
    parseReal,
)

class Cmd:
    """Class representing a command in the system."""
    
    def __init__(self, cmd):
        """Initialize a Cmd instance.

        Args:
            cmd (str): The command string.
        """
        checkType("cmd", cmd, str)
        self.cmd = cmd

    def __str__(self):
        """Return the string representation of the command.

        Returns:
            str: The command as a string.
        """
        return self.cmd

    def getVA(self, padding):
        """Return the VA Verilog command with the specified padding.

        Args:
            padding (int): The number of tabs for right shift.

        Returns:
            str: The formatted Verilog command.
        """
        checkType("padding", padding, int)
        chunks = self.cmd.split("\n")
        result = '\n'.join([f"{'    '*padding}{l}" for l in chunks])
        result = f"{result};\n"
        return result


class CmdList(list, Cmd):
    """Command list class that combines list behavior with Cmd functionality."""
    
    def __init__(self, *cmds):
        """Initialize a CmdList instance and append the provided commands.

        Args:
            *cmds: Variable number of commands to add.
        """
        super(CmdList, self).__init__()
        self.append(*cmds)
        
    def __str__(self):
        """Return a comma-separated string representation of the command list.

        Returns:
            str: The string representation.
        """
        return ", ".join([str(x) for x in self])
        
    def flat(self):
        """Return a flat list of commands, recursively flattening any CmdList 
        items.

        Returns:
            list: A flat list of commands.
        """
        ans = []
        for item in self:
            if type(item) == CmdList:   
                ans = ans + item.flat()
            else:
                ans.append(item)
        return ans

    def append(self, *cmds):
        """Override the append method to add commands with type checking.

        Args:
            *cmds: Variable number of commands to append.
        """
        i = 0
        for cmd in cmds:
            checkInstance(f"cmds[{i}]", cmd, Cmd)
            checkNotInstance(f"cmds[{i}]", cmd, WaitAnalogEvent)
            super(CmdList, self).append(cmd)
            i = i + 1
        
    def getVA(self, padding):
        """Return the concatenated VA Verilog commands with the specified 
        padding.

        Args:
            padding (int): Number of indentation tabs.

        Returns:
            str: The formatted Verilog command string.
        """
        checkType("padding", padding, int)
        return "".join([f"{l.getVA(padding)}" for l in self])


class Block(CmdList):
    """Command Block class for grouping commands under a header."""

    def __init__(self, header, *cmds):
        """Initialize a Block instance with a header and commands.

        Args:
            header (str): Header of the block.
            *cmds: Variable number of commands or CmdLists.
        """
        checkType("header", header, str)
        self.header = header
        super(Block, self).__init__(*cmds)
        
    def getHeader(self):
        """Return the header of the block.

        Returns:
            str: The block header.
        """
        return self.header
                
    def getVA(self, padding):
        """Return the formatted VA Verilog command for the block with padding.

        Args:
            padding (int): Number of indentation tabs.

        Returns:
            str: The formatted Verilog command string.
        """
        checkType("padding", padding, int)
        length = len(self.flat())
        if length > 1:
            result = (f"{'    '*padding}{self.header} begin\n"
                      f"{super(Block, self).getVA(padding + 1)}"
                      f"{'    '*padding}end\n")
        elif length == 1:
            result = (f"{'    '*padding}{self.header}\n"
                      f"{super(Block, self).getVA(padding + 1)}")     
        else:
            result = f"{'    '*padding}{self.header};\n"
        return result


def block(header):
    """Return a function that creates a Block with the given header.

    Args:
        header (str): The header for the block.

    Returns:
        function: A function that accepts commands and returns a Block.
    """
    def func(*cmds):
        return Block(header, *cmds)
    return func


class WaitAnalogEvent(Block):
    """Class representing a wait for an analog event."""
    
    def __init__(self, event, *cmds):
        """Initialize a WaitAnalogEvent instance.

        Args:
            event (Event): The event to wait for.
            *cmds: Variable number of commands or CmdLists.
        """
        checkInstance("event", event, Event)
        super(WaitAnalogEvent, self).__init__(f'@( {event} )', *cmds)    

def At(event):
    """Return a function that creates a WaitAnalogEvent for the given event.

    Args:
        event (Event): An Event instance representing the analog event.

    Returns:
        function: A function that accepts commands and returns a WaitAnalogEvent.
    """
    def func(*cmds):
        return WaitAnalogEvent(event, *cmds)
    return func
  

class RepeatLoop(Block):
    """Class representing a loop that repeats a block of commands."""

    def __init__(self, n, *cmds):
        """Initialize a RepeatLoop instance.

        Args:
            n (Integer, int, or convertible type): The repeat count.
            *cmds: Variable number of commands or CmdLists.
        """
        n = parseInteger("n", n)
        self.n = n
        super(RepeatLoop, self).__init__(f"repeat( {n} )", *cmds)  
        
    def getN(self):
        """Return the repeat count.

        Returns:
            Integer: The number of repetitions.
        """
        return self.n
        
                   
def Repeat(n):
    """Return a function that creates a RepeatLoop with the specified repeat count.

    Args:
        n (Integer, int, or convertible type): Number of times to repeat.

    Returns:
        function: A function that accepts commands and returns a RepeatLoop.
    """
    def func(*cmds):
        return RepeatLoop(n, *cmds)
    return func


class WhileLoop(Block):
    """Class representing a while loop block."""

    def __init__(self, cond, *cmds):
        """Initialize a WhileLoop instance.

        Args:
            cond (Bool or bool): The condition to control the loop.
            *cmds: Variable number of commands or command lists to execute.
        """
        cond = parseBool("cond", cond)
        self.cond = cond
        super(WhileLoop, self).__init__(f"while( {cond} )", *cmds)  
        
    def getCond(self):
        """Return the loop condition.

        Returns:
            Bool: The condition controlling the while loop.
        """
        return self.cond  

        
def While(cond):
    """Return a function that creates a WhileLoop with the given condition.

    Args:
        cond (Bool or bool): The condition for the while loop.

    Returns:
        function: A function that accepts commands and returns a WhileLoop.
    """
    def func(*cmds):
        return WhileLoop(cond, *cmds)
    return func


class ForLoop(Block):
    """Class representing a for loop block."""

    def __init__(self, start, cond, inc, *cmds):
        """Initialize a ForLoop instance.

        Args:
            start (Cmd or CmdList): The initialization command.
            cond (Bool or bool): The loop condition.
            inc (Cmd or CmdList): The increment command.
            *cmds: Additional commands to execute inside the loop.
        """
        cond = parseBool("cond", cond)
        if not isinstance(start, (Cmd, CmdList)):
            raise VagenTypeError(
               f"start must be Cmd or CmdList but a {type(start)} was given "
                 "instead")
        if not isinstance(inc, (Cmd, CmdList)):
            raise VagenTypeError(
               f"inc must be Cmd or CmdList but a {type(inc)} was given "
                 "instead")
        head = f"for( {start}; {cond}; {inc} )"
        self.cond = cond
        self.start = start
        self.inc = inc 
        super(ForLoop, self).__init__(head, *cmds)

    def getCond(self):
        """Return the for loop condition.

        Returns:
            Bool: The condition controlling the for loop.
        """
        return self.cond
        
    def getStart(self):
        """Return the for loop's start command.

        Returns:
            Cmd or CmdList: The initialization command.
        """
        return self.start
        
    def getInc(self):
        """Return the for loop's increment command.

        Returns:
            Cmd or CmdList: The increment command.
        """
        return self.inc 
    

def For(start, cond, inc):
    """Return a function that creates a ForLoop instance.

    Args:
        start (Cmd or CmdList): The initialization command.
        cond (Bool or bool): The loop condition.
        inc (Cmd or CmdList): The increment command.

    Returns:
        function: A function that accepts commands and returns a ForLoop.
    """
    def func(*cmds):
        return ForLoop(start, cond, inc, *cmds)
    return func
    

class Cond(Cmd):
    """Class representing a conditional (if-else) block."""

    def __init__(self, cond, *cmds):
        """Initialize a Cond instance.

        Args:
            cond (Bool or bool): The condition for the 'if' branch.
            *cmds: Commands to execute when the condition is true.
        """
        cond = parseBool("cond", cond)
        trueHead  = f"if( {cond} )"
        falseHead = "else"
        self.cond = cond
        self.cmdDict = {True:Block(trueHead, *cmds), \
                        False:Block(falseHead)}

    def getCond(self):
        """Return the condition for the if branch.

        Returns:
            Bool: The condition.
        """
        return self.cond
        
    def getBlock(self, state=True):
        """Return the command block corresponding to a state.

        Args:
            state (bool, optional): True for 'if', False for 'else'. 
                Defaults to True.

        Returns:
            Block: The command block for the given state.
        """
        checkType("state", state, bool)
        return self.cmdDict[state]
                
    def append(self, state, *cmds):
        """Append commands to the block corresponding to the given state.

        Args:
            state (bool): True for 'if' branch, False for 'else' branch.
            *cmds: Commands to append.
        """
        checkType("state", state, bool)
        self.cmdDict[state].append(*cmds)

    def Else(self, *cmds):
        """Append commands to the 'else' branch.

        Args:
            *cmds: Commands to append.

        Returns:
            Cond: The current instance.
        """
        self.cmdDict[False].append(*cmds)
        return self

    def getVA(self, padding):
        """Return the VA Verilog command string for the conditional block.

        Args:
            padding (int): Number of indentation tabs.

        Returns:
            str: The formatted Verilog command.
        """
        checkType("padding", padding, int)
        result = f"{self.cmdDict[True].getVA(padding)}" 
        if len(self.cmdDict[False]) > 0:
            result = f"{result}{self.cmdDict[False].getVA(padding)}"
        return result
        
        
def If(cond):
    """Return a function that creates a conditional block.

    Args:
        cond (Bool or bool): The condition for the 'if' structure.

    Returns:
        function: A function that accepts commands and returns a Cond instance.
    """
    def ifFunc(*cmds):
        ans = Cond(cond, *cmds)
        return ans
    return ifFunc


class CaseClass(Cmd):
    """Class representing a case structure with multiple conditional branches."""

    def __init__(self, test, *cmds):
        """Initialize a CaseClass instance.

        Args:
            test (Integer, Bool, or Real): The test expression.
            *cmds: Tuples where each tuple contains a condition and corresponding 
                commands.
        """
        self.test = parseNumber("test", test)
        self.cmds = []
        self.append(*cmds)

    def getBlockList(self):
        """Return the list of command blocks for each case branch.

        Returns:
            list: A list of Block instances.
        """
        return self.cmds
                      
    def append(self, *cmds):
        """Append tuples of condition and commands to the case structure.

        Args:
            *cmds: Tuples where the first element is the case condition 
                   (or None for default) followed by one or more commands.
        """
        i = 0
        for tup in cmds:
            if not isinstance(tup, tuple):
                raise VagenTypeError(f"cmds[{i}] must be tuple")
            if len(tup) <= 1:
                raise VagenValueError(f"cmds[{i}] length must > 1")
            if not isinstance(tup[0], type(None)):
                if isinstance(self.test, Bool)  and \
                   isinstance(tup[0], (Bool, bool)):
                   test = parseBool(f"cmds[{i}][0]", tup[0])
                elif isinstance(self.test, Integer)  and \
                     isinstance(tup[0], (Integer, int)):
                   test = parseInteger(f"cmds[{i}][0]", tup[0])
                elif isinstance(self.test, Real)  and \
                     isinstance(tup[0], (Real, float, int)):
                   test = parseReal(f"cmds[{i}][0]", tup[0])
                else:
                    raise VagenTypeError( (f"cmds[{i}][0] must be compatible with "  
                          f"{type(self.test)} but a {type(tup[0])} was given "
                           "instead."))
                blockCmd = Block(f"{test}:")
            else:
                blockCmd = Block("default:")  
            j = 1
            for cmd in tup[1:]:
                checkInstance(f"cmds[{i}][{j}]", cmd, Cmd)
                checkNotInstance(f"cmds[{i}][{j}]", cmd, WaitAnalogEvent)
                blockCmd.append(cmd)
                j = j + 1
            self.cmds.append(blockCmd)
            i = i + 1

    def getVA(self, padding):
        """Return the VA Verilog command string for the case structure.

        Args:
            padding (int): Number of indentation tabs.

        Returns:
            str: The formatted Verilog command.
        """
        checkType("padding", padding, int)
        result = (f"{'    '*padding}case( {self.test} )\n"
                  f"{''.join([l.getVA(padding+1) for l in self.cmds])}"
                  f"{'    '*padding}endcase\n")
        return result
        
        
def Case(test):
    """Return a function that creates a case structure.

    Args:
        test (Integer, Bool, or Real): The variable under test.

    Returns:
        function: A function that accepts command tuples and returns a CaseClass.
    """
    def caseFunc(*cmds):
        return CaseClass(test, *cmds)
    return caseFunc
    

def unfoldParams(*params):
    """Unfold a variable number of parameters into a comma-separated string.

    Args:
        *params: Parameters to be unfolded.

    Returns:
        str: A string with the parameters separated by commas.
    """
    cmd = ""
    i = 0
    for param in params:
        param = parseNumber("param[i]", param)
        cmd = f"{cmd}, {param}"
        i = i + 1
    return cmd


def Strobe(msg, *params):
    """Return a command representing a strobe operation.

    Args:
        msg (str): The message to be printed.
        *params: Additional parameters for the strobe.

    Returns:
        Cmd: A command for the strobe.
    """
    checkType("msg", msg, str)
    return Cmd(f'$strobe("{msg}"{unfoldParams(*params)})')


def Write(msg, *params):
    """Return a command representing a write operation.

    Args:
        msg (str): The message to be printed.
        *params: Additional parameters for the write.

    Returns:
        Cmd: A command for the write.
    """
    checkType("msg", msg, str)
    return Cmd(f'$write("{msg}"{unfoldParams(*params)})')


def Fopen(fileName):
    """Return an Integer representing the file descriptor from opening a file.

    Args:
        fileName (str): The name of the file.

    Returns:
        Integer: The file descriptor.
    """
    checkType("fileName", fileName, str)
    return Integer(f'$fopen("{fileName}")') 


def Fclose(desc):
    """Return a command to close a file.

    Args:
        desc (Integer or int): The file descriptor.

    Returns:
        Cmd: A command to close the file.
    """
    desc = parseInteger("desc", desc)
    return Cmd(f'$fclose({desc})') 


def Fstrobe(desc, msg, *params):
    """Return a command representing a file strobe operation.

    Args:
        desc (Integer or int): The file descriptor.
        msg (str): The message to be written.
        *params: Additional parameters.

    Returns:
        Cmd: A command for the file strobe.
    """
    desc = parseInteger("desc", desc)
    checkType("msg", msg, str)
    return Cmd(f'$fstrobe({desc}, "{msg}"{unfoldParams(*params)})')


def Fwrite(desc, msg, *params):
    """Return a command representing a file write operation.

    Args:
        desc (Integer or int): The file descriptor.
        msg (str): The message to be written.
        *params: Additional parameters.

    Returns:
        Cmd: A command for the file write.
    """
    desc = parseInteger("desc", desc)
    checkType("msg", msg, str)
    return Cmd(f'$fwrite({desc}, "{msg}"{unfoldParams(*params)})')
                         

def Discontinuity(degree=0):
    """Return a command representing a discontinuity in the derivative.

    Args:
        degree (Integer, int, or numeric, optional): The degree of discontinuity. 
            Defaults to 0.

    Returns:
        Cmd: A command for the discontinuity.
    """
    degree = parseInteger("degree", degree)
    return Cmd(f'$discontinuity({degree})')


def Finish():
    """Return a command representing finish.

    Returns:
        Cmd: A finish command.
    """
    return Cmd('$finish')


def Error(msg, *params):
    """Return a command representing an error message.

    Args:
        msg (str): The error message.
        *params: Additional parameters.

    Returns:
        Cmd: A command for the error.
    """
    checkType("msg", msg, str)
    return Cmd(f'$error("{msg}"{unfoldParams(*params)})')


def Fatal(msg, *params):
    """Return a command representing a fatal error.

    Args:
        msg (str): The error message.
        *params: Additional parameters.

    Returns:
        Cmd: A command for the fatal error.
    """
    checkType("msg", msg, str)
    return Cmd(f'$fatal(0, "{msg}"{unfoldParams(*params)})')


def BoundStep(step):
    """Return a command representing a bond step.

    Args:
        step (Real, float, or int): The step value.

    Returns:
        Cmd: A command for the bond step.
    """
    step = parseReal("step", step)
    return Cmd(f'$bound_step({step})')
