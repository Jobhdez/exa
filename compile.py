from passes.select_instructions import *

def compile(expr):
  """
  @params expr: a given Scheme expression
  @returns: an abstract syntax tree representing x86 instructions
  
  note: as of 3/9/23 this code has not been tested but I experimented with these functions in the repl while I developed it.
  """
  ast = parse_tree_to_ast(parser.parse(expr)
  return select_instructions(explicate_control(remove_complex(uniquify(ast,{},0)), 0, {}, {}))
