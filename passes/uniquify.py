from parser.parser import *

def uniquify(ast):
    """ 
    given a let expression that is nested this pass ensures that each var is
    unique.

    param: ast
    returns: a uniquified pass ast

    Example:
        (let ((x 2)) (+ (let ((x 5)) x) x))
        -> 
        (let ((x.1 2)) (+ (let ((x.2 5)) x.2) x.1))
    """
    #ast = ast[0]
    number_of_lets = {}
    counter = 0
    match ast:
        case x if isinstance(x, Let):
            bindings = x.bindings.bindings
            body = x.body
            for binding in bindings:
                if isinstance(binding, Atom):
                    atom = binding.atom
                    counter+=1
                    atom = atom + str(counter)
                    binding.atom = atom
                    number_of_lets[counter] = atom

            for exp in body.expressions:
                if isinstance(exp, Let):
                    bindings = exp.bindings.bindings
                    for binding in bindings:
                        if isinstance(binding, Atom) and binding.atom == 'x':
                            atom = binding.atom
                            counter+=1
                            atom = atom + str(counter)
                            binding.atom = atom
                            number_of_lets[counter] = atom

                    if isinstance(exp.body, Atom) and exp.body.atom == 'x':
                        atom = exp.body
                        atom.atom = number_of_lets[counter]
                        counter-=1

                elif isinstance(exp, Atom) and exp.atom == 'x':
                    exp.atom = number_of_lets[counter]

            return x
                            
                


            



            
            
