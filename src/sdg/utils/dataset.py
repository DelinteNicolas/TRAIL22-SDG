from typing import List, Tuple
import pandas as pd
import numpy as np
from datasets import load_dataset, DatasetDict
from transformers import PreTrainedTokenizer

def load_sdg_dataset(tokenizer: PreTrainedTokenizer) -> DatasetDict:
    """
    Load the SDG dataset. 
    If a tokenizer is provided, it is applied to the whole dataset.
    """
    ds = load_dataset(
        "csv",
        data_files={
            "train": "data/Train_data.csv", 
            "test": "data/Test_data.csv"
        }
    )
    ds = ds.remove_columns(["Unnamed: 0", "source", "header"])
    ds = ds.rename_column("SDG", "label")

    def tokenize(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    return ds.map(tokenize, batched=True)

def load_sdg() -> Tuple[List[str], List[int], List[str], List[int]]:
    """Returns the train and the test dataframe"""
    try:
        df_train = pd.read_csv("data/Train_data.csv")
        df_test = pd.read_csv("data/Test_data.csv")
    except FileNotFoundError:
        df_train = pd.read_csv("../data/Train_data.csv")
        df_test = pd.read_csv("../data/Test_data.csv")
    train_x = list(df_train["text"])
    train_y = np.array(df_train["SDG"]) - 1
    test_x = list(df_test["text"])
    test_y = np.array((df_test["SDG"])) -1
    return train_x, train_y, test_x, test_y
