from parser.parser import *

def uniquify(ast, lets_dict, counter):
    """ 
     given a let expression that is nested this pass ensures that each var is
    unique.

    param: ast
    returns: a uniquified pass ast

    Example:
        (let ((x 2)) (+ (let ((x 5)) x) x))
        -> 
        (let ((x.1 2)) (+ (let ((x.2 5)) x.2) x.1))
    Example 2:
        (let ((x 1)) (+ (let ((x 4)) (+ (let ((x 5)) x) x)) x))
        ->
        (let ((x.1 1)) (+ (let ((x.2 4)) (+ (let ((x.3)) x.3) x.2) x.1))
    """
    number_of_lets = lets_dict
    match ast:
        
        case x if isinstance(x, List):
            
            return [uniquify(node, number_of_lets, counter) for node in x.expressions]
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
            if isinstance(body, List):
                uniquify(body, number_of_lets, counter)

            elif isinstance(body, Atom) and body.atom == 'x':
                body.atom = number_of_lets[counter]
                counter-=1

        case x if isinstance(x, Atom) and x.atom == 'x':
            x.atom = number_of_lets[counter]

    return x







