import re
import sys


class PryzmaInterpreter:
    def __init__(self):
        self.variables = {'if_condition': 'true'}

    def interpret_file(self, file_path):
        file_path = file_path.strip('"')
        with open(file_path, 'r') as file:
            program = file.read()
            self.interpret(program)

    def interpret(self, program):
        lines = program.split('\n')

        for line in lines:
            line = line.strip()

            if line.startswith("PRINT"):
                value = line[len("PRINT"):].strip()
                self.print_value(value)
            elif line.startswith("INPUT"):
                variable = line[len("INPUT"):].strip()
                self.custom_input(variable)
            elif "=" in line:
                variable, expression = line.split('=')
                variable = variable.strip()
                expression = expression.strip()
                self.assign_variable(variable, expression)
            elif line.startswith("IF"):
                _, condition_action = line.split("(")
                condition, action = condition_action.split(",")
                condition = condition.strip()
                action = action.strip().rstrip(")")
                if condition in self.variables and self.variables[condition] == self.variables['if_condition']:
                    self.interpret(action)
            elif line == "STOP":
                self.stop_program()
            else:
                print(f"Invalid statement: {line}")




    def assign_variable(self, variable, expression):
        self.variables[variable] = expression  # Assign the raw expression to the variable

        # Re-evaluate all expressions that use the updated variable
        for var in self.variables:
            for key in self.variables.keys():
                if self.variables[key] == var:
                    self.variables[key] = self.evaluate_expression(var)

        value = self.evaluate_expression(expression)  # Re-evaluate the expression

        if value is not None:
            self.variables[variable] = value
        else:
            print(f"Invalid expression: {expression}")

    def evaluate_expression(self, expression):
        if re.match(r"^\d+$", expression):
            return int(expression)

        if expression in self.variables:
            return self.variables[expression]

        if re.match(r'^".*"$', expression):
            return expression[1:-1]

        if "+" in expression:
            parts = expression.split("+")
            evaluated_parts = [self.evaluate_expression(part.strip()) for part in parts]
            if all(isinstance(part, str) for part in evaluated_parts):
                return "".join(evaluated_parts)

        try:
            return eval(expression, {}, self.variables)
        except NameError:
            print(f"Unknown variable: {expression}")
        except:
            print(f"Invalid expression: {expression}")

    def print_value(self, value):
        evaluated_value = self.evaluate_expression(value)

        if evaluated_value is not None:
            print(evaluated_value)

    def custom_input(self, variable):
        prompt = f"Enter a value for {variable}: "
        value = self.get_input(prompt)
        self.variables[variable] = value

    def get_input(self, prompt):
        if sys.stdin.isatty():
            return input(prompt)
        else:
            sys.stdout.write(prompt)
            sys.stdout.flush()
            return sys.stdin.readline().rstrip('\n')

    def stop_program(self):
        input("Press Enter to exit...")

    def evaluate_condition(self, condition):
        if condition in self.variables:
            return bool(self.variables[condition])
        else:
            print(f"Unknown variable in condition: {condition}")
            return False

    def interpret_file2(self):
        file_path = input("Enter the file path of the program: ")
        self.interpret_file(file_path)

    def show_license(self):
        license_text = """
Pryzma
Copyright 2024 Igor Cielnaik

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
        """

        print(license_text)


if __name__ == "__main__":
    interpreter = PryzmaInterpreter()

    print("""Pryzma 3.0
To show the license type "license" or to run code from file type "file"
    """)

    while True:
        code = input("/// ")
        if code == "exit":
            break
        elif code == "run from file":
            interpreter.interpret_file2()
        elif code == "license":
            interpreter.show_license()
        else:
            interpreter.interpret(code)
            print(interpreter.variables)