import lark

grammar = '''
start  : _exprs
_exprs : _e* _e
_e     : if
       | let
       | ATOM
       | _num
       | BOOL
       | list
TRUE   : "#t"
FALSE  : "#f"
BOOL   : TRUE | FALSE
list   : "(" _exprs? ")"
let    : "(" "let" "(" binding+ ")" _exprs ")"
if     : "(" "if" _e _e _e ")"
binding : "(" ATOM _e ")"
INT    : /[-+]?[0-9]+/
ATOM   : /[a-zA-Z]+[a-zA-Z0-9\-\?\!]*/
       | /[\*\/\=\>\<]/
       | /[\-\+](?![0-9])/
FLOAT  : /[-+]?[0-9]+\.[0-9]*/
_num   : INT | FLOAT
%import common.WS
%import common.NEWLINE
%ignore WS
    '''
# keyword : /[a-z]+/


parser = lark.Lark(grammar)


### Parse Nodes

class Program:
    "PROGRAM node."
    def __init__(self, expressions):
        self.expressions = expressions

    def __repr__(self):
        return f'(Program {self.expressions})'
class If:
    "IF node."
    def __init__(self, condition, scmthen, scmelse):
        self.condition = condition
        self.scmthen = scmthen
        self.scmelse = scmelse

    def __repr__(self):
        return f'(IF (Condition {self.condition}) (Then {self.scmthen}) (Else {self.scmelse}))'

class List:
    "LIST node."
    def __init__(self, expressions):
        self.expressions = expressions

    def __repr__(self):
        return f'(List {self.expressions})'

class Atom:
    "ATOM node."
    def __init__(self, atom):
        self.atom = atom

    def __repr__(self):
        return f'(Atom {self.atom})'

class Int:
    "INT node."
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return f'(Int {self.num})'

class Let:
    "LET node."
    def __init__(self, bindings, body):
        self.bindings = bindings
        self.body = body

    def __repr__(self):
        return f'(Let (Binding {self.bindings}) (Body {self.body}))'

class Binding:
    "BINDING node."
    def __init__(self, bindings):
        self.bindings = bindings

    def __repr__(self):
        return f'{self.bindings}'

def parse_tree_to_ast(tree):
    """
    converts the parse tree into an abstract synstax tree.

    @param tree: the parse tree
    @returns: abstract syntax tree
    """
    match tree:
        case x if isinstance(x, lark.tree.Tree):
            if tree.data == 'start':
                return [make_parse_tree(x) for x in tree.children]
            elif tree.data == 'if':
                if_exps = [make_parse_tree(x) for x in tree.children]
                if_cond = if_exps[0]
                if_then = if_exps[1]
                if_else = if_exps[2]
                return If(if_cond, if_then, if_else)
            elif tree.data == 'let':
                let_exps = [make_parse_tree(x) for x in tree.children]
                if len(let_exps) == 2:
                    let_bindings = let_exps[0]
                    let_body = let_exps[1]
                    return Let(let_bindings, let_body)
                else:
                    length = len(let_exps)
                    let_bindings = let_exps[:length-1]
                    let_body = let_exps[length-1]
                    return Let(let_bindings, let_body)
            elif tree.data == 'binding':
                return Binding([make_parse_tree(x) for x in tree.children])
            else:
                return List([make_parse_tree(x) for x in tree.children])

        case x if isinstance(x, lark.lexer.Token):
            ty = tree.type.lower()
            if ty == 'atom':
                return Atom(tree.value)

            else:
                return Int(tree.value)

        
