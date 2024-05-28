from ang_modules.lexer import Lexer
from ang_modules.parser import Parser
from ang_modules.interpreter import Interpreter

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python anuraglang.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    with open(source_file, 'r') as file:
        source_code = file.read()

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)  # Debugging print

    parser = Parser(tokens, source_code)
    ast = parser.parse()
    print("AST:", ast)  # Debugging print

    interpreter = Interpreter(ast)
    interpreter.interpret()

if __name__ == "__main__":
    main()
