import numpy as np
import mne
import pandas as pd

people_list = []

like_cnt = 0
like_list = []
unlike_cnt = 0
unlike_list = []
for people in people_list:
    epochs_1 = mne.read_epochs('./record/' + people + '_like-epo.fif', preload=True)
    epochs_2 = mne.read_epochs('./record/' + people + '_unlike-epo.fif', preload=True)
    like_cnt += epochs_1.get_data().shape[0]
    like_list.append(epochs_1.get_data().shape[0])
    unlike_cnt += epochs_2.get_data().shape[0]
    unlike_list.append(epochs_2.get_data().shape[0])
print(like_cnt)
print(unlike_cnt)
print(like_list)
print(unlike_list)
