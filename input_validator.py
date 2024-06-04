class InputValidator:
    MAIN_OPERATIONS = ["+", "-", "*", "/", "//", "%", "**"]
    TRIGONOMETRY_OPERATIONS = ["sin"]

    def __check_operations(self, user_input):
        if not any([operation in user_input for operation in self.MAIN_OPERATIONS + self.TRIGONOMETRY_OPERATIONS]):
            raise ValueError("Wrong operation")

    def __is_trigonometry(self, user_input):
        return any([operation in user_input for operation in self.TRIGONOMETRY_OPERATIONS])

    @staticmethod
    def __check_sign(value):
        sign = value[0]
        if sign == "-" or sign == "+":
            if value[1] == "-" or value[1] == "+":
                raise ValueError("Wrong signs before value.")
            return sign

    def __validate_trig_argument(self, trig_argument):
        sign = self.__check_sign(trig_argument)
        if sign:
            trig_argument = trig_argument[1:]

        if not trig_argument.isdigit():
            print(trig_argument)
            raise ValueError("Wrong argument in trigonometry function.")

    def __validate_trig_function(self, trig_function):
        if trig_function not in self.TRIGONOMETRY_OPERATIONS:
            raise ValueError("Wrong trigonometry function or wrong sign before function")

    def __validate_trigonometry(self, user_input):
        left_bracket, right_bracket = user_input.find("("), user_input.rfind(")")
        if left_bracket == -1 or right_bracket == -1:
            raise ValueError("Wrong brackets")

        trig_argument = user_input[left_bracket + 1: right_bracket]
        self.__validate_trig_argument(trig_argument)
        self.__validate_trig_function(user_input[:left_bracket])

    @staticmethod
    def __remove_sign(user_input):
        sign = user_input[0]
        if sign == "-" or sign == "+":
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
            raise ValueError("Wrong amount of components.")

        left_operand, right_operand = components
        left_operand, right_operand = left_operand.replace(".", "", 1), right_operand.replace(".", "", 1)
        if not left_operand.isdigit() and right_operand.isdigit():
            raise ValueError("Wrong operands.")

        if (operation_name == '/' or operation_name == "//") and float(right_operand) == 0:
            raise ValueError("Division by zero.")

    @staticmethod
    def not_correct_continue_input(user_input):
        if len(user_input) != 0:
            return user_input not in ["n", "y"]
        return False

    def validate_user_input(self, user_input):
        user_input = user_input.strip().lower()
        sign = self.__check_sign(user_input)
        if sign:
            user_input = user_input[1:]

        self.__check_operations(user_input)

        if self.__is_trigonometry(user_input):
            self.__validate_trigonometry(user_input)
            return "TRIG"

        self.__validate_classic_input(user_input)
        return "CLASSIC"
