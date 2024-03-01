import numpy as np
import mne
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import seaborn as sns
import matplotlib.pyplot as plt

people_list = []

FREQ_BANDS = {
    "delta": [0.5, 4],  # 1-3
    "theta": [4, 8],  # 4-7
    "alpha": [8, 13],  # 8-12
    "beta": [13, 31],  # 13-30
    "gamma": [31, 81]  # 31-80
}
pre_frontal = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4']
frontal = ['F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8']
central = ['CZ', 'FCZ', 'C1', 'C2', 'C3', 'C4', 'FC1', 'FC2', 'FC3', 'FC4']
l_temporal = ['FT7', 'FC5', 'T7', 'C5', 'TP7', 'CP5', 'P7', 'P5']
r_temporal = ['FT8', 'FC6', 'T8', 'C6', 'TP8', 'CP6', 'P8', 'P6']
parietal = ['CPZ', 'CP1', 'CP3', 'CP2', 'CP4', 'PZ', 'P1', 'P3', 'P2', 'P4']
occipital = ['POZ', 'PO3', 'PO5', 'PO7', 'PO4', 'PO6', 'PO8', 'O1', 'O2', 'OZ', 'CB1', 'CB2']
test_size = 50


def cal_de(raw):
    psds, freqs = mne.time_frequency.psd_welch(raw, fmin=0.5, fmax=80.)
    psds /= np.sum(psds, axis=-1, keepdims=True)

    de_feat_list = []
    for fmin, fmax in FREQ_BANDS.values():
        psds_band = psds[:, :, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
        des_band = np.log2(100 * psds_band)
        de_feat_list.append(des_band.reshape(len(psds), -1))

    return np.concatenate(de_feat_list, axis=1)


area = []
importance = []
for people in people_list:
    epochs_1 = mne.read_epochs('./record/' + people + '_like-epo.fif', preload=True).pick_channels(
        pre_frontal + frontal + central + parietal + l_temporal + r_temporal + occipital)
    epochs_2 = mne.read_epochs('./record/' + people + '_unlike-epo.fif', preload=True).pick_channels(
        pre_frontal + frontal + central + parietal + l_temporal + r_temporal + occipital)
    data_like = np.column_stack((cal_de(epochs_1), [1] * epochs_1.get_data().shape[0]))
    data_unlike = np.column_stack((cal_de(epochs_2), [0] * epochs_2.get_data().shape[0]))
    data = np.vstack((data_like, data_unlike))
    np.random.shuffle(data)
    x_train = data[:data.shape[0] - test_size, :-1]
    y_train = data[:data.shape[0] - test_size, -1]
    x_test = data[data.shape[0] - test_size:, :-1]
    y_test = data[data.shape[0] - test_size:, -1]
    lr = LogisticRegression(C=1.0, max_iter=1000)
    svm = SVC(kernel='linear', C=1.0, probability=True)
    rf = RandomForestClassifier(n_estimators=200)
    gbdt = GradientBoostingClassifier(n_estimators=100)
    rf.fit(x_train, y_train)
    # importance.append(rf.feature_importances_)
    area.append(roc_auc_score(y_test, rf.predict_proba(x_test)[:, 1]))
# importance = np.array(importance).mean(axis=0).reshape((5, -1))
# plt.figure(figsize=(12, 8))
# ax = sns.heatmap(importance,
#                  xticklabels=pre_frontal + frontal + central + parietal + l_temporal + r_temporal + occipital,
#                  yticklabels=["delta", "theta", "alpha", "beta", "gamma"])
# plt.show()
with open('svm.txt', 'a') as f:
    f.write(str(np.round(area, 3)) + '\n')
with open('classification.txt', 'a') as f:
    f.write(str(np.array(area).mean()) + '\n')
print(np.array(area))
print(np.array(area).mean())

# data_all = np.zeros((0, 64 * 5 + 1))
# for people in people_list[:-1]:
#     epochs_1 = mne.read_epochs('./record/' + people + '_like-epo.fif', preload=True)
#     epochs_2 = mne.read_epochs('./record/' + people + '_unlike-epo.fif', preload=True)
#     data_like = np.column_stack((cal_de(epochs_1), [1] * epochs_1.get_data().shape[0]))
#     data_unlike = np.column_stack((cal_de(epochs_2), [0] * epochs_2.get_data().shape[0]))
#     data = np.vstack((data_like, data_unlike))
#     data_all = np.vstack((data_all, data))
# x_train = data_all[:, :-1]
# y_train = data_all[:, -1]
# epochs_1 = mne.read_epochs('./record/' + people_list[-1] + '_like-epo.fif', preload=True)
# epochs_2 = mne.read_epochs('./record/' + people_list[-1] + '_unlike-epo.fif', preload=True)
# x_test = np.vstack((cal_de(epochs_1), cal_de(epochs_2)))
# y_test = np.vstack((np.ones((epochs_1.get_data().shape[0], 1)), np.zeros((epochs_2.get_data().shape[0], 1))))
# svm = SVC(kernel='linear', C=1.0, probability=True)
# rf = RandomForestClassifier(n_estimators=200)
# rf.fit(x_train, y_train)
# y_predict = rf.predict(x_test)
# print((y_predict == y_test).mean())
