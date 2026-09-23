"""Utility functions for Verilog-A generation."""

from vagen.validation import checkType

def blockComment(padding, message, align = "center"):
    """Creates a formatted comment block.

    Args:
        padding (int): Number of tabs for left alignment.
        message (str): The comment text.
        align (str, optional): Alignment of the text 
            ('center', 'left', or 'right'). Defaults to "center".

    Returns:
        str: The formatted comment block.
    """
    #assertions 
    checkType("padding", padding, int)
    checkType("message", message, str)
    checkType("align", align, str)
    #Calculate the block size and the text line width.
    #If the text width is lower than 20 columns, don't return anything
    size = 80 - padding*4
    lineLen = size - 6
    if lineLen < 20:
        return '' 
    #Beginning of the block comment 
    result = "    "*padding + "/" + '*'*(size - 2) + "\n"
    #Look for \n and split the message in lines
    msgChunks = message.split('\n')
    #Go trough every line and build the message. If the message can't fit
    #in a row, it will be split in as many rows as necessary
    for item in msgChunks:
        lines = [item[i:i+lineLen] for i in range(0, len(item), lineLen)]
        for lineItem in lines:
            if align == "center":
                blankSpaceLen = lineLen-len(lineItem)
                half  = round(blankSpaceLen/2)
                left  = " * " + " "*half
                right = " "*(blankSpaceLen - half) + " * " 
            elif align == "left":
                left  = " * " 
                right = " "*(lineLen - len(lineItem)) + " * "
            else:
                left = " * " + " "*(lineLen - len(lineItem))
                right = " * "
            result = result + "    "*padding + left + lineItem + right + "\n"
    #End of the block comment
    result = result + "    "*padding + " " + '*'*(size - 2) + "/\n"
    return result 
    
    
def unary(Type, op1, operator):
    """Generate a unary expression of the form: operator(op1).

    Args:
        Type (type): The type constructor (Real, Integer, or Bool).
        op1 (any): Operand for the unary operation.
        operator (str): String representing the unary operator.

    Returns:
        An instance of Type representing the unary operation.
    """
    return Type(f"{operator}( {op1} )")
    
 
def binary(Type, op1, op2, operator):
    """Generate a binary expression combining op1 and op2 with the given 
    operator.

    Args:
        Type (type): The type constructor (Real, Integer, or Bool).
        op1 (any): The left-hand operand.
        op2 (any): The right-hand operand.
        operator (str): The binary operator as a string.

    Returns:
        An instance of Type representing the binary operation.
    """
    return Type(f"( {op1} ){operator}( {op2} )")