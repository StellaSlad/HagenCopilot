from langchain_core.prompts import PromptTemplate


prompt_template = """
Beantworten Sie die Fragen des Benutzers auf der Grundlage des unten stehenden Kontexts in der deutschen Sprache. 
Wenn der Kontext keine relevanten Informationen für die Frage enthält, denken Sie sich nichts aus und sagen Sie einfach „Ich weiß es nicht“:

Kontext: 
{context}

Frage: 
{input}

Hilfreiche Antwort:
"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "input"]
)
