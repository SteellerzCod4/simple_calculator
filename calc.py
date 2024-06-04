from messages import *
from input_validator import InputValidator
from math import sin


class Calculator:
    def __init__(self):
        self.__validator = InputValidator()
        self.__valid_functions = {
            "sin": sin,
            "+": self.__add__,
            "-": self.__sub__,
            "%": self.__divmod__,
            "*": self.__mul__,
            "**": self.__pow__,
            "/": self.__truediv__,
            "//": self.__floordiv__
        }

    def __add__(self, l, r):
        return l + r

    def __mul__(self, l, r):
        return l * r

    def __divmod__(self, l, r):
        return l % r

    def __sub__(self, l, r):
        return l - r

    def __pow__(self, l, r):
        return l ** r

    def __truediv__(self, l, r):
        return l / r

    def __floordiv__(self, l, r):
        return l // r

    def __neg__(self, v):
        return -v

    def __process_trigonometry_input(self, user_input):
        func, argument = user_input.split("(")
        argument = argument.replace(")", "", 1)

        sign = self.__check_sign(func)
        if sign:
            func = func[1:]

        result = round(self.__valid_functions[func](float(argument)), 3)
        if sign == "-":
            result = self.__neg__(result)
        return result

    def __check_sign(self, user_input):
        sign = user_input[0]
        if sign == "-" or sign == "+":
            return sign

    def __process_classic_input(self, user_input):
        operation_name = self.__validator.get_operation_name(user_input)

        sign = self.__check_sign(user_input)
        if sign:
            user_input = user_input[1:]

        left_operand_to_output, right_operand_to_output = user_input.split(operation_name)
        left_operand, right_operand = float(left_operand_to_output), float(right_operand_to_output)

        if sign == "-":
            left_operand = self.__neg__(left_operand)
            left_operand_to_output = sign + left_operand_to_output

        result = self.__valid_functions[operation_name](left_operand, right_operand)

        if int(result) == float(result):
            result = int(result)

        return f"{left_operand_to_output} {operation_name} {right_operand_to_output} = {result}"

    def start_working(self):
        process_functions = {
            "TRIG": self.__process_trigonometry_input,
            "CLASSIC": self.__process_classic_input
        }
        print(HELLO_MESSAGE)
        while True:
            user_input = input(INPUT_MESSAGE).lower()

            input_type = self.__validator.validate_user_input(user_input)
            print(process_functions[input_type](user_input))
            user_input = input(CONTINUE_MESSAGE).lower()
            while self.__validator.not_correct_continue_input(user_input):
                print(INCORRECT_CONTINUE_MESSAGE)
                user_input = input(CONTINUE_MESSAGE).lower()

            if user_input == "n":
                break


if __name__ == '__main__':
    calc = Calculator()
    calc.start_working()
