from transformers import T5Tokenizer, T5ForConditionalGeneration


class ModelService():
    """_summary_
    """
    def __init__(self, model_dir):
        self.tokenizer = T5Tokenizer.from_pretrained('t5-large')
        self.model = T5ForConditionalGeneration.from_pretrained(model_dir)
        self.output = []

    def forward_model(self, problem):
        input_ids = self.tokenizer(problem, return_tensors="pt").input_ids
        output = self.model.generate(input_ids, max_length=50)
        output = self.tokenizer.decode(output[0], skip_special_tokens=True)
        self.output.append([problem, output])
        return output
