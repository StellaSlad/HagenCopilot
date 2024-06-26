from langchain_core.prompts import PromptTemplate


prompt_template = """
Beantworte die Fragen des Benutzers in der deutschen Sprache. Nutze nur die Informationen, die im Kontext gegeben sind.
Wenn der Kontext keine relevanten Informationen für die Frage enthält, entschuldige dich und sage, dass du keine Antwort hast.

Kontext: 
{context}

Frage: 
{input}

Hilfreiche Antwort:
"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "input"]
)
