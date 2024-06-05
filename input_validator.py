class InputValidator:
    MAIN_OPERATIONS = ["+", "-", "*", "/", "//", "%", "**"]
    TRIGONOMETRY_OPERATIONS = ["sin"]
    CORRECT_SIGNS = {"+", "-"}
    CORRECT_CONTINUE_SYMBOLS = {"n", "y"}

    def __check_operations(self, user_input):
        if not any([operation in user_input for operation in self.MAIN_OPERATIONS + self.TRIGONOMETRY_OPERATIONS]):
            return ValueError("Wrong operation.")

    def __is_trigonometry(self, user_input):
        return any([operation in user_input for operation in self.TRIGONOMETRY_OPERATIONS])

    def __check_signs(self, value):
        sign = value[0]
        if sign in self.CORRECT_SIGNS:
            if value[1] == "-" or value[1] == "+":
                return ValueError("Wrong signs before value.")
            return sign

    def __validate_trig_argument(self, trig_argument):
        sign_or_error = self.__check_signs(trig_argument)
        if sign_or_error in self.CORRECT_SIGNS:
            trig_argument = trig_argument[1:]
        if isinstance(sign_or_error, ValueError):
            return sign_or_error

        if not trig_argument.replace(".", "", 1).isdigit():
            return ValueError("Wrong argument in trigonometry function.")

    def __validate_trig_function(self, trig_function):
        if trig_function not in self.TRIGONOMETRY_OPERATIONS:
            return ValueError("Wrong trigonometry function or wrong sign before function.")

    def __validate_trigonometry(self, user_input):
        left_bracket, right_bracket = user_input.find("("), user_input.rfind(")")
        if left_bracket == -1 or right_bracket == -1:
            return ValueError("Wrong brackets.")

        trig_argument = user_input[left_bracket + 1: right_bracket]
        error = self.__validate_trig_argument(trig_argument)
        if isinstance(error, ValueError):
            return error

        error = self.__validate_trig_function(user_input[:left_bracket])
        if isinstance(error, ValueError):
            return error

    def __remove_sign(self, user_input):
        sign = user_input[0]
        if sign in self.CORRECT_SIGNS:
            user_input = user_input[1:]
        return user_input

    def get_operation_name(self, user_input):
        user_input = self.__remove_sign(user_input)
        operation_name = ""
        for operation in self.MAIN_OPERATIONS:
            if operation in user_input:
                operation_name = operation

        return operation_name

    def __validate_classic_input(self, user_input):
        operation_name = self.get_operation_name(user_input)

        components = [element.strip() for element in user_input.split(operation_name)]
        if len(components) != 2:
            return ValueError("Wrong amount of components.")

        left_operand, right_operand = components
        left_operand, right_operand = left_operand.replace(".", "", 1), right_operand.replace(".", "", 1)
        if not (left_operand.isdigit() and right_operand.isdigit()):
            return ValueError("Wrong operands.")

        if (operation_name == '/' or operation_name == "//") and float(right_operand) == 0:
            return ValueError("Division by zero.")

    def not_correct_continue_input(self, user_input):
        if len(user_input) != 0:
            return user_input not in self.CORRECT_CONTINUE_SYMBOLS
        return False

    def validate_user_input(self, user_input):
        sign_or_error = self.__check_signs(user_input)
        if sign_or_error in self.CORRECT_SIGNS:
            user_input = user_input[1:]
        if isinstance(sign_or_error, ValueError):
            return sign_or_error

        error = self.__check_operations(user_input)
        if isinstance(error, ValueError):
            return error

        if self.__is_trigonometry(user_input):
            error = self.__validate_trigonometry(user_input)
            if isinstance(error, ValueError):
                return error
            return "TRIG"

        error = self.__validate_classic_input(user_input)
        if isinstance(error, ValueError):
            return error
        return "CLASSIC"
