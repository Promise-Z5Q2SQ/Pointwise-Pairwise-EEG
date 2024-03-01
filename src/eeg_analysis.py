import mne
import numpy as np
import json
from mne.preprocessing import ICA

file_name = 'filename'


def cal_pair_events(_events):
    for i in np.arange(_events.shape[0]):
        if _events[i][2] == 5:
            _events[i - 3][2] = 111
            _events[i - 4][2] = 112
        elif _events[i][2] == 8:
            _events[i - 3][2] = 110
            _events[i - 4][2] = 112
    np.save('./record/' + file_name + '.npy', _events)
    for i in np.arange(_events.shape[0]):
        print(_events[i])


def cal_point_events(_events):
    for i in np.arange(_events.shape[0]):
        if _events[i][2] == 1:
            _events[i - 2][2] = 111
        elif _events[i][2] == 27:
            _events[i - 2][2] = 111
        # elif _events[i][2] == 28:
        #     _events[i - 2][2] = 111
        elif _events[i][2] == 29:
            _events[i - 2][2] = 110
        elif _events[i][2] == 30:
            _events[i - 2][2] = 110
    np.save('./record/' + file_name + '.npy', _events)
    for i in np.arange(_events.shape[0]):
        print(_events[i])


def abs_threshold(epochs, threshold):
    data = epochs.pick_channels(['FZ']).get_data()
    # channels and times are last two dimension in MNE ndarrays,
    # and we collapse across them to get a (n_epochs,) shaped array
    rej = np.any(np.abs(data) > threshold, axis=(-1, -2))
    return rej


if __name__ == '__main__':
    raw = mne.io.read_raw_curry('./record/' + file_name + '.cdt', preload=True)
    montage = mne.channels.read_dig_fif('./data/mode/montage.fif')
    montage.ch_names = json.load(open("./data/mode/montage_ch_names.json"))
    raw.set_montage(montage)
    raw.plot_sensors(ch_type='eeg', show_names=True)
    raw.set_eeg_reference(['M1', 'M2'])
    print(raw)
    print(raw.info)
    raw = raw.notch_filter(freqs=50)
    raw = raw.filter(l_freq=0.1, h_freq=30)

    # ica = ICA(n_components=15, max_iter='auto')
    # ica.fit(raw)
    # ica.plot_components()
    # ica.exclude = [0]
    # ica.apply(raw)

    events, event_id = mne.events_from_annotations(raw)
    print(events.shape, event_id)
    # cal_point_events(events)
    events = np.load('./record/' + file_name + '.npy')

    epochs_1 = mne.Epochs(raw, events, event_id=110, tmin=-0.2, tmax=1, baseline=(-0.2, 0), preload=True)
    print(epochs_1)
    # epochs_1.save('./record/' + file_name + '_like-epo.fif')
    epochs_2 = mne.Epochs(raw, events, event_id=111, tmin=-0.2, tmax=1, baseline=(-0.2, 0), preload=True)
    print(epochs_2)
    # epochs_2.save('./record/' + file_name + '_unlike-epo.fif')
    # epochs_3 = mne.Epochs(raw, events, event_id=112, tmin=-0.2, tmax=1, baseline=(-0.2, 0), preload=True)
    # print(epochs_3)
    # epochs_3.save('./record/' + file_name + '_first-epo.fif')
    # bad_epoch_mask = abs_threshold(epochs_1, 100e-6)
    # epochs_1.drop(bad_epoch_mask, reason="absolute threshold")
    # bad_epoch_mask = abs_threshold(epochs_2, 50e-6)
    # epochs_2.drop(bad_epoch_mask, reason="absolute threshold")
    evoked_1 = epochs_1.average()
    evoked_2 = epochs_2.average()
    # evoked_3 = epochs_3.average()
    mne.viz.plot_compare_evokeds(evokeds={'Like': evoked_1, 'Unlike': evoked_2},
                                 picks=['FCZ'])
