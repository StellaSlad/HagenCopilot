"""
evaluation.py

This module evaluates the performance of various language models on predefined question-answer pairs.
It loads QA pairs from JSON files, invokes the models to get answers, and evaluates the results using specified metrics.
"""

from pydantic import BaseModel
import json
from chat import get_llm, invoke
from embeddings import embeddings

from ragas import RunConfig, evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall, context_entity_recall, answer_similarity, answer_correctness

from datasets import Dataset

import nest_asyncio
nest_asyncio.apply()


class QAPair(BaseModel):
    """
    A class used to represent a Question-Answer pair.

    Attributes:
    ----------
    question : str
        The question part of the QAPair.
    answer : str
        The answer part of the QAPair.
    """
    question: str
    answer: str


def clean_text(text: str) -> str:
    """
    Clean the input text by replacing specific characters with their ASCII equivalents.

    This function replaces German umlauts (ä, ü, ö) and their uppercase versions (Ä, Ü, Ö)
    with their ASCII equivalents (ae, ue, oe, Ae, Ue, Oe). It also replaces newline characters
    with spaces.

    Parameters:
    text (str): The input text to be cleaned.

    Returns:
    str: The cleaned text with specified replacements applied.
    """
    # Extend replacements to include ä, ü, and ö
    replacements = {
        'ä': 'ae',
        'ü': 'ue',
        'ö': 'oe',
        # Add the uppercase versions if needed
        'Ä': 'Ae',
        'Ü': 'Ue',
        'Ö': 'Oe',
    }

    # Iterate over the replacements and apply them
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)

    text = text.replace('\n', ' ')
    return text


files = ["einfach.json", "unbekannt.json", "schwierig.json", "modulhb.json"]
models = ["llama3:latest", "mixtral:latest",
          "llama3:70b", "mistral:latest", "gemma:latest"]
PATH = "backend/evaluation"
VERSION = "5"

for model in models:
    for file in files:
        # Load pre-defined QA pairs from JSON file
        with open(f"{PATH}/{file}", encoding="utf-8") as json_file:
            qa_pairs_data: list[dict] = json.load(json_file)
            qa_pairs = [QAPair(question=clean_text(pair.get("question")),
                               answer=clean_text(pair.get("answer")))
                        for pair in qa_pairs_data]

        results = []
        contexts = []
        for qa in qa_pairs:
            # Invoke the model to get the answer
            result = invoke(qa.question, model=model)
            results.append(clean_text(result['answer']))

            # Extract and clean the context from the result
            sources: list[dict] = result["context"]
            contents = []
            for i in range(len(sources)):
                contents.append(clean_text(sources[i].get("page_content")))

            contexts.append(contents)

        # Prepare the dataset for evaluation
        d = {
            "question": [qa.question for qa in qa_pairs],
            "answer": results,
            "contexts": contexts,
            "ground_truth": [qa.answer for qa in qa_pairs],
        }

        dataset = Dataset.from_dict(d)
        score = evaluate(dataset,
                         llm=get_llm(model=model),
                         embeddings=embeddings,
                         is_async=False,
                         raise_exceptions=False,
                         run_config=RunConfig(timeout=60*2,
                                              max_retries=10*2,
                                              max_wait=60*2,
                                              max_workers=1,
                                              thread_timeout=80.0*2),
                         metrics=[
                             # answer_relevancy,
                             # faithfulness,
                             # context_recall,
                             # context_precision,
                             answer_correctness])

        # Save the evaluation results to a CSV file
        score_df = score.to_pandas()
        score_df.to_csv(f"{PATH}/Evaluation_{file}_{model.replace(':', '_')}_v{VERSION}.csv",
                        encoding="utf-8", index=False)
        print(f"Model: {model}, File: {file}")
        print(score_df[[
            # 'answer_relevancy',
            # 'faithfulness',
            # 'context_recall',
            # 'context_precision',
            'answer_correctness']].mean(axis=0))
