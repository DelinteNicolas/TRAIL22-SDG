from typing import Tuple
import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer, AutoTokenizer, PreTrainedTokenizer
from datasets import load_metric

from .utils.dataset import load_sdg_dataset


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    metric = load_metric("accuracy")
    return metric.compute(predictions=predictions, references=labels)

def fine_tune_bert(save_location: str, n_epochs=3) -> Tuple[torch.nn.Module, PreTrainedTokenizer]:
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    dataset = load_sdg_dataset(tokenizer)
    id2label = {
        0: "Easter egg",
        1: "SDG1: No Poverty",
        2: "SDG2: Zero Hunger",
        3: "SDG3: Good Health and Well-being",
        4: "SDG4: Quality Education",
        5: "SDG5: Gender Equality",
        6: "SDG6: Clean Water and Sanitation",
        7: "SDG7: Affordable and Clean Energy",
        8: "SDG8: Decent Work and Economic Growth",
        9: "SDG9: Industry, Innovation and Infrastructure",
        10: "SDG10: Reduced Inequality",
        11: "SDG11: Sustainable Cities and Communities",
        12: "SDG12: Responsible Consumption and Production",
        13: "SDG13: Climate Action",
        14: "SDG14: Life Below Water",
        15: "SDG15: Life on Land",
        16: "SDG16: Peace and Justice Strong Institutions",
        17: "SDG17: Partnerships to achieve the Goal"
    }
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=len(id2label), id2label=id2label)
    training_args = TrainingArguments(
        output_dir="test_trainer", 
        evaluation_strategy="epoch",
        num_train_epochs=n_epochs
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        compute_metrics=compute_metrics
    )

    trainer.train()
    model.save_pretrained(save_location)
    return model, tokenizer
