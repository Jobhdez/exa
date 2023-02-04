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

    Example 3:
       (let ((temp.1 (- 10))) (+ 53 temp.1))
       ->
       start:
          temp.1 = - 10
          return 53 + temp1

    Example 4:
        (let ((x (let ((temp.1 (- 3))) (+ 10 temp.1))) x)
        ->
        start:
            temp1 = - 3
            x = 10 + temp1
            return x
    Example 5:
         (+ 3 4)
    """
    
    vars = vars
    assignments = assignments
    match ast:
        case x if isinstance(x, Int):
            return x
        case x if isinstance(x, Let):
            if isinstance(x.bindings, Binding):
                bindings = x.bindings.bindings 
                var, exp = bindings
                vars[counter] = var
                assignments[counter] = Assign(var, exp)
                if isinstance(x.body, List) and x.body.expressions[0].atom == '+' and isinstance(x.body.expressions[1], Let):
                    counter += 1
                    explicate_control(x.body.expressions[1], counter, vars, assignments)
                    creturn = []
                    creturn.append(CReturn(Prim(Atom('+'), list(vars.values()))))
                    return CProgram(list(assignments.values()) + creturn)
            elif isinstance(x.bindings, list):
                bindings = x.bindings
                var, exp = bindings
                vars[counter] = var
                assignments[counter] = Assign(var, exp)
                
                if isprim_addition(x.body) and x.body.expressions[0].atom == '+':
                    exp1 = x.body.expressions[1]
                    exp2 = x.body.expressions[2]
                    prim_exps = []
                    prim_exps.append(exp1)
                    prim_exps.append(exp2)
                    cret = []
                    cret.append(CReturn(Prim(Atom('+'), prim_exps)))
                    return CProgram(list(assignments.values()) + cret)

                elif isinstance(bindings[1], Let):
                    program = explicate_control(bindings[1], 0, {}, {})
                    bind = bindings[0]
                    assigns = []
                    ret = []
                    for statement in program.exps:
                        if isinstance(statement, Assign):
                            assigns.append(statement)
                        else:
                            ret.append(statement)

                    retexp = ret[0].exps
                    new_assigment = Assign(bind, retexp)
                    assigns.append(new_assigment)
                    newret = CReturn(bind)
                    ret = []
                    ret.append(newret)
                    return CProgram(assigns + ret)
        case x if isprim_addition(x):
            e1 = x.expressions[1]
            e2 = x.expressions[2]
            exps = []
            exps.append(e1)
            exps.append(e2)
            
            return CProgram(CReturn(Prim(Atom('+'), exps)))



def isprim_addition(ast):
    match ast:
        case x if isinstance(x, List) and x.expressions[0].atom =='+':
            return isinstance(x.expressions[1], Int) and (isinstance(x.expressions[2], Atom) or isinstance(x.expressions[2], Int))
