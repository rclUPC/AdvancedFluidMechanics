import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft
import pandas as pd
from matplotlib import rc

import csv
import os

rc('text', usetex=True)


def fft_module_individual(filename_read, column_header, color_choice):
    header = ['Freq', 'Amplitude']
    # filename_read = 'FFT_sample.csv'
    # column_header = 'u'
    # color_choice='red'
    print("filename_read in FFT module", filename_read)
    (filename_without_extension, ext) = os.path.splitext(filename_read)
    print(filename_without_extension)

    data_filename_write = filename_without_extension + '_Column_Header_' + column_header + '_FFT_Data.csv'
    image_filename_write = filename_without_extension + '_Column_Header_' + column_header + '_FFT_Spectra.jpg'
    #
    # data_filename_write = filename_read.split('.')[0] + '_Column_Header_' + column_header + '_FFT_Data.csv'
    # image_filename_write = filename_read.split('.')[0] + '_Column_Header_' + column_header + '_FFT_Spectra.jpg'

    df = pd.read_csv(filename_read)
    df.dropna(inplace=True)
    print(column_header)
    u_list = df[column_header].tolist()
    column_to_numpy_array = np.asarray(u_list)
    slice_of_input_array_for_processing_FFT = []

    # Uncomment in FFT

    percentage = float(input(
        "Enter the % number of samples for FFT Calculation (default 10 percent). Press Enter to accept default : ") or "10")
    frequency = int(input("Enter the sampling frequency: "))

    # percentage = 10
    # frequency = 100

    N = int(len(u_list) * (percentage / 100))

    # num_samples = 3000
    for i in range(0, N):
        slice_of_input_array_for_processing_FFT.append(column_to_numpy_array[i])

    # frequency of signal
    T = 1 / frequency
    # x=np.linspace(0,N*T,N)#0, ,21
    y = slice_of_input_array_for_processing_FFT
    ####### processs via window  y = windowing(y)
    yf = fft(y)

    xf = np.linspace(0.0, 1.0 / (2 * T), N // 2)  # 0, ,10
    my_list = 2.0 / N * np.abs(yf[0:N // 2])

    with open(data_filename_write, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(i for i in header)
        writer.writerows(zip(xf, my_list))

    plt.clf()
    plt.loglog(xf, 2.0 / N * np.abs(yf[0:N // 2]), color=color_choice,
               label=r'Spectrum of \textit{' + str(column_header).upper() + '}')
    plt.legend()
    plt.grid()
    plt.xlabel('Frequency')
    plt.ylabel('Peaks')
    plt.savefig(image_filename_write)
    # plt.show()
    plt.clf()


def fft_module_merged(filename_read, column_header, color_choice):
    print("In FFT Merged Module")
    header = ['Freq', 'Amplitude_U', 'Amplitude_V', 'Amplitude_W']
    # filename_read = 'FFT_sample.csv'
    # column_header = 'u'
    # color_choice='red'

    print("filename_read in FFT module", filename_read)
    (filename_without_extension, ext) = os.path.splitext(filename_read)
    print(filename_without_extension)

    data_filename_write = filename_without_extension + '_Column_Header_uvw' + '_FFT_Data_Merged.csv'
    image_filename_write = filename_without_extension + '_Column_Header_uvw' + '_FFT_Spectra_Merged.jpg'

    df = pd.read_csv(filename_read)
    df.dropna(inplace=True)

    for i in column_header:
        print(column_header)

    u_list = df[column_header].tolist()
    column_to_numpy_array = np.asarray(u_list)

    column_to_numpy_array_U = np.asarray(df["u"].tolist())
    column_to_numpy_array_V = np.asarray(df["v"].tolist())
    column_to_numpy_array_W = np.asarray(df["w"].tolist())

    slice_of_input_array_for_processing_FFT_U = []
    slice_of_input_array_for_processing_FFT_V = []
    slice_of_input_array_for_processing_FFT_W = []

    # Uncomment in FFT
    percentage = float(
        input(
            "Enter the % number of samples for FFT Calculation (default 10 percent). Press Enter to accept default : ") or "10")

    frequency = int(input("Enter the sampling frequency: "))

    # percentage = 10
    # frequency = 100

    N = int(len(u_list) * (percentage / 100))

    # num_samples = 3000
    for i in range(0, N):
        slice_of_input_array_for_processing_FFT_U.append(column_to_numpy_array_U[i])
        slice_of_input_array_for_processing_FFT_V.append(column_to_numpy_array_V[i])
        slice_of_input_array_for_processing_FFT_W.append(column_to_numpy_array_W[i])

    # frequency of signal
    T = 1 / frequency
    # x=np.linspace(0,N*T,N)#0, ,21
    y = slice_of_input_array_for_processing_FFT_U
    ####### processs via window  y = windowing(y)
    yf = fft(y)
    xf = np.linspace(0.0, 1.0 / (2 * T), N // 2)  # 0, ,10
    my_list = 2.0 / N * np.abs(yf[0:N // 2])
    my_list_u = my_list
    plt.loglog(xf, 2.0 / N * np.abs(yf[0:N // 2]), color="r", label=r'Spectrum of \textit{U}')
    plt.legend()

    y = slice_of_input_array_for_processing_FFT_V
    ####### processs via window  y = windowing(y)
    yf = fft(y)
    my_list = 2.0 / N * np.abs(yf[0:N // 2])
    my_list_v = my_list
    plt.loglog(xf, 2.0 / N * np.abs(yf[0:N // 2]), color="g", label=r'Spectrum of \textit{V}')
    plt.legend()

    y = slice_of_input_array_for_processing_FFT_W
    ####### processs via window  y = windowing(y)
    yf = fft(y)
    my_list = 2.0 / N * np.abs(yf[0:N // 2])
    my_list_w = my_list
    plt.loglog(xf, 2.0 / N * np.abs(yf[0:N // 2]), color="b", label=r'Spectrum of \textit{W}')
    plt.legend()

    plt.grid()
    plt.xlabel('Frequency')
    plt.ylabel('Peaks')
    plt.savefig(image_filename_write)
    with open(data_filename_write, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(i for i in header)
        writer.writerows(zip(xf, my_list_u, my_list_v, my_list_w))

    # plt.show()

# fft_module_merged(filename_read, column_header, colors)
