import warnings
warnings.filterwarnings('ignore')
from transformers import AutoTokenizer




sentence = "Hello World"
print("--------------------Token ID ----------------------------")
tokenizer=AutoTokenizer.from_pretrained("bert-base-cased")
token_ids = tokenizer(sentence).input_ids
print(token_ids)
print("----------------Token ID to Text-------------------------")
token_to_text = tokenizer.convert_ids_to_tokens(token_ids)
print(token_to_text)

text = tokenizer.decode(token_ids)
print(text)



