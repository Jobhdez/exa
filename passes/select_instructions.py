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
        start:
         x.1 = 2
         x.2 = 5
         return x.1 + x.2
        ->
        movq 2, x
        addq 5, x
        retq

    Example 2:
         start:
           x.1 = 1
           x.2 = 4
           x.3 = 5
           return x.1 + x.2 + x.4
        ->
        movq 1, x1
        addq 4, x1
        addq 5, x1
        retq

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

        case x if isinstance(x, CProgram):
            exps = x.exps
            ret = exps[len(exps)-1]
            ret = ret.exps
            if isinstance(ret, Prim) and all(isinstance(x, Atom) for x in ret.operands):
                length = len(exps)
                ret = exps[length-1]
                assi1 = exps[0]
                var = assi1.var
                rest_assi = exps[1:]
                firsts = rest_assi[:-1]
                addqs = [make_addqs(x,var) for x in firsts]
                imm = Immediate(assi1.exp)
                instr = Instruction('movq', imm, var)
                retq = Retq('retq')
                instrs = []
                instrs.append(instr)
                instrs = instrs + addqs
                instrs.append(retq)
                return AssemblyProgram(instrs)
        

def make_addqs(assignment, var):
    exp = assignment.exp
    instr = Instruction('addq', Immediate(exp), var)
    return instr
        




        