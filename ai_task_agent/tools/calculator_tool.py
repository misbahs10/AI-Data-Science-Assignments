
import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def calculate(expression: str) -> str:
    """Safely evaluate basic mathematical expressions."""

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) not in (int, float):
                    raise ValueError("Only numeric values are allowed.")
                return node.value

            if isinstance(node, ast.BinOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Unsupported operator.")

                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Pow) and abs(right) > 10:
                    raise ValueError("Exponent is too large.")

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Unsupported operator.")

                return operation(evaluate(node.operand))

            raise ValueError("Invalid mathematical expression.")

        result = evaluate(tree)

        if isinstance(result, (int, float)) and abs(result) > 1e100:
            raise ValueError("Result is too large.")

        return str(result)

    except Exception as error:
        return f"Calculation error: {error}"
