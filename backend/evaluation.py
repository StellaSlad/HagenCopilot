from pydantic import BaseModel
import json
import os
from chat import get_llm, invoke
from embeddings import embeddings

from ragas import RunConfig, evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall, context_entity_recall, answer_similarity, answer_correctness

from datasets import Dataset

import nest_asyncio
nest_asyncio.apply()


def clean_text(text: str) -> str:
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


class QAPair(BaseModel):
    question: str
    answer: str


version = "3"
files = ["einfach.json", "unbekannt.json", "schwierig.json"]
models = ["llama3:latest", "mixtral:latest",
          "llama3:70b", "mistral:latest", "gemma:latest"]
path = "backend/evaluation"

for model in models:

    for file in files:

        # load pre-defined qa pairs
        with open(f"{path}/{file}", encoding="utf-8") as json_file:
            qa_pairs_data: list[dict] = json.load(json_file)
            qa_pairs = [QAPair(question=clean_text(pair.get("question")),
                               answer=clean_text(pair.get("answer")))
                        for pair in qa_pairs_data]

        results = []
        contexts = []
        for qa in qa_pairs:
            result = invoke(qa.question, model=model)
            results.append(clean_text(result['answer']))

            sources: list[dict] = result["context"]
            contents = []
            for i in range(len(sources)):
                contents.append(clean_text(sources[i].get("page_content")))

            contexts.append(contents)

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
                         metrics=[answer_relevancy,
                                  faithfulness,  # this metric is not working
                                  context_recall,  # this metric is not working
                                  context_precision,
                                  answer_correctness])

        score_df = score.to_pandas()
        score_df.to_csv(f"{path}/Evaluation_{file}_{model}_v{version}.csv",
                        encoding="utf-8", index=False)
        print(f"Model: {model}, File: {file}")
        print(score_df[['answer_relevancy',
                        'faithfulness',
                        'context_recall',
                        'context_precision',
                        'answer_correctness']].mean(axis=0))
