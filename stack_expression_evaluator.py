

from __future__ import annotations
from typing import Generic, List, TypeVar
import re

T = TypeVar("T")


class Stack(Generic[T]):
    """A simple LIFO (Last-In, First-Out) stack implementation."""

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True when the stack contains no items."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self._items)


# Operator precedence: larger value means higher precedence.
PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}

OPERATORS = set(PRECEDENCE)


def apply_operator(values: Stack[float], operator: str) -> None:
    """Pop two operands, apply an operator, and push the result."""
    right = values.pop()
    left = values.pop()

    if operator == "+":
        result = left + right
    elif operator == "-":
        result = left - right
    elif operator == "*":
        result = left * right
    elif operator == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        result = left / right
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    values.push(result)


def tokenize(expression: str) -> List[str]:
    """
    Convert an expression into numbers, operators, and parentheses.

    Unary + or - is attached to a number, e.g. -5 or 3*-2.
    """
    tokens: List[str] = []
    i = 0
    expecting_operand = True

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        # Unary sign before a number.
        if char in "+-" and expecting_operand:
            j = i + 1
            while j < len(expression) and expression[j].isspace():
                j += 1

            if j < len(expression) and (expression[j].isdigit() or expression[j] == "."):
                start = i
                i = j

                dot_count = 0
                digit_count = 0
                while i < len(expression) and (
                    expression[i].isdigit() or expression[i] == "."
                ):
                    if expression[i] == ".":
                        dot_count += 1
                    else:
                        digit_count += 1
                    i += 1

                if dot_count > 1 or digit_count == 0:
                    raise ValueError("Invalid number.")
                tokens.append(expression[start:i].replace(" ", ""))
                expecting_operand = False
                continue

        # Number (integer or decimal).
        if char.isdigit() or char == ".":
            start = i
            dot_count = 0
            digit_count = 0

            while i < len(expression) and (
                expression[i].isdigit() or expression[i] == "."
            ):
                if expression[i] == ".":
                    dot_count += 1
                else:
                    digit_count += 1
                i += 1

            if dot_count > 1 or digit_count == 0:
                raise ValueError("Invalid number.")

            tokens.append(expression[start:i])
            expecting_operand = False
            continue

        if char == "(":
            tokens.append(char)
            expecting_operand = True
            i += 1
            continue

        if char == ")":
            tokens.append(char)
            expecting_operand = False
            i += 1
            continue

        if char in OPERATORS:
            tokens.append(char)
            expecting_operand = True
            i += 1
            continue

        raise ValueError(f"Invalid character: {char!r}")

    if not tokens:
        raise ValueError("Expression is empty.")

    return tokens


def evaluate_expression(expression: str) -> float:
    """
    Evaluate an arithmetic expression using two stacks.

    values: stores operands/results.
    operators: stores operators and parentheses.

    Time complexity: O(n)
    Space complexity: O(n)
    """
    tokens = tokenize(expression)
    values: Stack[float] = Stack()
    operators: Stack[str] = Stack()

    for token in tokens:
        if re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", token):
            values.push(float(token))

        elif token == "(":
            operators.push(token)

        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(values, operators.pop())

            if operators.is_empty():
                raise ValueError("Mismatched parentheses.")

            operators.pop()  # Remove '('.

        elif token in OPERATORS:
            while (
                not operators.is_empty()
                and operators.peek() != "("
                and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]
            ):
                apply_operator(values, operators.pop())

            operators.push(token)

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("Mismatched parentheses.")
        apply_operator(values, operators.pop())

    if values.size() != 1:
        raise ValueError("Invalid expression.")

    return values.pop()


def format_result(value: float) -> str:
    """Write whole-number results without an unnecessary .0."""
    if value.is_integer():
        return str(int(value))
    return f"{value:.10f}".rstrip("0").rstrip(".")


def is_separator(line: str) -> bool:
    """Recognize a separator line such as ---- or =====."""
    stripped = line.strip()
    return (
        len(stripped) >= 2
        and all(char in "-=_~" for char in stripped)
    )


def process_file(input_file: str = "input.txt", output_file: str = "output.txt") -> None:
    """Read, evaluate, and write expressions while preserving separators."""
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    output_lines: List[str] = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        if is_separator(line):
            output_lines.append(line)
            continue

        try:
            result = evaluate_expression(line)
            output_lines.append(format_result(result))
        except (ValueError, IndexError, ZeroDivisionError) as error:
            output_lines.append(f"ERROR: {error}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(output_lines))
        if output_lines:
            outfile.write("\n")


def main() -> None:
    process_file("input.txt", "output.txt")
    print("Evaluation complete. Results written to output.txt.")


if __name__ == "__main__":
    main()
