from .utils import sum_numbers, multiply_numbers, divide_numbers, subtract_numbers


class Calculator:
    def add(self, a, b):
        return sum_numbers(a, b)

    def subtract(self, a, b):
        return subtract_numbers(a, b)

    def multiply(self, a, b):
        return multiply_numbers(a, b)

    def divide(self, a, b):
        return divide_numbers(a, b)
