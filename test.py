from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
print(tokenizer("This is a test."))
