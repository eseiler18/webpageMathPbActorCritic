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

    def create_math_pb(self):
        clean_body = self.body.values
        clean_question = self.question.values
        # change number# to the value
        numbers = [i.split(" ") for i in self.numbers]
        for i in range(len(self.numbers)):
            clean_body[i] = clean_body[i].capitalize()
            if not isinstance(clean_question[i], str):
                clean_question[i] = ""
            clean_question[i] = clean_question[i].capitalize()
            # for j, number in enumerate(numbers[i]):
            #     clean_body[i] = clean_body[i].replace("number" + str(j), number)
            #     clean_question[i] = clean_question[i].replace("number" + str(j), number)
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


if __name__ == '__main__':
    DataService(file=r"static/data/dev.csv")
