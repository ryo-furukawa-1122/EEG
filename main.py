# %%
import general.loadings as ld
import general.settings as st
import analysis.waveform as wv
import analysis.filter as fl
import numpy as np

E_NAME = "EVT01"
FS, PRE_STIMULI, POST_STIMULI, chs, stimuli = st.Settings().set_basic_params()
kwargs_signal, kwargs_stimuli = st.Settings().set_plot_theme()
directory, date, file, scale = ld.Loadings().read_config()
data = ld.Loadings().read_mat(f'{directory}/{date}/{file}.mat')

t = np.arange(-PRE_STIMULI, POST_STIMULI, 1/FS)
stim_number = stimuli["2 kHz"]
lag = data[f"WB{chs[0]:02}_ts"]
lag_sample = int(lag * FS)

stim_times = data[E_NAME][stim_number::5] - lag
stim_stamp = np.array([int((stim_time) * FS) for stim_time in stim_times])

# %%
signals = wv.Waveform().arange_data(data, chs, stim_stamp, FS, PRE_STIMULI, POST_STIMULI)
# %%
filtered_signals = fl.Filter().filter_signals(signals, FS)

# # %%
# # ---
# import numpy as np
# import pandas as pd
# from scipy import signal
# import matplotlib.pyplot as plt

# def lowpass(time, samplerate, fp, fs, gpass, gstop):
#     fn = samplerate / 2                              # ナイキスト周波数
#     wp = fp / fn                                     # ナイキスト周波数で通過域端周波数を正規化
#     ws = fs / fn                                     # ナイキスト周波数で阻止域端周波数を正規化
#     N, Wn = signal.buttord(wp, ws, gpass, gstop)     # オーダーとバターワースの正規化周波数を計算
#     b, a = signal.butter(N, Wn, "low")               # フィルタ伝達関数の分子と分母を計算
#     y = signal.filtfilt(b, a, time)                  # 信号に対してフィルタをかける
#     return y 



# fp = 50                                              # 通過域端周波数[Hz]
# fs = 100                                             # 阻止域端周波数[Hz]
# gpass = 3                                            # 通過域端最大損失[dB]
# gstop = 20                                           # 阻止域端最小損失[dB]

# fs1 = samplerate = 40000
# base_left = -0.2
# base_right = 0
# analy_lenbase = 8000
# time_base = np.arange(base_left,base_right,1/fs1)
# cut_left = -0.2
# cut_right = 0.7
# analy_len = 36000
# time = np.arange(cut_left,cut_right,1/fs1)
# stimuli = 2                                          # 刺激の種類変更（0～4：Click, 2, 4, 8, 16）

# WB = 'WB'
# Ch = 'Ch'
# name = 'ampsum_leave'
# plt.rcParams["font.size"] = 14

# # lab = mat['WB09_ts']
# # lag_sample = int(lab * fs1)

# sttime_base = mat['EVT01'][stimuli::5] + base_left 
# lists_st_base = [] 
# for sm in sttime_base:
#     stsample_base = int(sm * fs1 - lag_sample)
#     lists_st_base.append(stsample_base) 

# edtime_base = mat['EVT01'][stimuli::5] + base_right 
# lists_ed_base = []
# for sm2 in edtime_base:
#     edsample_base = int(sm2 * fs1 - lag_sample)
#     lists_ed_base.append(edsample_base)

# amp_sum_base = []
# amp_del_base = [] #数が合わない用

# ampsum_baseleave9 = [] #残す用
# ampsum_baseleave10 = []
# ampsum_baseleave11 = []
# ampsum_baseleave12 = []
# ampsum_baseleave13 = []
# ampsum_baseleave14 = []

# for No_base in range(9, 15):
#    for i_base in range(len(lists_st_base)):
#       ss_base = lists_st_base[i_base]
#       ed_base = lists_ed_base[i_base]
#       amp_base = [np.concatenate(mat[f'{WB}{No_base:02}'][ss_base:ed_base])]
#       data_lofilt = lowpass(amp_base, samplerate, fp, fs, gpass, gstop)

#       if len(data_lofilt[0])==analy_lenbase:
#          A_base = [data_lofilt.T]
#       elif len(data_lofilt[0])==analy_lenbase-1:
#          data_lofilt = np.append(data_lofilt, 0)
#          data_lofilt = data_lofilt.reshape(1,analy_lenbase)
#          A_base = [data_lofilt.T]
#       elif len(data_lofilt[0])==analy_lenbase+1:
#          data_lofilt = np.delete(data_lofilt, -1)
#          data_lofilt = data_lofilt.reshape(1,analy_lenbase)
#          A_base = [data_lofilt.T]

#       #A_base = [data_lofilt.T]
#       if len(A_base[0])==analy_lenbase: #8000:
#          amp_sum_base += A_base
#       else:
#          amp_del_base += A_base
      
