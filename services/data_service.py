import pandas as pd
import numpy as np


class DataService():
    """_summary_
    """
    def __init__(self, file):
        self.file = file
        self.data = pd.read_csv(file)
        self.numbers = self.data["Numbers"]
        self.body = self.data["Body"]
        self.question = self.data["Ques"]
        self.answer = self.data["Answer"]
        self.n = self.numbers.shape[0]
        self.create_math_pb()
        self.create_label()
        self.create_linear_equation()
        # drop data with incorrect linear formula
        index_names = self.data[self.data['linear_equation'] == 'NAN'].index
        self.data.drop(index_names, inplace=True)

    def create_math_pb(self):
        clean_body = self.body.values
        clean_question = self.question.values
        for i in range(len(self.numbers)):
            clean_body[i] = clean_body[i].capitalize()
            if not isinstance(clean_question[i], str):
                clean_question[i] = ""
            clean_question[i] = clean_question[i].capitalize()
        clean_body = np.array([self.clean_sentence(i) for i in clean_body])
        clean_question = np.array([self.clean_sentence(i, True) for i in clean_question])
        self.math_pb = []
        for body, quest in zip(clean_body, clean_question):
            self.math_pb.append(body + " " + quest)
        self.math_pb = np.array(self.math_pb)

    def create_label(self):
        file_name = self.file.split("/")[-1]
        self.data["label"] = self.data.index.astype('str') + ";" + file_name
        self.label = self.data["label"].values

    def create_linear_equation(self):
        linear_equation = []
        for equation in self.data["Equation"]:
            linear_equation.append(self.tree2linear(equation)[:-3])
        self.data["linear_equation"] = linear_equation

    def get_item(self, index):
        return self.data.iloc[index].to_dict()

    def get_math_pb(self, index):
        return self.math_pb[index]

    @staticmethod
    def clean_sentence(sentence, question=False):
        # capitalize first letter
        sentence = sentence.capitalize()
        # sentence = "bonjour .moi j'ai 25.2 a ans avec 2."
        # add , and manage space
        sentence_split = sentence.split(".")
        if sentence_split[-1] == "":
            del sentence_split[-1]
        sentence_split2 = []
        follow = True
        for i in range(len(sentence_split)):
            if i == len(sentence_split)-1 and not(follow):
                follow = True
            elif i == len(sentence_split)-1:
                sentence_split2.append(sentence_split[i])
            elif sentence_split[i][-1].isdigit() and sentence_split[i+1][0].isdigit():
                sentence_split2.append(sentence_split[i] + "." + sentence_split[i+1])
                follow = False
            elif follow:
                sentence_split2.append(sentence_split[i])
            else:
                follow = True
        new_sentence = ""
        for i, s in enumerate(sentence_split2):
            if s != "":
                if s[0] != " ":
                    s = " " + s
                if s[-1] == " ":
                    s = s[:-1]
                new_sentence = new_sentence + "," + s
        if question:    
            if new_sentence != "":
                if new_sentence[-1] != "?":
                    new_sentence = new_sentence[:-1] + "?"
            return new_sentence[2:]
        else:
            return new_sentence[2:] + "."

    def tree2linear(self, equation):
        """
        - + number1 number2 number3 --> add(number1, number2) | subtract(#0, number3)
        - number1 + number2 number3 --> add(number2, number3) | subtract(#0, number1)
        """
        number_list = ['number0', 'number1', 'number2', 'number3', 'number4', 'number5', 'number6']
        operation_dict = {'+': 'add', '-': 'substract', '/': 'divide', '*': 'multiply'}
        operation_list = ['*', '+', '-', '/']
        operation_list2 = ["multiply", "add", "substract", "divide"]

        # equation = "- number1 + number2 number3"
        # equation = "* - 1.0 * + 1.0 * number0 0.01 - 1.0 * number0 0.01 100.0"
        operations, numbers = self._occurance(operation_list, number_list, equation)
        o_index, v_index, c_index = self.get_index(operation_list, number_list, equation)
        list_equation = equation.split(' ')
        if len(operations) == 1:
            i = 0
            if c_index == []:
                linear_equation = '#'+str(0) + ": " + operation_dict[operations[0]] + ' ( '+numbers[i] + ', '+numbers[i+1]+' )' + ' | '
            else:
                linear_equation = '#'+str(0) + ": " + operation_dict[operations[0]] + ' ( '+list_equation[i+1] + ', '+list_equation[i+2]+' )' + ' | '
        
        elif len(operations) == 2:
            # if the pattern is operation2 operation1 numberX numberY numberZ
            operations = operations[::-1]
            if 0 in o_index and 1 in o_index:
                for i in range(len(operations)):
                    if i == 0:
                        linear_equation = '#'+str(i) + ": " + operation_dict[operations[i]] + ' ( '+list_equation[i+2] + ', '+list_equation[i+3]+' )' + ' | '
                    else:
                        linear_equation = linear_equation + '#'+str(i) + ": " + operation_dict[operations[i]]+' ( ' + '#'+str(i-1) + ', '+list_equation[i+3]+' )' + ' | '
            else:
                # if the pattern is operation2 numberZ operation1 numberX numberY
                start_index = len(operations)
                for i in range(len(operations)):
                    if i == 0:
                        linear_equation = '#'+str(i) + ": " + operation_dict[operations[i]] + ' ( '+list_equation[start_index+i+1] + ', '+list_equation[start_index+i+2] + ' )' + ' | '
                    else:
                        linear_equation = linear_equation + '#'+str(i) + ": " + operation_dict[operations[i]] + ' ( '+list_equation[start_index-i] + ', #'+str(i-1) + ' )' + ' | '

        elif len(operations) > 2:
            operations = operations[::-1]
            start_index = len(operations)
            if not o_index[0] and all(y-x == 1 for x, y in zip(o_index, o_index[1:])): # check if the o_index is incrementing one at a time 0,1,2,3,..., len(operations)
                for i in range(len(operations)):
                    if i == 0:
                        linear_equation = '#'+str(i) + ": " + operation_dict[operations[i]] +' ( ' + list_equation[start_index+i] + ', ' + list_equation[start_index+i+1] + ' )' + ' | '
                    else:
                        linear_equation = linear_equation + '#'+str(i) + ": " + operation_dict[operations[i]] + ' ( ' + '#'+str(i-1) + ', ' + list_equation[start_index+i+1] + ' )' + ' | '

            else:
                linear_equation = "NAN"
        else:
            linear_equation = "NAN"

        return linear_equation

    @staticmethod
    def _occurance(operation_list, number_list, equation):
        operations = []
        numbers = []
        list_equation = equation.split(' ')

        for i in range(len(list_equation)):
            if list_equation[i] in operation_list:
                operations.append(list_equation[i])
            elif list_equation[i] in number_list:
                numbers.append(list_equation[i])

        return operations, numbers

    @staticmethod
    def get_index(operation_list, number_list, equation):
        operation_index = []
        value_index = []
        constant_index = []
        list_equation = equation.split(' ')
        for i in range(len(list_equation)):
            if list_equation[i] in operation_list:
                operation_index.append(i)
            elif list_equation[i] in number_list:
                value_index.append(i)
            else:
                constant_index.append(i)

        return operation_index, value_index, constant_index


