
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


def get_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key not found.")

    return genai.Client(api_key=api_key)


def ask_gemini(question, dataset_context=None):

    try:
        client = get_gemini_client()

        prompt = f"""
You are an intelligent AI assistant.

Answer the user's question in clear, simple English.

If the question is general:
Answer using your general knowledge.

If dataset information is provided:
Use only that information.
Never invent dataset values or calculations.

Explain answers in a beginner-friendly way.

DATASET INFORMATION:
{dataset_context if dataset_context else "No dataset provided."}

USER QUESTION:
{question}
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text or "No answer generated."

    except Exception as e:
        return f"Gemini API error: {e}"



def create_analysis_plan(question, columns, data_types, sample_data):

    try:
        client = get_gemini_client()

        prompt = f"""
You are an intelligent data analysis planner.

Understand the user's question and create the correct JSON plan.

Available columns: {columns}
Data types: {data_types}
Sample records: {sample_data}

User question: {question}

RULES:

1. Use only actual dataset column names.
2. If the question asks average, use mean.
3. If it asks highest/lowest average by a category,
   use groupby with the category as group_by.
4. For highest/lowest group results:
   set sort to desc/asc respectively.
5. For general knowledge questions, return:
   {{"type": "general"}}

For dataset questions, return:
{{
  "type": "dataset",
  "operation": "aggregate",
  "column": "Salary",
  "statistic": "mean",
  "group_by": null,
  "filters": [],
  "limit": 5,
  "sort": "desc"
}}

For department-wise average salary:
{{
  "type": "dataset",
  "operation": "groupby",
  "column": "Salary",
  "statistic": "mean",
  "group_by": "Department",
  "filters": [],
  "limit": 5,
  "sort": "desc"
}}

Allowed operations:
aggregate, filter, groupby, sort, describe,
count_rows, count_columns, missing, duplicates,
unique, correlation.

Allowed statistics:
mean, sum, max, min, median, count, std, var.

For filters:
{{"column": "Age", "operator": ">", "value": 22}}

If unclear, return:
{{"type": "unsupported"}}

Return ONLY valid JSON.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except Exception as e:
        return {
            "type": "error",
            "message": str(e)
        }
