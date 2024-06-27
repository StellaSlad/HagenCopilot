from pydantic import BaseModel
import os
import json
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.pdf import PyPDFLoader

from chat import llm, invoke
from embeddings import embeddings

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall, context_entity_recall, answer_similarity, answer_correctness

from datasets import Dataset

import nest_asyncio
nest_asyncio.apply()


class QAPair(BaseModel):
    question: str
    answer: str


# load pre-defined qa pairs
with open("backend/qa_pairs.json") as json_file:
    qa_pairs_data = json.load(json_file)
    qa_pairs = [QAPair(**pair) for pair in qa_pairs_data]

results = []
contexts = []
for qa in qa_pairs:
    result = invoke(qa.question)
    results.append(result['answer'])

    sources = result["context"]
    contents = []
    for i in range(len(sources)):
        contents.append(sources[i].get("page_content"))

    contexts.append(contents)

d = {
    "question": [qa.question for qa in qa_pairs],
    "answer": results,
    "contexts": contexts,
    "ground_truth": [qa.answer for qa in qa_pairs],
}

dataset = Dataset.from_dict(d)
score = evaluate(dataset,
                 llm=llm,
                 embeddings=embeddings,
                 is_async=False,
                 metrics=[answer_relevancy,
                          # faithfulness, # this metric is not working
                          # context_recall, # this metric is not working
                          # context_precision,
                          answer_correctness])

score_df = score.to_pandas()
score_df.to_csv("EvaluationScores.csv", encoding="utf-8", index=False)

print(score_df[['answer_relevancy',
                # 'faithfulness',
               # 'context_recall',
                # 'context_precision',
                'answer_correctness']].mean(axis=0))
