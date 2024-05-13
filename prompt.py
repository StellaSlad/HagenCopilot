from langchain_core.prompts import PromptTemplate

template = """Verwenden die folgenden Kontextinformationen, um die Frage am Ende zu beantworten. Wenn du die Antwort nicht kennst, sag einfach, dass du es nicht weisst. versuche nicht eine Antwort zu erfinden. antworte auf deutsch. gibt die quelle in der antwort mit an.

Kontext:
{context}
Frage: {input}
Hilfreiche Antwort:
"""

QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "input"], template=template)
