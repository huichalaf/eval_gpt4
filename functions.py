import openai
import os
import math

openai.api_key = os.getenv("OPENAI_API_KEY")

def calculate_size_sample(confidence_level, z_value, margin_of_error, population_size, estimated_proportion):
    # confidence_level = 0.95  # 90% confidence level
    # z_value = 1.645  # Z-value for a 90% confidence level
    # margin_of_error = 0.1  # 10% margin of error
    # population_size = 3000  # Total number of students
    # estimated_proportion = 0.5  # Maximizes the sample size

    # Calculate sample size for infinite population
    sample_size_infinite = math.ceil((z_value ** 2) * estimated_proportion * (1 - estimated_proportion) / (margin_of_error ** 2))

    # Adjust for finite population
    sample_size_finite = math.ceil(sample_size_infinite / (1 + ((sample_size_infinite - 1) / population_size)))
    return sample_size_infinite, sample_size_finite

def call_gpt_4_eval(goal, model_judge, question, response):
    system_message_gpt4 = f"""You're an llm evaluator, your task is to evaluate in grades from 0 to 100, be strict and rigurous with the grades, the score of a response to a question having in mind that the ultimate goal is to {goal}, the format of input will be:
        answer:
        ###
        response:
        ###
        and you should give as output, the score and only the score, only the number"""
    message = f"""
    answer:
    ###
    {question}
    response:
    ###
    {response}
    """
    response = openai.ChatCompletion.create(
        model=model_judge,
        messages=[
            {"role": "system", "content": system_message_gpt4},
            {"role": "user", "content": message},
        ],
        temperature=0,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']["content"]

def call_gpt_4_judge(goal, model_judge, question, response1, response2):
    system_message_gpt4 = """You're an llm evaluator, your task is to evaluate in grades from 0 to 100, be strict and rigurous with the grades, the score of a response to a question having in mind that the ultimate goal is to give helpfull and correct response to the user about math subjects and problems, the format of input will be:
    question:
    ###
    answer 1:
    ###
    answer 2:
    ###
    and you should give as output, the number of the better response (1 or 2) remember, only 1 or 2 as output, ONLY RESPONSE WITH THE BETTER OPTION. IMPORTANT JUST THE NUMBER 1 or 2"""
    message = f"""
    question:
    ###
    {question}
    answer 1:
    ###
    {response1}
    answer 2:
    ###
    {response2}
    """
    response = openai.ChatCompletion.create(
        model=model_judge,
        messages=[
            {"role": "system", "content": system_message_gpt4},
            {"role": "user", "content": message},
        ],
        temperature=0,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']["content"]

def call_model(model, system_message, question):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question},
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    response = response['choices'][0]["message"]["content"]
    return response