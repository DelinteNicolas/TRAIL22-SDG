#! /usr/bin/env python3
import sdg

if __name__ == "__main__":
    clf = sdg.models.zero_shot_classifier(device=0)
    _, _, test_x, test_y = sdg.dataset.load_sdg()
    res = clf(test_x[0])    
    print(test_x[0])
    for score, label in res:
        print(f"[{score*100:.2f}]\t{label}")
    print(f"Actual label: {test_y[0]}")
    