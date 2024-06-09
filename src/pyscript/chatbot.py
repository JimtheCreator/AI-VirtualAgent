import gradio as gr
import pandas as pd
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import re
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the CSV file
product_path = os.path.join(script_dir, 'products.csv')
api_path = os.path.join(script_dir, 'api-key')
knowledge_base = os.path.join(script_dir, 'knowledgebase.txt')
rules_path = os.path.join(script_dir, 'rules.txt')

# # Load the csv file
df = pd.read_csv(product_path)

client = OpenAI(api_key=open(api_path).read())
chatHistory = []
# Function to load FixMyCrack information from a text file
def loadInfo(file_path):
    with open(file_path, 'r') as file:
        fixmycrack_info = file.read()
    return fixmycrack_info

def rule(file_path):
    with open(file_path, 'r') as file:
        fixmycrack_info = file.read()
    return fixmycrack_info

def send_email(subject, message, sender_email, receiver_email):
    password = #Your password comes here
     
    # Create a MIMEText object
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    # Send email using SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(receiver_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


def CustomChatGPT(You):
    knowledge = loadInfo(knowledge_base)
    rules = rule(rules_path)
    # Add user message to chat history
    chatHistory.append({"role": "user", "content": You})
    
    # Check if any product name from the DataFrame is in the user's query
    if any(product_name in You for product_name in df['PRODUCT']):
        assistant_prompt = f"Am here to assist you, {df}"
    else:
        assistant_prompt = f"How may I help you, {df}"
    
    messages=[
            {"role": "system", "content": f"{knowledge} and {df} and {rules}"},
            {"role": "user", "content": You},
            {"role": "assistant", "content": assistant_prompt}
        ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    chatgpt_reply = response.choices[0].message.content
    
    # Append the actual assistant's response to the conversation history
    chatHistory.append({"role": "assistant", "content": chatgpt_reply})
    
    if 'live agent' in You:
        staticRespond(You)
    
    return chatgpt_reply


def staticRespond(You):
    # Add assistant prompt to chat history
    chatHistory.append({"role": "user", "content": You})
    
    # Default assistant prompt
    assistant_prompt = "Did not quite get that? Kindly repeat"
    
    # Add assistant prompt to chat history
    chatHistory.append({"role": "assistant", "content": assistant_prompt})
        
    if 'live agent' in You:
         # Add assistant prompt to chat history
        chatHistory.append({"role": "user", "content": You})
        
        assistant_prompt = "Kindly assist us with your email address so that we can proceed."
        # Add assistant prompt to chat history
        chatHistory.append({"role": "assistant", "content": assistant_prompt})
        
        if '@' in You:
             # Add assistant prompt to chat history
            chatHistory.append({"role": "user", "content": You})
            # Regular expression pattern to match email addresses
            pattern = r'[\w\.-]+@[\w\.-]+'
            # Use findall to search for email addresses in the text
            receiver_emails = re.findall(pattern, You)
            # Add assistant prompt to chat history
            assistant_prompt = "A live agent should get back to you in a few minutes. Feel free to exit the chat."
            
            chatHistory.append({"role": "assistant", "content": assistant_prompt})
            # Create the email message from chat history
            emailMessage = "\n".join([f"{message['role'].capitalize()}: {message['content']}" for message in chatHistory])
            
            send_email("User Requested Live Agent", f"Client id: {receiver_emails}\n\n [bold]Your past conversation with our Virtual Agent[/bold]: \n\n{emailMessage}", 'jimmywire@skiff.com', 'mappedvision@gmail.com')
        
    return assistant_prompt  # Return the assistant prompt



def checkForState():
    for message in chatHistory:
        if 'live agent' in message['content']:
            return True
    return False

def chat_response(You):
    if checkForState():
        return staticRespond(You)
    else:
        return CustomChatGPT(You)

# demo = gr.Interface(fn=chat_response, inputs="text", outputs="text", title="FixMyCrack Assistant")
# demo.launch()
