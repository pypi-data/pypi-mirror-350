import numpy as np

from transformers import BertTokenizer, BertModel

from patronus import StructuredEvaluator, EvaluationResult
from patronus.experiments import run_experiment


class BERTScore(StructuredEvaluator):
    def __init__(self, pass_threshold: float):
        self.pass_threshold = pass_threshold
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")

    def evaluate(
        self, *, task_output: str, gold_answer: str, **kwargs
    ) -> EvaluationResult:
        output_toks = self.tokenizer(
            task_output, return_tensors="pt", padding=True, truncation=True
        )
        gold_answer_toks = self.tokenizer(
            gold_answer, return_tensors="pt", padding=True, truncation=True
        )

        output_embeds = (
            self.model(**output_toks).last_hidden_state.mean(dim=1).detach().numpy()
        )
        gold_answer_embeds = (
            self.model(**gold_answer_toks)
            .last_hidden_state.mean(dim=1)
            .detach()
            .numpy()
        )

        score = np.dot(output_embeds, gold_answer_embeds.T) / (
            np.linalg.norm(output_embeds) * np.linalg.norm(gold_answer_embeds)
        )

        return EvaluationResult(
            score=score,
            pass_=score >= self.pass_threshold,
            tags={"pass_threshold": str(self.pass_threshold)},
        )


experiment = run_experiment(
    dataset=[
        {
            "task_output": "Translate 'Goodbye' to Spanish.",
            "gold_answer": "Adiós",
        }
    ],
    evaluators=[BERTScore(pass_threshold=0.8)],
)
