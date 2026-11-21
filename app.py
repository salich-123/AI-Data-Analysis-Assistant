
from utils.data_loader import load_csv
from utils.data_inspector import inspect_data
from utils.data_cleaner import clean_data
from agents.question_answer_agent import answer_question
from agents.data_analyst import analyze_data
from agents.visualizer import create_visualizations
from agents.report_generator import generate_report


print("\n===== AI DATA ANALYSIS ASSISTANT =====")

df = load_csv("data/students_dirty.csv")

if df is not None:
    inspect_data(df)

    cleaned_df = clean_data(df)

    analyze_data(cleaned_df)

    create_visualizations(cleaned_df)

    generate_report(cleaned_df)

print("\n===== PROJECT COMPLETED =====")
