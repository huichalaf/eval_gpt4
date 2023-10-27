import openai
import os, sys
import json
import random
import tiktoken
from functions import call_gpt_4_eval, call_model
from time import time
import dotenv
dotenv.load_dotenv()

start = time()
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

file_questions = sys.argv[1]

openai.api_key = os.getenv("OPENAI_API_KEY")

goal = "give a correct and helpfull answer to a student about the question or math problem"
#this is a gpt-4 evaluator
system_message_gpt4 = f"""You're an llm evaluator, your task is to evaluate in grades from 0 to 100, the score of a response to a question having in mind that the ultimate goal is to {goal}, the format of input will be:
answer:
###
response:
###
and you should give as output, the score"""
system_message_chats = "You are a seasoned mathematics teacher named Richard. Your role is to solve and provide step-by-step explanations for the user's questions. The user might offer additional context to assist you; it's your task to discern its relevance and utility."

questions = []
with open(file_questions) as f:
    texto = f.readlines()
    for line in texto:
        questions.append(line)

print(len(questions))
#las revolvemos
random.shuffle(questions)

model_judge = "gpt-4"
model_base = "gpt-3.5-turbo"
model_tested = "ft:gpt-3.5-turbo-0613:aidtogrow::8EPRXQk8"

base_responses = []
test_responses = []

total_tokens_base = 0
total_tokens_test = 0
total_tokens_base_send = 0
total_tokens_test_send = 0
scores_base = []
scores_test = []
base_avg = 0
test_avg = 0
tokens_system = num_tokens_from_string(system_message_chats, "cl100k_base")

for question in questions:
    #primero preguntamos a gpt-3.5-turbo
    index = questions.index(question)
    print(round(index/len(questions)*100),"%")
    question = question.replace("\n", "")
    tokens_question = num_tokens_from_string(question, "cl100k_base")
    total_tokens_base_send += tokens_question
    total_tokens_test_send += tokens_question
    total_tokens_base_send += tokens_system
    total_tokens_test_send += tokens_system
    response = ''
    score = 0
    try:
        response = call_model(model_base, system_message_chats, question)
        score = call_gpt_4_eval(question, response)
    except:
        continue
    scores_base.append(float(score))
    base_responses.append(response)
    total_tokens_base += num_tokens_from_string(response, "cl100k_base")
    try:
        response = call_model(model_tested, system_message_chats, question)
        score = call_gpt_4_eval(question, response)
    except:
        scores_base.pop()
        base_responses.pop()
        total_tokens_base -= num_tokens_from_string(response, "cl100k_base")
        continue
    scores_test.append(float(score))
    test_responses.append(response)
    total_tokens_test += num_tokens_from_string(response, "cl100k_base")
    if index == 100:
        break


print("tokens base completion: ",total_tokens_base)
print("tokens tested completion: ",total_tokens_test)
print("tokens base send: ",total_tokens_base_send)
print("tokens tested send: ",total_tokens_test_send)
print("scores base: ", scores_base)
print("scores test: ", scores_test)
print("avg base: ", sum(scores_base)/len(scores_base))
print("avg test: ", sum(scores_test)/len(scores_test))
#escribimos todos los datos del test en un dataframe
import pandas as pd
df = pd.DataFrame()
df['question'] = questions
df['base_responses'] = base_responses
df['test_responses'] = test_responses
df['scores_base'] = scores_base
df['scores_test'] = scores_test
df.to_csv("eval_results.csv")

#escribimos las respuestas en un archivo
with open(f'base_responses.txt', 'w') as f:
    for response in base_responses:
        f.write(response)
        f.write('\n')

with open(f'test_responses.txt', 'w') as f:
    for response in test_responses:
        f.write(response)
        f.write('\n')
print("total time: ", time()-start)