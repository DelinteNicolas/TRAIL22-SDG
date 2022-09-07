import pandas as pd
import sdg


def _create_histogram(filename, df):
    plot = pd.value_counts(df['label']).plot.bar(title="Class balance")
    fig = plot.get_figure()
    fig.savefig(filename)

def class_balance(filename):
    ds = sdg.dataset.load_sdg_dataset()
    df = pd.DataFrame.from_dict(ds["train"])
    _create_histogram(f"{filename}_train.png", df)
    df = pd.DataFrame.from_dict(ds["test"])
    _create_histogram(f"{filename}_test.png", df)
    
    