"""Disciplines currently with Electrical signal and branch primitives."""

from vagen.commands import Cmd
from vagen.types import Real
from vagen.validation import (
    checkInstance, 
    checkNotInstance, 
    checkType, parseBool, 
    parseReal
)

class Electrical():
    """Class representing an electrical signal with voltage and current."""

    def __init__(self, name):
        """Initialize an Electrical signal.

        Args:
            name (str): The name of the electrical signal.
        """
        checkType("name", name, str)
        self.name = name
        self.v = Real(f"V({name})") 
        self.i = Real(f"I({name})") 
        
    def getName(self):
        """Return the name of the electrical signal.

        Returns:
            str: The signal's name.
        """
        return self.name

    def vCont(self, value):
        """Return a command for a voltage contribution.

        Args:
            value (Real, float, or int): The contribution value.

        Returns:
            Cmd: A command representing the voltage contribution.
        """
        value = parseReal("value", value)
        return Cmd(f'V({self.name}) <+ {value}')

    def iCont(self, value):
        """Return a command for a current contribution.

        Args:
            value (Real, float, or int): The contribution value.

        Returns:
            Cmd: A command representing the current contribution.
        """
        value = parseReal("value", value)
        return Cmd(f'I({self.name}) <+ {value}')

    def vAttr(self, value):
        """Return a command for a voltage attribution.

        Args:
            value (Real, float, or int): The attribution value.

        Returns:
            Cmd: A command representing the voltage attribution.
        """
        value = parseReal("value", value)
        return Cmd(f'V({self.name}) = {value}')

    def iAttr(self, value):
        """Return a command for a current attribution.

        Args:
            value (Real, float, or int): The attribution value.

        Returns:
            Cmd: A command representing the current attribution.
        """
        value = parseReal("value", value)
        return Cmd(f'I({self.name}) = {value}')

    def vInd(self, value):
        """Return a command for a voltage indirect assignment.

        Args:
            value (Bool or bool): The condition for the assignment.

        Returns:
            Cmd: A command representing the voltage indirect assignment.
        """
        value = parseBool("value", value)
        return Cmd(f'V({self.name}) : {value}')

    def iInd(self, value):
        """Return a command for a current indirect assignment.

        Args:
            value (Bool or bool): The condition for the assignment.

        Returns:
            Cmd: A command representing the current indirect assignment.
        """
        value = parseBool("value", value)
        return Cmd(f'I({self.name}) : {value}')
 

class Branch(Electrical):
    """Class representing a branch connecting two electrical signals."""

    def __init__(self, node1, node2):
        """Initialize a Branch instance connecting two nodes.

        Args:
            node1 (Electrical): The first node.
            node2 (Electrical): The second node.
        """
        checkInstance("node1", node1, Electrical)
        checkInstance("node2", node2, Electrical)
        checkNotInstance("node1", node1, Branch)
        checkNotInstance("node2", node2, Branch)
        super(Branch, self).__init__(f"{node1.getName()}, {node2.getName()}")
