import gradio as gr
import pandas as pd
from openai import OpenAI
import json
# Using a simplified tokenization approximation: splitting by whitespace and punctuation
import re

# Load the csv file
# df = pd.read_csv('products.csv')

# api_key = "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"

# client = OpenAI(api_key=api_key)

# messages = [{"role": "assistant", "content": f"You are the FixMyCrack Assistant. Your answer should be based on the {df}."}]

# def CustomChatGPT(You):
#     messages.append({"role": "user", "content": You})
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )
    
#     chatgpt_reply = response.choices[0].message.content

#     # Check if the reply contains any product or service from the csv file
#     for index, row in df.iterrows():
#         if row['PRODUCT'].lower() in chatgpt_reply or row['SERVICE'].lower() in chatgpt_reply:
#             # If it does, append the corresponding quote to the reply
#             chatgpt_reply += '\n' + row['QUOTES']

#     messages.append({"role": "assistant", "content": chatgpt_reply})
#     return chatgpt_reply


# demo = gr.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="FixMyCrack Assistant")

# demo.launch(share=True)

theBrainBase = pd.read_csv('products.csv')

roleOfModel = "You are the FixMyCrack Assistant. You answer queries on the following: product repair, refurbished tech, quotes and how long it takes to fix certain products."
allConversation = []


for idx, row in theBrainBase.iterrows():
    # Your code here
    content = f"We have a {row['SERVICE TYPE']} for {row['PRODUCT']} which may cost {row['QUOTES']}. This may take you {row['DURATION']}"
    allConversation.append({
        "messages": [
            {"role": "system", "content": roleOfModel},
            {"role": "user", "content": "What is the price of..."},
            {"role": "assistant", "content": content}
        ]
    })
    
   
with open('trainhub.jsonl', 'w') as file:
    for conversation in allConversation:
        json.dump(conversation, file)
        file.write('\n')
        
# Read the CSV file content
with open('products.csv', "r") as file:
    csv_content = file.read()

# Tokenize the content: using a simplified tokenization approximation
tokens = re.findall(r'\w+|\£\d+\.\d+|\d+\.\d+hours|\d+hours|\d+,\d+', csv_content)

# Count the number of tokens
num_tokens = len(tokens)

print(num_tokens)

client = OpenAI(api_key=open('api-key').read())

with open('trainhub.jsonl', 'rb') as file:
    response = client.files.create(file=file, purpose='fine-tune')
    
response = client.fine_tuning.jobs.create(
    training_file=open('file-id').read(),
    model='gpt-3.5-turbo'
)

print(client.fine_tuning.jobs.list(limit=1))