from passes.remove_complex import *
from passes.uniquify import *
from passes.explicate_control import *
from parser.parser import *


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