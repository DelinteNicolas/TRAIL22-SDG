from datasets import load_dataset, DatasetDict
from transformers import PreTrainedTokenizer


def load_sdg_dataset(tokenizer: PreTrainedTokenizer=None) -> DatasetDict:
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

    if tokenizer is not None:
        def tokenize(examples):
            return tokenizer(examples["text"], padding="max_length", truncation=True)

        ds = ds.map(tokenize, batched=True)
    return ds
