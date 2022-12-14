import transformers as tfs
import pandas as pd
from icecream import ic

SDGS = [
    "End poverty in all its forms everywhere",
    "End hunger, achieve food security and improved nutrition and promote sustainable agriculture",
    "Ensure healthy lives and promote well-being for all at all ages",
    "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all",
    "Achieve gender equality and empower all women and girls",
    "Ensure availability and sustainable management of water and sanitation for all",
    "Ensure access to affordable, reliable, sustainable and modern energy for all",
    "Promote sustained, inclusive and sustainable economic growth, full and productive employment and decent work for all",
    "Build resilient infrastructure, promote inclusive and sustainable industrialization and foster innovation",
    "Reduce inequality within and among countries",
    "Make cities and human settlements inclusive, safe, resilient and sustainable",
    "Ensure sustainable consumption and production patterns",
    "Take urgent action to combat climate change and its impacts",
    "Conserve and sustainably use the oceans, seas and marine resources for sustainable development",
    "Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss",
    "Promote peaceful and inclusive societies for sustainable development, provide access to justice for all and build effective, accountable and inclusive institutions at all levels",
    "Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development"        
]

def display_result(res):
    print(res["sequence"])
    for label, score in zip(res["labels"], res["scores"]):
        i = SDGS.index(label) + 1
        print(f"\t[{score}] {i} {label}")


if __name__ == "__main__":
    df = pd.read_csv("data/train.csv")
    ic(df)
    exit()

    classifier = tfs.pipeline("zero-shot-classification")
    results = classifier([
            "These efforts have been supported by the international community, with financial and technical contributions to regional communities and specific initiatives to foster African development."
        ],
        candidate_labels=SDGS
    )
    for result in results:
        display_result(result)
