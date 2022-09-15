from typing import Tuple
import torch
import os
import numpy as np
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer, AutoTokenizer, PreTrainedTokenizer
from datasets import load_metric, DatasetDict

from .utils.dataset import load_sdg_dataset


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    metric = load_metric("accuracy")
    return metric.compute(predictions=predictions, references=labels)


def to_binary(dataset: DatasetDict, label_to_extract: int) -> DatasetDict:
    def map_function(line):
        label = line["label"]
        if label == label_to_extract:
            label = 1
        else:
            label = 0
        line["label"] = label
        return line

    return {
        "train": dataset["train"].map(map_function),
        "test": dataset["test"].map(map_function)
    } 


def train_17_classifiers(save_directory: str, n_epochs: int):
    base_model = "bert-base-cased"
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    
    os.makedirs(save_directory, exist_ok=True)
    labels = [
        "SDG1: No Poverty", 
        "SDG2: Zero Hunger", 
        "SDG3: Good Health and Well-being", 
        "SDG4: Quality Education", 
        "SDG5: Gender Equality", 
        "SDG6: Clean Water and Sanitation",
        "SDG7: Affordable and Clean Energy",
        "SDG8: Decent Work and Economic Growth",
        "SDG9: Industry, Innovation and Infrastructure",
        "SDG10: Reduced Inequality",
        "SDG11: Sustainable Cities and Communities",
        "SDG12: Responsible Consumption and Production",
        "SDG13: Climate Action",
        "SDG14: Life Below Water",
        "SDG15: Life on Land",
        "SDG16: Peace and Justice Strong Institutions",
        "SDG17: Partnerships to achieve the Goal"
    ]
    for i, label in enumerate(labels):
        dataset = load_sdg_dataset(tokenizer)
        model_dataset = to_binary(dataset, i + 1)
        model = AutoModelForSequenceClassification.from_pretrained(base_model, num_labels=2, id2label={0: "None", 1: label}, device=-1)
        training_args = TrainingArguments(
            output_dir="test_trainer", 
            evaluation_strategy="epoch",
            num_train_epochs=n_epochs
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=model_dataset["train"],
            eval_dataset=model_dataset["test"],
            compute_metrics=compute_metrics
        )

        trainer.train()
        model.save_pretrained(os.path.join(save_directory, f"model_sdg_{i}"))
    
    

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
