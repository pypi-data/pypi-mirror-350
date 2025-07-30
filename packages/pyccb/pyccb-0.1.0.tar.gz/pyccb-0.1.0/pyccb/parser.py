import ast
from . import utils

def parse(source: str):
    return ast.parse(source, utils.file_name)
