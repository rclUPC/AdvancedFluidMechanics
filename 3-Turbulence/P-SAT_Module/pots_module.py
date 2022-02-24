#git add . &&    git commit -m "EMS Ready Code. Latex Paper v7" &&   git push
#dir /b *.dat | cut -c1-3 | uniq > input_files_corresponding_depths.txt
import csv, datetime, os, sys, glob
import numpy as np

import csv, xlwt, time, timeit, math

import acceleration_module as z_acceleration_module
import correlation_module as z_correlation_module
import snr_module as z_snr_module
import FFT_module as z_fft_module
import itertools
import matplotlib.pyplot as plt
import datetime


def del_files():
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob.glob('Filtered*.csv')
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


def write_files(filtering_method_name, t, u, v, w, snr_u=0, snr_v=0, snr_w=0, cor_u=0, cor_v=0, cor_w=0,input_filename=""):
    filename =  str(input_filename).strip('.dat') + "_Filtered_by_" + str(filtering_method_name).strip().upper() + "_" + str(
        datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f")) + ".csv"

    if filtering_method_name == "acceleration":
        header = ['t', 'u', 'v', 'w']
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(zip(t, u, v, w))
    elif filtering_method_name == "correlation":
        header = ['t', 'u', 'v', 'w','cor_u', 'cor_v','cor_w']
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(zip(t, u, v, w, cor_u, cor_v, cor_w))
    elif filtering_method_name == "snr":
        header = ['t', 'u', 'v', 'w',  'snr_u', 'snr_v', 'snr_w']
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(zip(t, u, v, w, snr_u, snr_v, snr_w))
    elif filtering_method_name == "all":
        header = ['t', 'u', 'v', 'w',  'snr_u', 'snr_v', 'snr_w', 'cor_u', 'cor_v',
                  'cor_w']
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(zip(t, u, v, w,  snr_u, snr_v, snr_w,cor_u, cor_v, cor_w, ))
    else:
        print("Invalid Write Operation")

def full_write_files(filtering_method_name, t, u, v, w, backup_u, backup_v, backup_w, snr_u=0, snr_v=0, snr_w=0, cor_u=0, cor_v=0, cor_w=0,input_filename=""):
    filename = str(input_filename).strip('.dat') + "_Filtered_by_" + str(filtering_method_name).strip().upper() + "_" + str(
        datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f")) + ".dat"

    header = ['t', 'u', 'v', 'w', 'backup_u', 'backup_v', 'backup_w', 'snr_u', 'snr_v', 'snr_w','cor_u', 'cor_v', 'cor_w' ]

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(zip(t, u, v, w, backup_u, backup_v, backup_w,  snr_u, snr_v, snr_w, cor_u, cor_v, cor_w))

    print("File written : ",filename)
    print("Computing FFTs")

    column_header = ['u', 'v', 'w']
    colors = ["red", "green", "blue"]
    for i, j in zip(column_header, colors):
        z_fft_module.fft_module_individual(filename, i, j)

    z_fft_module.fft_module_merged(filename, column_header[0], colors[0])




def process_input_files(input_filename,threshold_correlation=70,threshold_snr=15,threshold_acc=1):
    input_filename = input_filename

    # input_filename = str(sys.argv[1].strip())
    t, u, v, w, snr_u, snr_v, snr_w, cor_u, cor_v, cor_w = np.loadtxt(input_filename, dtype=float, delimiter=',',
                                                                      skiprows=2,
                                                                      usecols=(0, 3, 4, 5, 11, 12, 13, 15, 16, 17),
                                                                      unpack=True)
    backup_u, backup_v, backup_w = list(u), list(v), list(w)

    #del_files()

    # print("IN Main RAW U,V,W: Before Processing", u[:20], v[:20], w[:20])
    print("######################################################")
    print("Current Filename under Process: {}".format(input_filename))
    print("Filtering Technique to be Applied:   correlation thresholding")
    # threshold_correlation =   float(input("Enter the threshold for Correlation (default 70). Press Enter to accept default : ") or "70")
    u, cor_u = z_correlation_module.process_uvw_correlation_thresholding(t, u, cor_u, threshold_correlation)
    v, cor_v = z_correlation_module.process_uvw_correlation_thresholding(t, v, cor_v, threshold_correlation)
    w, cor_w = z_correlation_module.process_uvw_correlation_thresholding(t, w, cor_w, threshold_correlation)
    write_files("correlation", t, u, v, w, cor_u=cor_u, cor_v=cor_v, cor_w=cor_w,input_filename=input_filename)
    # print("IN Main RAW U,V,W: After Processing CORR", u[:20], v[:20], w[:20])

    # print("IN Main RAW U,V,W: Before Processing", u[:20], v[:20], w[:20])
    print("Filtering Technique to be Applied:   SNR thresholding")
    # threshold_snr = float(input("Enter the threshold for SNR (default 15). Press Enter to accept default : ") or "15")
    u, snr_u = z_snr_module.process_uvw_snr_thresholding(t, u, snr_u,threshold_snr)
    v, snr_v = z_snr_module.process_uvw_snr_thresholding(t, v, snr_v,threshold_snr)
    w, snr_w = z_snr_module.process_uvw_snr_thresholding(t, w, snr_w,threshold_snr)
    write_files("snr", t, u, v, w, snr_u=snr_u, snr_v=snr_v, snr_w=snr_w, input_filename=input_filename)
    # print("IN Main RAW U,V,W: After Processing SNR", u[:20], v[:20], w[:20])

    # print("IN Main RAW U,V,W: Before Processing", u[:20], v[:20], w[:20])
    print("Filtering Technique to be Applied:   ACC thresholding")
    # threshold_acc = float(
    #     input("Enter the threshold for ACC thresholding (default 1 [implies 1g]). Press Enter to accept default : ") or "1")
    u = z_acceleration_module.process_uvw_acceleration_thresholding(t, u,threshold_acc)
    v = z_acceleration_module.process_uvw_acceleration_thresholding(t, v,threshold_acc)
    w = z_acceleration_module.process_uvw_acceleration_thresholding(t, w,threshold_acc)
    write_files("acceleration", t, u, v, w, snr_u=snr_u, snr_v=snr_v, snr_w=snr_w, cor_u=cor_u, cor_v=cor_v,
                cor_w=cor_w, input_filename=input_filename)
    # print("IN Main RAW U,V,W: After Processing ACC", u[:20], v[:20], w[:20])
    full_write_files("ALL", t, u, v, w, backup_u=backup_u, backup_v=backup_v, backup_w=backup_w, snr_u=snr_u,
                     snr_v=snr_v, snr_w=snr_w, cor_u=cor_u, cor_v=cor_v,
                     cor_w=cor_w, input_filename=input_filename)


def main():
    start_time1 = datetime.datetime.now()

    print("Hello, World!")
    if __name__ == "__main__":

        # os.system("del_filter_files.bat")
        os.system('mkdir Logs')

        # from datetime import datetime
        start_time = datetime.datetime.now()

        # threshold_correlation = 70
        # threshold_snr = 15
        # threshold_acc = 1
        # shear_velocity=2.6

        threshold_correlation = float(
            input("Enter the threshold for Correlation (default 70). Press Enter to accept default : ") or "70")
        threshold_snr = float(
            input("Enter the threshold for SNR (default 15). Press Enter to accept default : ") or "15")
        threshold_acc = float(
            input("Enter the threshold for ACC thresholding (default 1 [implies 1g]). Press Enter to accept default : ") or "1")

        # shear_velocity = float(
        #     input("Enter the value of Shear Velocity: "))
        # shear_velocity = float(input("Enter the value of Shear Velocity: "))

        print(threshold_correlation, threshold_snr, threshold_acc)#shear_velocity)

        with open("input_files.txt",'r') as f:
            lines = f.readlines()
            for line in lines:
                process_input_files(line.strip(),threshold_correlation, threshold_snr, threshold_acc)


        print("Calculating Parameters . ..  ")



        import parameters_module
        print(os.getcwd())
        import file_mover_module

        time_elapsed = datetime.datetime.now() - start_time

        print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
main()
