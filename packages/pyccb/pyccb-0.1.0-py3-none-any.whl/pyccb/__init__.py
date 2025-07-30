from . import utils
from . import parser
from . import generate


def compile(source: str, source_name: str):
    utils.file_name = source_name

    ast = parser.parse(source)
    output = generate.generate(ast)

    return output
