# Generates a shell script from an AST
# Core Bash generator
import ast
from . import utils


def create_expr(val):
    if type(val) == ast.Constant:
        if type(val.value) == str:
            return f'"{val.value}"'
        return f"{val.value}"
    elif type(val) == ast.Name:
        return f"${{{val.id}}}"
    elif type(val) == ast.BinOp:
        if type(val.op) == ast.Add:
            op = "+"
        elif type(val.op) == ast.Sub:
            op = "-"
        elif type(val.op) == ast.Mult:
            op = "*"
        elif type(val.op) == ast.Div:
            op = "/"
        return f"$(( {create_expr(val.left)} {op} {create_expr(val.right)} ))"
    elif type(val) == ast.Compare:
        # TODO:
        # Logical Operators:
        # !: NOT
        # &&: AND
        # ||: OR
        # Support for compound expressions
        left = create_expr(val.left)
        right = create_expr(val.comparators[0])
        if left.isnumeric() or right.isnumeric():
            if type(val.ops[0]) == ast.Lt:
                op = "-lt"
            elif type(val.ops[0]) == ast.LtE:
                op = "-le"

            elif type(val.ops[0]) == ast.Gt:
                op = "-gt"
            elif type(val.ops[0]) == ast.GtE:
                op = "-ge"

            elif type(val.ops[0]) == ast.Eq:
                op = "-eq"
            elif type(val.ops[0]) == ast.NotEq:
                op = "-ne"
        else:
            if type(val.ops[0]) == ast.Lt:
                op = "<"
            elif type(val.ops[0]) == ast.Gt:
                op = ">"

            elif type(val.ops[0]) == ast.Eq:
                op = "=="
            elif type(val.ops[0]) == ast.NotEq:
                op = "!="
        return f"{left} {op} {create_expr(val.comparators[0])}"
    else:
        utils.error(f"unknown value type '{type(val).__name__}'")
    return ""


def create_block(block: list[ast.stmt], indent=0) -> str:
    compiled = ""
    for command in block:
        compiled += ("   " * indent) + create_statement(command) + "\n"

    return compiled


def create_statement(command: ast.stmt) -> str:
    if type(command) == ast.Expr:
        return create_statement(command.value)
    elif type(command) == ast.Call:
        return (
            f"{command.func.id} {' '.join([create_expr(arg) for arg in command.args])}"
        )
    elif type(command) == ast.Assign:
        return f"{command.targets[0].id}={create_expr(command.value)}"
    elif type(command) == ast.If:
        else_ = ""
        if command.orelse:
            else_ = "else\n" + create_block(command.orelse, 1)
        return (
            f"if [ {create_expr(command.test)} ]; then\n"
            + create_block(command.body, 1)
            + else_
            + "fi"
        )
    elif type(command) == ast.While:
        # command.test
        return f"while [ {create_expr(command.test)} ]\ndo\n" + create_block(command.body, 1) + "done"
    else:
        utils.error(f"unknown command '{type(command).__name__}'")
    return ""


def generate(program: ast.Module) -> str:
    return create_block(program.body)
