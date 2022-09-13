from transformers import pipeline
from transformers import AutoTokenizer
from datasets import load_dataset
import pandas as pd
from transformers import AutoModelForSequenceClassification
import numpy as np
from datasets import load_metric
from transformers import TrainingArguments, Trainer

TRAIN_PATH = './../data/Train_data.csv'
TEST_PATH = './../data/Test_data.csv'


def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


for i in range(1,18):
    print("Load data SDG {}".format(i))
    df_train = pd.read_csv(TRAIN_PATH)
    df_test = pd.read_csv(TEST_PATH)
    df_train.loc[df_train["SDG"] != i, "SDG"] = 0
    df_train.loc[df_train["SDG"] == i, "SDG"] = 1
    df_train.to_csv("train_{}.csv".format(i))
    df_test.loc[df_test["SDG"] != i, "SDG"] = 0
    df_test.loc[df_test["SDG"] == i, "SDG"] = 1
    df_test.to_csv("test_{}.csv".format(i))

    dataset = load_dataset('csv', data_files={'train': "train_{}.csv".format(i), 'test': "test_{}.csv".format(i)})

    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    tokenized_dataset = tokenized_dataset.rename_column("SDG", "labels")
    tokenized_dataset = tokenized_dataset.remove_columns(["Unnamed: 0"])
    tokenized_dataset = tokenized_dataset.remove_columns(["source"])
    tokenized_dataset = tokenized_dataset.remove_columns(["header"])
    tokenized_dataset = tokenized_dataset.remove_columns(["text"])

    model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=2)

    metric = load_metric("accuracy")

    training_args = TrainingArguments(output_dir="test_trainer", evaluation_strategy="epoch")

    print("Start training SDG {}".format(i))
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset['test'],
        compute_metrics=compute_metrics,)

    trainer.train()

    model.save_pretrained("./saved_model_{}".format(i))
    print("Saved model SDG {}".format(i))
