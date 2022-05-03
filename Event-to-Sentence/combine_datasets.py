# This script combines all datasets into one dataset
import os
import glob

root_dir = "/xmotors_ai_shared_cephfs/team/perception/adam/datasets/nlp/Event-to-Sentence"
save_dir = os.path.join(root_dir, "1-6")
os.makedirs(save_dir, exist_ok=True)

subdir_names = [str(x) for x in range(1,7)]
for subdir_name in subdir_names:
    subdir = os.path.join(root_dir, subdir_name)

