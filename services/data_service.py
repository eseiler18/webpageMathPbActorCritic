import pandas as pd


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
        # upper first letter
        clean_body = self.body.values
        clean_question = self.question.values
        # change number# to the value
        numbers = [i.split(" ") for i in self.numbers]
        for i in range(len(self.numbers)):
            clean_body[i] = clean_body[i].capitalize()
            if not isinstance(clean_question[i], str):
                clean_question[i] = ""
            clean_question[i] = clean_question[i].capitalize()
            for j, number in enumerate(numbers[i]):
                clean_body[i] = clean_body[i].replace("number" + str(j), number)
                clean_question[i] = clean_question[i].replace("number" + str(j), number)
        self.math_pb = clean_body + clean_question

    def create_label(self):
        file_name = self.file.split("/")[-1]
        self.data["label"] = self.data.index.astype('str') + ";" + file_name
        self.label = self.data["label"].values

    def get_item(self, index):
        return self.data.iloc[index].to_dict()


if __name__ == '__main__':
    DataService(file=r"static/data/dev.csv")
