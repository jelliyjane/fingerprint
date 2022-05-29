import os
import csv
import scipy
import shutil
import pandas as pd
import numpy as np
from scipy import signal
from scipy.io import wavfile
from scipy.io.wavfile import write

# wav_path(load path)
cut_folder = "C:\\Users\\cbseo\\Desktop\\test\\FRC100 beamforming2\\2. cut" 
#csv_path(save_path)
csv_folder = "C:\\Users\\cbseo\\Desktop\\test\\FRC100 beamforming2\\3. analysis(csv)" 


def csv_store(cut_wav, wav_csv):
    file_list = os.listdir(cut_wav)
    file_list_wav = [file for file in file_list if file.endswith(".wav")]
    
    total = []
    line = []
    data_length = 1
    
    for wavlist in file_list_wav:
        filename = cut_wav + "\\" + wavlist
        sci_sr, sci_sig = wavfile.read(filename)
        time = len(sci_sig)/sci_sr
        data_num = int(time/data_length)
        
        index = 0
        
        if "FRC" in wavlist:
            step_name = 3
            term = 3
            name_index = wavlist.index("FRC")
            step = int(wavlist[name_index+term:name_index+term+step_name])
            start_freq = 18000
            if step == 400:
                start_freq = 4000
        end_freq = int(sci_sr/2) * time

        
        for i,_ in enumerate(range(data_num)):
            temp_sig = sci_sig[int((i)*sci_sr*data_length) : int((i+1)*sci_sr*data_length)]
            temp_time = np.arange(0, data_length, data_length/len(temp_sig))
            each_magnitude = ["step "+str(i)]
            each_frequency =[wavlist[:-4]]
            
            #fft
            fft = np.fft.fft(temp_sig) / len(temp_sig)
            fft_magnitude = np.abs(fft) 
            f = np.arange(0,sci_sr,sci_sr/len(fft_magnitude))
            left_spectrum = fft_magnitude[:int(len(fft_magnitude)/2)]
            left_f = f[:int(len(fft_magnitude)/2)]

            start_f = start_freq*2/(sci_sr/len(left_spectrum))
            end_f = len(left_spectrum)/24000*22050
            step_f = step*2*(len(left_spectrum)/sci_sr)

            for j in np.arange(start_f, end_f, step_f):
                minimum = int(j - (step_f/step)*5)
                maximum = int(j + (step_f/step)*5)
                each_magnitude.append(left_spectrum[minimum:maximum].max())
                each_frequency.append(left_f[int(j)])
            if(index == 0):
                total.append(each_frequency)
                index = 1
            total.append(each_magnitude)
        total.append(line)
        print(wavlist+"-----done")
    store_csv = wav_csv + "\\" +wavlist[:-14]+wavlist[-10:-4]+".csv"
    with open(store_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(total)
    print("done")


for trans in os.listdir(cut_folder): 
    cut_trans = cut_folder + "\\" + trans
    csv_trans = csv_folder + "\\" + trans
    if(os.path.isdir(csv_trans) == False): #make 'beam' folder
        os.mkdir(csv_trans)
    for devices in os.listdir(cut_trans):
        cut_device = cut_trans + "\\" + devices
        for distances in os.listdir(cut_device):
            cut_distance = cut_device + "\\" + distances
            csv_store(cut_distance, csv_trans) 