from haystack.components.evaluators.document_mrr import DocumentMRREvaluator
from haystack.components.evaluators.faithfulness import FaithfulnessEvaluator
from haystack.components.evaluators.sas_evaluator import SASEvaluator
from haystack.evaluation.eval_run_result import EvaluationRunResult
from haystack import Pipeline
from haystack.evaluation.eval_run_result import EvaluationRunResult
from sklearn.metrics import PredictionErrorDisplay
import os
import pandas as pd


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # Change the current working directory to the script's directory
    os.chdir(script_dir)

# Functions
def extract_questions_answers(file_path):
    questions = []
    answers = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespace characters from the line
            line = line.strip()
            # Split the line by the tab character
            parts = line.split('\t')
            
            if len(parts) == 2:
                question, answer = parts
                questions.append(question)
                answers.append(answer)
            else:
                print(f"Line '{line}' is not in the expected format and was skipped.")
    
    return questions, answers

eval_pipeline = Pipeline()
# eval_pipeline.add_component("doc_mrr_evaluator", DocumentMRREvaluator())
# eval_pipeline.add_component("faithfulness", FaithfulnessEvaluator())
eval_pipeline.add_component("sas_evaluator", SASEvaluator(model="sentence-transformers/all-MiniLM-L6-v2"))

file_path = 'ja_nein2.txt'
questions, answers = extract_questions_answers(file_path)
predicted_answers = answers

results = eval_pipeline.run({
    "sas_evaluator": {"predicted_answers": predicted_answers, "ground_truth_answers": answers}
})

inputs= {
        "question": questions,
        #"contexts": list([d.content] for d in ground_truth_docs),
        "answer": answers,
        "predicted_answer": predicted_answers,
        }

evaluation_result = EvaluationRunResult(run_name="HagenCopilot", inputs=inputs, results=results)
evaluation_result.score_report()

results_df = evaluation_result.to_pandas()

top_3 = results_df.nlargest(3, 'sas_evaluator')
bottom_3 = results_df.nsmallest(3, 'sas_evaluator')
pd.concat([top_3, bottom_3])
results_df.to_csv('results_'+ file_path)
