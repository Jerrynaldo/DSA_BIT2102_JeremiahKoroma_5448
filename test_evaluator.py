from stack_expression_evaluator import evaluate_expression

tests = {
    "3 + 5 * 2": 13,
    "(8 / 4) + 7 * 2": 16,
    "10 - (2 + 3) * 4": -10,
    "5 / 2": 2.5,
    "-3 + 5": 2,
    "3 * -2": -6,
    "2 * (3 + 4)": 14,
    "((2 + 3) * 4) / 5": 4,
    "2 + 3 * 4 - 5": 9,
}

for expression, expected in tests.items():
    actual = evaluate_expression(expression)
    assert actual == expected, f"{expression}: expected {expected}, got {actual}"

try:
    evaluate_expression("2 / (1 - 1)")
except ZeroDivisionError:
    pass
else:
    raise AssertionError("Division by zero was not detected.")

print("All automated tests passed.")
