from passes.remove_complex import *
from passes.uniquify import *
from parser.parser import *

class CProgram:
    def __init__(self, exps):
        self.exps = exps

    def __repr__(self):
        return f'(CProgram {self.exps})'

class CReturn:
    def __init__(self, exps):
        self.exps = exps
    def __repr__(self):
        return f'(Return {self.exps})'

class Assign:
    def __init__(self, var, exp):
        self.var = var
        self.exp = exp
    def __repr__(self):
        return f'(Assign {self.var} {self.exp})'

class Prim:
    def __init__(self, op, operands):
        self.op = op
        self.operands = operands

    def __repr__(self):
        return f'(Prim {self.op} {self.operands})'

def explicate_control(ast, counter, vars, assignments):
    """
    Make order of execution clear.

    @param ast
    @returns: ast with clear order of exceution

    Example:
       (let ((x.1 2)) (+ (let ((x.2 5)) x.2) x.1))
       ->
       start:
         x.1 = 2
         x.2 = 5
         return x.1 + x.2

    Example 2:
        (let ((x.1 1)) (+ (let ((x.2 4)) (+ (let ((x.3 5)) x.3) x.2) x.1))
        ->
        start:
           x.1 = 1
           x.2 = 4
           x.3 = 5
           return x.1 + x.2 + x.4
    """
    
    vars = vars
    assignments = assignments
    match ast:
        case x if isinstance(x, Int):
            return x
        case x if isinstance(x, Let):
            bindings = x.bindings.bindings 
            var, exp = bindings
            vars[counter] = var
            assignments[counter] = Assign(var, exp)
            if isinstance(x.body, List) and x.body.expressions[0].atom == '+':
               counter += 1
               explicate_control(x.body.expressions[1], counter, vars, assignments)
            
    creturn = []
    creturn.append(CReturn(Prim(Atom('+'), list(vars.values()))))
    return CProgram(list(assignments.values()) + creturn)