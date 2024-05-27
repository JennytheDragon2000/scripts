import openai
import json
import time
from datetime import datetime, timedelta

# Initialize your OpenAI API key
openai.api_key = "your-api-key-here"

# Initialize knowledge tracking and review schedule
knowledge = {"known": [], "seen": [], "unseen": []}

review_schedule = {}

# Sample questions to start with
initial_questions = [
    {
        "question": "What is Azure Data Factory primarily used for?",
        "options": [
            "Data storage",
            "Data integration",
            "Machine learning",
            "Web hosting",
        ],
        "answer": "Data integration",
        "explanation": "Azure Data Factory is a cloud-based data integration service that allows you to create data-driven workflows for orchestrating and automating data movement and data transformation.",
    }
]


# Function to call GPT-4 for generating questions and explanations
def generate_question(topic):
    prompt = f"Generate a multiple-choice question about {topic} with four options. Provide the correct answer and a brief explanation."
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=150
    )
    result = response.choices[0].text.strip()
    question, options, answer, explanation = parse_gpt_response(result)
    return {
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
    }


# Function to parse GPT-4 response (assuming a specific format)
def parse_gpt_response(response):
    lines = response.split("\n")
    question = lines[0].strip()
    options = [line.split(". ")[1].strip() for line in lines[1:5]]
    answer = lines[5].split(": ")[1].strip()
    explanation = lines[6].split(": ")[1].strip()
    return question, options, answer, explanation


# Function to ask a question and get user input
def ask_question(question):
    print(question["question"])
    for idx, option in enumerate(question["options"], 1):
        print(f"{idx}. {option}")
    return question["answer"]


# Function to check the answer
def check_answer(question, user_answer):
    correct = question["options"][user_answer - 1] == question["answer"]
    return correct


# Function to provide an explanation
def provide_explanation(question):
    print(f"Explanation: {question['explanation']}")


# Function to update knowledge tracking and review schedule
def update_knowledge(question, correct):
    topic = question["question"]
    if correct:
        knowledge["known"].append(topic)
        if topic in knowledge["seen"]:
            knowledge["seen"].remove(topic)
        next_review = datetime.now() + timedelta(
            days=2
        )  # Increase interval for correct answers
    else:
        if topic not in knowledge["seen"]:
            knowledge["seen"].append(topic)
        if topic not in knowledge["unseen"]:
            knowledge["unseen"].append(topic)
        next_review = datetime.now() + timedelta(
            hours=1
        )  # Decrease interval for incorrect answers

    review_schedule[topic] = next_review


# Function to get questions due for review
def get_due_questions():
    current_time = datetime.now()
    due_questions = [
        q
        for q in initial_questions
        if review_schedule.get(q["question"], datetime.min) <= current_time
    ]
    return due_questions


# Main function to run the quiz
def main():
    questions = initial_questions

    while True:
        due_questions = get_due_questions()
        if not due_questions:
            print("No questions due for review. Please check back later.")
            break

        for question in due_questions:
            answer = ask_question(question)
            user_answer = int(input("Your answer: "))
            correct = check_answer(question, user_answer)
            provide_explanation(question)
            update_knowledge(question, correct)
            if not correct:
                additional_topic = question["options"][user_answer - 1]
                new_question = generate_question(additional_topic)
                questions.append(new_question)
        if input("Do you want to continue? (yes/no): ").lower() != "yes":
            break


if __name__ == "__main__":
    main()
