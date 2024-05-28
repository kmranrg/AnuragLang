class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
        self.functions = {}

    def interpret(self):
        for node in self.ast:
            result = self.evaluate(node)
            if result is not None and isinstance(result, dict) and 'return' in result:
                return result['return']

    def evaluate(self, node):
        node_type = node[0]
        if node_type == 'assignment':
            var_name = node[1]
            value = self.evaluate(node[2])
            self.variables[var_name] = value
        elif node_type == 'produce':
            value = self.evaluate(node[1])
            print(value)
        elif node_type == 'return':
            return {'return': self.evaluate(node[1])}
        elif node_type == 'take':
            var_name = node[1]
            input_value = input()
            try:
                self.variables[var_name] = int(input_value)
            except ValueError:
                self.variables[var_name] = input_value
        elif node_type == 'incase':
            condition = self.evaluate(node[1])
            if condition:
                for stmt in node[2]:
                    self.evaluate(stmt)
            else:
                for stmt in node[3]:
                    self.evaluate(stmt)
        elif node_type == 'while':
            condition = self.evaluate(node[1])
            while condition:
                for stmt in node[2]:
                    self.evaluate(stmt)
                condition = self.evaluate(node[1])
        elif node_type == 'function':
            func_name = node[1]
            parameters = node[2]
            body = node[3]
            self.functions[func_name] = (parameters, body)
            print("Stored function:", func_name, "with parameters:", parameters, "and body:", body)
        elif node_type == 'call':
            func_name = node[1][1]  # Extract the function name directly
            print("Evaluating function call node:", node)
            print("Function name:", func_name)
            arguments = [self.evaluate(arg) for arg in node[2]]
            print("Arguments:", arguments)
            if func_name not in self.functions:
                print("Functions:", self.functions)
                raise ValueError(f'Undefined function: {func_name}')
            parameters, body = self.functions[func_name]
            backup = self.variables.copy()
            self.variables.update(zip(parameters, arguments))
            try:
                for stmt in body:
                    result = self.evaluate(stmt)
                    if isinstance(result, dict) and 'return' in result:
                        return result['return']
            finally:
                self.variables = backup
        elif node_type == 'number':
            return int(node[1])
        elif node_type == 'string':
            return node[1]
        elif node_type == 'variable':
            return self.variables[node[1]]
        elif node_type == 'array':
            return [self.evaluate(element) for element in node[1]]
        elif node_type == 'index':
            array = self.evaluate(node[1])
            index = self.evaluate(node[2])
            if not isinstance(array, list):
                raise TypeError(f"Cannot index non-array type {type(array).__name__}")
            return array[index]
        elif node_type == 'binary':
            left = self.evaluate(node[2])
            right = self.evaluate(node[3])
            operator = node[1][0]
            return self.apply_binary_operator(operator, left, right)
        elif node_type == 'unary':
            operator = node[1][0]
            right = self.evaluate(node[2])
            if operator == 'MINUS':
                return -right
        else:
            raise ValueError(f'Unknown node type: {node_type}')

    def apply_binary_operator(self, operator, left, right):
        if operator == 'PLUS':
            return left + right
        elif operator == 'MINUS':
            return left - right
        elif operator == 'MULTIPLY':
            return left * right
        elif operator == 'DIVIDE':
            return left / right
        elif operator == 'GT':
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left > right
            raise TypeError(f"Cannot compare '>' between {type(left).__name__} and {type(right).__name__}")
        elif operator == 'LT':
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left < right
            raise TypeError(f"Cannot compare '<' between {type(left).__name__} and {type(right).__name__}")
        elif operator == 'EQ':
            return left == right
        else:
            raise ValueError(f"Unknown operator: {operator}")
