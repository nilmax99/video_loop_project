import cv2
import numpy as np
import os
import shutil

def similarity(img1, img2):
    if img1 is None or img2 is None:
        return float("inf")
    diff = cv2.absdiff(img1, img2)
    return np.sum(diff) / (img1.shape[0] * img1.shape[1])

def find_best_loop(folder, loop_min, loop_max):
    files = sorted(os.listdir(folder))
    scores = {}
    for i in range(len(files)):
        time_i = float(files[i].split("_")[1].replace(".png", ""))
        img1 = cv2.imread(os.path.join(folder, files[i]))

        for j in range(i + 1, len(files)):
            time_j = float(files[j].split("_")[1].replace(".png", ""))
            duration = time_j - time_i
            if loop_min <= duration <= loop_max:
                img2 = cv2.imread(os.path.join(folder, files[j]))
                score = similarity(img1, img2)
                scores[(i, j)] = score

    if not scores:
        shutil.rmtree(folder)
        return None

    best = min(scores.items(), key=lambda x: x[1])
    i, j = best[0]
    start_time = float(files[i].split("_")[1].replace(".png", ""))
    end_time = float(files[j].split("_")[1].replace(".png", ""))
    transition_type = "blurplus"
    shutil.rmtree(folder)
    return (start_time, end_time, transition_type)
