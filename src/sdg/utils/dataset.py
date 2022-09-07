from datasets import load_dataset, DatasetDict
from transformers import PreTrainedTokenizer


def load_sdg_dataset(tokenizer: PreTrainedTokenizer) -> DatasetDict:
    """Load the SDG dataset and return it alongside with the tokenizer that has been used"""
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

    tokenized_dataset = ds.map(tokenize, batched=True)
    return tokenized_dataset