#    ave_base = np.mean(amp_sum_base,axis=0)
#    base = [np.mean(ave_base)]
#    globals()['ampsum_baseleave%s'%No_base].extend(base)
#    print(base)
#    amp_sum_base.clear()

# lag = mat['WB09_ts']
# lag_sample = int(lag * fs1)

# start_time = mat['EVT01'][stimuli::5] + cut_left 
# lists_st = [] 
# for sample in start_time:
#     start_sample = int(sample * fs1 - lag_sample)
#     lists_st.append(start_sample) 
#     #print(start_sample)

# end_time = mat['EVT01'][stimuli::5] + cut_right 
# lists_ed = []
# for sample2 in end_time:
#     end_sample = int(sample2 * fs1 - lag_sample)
#     lists_ed.append(end_sample)
#     #print(end_sample)


# fig, axes = plt.subplots(16, 1, figsize=(20,20), constrained_layout=True, sharex=True, sharey=True)

# amp_sum = []
# amp_del = [] #数が合わない用

# ampsum_leave9 = []
# ampsum_leave10 = []
# ampsum_leave11 = []
# ampsum_leave12 = []
# ampsum_leave13 = []
# ampsum_leave14 = []

# for No in range(9, 15):
#     amp_sum.clear()
#     for i in range(len(lists_st)):
#         ss = lists_st[i]
#         ed = lists_ed[i]
#         amp = [np.concatenate(mat[f'{WB}{No:02}'][ss:ed])]
#         data_lofilt = lowpass(amp, samplerate, fp, fs, gpass, gstop)


#         if len(data_lofilt[0])==analy_len:
#             A = [data_lofilt.T]
#         elif len(data_lofilt[0])==analy_len-1:
#             data_lofilt = np.append(data_lofilt, 0)
#             data_lofilt = data_lofilt.reshape(1,analy_len)
#             A = [data_lofilt.T]
#         elif len(data_lofilt[0])==analy_len+1:
#             data_lofilt = np.delete(data_lofilt, -1)
#             data_lofilt = data_lofilt.reshape(1,analy_len)
#             A = [data_lofilt.T]


#         #A = [data_lofilt.T]
#         if len(A[0])==analy_len:#40000:
#             amp_sum += A
#         else:
#             amp_del += A

#     ave = np.mean(amp_sum,axis=0)
#     new_ave = list(map(lambda G: G - globals()['ampsum_baseleave%s'%No][0], ave))
#     axes[No-1].set_title(f'{Ch}{No}')
#     axes[No-1].plot(time,new_ave,color='k')
#     axes[No-1].set_xlim(cut_left, cut_right)
#     axes[No-1].set_ylim(-0.005, 0.005)
#     axes[No-1].vlines(x=0, ymin=-0.02, ymax=0.02, color='r', alpha=.7, linestyles='dashed')
#     axes[No-1].hlines(y=0, xmin=cut_left, xmax=cut_right, color='k', linewidth=0.7)
#     fig.supxlabel("Time (s)")
#     fig.supylabel("Amplitude (mV)")   

#     if len(ampsum_leave9)==0:
#         ampsum_leave9.extend(amp_sum)
#     elif len(ampsum_leave10)==0:
#         ampsum_leave10.extend(amp_sum)
#     elif len(ampsum_leave11)==0:
#         ampsum_leave11.extend(amp_sum) 
#     elif len(ampsum_leave12)==0:
#         ampsum_leave12.extend(amp_sum)  
#     elif len(ampsum_leave13)==0:
#         ampsum_leave13.extend(amp_sum)
#     elif len(ampsum_leave14)==0:
#         ampsum_leave14.extend(amp_sum) 

#     # plt.savefig("temp.png", bbox_inches="tight")

# mean_leave9 = []
# mean_leave10 = []
# mean_leave11 = []
# mean_leave12 = []
# mean_leave13 = []
# mean_leave14 = []
# for No in range(9, 15):
#     fig = plt.figure(figsize=(8,5))
#     plt.rcParams["font.size"] = 14
#     plt.grid()
#     ave4 = np.mean(globals()['ampsum_leave%s'%No],axis=0)
#     new_ave4 = list(map(lambda G: G - globals()['ampsum_baseleave%s'%No][0], ave4))
#     globals()['mean_leave%s'%No].extend(new_ave4)
#     plt.plot(time, new_ave4, color='b')
#     plt.title(f'{Ch}{No}')
#     plt.xlabel("Time (s)")
#     plt.ylabel("Amplitude (mV)")
#     plt.vlines(x=0, ymin=-0.002, ymax=0.002, color='r', alpha=.7, linestyles='dashed')
#     plt.hlines(y=0, xmin=cut_left, xmax=cut_right, color='k', linewidth=0.7)
#     plt.show()
# # %%
# # ts_step: sampling period
# # ts: lag time stanp (not for evt)