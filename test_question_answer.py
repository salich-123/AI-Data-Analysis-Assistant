from utils.data_loader import load_csv
from utils.data_cleaner import clean_data
from agents.question_answer_agent import answer_question

df = load_csv("data/students_dirty.csv")

cleaned_df = clean_data(df)

question = input("\nAsk a question: ")

answer = answer_question(cleaned_df, question)

print("\nAssistant:", answer)