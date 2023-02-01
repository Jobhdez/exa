from passes.uniquify import *
from parser.parser import *

def remove_complex(ast):
    """
    removes the complex expressions resulting only in atomic expressions.

    @params ast: the ast transformed by the `uniquify` pass
    @returns: ast with atomic expressions

    Example:
        (+ 53 (- 10)) -> (let ((temp.1 (- 10))) (+ 53 temp.1))

    Example 2:
        (let ((x (+ 10 (- 3))) x))
        ->
        (let ((x (let ((temp.1 (- 3))) (+ 10 temp.1))) x)

    """
    match ast:
        case x if isinstance(x, List) and x.expressions[0].atom == '+':
            counter = 0
            temp = "temp"
            if len(x.expressions) == 3:
                if isinstance(x.expressions[1], Int) and isinstance(x.expressions[2], Int):
                    return x
                elif isinstance(x.expressions[1], Int) and isinstance(x.expressions[2], List):
                    if x.expressions[2].expressions[0].atom == '-' and len(x.expressions[2].expressions) == 2:
                        counter += 1
                        atom = temp + str(counter)
                        atom_node = Atom(atom)
                        return Let([atom_node, x.expressions[2]], List([x.expressions[0], x.expressions[1], atom_node]))

        case x if isinstance(x, Let):
            bindings = x.bindings.bindings
            expr = bindings[1]
            if iscomplex(expr):
                return Let([bindings[0], remove_complex(expr)], x.body)


def iscomplex(expr):
    "checks if `expr` is complex."
    match expr:
        case x if isinstance(x, List) and len(x.expressions) == 3:
            exprs = x.expressions[2].expressions
            if len(exprs) == 2:
                atom = exprs[0].atom
                num = exprs[1]
                if atom == '-' and isinstance(num, Int):
                    return True
                else:
                    return False


            