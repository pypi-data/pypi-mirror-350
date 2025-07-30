# sum number
def sum_numbers(a: int, b: int):
    """
    Sums two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    return a + b


def multiply_numbers(a, b):
    """
    Multiplies two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of the two numbers.
    """
    return a * b


def divide_numbers(a, b):
    """
    Divides two numbers.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The quotient of the two numbers.

    Raises:
        ValueError: If the denominator is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def subtract_numbers(a, b):
    """
    Subtracts two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The result of subtracting the second number from the first.
    """
    return a - b
