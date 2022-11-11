from transformers import T5Tokenizer, T5ForConditionalGeneration


tokenizer = T5Tokenizer.from_pretrained('t5-large')
input_ids = tokenizer("julia played tag with number0 kids on monday and number1 kids on tuesday . she played cards wtih number2 kids on wednesday. how many kids did she play with altogether ?", return_tensors="pt").input_ids
print(input_ids)

model = T5ForConditionalGeneration.from_pretrained(r"static/model/output_reasoning_iteration")

outputs = model.generate(input_ids, max_length=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))