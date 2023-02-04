from passes.remove_complex import *
from passes.uniquify import *
from passes.explicate_control import *
from parser.parser import *

class AssemblyProgram:
    def __init__(self, instructions):
        self.instructions = instructions

    def __repr__(self):
        return f'(AssemblyProgram {self.instructions})'

class Instruction:
    def __init__(self, instr, param1, param2):
        self.instr = instr
        self.param1 = param1
        self.param2 = param2

    def __repr__(self):
        return f'(Instruction {self.instr} (Arg {self.param1}) (Register {self.param2}))'


class Immediate:
    def __init__(self, num):
        self.num = num
    def __repr__(self):
        return f'(Immediate {self.num})'


class Register:
    def __init__(self, reg):
        self.reg = reg

    def __repr__(self):
        return f'(Register {self.reg})'

class Retq:
    def __init__(self, instr):
        self.instr = instr

    def __repr__(self):
        return f'(Retq {self.instr})'



def select_instructions(ast):
    """
    makes the assembly instructions explicit.

    @param ast
    @returns: assembly (x86-64) based ast.

    Example:
        (+ 2 3)

    """

    match ast:
        case x if isprim_addition(x):
            e1 = x.expressions[1]
            e2 = x.expressions[2]
            imm = Immediate(e1)
            imm2 = Immediate(e2)
            reg = Register('%rax')
            instr = Instruction('movq', imm, reg)
            instr2 = Instruction('addq', imm2, reg)
            instr3 = Retq('retq')
            assembly_program = []
            assembly_program.append(instr)
            assembly_program.append(instr2)
            assembly_program.append(instr3)
            return AssemblyProgram(assembly_program)