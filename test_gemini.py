
from agents.gemini_agent import ask_gemini

question = "Explain data analysis in simple English."

answer = ask_gemini(question)

print("\nGemini Assistant:")
print(answer)
