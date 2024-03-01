import scipy.stats as stats
import numpy as np
import mne
import pandas as pd

people_list = []

df_dict = {}
time_windows = [[50, 200], [180, 380], [320, 500], [550, 650], [600, 950]]

for item in time_windows:
    item[0] += 200
    item[1] += 200


def abs_threshold(epochs, threshold):
    data = epochs.copy().pick_channels(['FZ']).get_data()
    # channels and times are last two dimension in MNE ndarrays,
    # and we collapse across them to get a (n_epochs,) shaped array
    rej = np.any(np.abs(data) > threshold, axis=(-1, -2))
    return rej


def time_split(data):
    re = {}
    data = np.mean(data.get_data(), axis=1)
    data = np.mean(data, axis=0)
    for _idx, window in enumerate(time_windows):
        re[_idx] = np.mean(10 ** 6 * data[int(window[0]):int(window[1])])
    return re


pre_frontal = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4']
frontal = ['F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8']
central = ['CZ', 'FCZ', 'C1', 'C2', 'C3', 'C4', 'FC1', 'FC2', 'FC3', 'FC4']
l_temporal = ['FT7', 'FC5', 'T7', 'C5', 'TP7', 'CP5', 'P7', 'P5']
r_temporal = ['FT8', 'FC6', 'T8', 'C6', 'TP8', 'CP6', 'P8', 'P6']
parietal = ['CPZ', 'CP1', 'CP3', 'CP2', 'CP4', 'PZ', 'P1', 'P3', 'P2', 'P4']
occipital = ['POZ', 'PO3', 'PO5', 'PO7', 'PO4', 'PO6', 'PO8', 'O1', 'O2', 'OZ', 'CB1', 'CB2']

for idx, channel_chosen in enumerate([l_temporal]):
    for people in people_list:
        epochs_1 = mne.read_epochs('./record/' + people + '_like-epo.fif', preload=True)
        # bad_epoch_mask = abs_threshold(epochs_1, 50e-6)
        # epochs_1.drop(bad_epoch_mask, reason="absolute threshold")
        epochs_2 = mne.read_epochs('./record/' + people + '_unlike-epo.fif', preload=True)
        # bad_epoch_mask = abs_threshold(epochs_2, 50e-6)
        # epochs_2.drop(bad_epoch_mask, reason="absolute threshold")

        raw_data = {'like': epochs_1.pick_channels(channel_chosen),
                    'unlike': epochs_2.pick_channels(channel_chosen)}
        df_dict[people] = {}
        for key in raw_data.keys():
            df_dict[people][key] = time_split(raw_data[key])

    fw = open('anova' + '.txt', 'w')
    for i in range(len(time_windows)):
        fw.write("-----------------")
        fw.write(str([item - 200 for item in time_windows[i]]))
        df_dict2 = {}
        for k, v in df_dict.items():
            for k1, v1 in v.items():
                if k1 not in df_dict2.keys():
                    df_dict2[k1] = []
                df_dict2[k1].append(v1[i])

        df = pd.DataFrame(df_dict2)
        df_melt = df.melt()
        df_melt.insert(df_melt.shape[1], 'id', people_list * 2)
        df_melt.columns = ['Treat', 'Value', 'id']
        # print(df_melt)
        fw.write('\n' + df.to_string() + '\n')
        from scipy.stats import bartlett

        tmp_bar = df.values.T.tolist()
        fw.write(str(bartlett(tmp_bar[0], tmp_bar[1])) + '\n')
        import seaborn as sns

        sns.boxplot(x='Treat', y='Value', data=df_melt)
        from statsmodels.stats.anova import AnovaRM
        from pingouin import rm_anova

        fw.write(str(rm_anova(dv='Value', within='Treat',
                              subject='id', data=df_melt, correction=True)))
        anova_table = AnovaRM(df_melt, 'Value', 'id', within=['Treat']).fit()
        fw.write(str(anova_table))

        from statsmodels.stats.multicomp import MultiComparison

        mc = MultiComparison(df_melt['Value'], df_melt['Treat'])
        tukey_result = mc.allpairtest(stats.ttest_rel, alpha=0.15)
        fw.write(str(tukey_result[0]))
    fw.close()
