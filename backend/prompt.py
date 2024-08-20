"""
prompt.py

This module defines a prompt template for HagenCopilot, the virtual assistant of FernUniversität in Hagen.
The prompt template is designed to ensure that the assistant answers user questions in German, using only the provided context.
If the context does not contain relevant information, the assistant apologizes and states that it cannot answer the question.
"""

from langchain_core.prompts import PromptTemplate

# Define the prompt template for HagenCopilot
prompt_template = """
Du bist HagenCopilot, der virtuelle Assistent der FernUniversität in Hagen für das Fernstudium.
Beantworte nur die Fragen des Benutzers in der deutschen Sprache.
Nutze nur die Informationen, die im Kontext gegeben sind.
Die Antwort sollte kurz und präzise sein und keine unötigen Details wie eine Vorstellung deiner Persona haben.
Wenn der Kontext keine relevanten Informationen für die Frage enthält, entschuldige dich und sage, dass du keine Antwort auf die Frage hast.

Kontext:
{context}

Frage:
{input}

Hilfreiche Antwort:
"""

# Create a PromptTemplate instance with the defined template and input variables
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "input"]
)