def oracle_hint(linear_equation_gen, linear_equation_true):
    if linear_equation_gen == linear_equation_true:
        return "No"
    hint = ""
    nb_operation_gen = len(linear_equation_gen.split('|'))
    nb_operation_true = len(linear_equation_true.split('|'))
    n = nb_operation_true
    if nb_operation_gen > nb_operation_true:
        hint += "Remove an operation. "
        n = nb_operation_true
    if nb_operation_gen < nb_operation_true:
        hint += "Add an operation. "
        n = nb_operation_gen
    for i in range(n):
        operation_true = linear_equation_true.split('|')[i].split(" ")
        operation_gen = linear_equation_gen.split('|')[i].split(" ")
        while "" in operation_true:
            operation_true.remove("")
        while "" in operation_gen:
            operation_gen.remove("")
        if operation_true != operation_gen:
            # check operator
            operator_true = operation_true[1]
            operator_gen = operation_gen[1]
            if operator_gen != operator_true:
                hint += "The operator in the position " + str(i*7+1) + " is incorrect. "
            # check number
            num0_true = operation_true[3][:-1]
            num1_true = operation_true[4]
            num0_gen = operation_gen[3][:-1]
            num1_gen = operation_gen[4]
            if operator_true in ["add", "multiply"]:
                # verify swap number for swapable operation
                if (num0_gen != num1_true) | (num0_gen != num1_true):
                    if num0_true != num0_gen:
                        hint += "The number in the position " + str(i*7+3) + " is incorrect. "
                    if num1_true != num1_gen:
                        hint += "The number in the position " + str(i*7+4) + " is incorrect. "
            else:
                if num0_true != num0_gen:
                    hint += "The number in the position " + str(i*7+3) + " is incorrect. "
                if num1_true != num1_gen:
                    hint += "The number in the position " + str(i*7+4) + " is incorrect. "
    if hint == "":
        hint = "No"
    return hint


if __name__ == '__main__':
    data = DataService(file=r"static/data/train.csv")
    linear_equation_gen = "#0: multiply ( number2, number1 ) | #1: divide ( number2, #0 ) | #1: divide ( 2, number2 )"
    linear_equation_true = "#0: add ( number0, number1 ) | #1: add ( #0, number2 )"
    print(oracle_hint(linear_equation_gen, linear_equation_true))
