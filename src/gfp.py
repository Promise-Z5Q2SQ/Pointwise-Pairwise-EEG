import numpy as np
import mne
from matplotlib import pyplot as plt
import scipy.signal

pre_frontal = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4']
frontal = ['F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8']
central = ['CZ', 'FCZ', 'C1', 'C2', 'C3', 'C4', 'FC1', 'FC2', 'FC3', 'FC4']
l_temporal = ['FT7', 'FC5', 'T7', 'C5', 'TP7', 'CP5', 'P7', 'P5']
r_temporal = ['FT8', 'FC6', 'T8', 'C6', 'TP8', 'CP6', 'P8', 'P6']
parietal = ['CPZ', 'CP1', 'CP3', 'CP2', 'CP4', 'PZ', 'P1', 'P3', 'P2', 'P4']
occipital = ['POZ', 'PO3', 'PO5', 'PO7', 'PO4', 'PO6', 'PO8', 'O1', 'O2', 'OZ', 'CB1', 'CB2']


def abs_threshold(epochs, threshold):
    data = epochs.copy().pick_channels(['FZ']).get_data()
    # channels and times are last two dimension in MNE ndarrays,
    # and we collapse across them to get a (n_epochs,) shaped array
    rej = np.any(np.abs(data) > threshold, axis=(-1, -2))
    return rej


people_list = []
people_list1 = []

threshold = 50e-6
like_epochs = []
unlike_epochs = []
first_epochs = []
like1_epochs = []
unlike1_epochs = []
for people in people_list:
    epochs_1 = mne.read_epochs('./record/' + people + '_like-epo.fif', preload=True)
    bad_epoch_mask = abs_threshold(epochs_1, threshold)
    epochs_1.drop(bad_epoch_mask, reason="absolute threshold")
    like_epochs.append(epochs_1)
    epochs_2 = mne.read_epochs('./record/' + people + '_unlike-epo.fif', preload=True)
    bad_epoch_mask = abs_threshold(epochs_2, threshold)
    epochs_2.drop(bad_epoch_mask, reason="absolute threshold")
    unlike_epochs.append(epochs_2)
    epochs_3 = mne.read_epochs('./record/' + people + '_first-epo.fif', preload=True)
    bad_epoch_mask = abs_threshold(epochs_3, threshold)
    epochs_3.drop(bad_epoch_mask, reason="absolute threshold")
    first_epochs.append(epochs_3)
for people in people_list1:
    epochs_3 = mne.read_epochs('./record/' + people + '_like-epo.fif', preload=True)
    bad_epoch_mask = abs_threshold(epochs_3, threshold)
    epochs_3.drop(bad_epoch_mask, reason="absolute threshold")
    like1_epochs.append(epochs_3)
    epochs_4 = mne.read_epochs('./record/' + people + '_unlike-epo.fif', preload=True)
    bad_epoch_mask = abs_threshold(epochs_4, threshold)
    epochs_4.drop(bad_epoch_mask, reason="absolute threshold")
    unlike1_epochs.append(epochs_4)

like = []
unlike = []
first = []
like1 = []
unlike1 = []
times = like_epochs[0].times
for i in np.arange(len(like_epochs)):
    like.append(like_epochs[i].average(r_temporal).get_data().mean(axis=0))
for i in np.arange(len(unlike_epochs)):
    unlike.append(unlike_epochs[i].average(r_temporal).get_data().mean(axis=0))
for i in np.arange(len(first_epochs)):
    first.append(first_epochs[i].average(central).get_data().mean(axis=0))
for i in np.arange(len(like1_epochs)):
    like1.append(like1_epochs[i].average(central + parietal).get_data().mean(axis=0))
for i in np.arange(len(unlike1_epochs)):
    unlike1.append(unlike1_epochs[i].average(central + parietal).get_data().mean(axis=0))

like = np.array(like).mean(axis=0)
unlike = np.array(unlike).mean(axis=0)
first = np.array(first).mean(axis=0)
like1 = np.array(like1).mean(axis=0)
unlike1 = np.array(unlike1).mean(axis=0)

# pair = scipy.signal.savgol_filter(- like + unlike, 93, 1)
# point = scipy.signal.savgol_filter(- like1 + unlike1, 93, 1)

fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(12, 12))

ax1.plot(times, like / 1e6, label='highRel')
ax1.plot(times, unlike / 1e6, label='lowRel')
# ax1.plot(times, first / 1e6, label='first(pair-wise)')
ax2.plot(times, like1 / 1e6, label='highRel')
ax2.plot(times, unlike1 / 1e6, label='lowRel')
# ax1.plot(times, pair / 1e6, label='pair-wise')
# ax1.plot(times, point / 1e6, label='point-wise')
ax1.axvline(x=0, ls="--", c="green")
ax2.axvline(x=0, ls="--", c="green")
ax1.axvline(x=0.180, ymin=0.1, ymax=0.7, ls="-", c="black")
ax1.axvline(x=0.380, ymin=0.1, ymax=0.7, ls="-", c="black")
ax2.axvline(x=0.150, ymin=0.1, ymax=0.7, ls="-", c="black")
ax2.axvline(x=0.380, ymin=0.1, ymax=0.7, ls="-", c="black")
ax1.set_xlabel('Time (s)', fontsize=15)
ax1.set_ylabel('Amplitude (μV)', fontsize=15)
ax1.set_title('pair-wise relevance judgment', fontsize=20)
ax1.tick_params(labelsize=15)
ax1.yaxis.get_offset_text().set_fontsize(15)
ax1.legend(fontsize=15, loc="upper left")
ax2.set_xlabel('Time (s)', fontsize=15)
ax2.set_ylabel('Amplitude (μV)', fontsize=15)
ax2.set_title('point-wise relevance judgment', fontsize=20)
ax2.legend(fontsize=15, loc="upper left")
ax2.tick_params(labelsize=15)
ax2.yaxis.get_offset_text().set_fontsize(15)
plt.subplots_adjust(hspace=0.3)  # 调整垂直间距
plt.show()
