import os, math, sys
import numpy as np
import csv, xlwt, time, timeit
from xlrd import open_workbook
import logging
import octant_module as z_octant_module
from scipy.stats import skew
from scipy.stats import kurtosis

# import graph_3d_octant as z_octant_graphs

start_time = time.time()


def precision(value, p=5):
    return round(value, p)


def rename(fname):
    fname = fname.split(" ")
    return "_".join(fname)


def rounding(value):
    return round(value, 10)

shear_velocity = float(input("Enter the value of Shear Velocity: "))
flow_depth = float(input("Enter the value of Flow Depth: "))
os.system('dir /b *Filtered_by_ALL*.dat > dat_files_list.txt')
p = 20

with open("dat_files_list.txt", "rt", encoding="utf8") as f:
    for dat_filename_read in f:
        dat_filename_read = dat_filename_read.strip()
        # try:
        os.rename(dat_filename_read, rename(dat_filename_read))
        # except PermissionError:
        #    print("Permission Error")
        dat_filename_read = rename(dat_filename_read)
        print("Filename Read: %s" % dat_filename_read)
        try:
            f = open(dat_filename_read, 'rt')
            # g = csv.reader ((f), delimiter=",")
            g = csv.reader(f, delimiter=",")
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("Sheet 1")

            # with open("dat_files_list.txt") as f:
            # for dat_filename_read in f:
            # dat_filename_read=dat_filename_read.strip()
            # print("Filename Read: %s" %dat_filename_read)
            # f=open(dat_filename_read, 'rb')
            # g = csv.reader ((f), delimiter=",")
            # wbk= xlwt.Workbook()
            # sheet = wbk.add_sheet("Sheet 1")

            for rowi, row in enumerate(g):
                for coli, value in enumerate(row):
                    try:
                        sheet.write(rowi, coli, float(value))
                    except:
                        sheet.write(rowi, coli, value)

            wbk.save(dat_filename_read + '.xls')
            print("Conversion of %s to %s.xls Done" % (dat_filename_read, dat_filename_read))
            f.close()
        except Exception as e:
            current = os.getcwd()
            dstDir = os.getcwd() + "\Logs"
            os.chdir(dstDir)
            logger = logging.getLogger(dat_filename_read)
            logger.setLevel(logging.INFO)

            # Assign a file-handler to that instance
            fh = logging.FileHandler(dat_filename_read + ".txt")
            fh.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.exception(e)

            fh.close()
            os.chdir(current)
try:
    print("Conversion of All DAT Files to XLS Done")

    os.system('dir /b *.xls > excel_files_list.txt')
    print("Success")
    os.system('type excel_files_list.txt')

    file1 = "excel_files_list.txt"
    file2 = open("input_files_corresponding_depths.txt", 'r')

    # with open(file1) as f, open(file2) as f2:
    #     for x, y in zip(f, f2):
    #         depth_info = y.strip()
    #         # print("{0}\t{1}".format(x.strip(), y.strip()))

    with open("excel_files_list.txt") as f:
        for filename_read in f:
            # with open(file1) as f, open(file2) as f2:
            #     for filename_read, y in zip(f, f2):
            #         depth_info = y.strip()
            print("\n-------------------------------------------------------------------")
            print("File Read %s" % filename_read)
            filename_read = filename_read.strip()
            book = open_workbook(str(filename_read))

            depth_info = file2.readline().strip()
            print("Depth info = {}".format(depth_info))

            octant_file_name = filename_read.strip('.xls')
            print("Dat file corresponding to octant file is : ", octant_file_name)

            first_sheet = book.sheet_by_index(0)  # 1 in case of Quadrant Conditional

            print("Total Cols: %d" % first_sheet.ncols)
            print("Total Rows: %d" % first_sheet.nrows)
            total_rows = first_sheet.nrows - 3

            #shear_velocity = 2.6
            multiplying_factor_2d = 0.75
            multiplying_factor_3d = 0.5
#            flow_depth = 14
            kinematic_viscosity = 0.000000850488830581204

            all_quadrant = 0
            threshold = 0

            Q1H0 = 0
            Q1H2 = 0

            Q2H0 = 0
            Q2H2 = 0

            Q3H0 = 0
            Q3H2 = 0

            Q4H0 = 0
            Q4H2 = 0

            inst_velocity_U = 0
            inst_velocity_V = 0
            inst_velocity_W = 0

            U_prime = 0
            V_prime = 0
            W_prime = 0

            U_prime_sum_of_square = 0
            V_prime_sum_of_square = 0
            W_prime_sum_of_square = 0

            U_prime_sum_of_cubes = 0
            V_prime_sum_of_cubes = 0
            W_prime_sum_of_cubes = 0

            U_prime_U_prime_U_prime = 0
            U_prime_V_prime_V_prime = 0
            U_prime_W_prime_W_prime = 0
            U_prime_U_prime_W_prime = 0
            V_prime_V_prime_W_prime = 0
            W_prime_W_prime_W_prime = 0

            Reynolds_stress_uv = 0
            Reynolds_stress_uw = 0
            Reynolds_stress_vw = 0

            del_u_by_del_t = 0
            del_u = 0
            e = 0
            ED = 0

            for i in range(3, first_sheet.nrows):
                row = first_sheet.row_slice(i)

                inst_velocity_U = inst_velocity_U + row[1].value
                inst_velocity_V = inst_velocity_V + row[2].value
                inst_velocity_W = inst_velocity_W + row[3].value

            average_velocity_U = inst_velocity_U / total_rows
            average_velocity_V = inst_velocity_V / total_rows
            average_velocity_W = inst_velocity_W / total_rows

            # Computation for intensities
            for i in range(3, first_sheet.nrows):
                previous_row = first_sheet.row_slice(i - 1)
                row = first_sheet.row_slice(i)

                time_instance = row[0].value

                U_prime = row[1].value - average_velocity_U
                U_prime_sum_of_square = U_prime_sum_of_square + U_prime * U_prime
                U_prime_sum_of_cubes = U_prime_sum_of_cubes + U_prime * U_prime * U_prime

                V_prime = row[2].value - average_velocity_V
                V_prime_sum_of_square = V_prime_sum_of_square + V_prime * V_prime
                V_prime_sum_of_cubes = V_prime_sum_of_cubes + V_prime * V_prime * V_prime

                W_prime = row[3].value - average_velocity_W
                W_prime_sum_of_square = W_prime_sum_of_square + W_prime * W_prime
                W_prime_sum_of_cubes = W_prime_sum_of_cubes + W_prime * W_prime * W_prime

                U_prime_U_prime_W_prime = U_prime_U_prime_W_prime + U_prime * U_prime * W_prime
                U_prime_W_prime_W_prime = U_prime_W_prime_W_prime + U_prime * W_prime * W_prime

                U_prime_V_prime_V_prime = U_prime_V_prime_V_prime + U_prime * V_prime * V_prime
                V_prime_V_prime_W_prime = V_prime_V_prime_W_prime + V_prime * V_prime * W_prime

                Reynolds_stress_uw = Reynolds_stress_uw + U_prime * W_prime
                Reynolds_stress_uv = Reynolds_stress_uv + U_prime * V_prime
                Reynolds_stress_vw = Reynolds_stress_vw + V_prime * W_prime

                if i > 3:  # 1st Row needs to be ignored as it has headers
                    U_prime_previous_row = previous_row[1].value - average_velocity_U
                    time_previous_row = previous_row[0].value
                    del_u_by_del_t = del_u_by_del_t + (
                            (U_prime - U_prime_previous_row) / (time_instance - time_previous_row)) * (
                                             (U_prime - U_prime_previous_row) / (time_instance - time_previous_row))

                all_quadrant = all_quadrant + U_prime * W_prime

            del_u = (del_u_by_del_t / (total_rows - 1))
            e = 15 * del_u * (kinematic_viscosity) / (average_velocity_U * average_velocity_U)

            ED = (e * flow_depth) / (shear_velocity * shear_velocity * shear_velocity)

            Reynolds_stress_uw = Reynolds_stress_uw / total_rows
            Reynolds_stress_uv = Reynolds_stress_uv / total_rows
            Reynolds_stress_vw = Reynolds_stress_vw / total_rows

            U_variance = U_prime_sum_of_square / total_rows
            V_variance = V_prime_sum_of_square / total_rows
            W_variance = W_prime_sum_of_square / total_rows

            U_stdev = math.sqrt(U_variance)
            V_stdev = math.sqrt(V_variance)
            W_stdev = math.sqrt(W_variance)

            threshold = 2 * U_stdev * W_stdev
            print("Threshold: %0.10f" % threshold)

            for i in range(3, first_sheet.nrows):

                row = first_sheet.row_slice(i)

                U_prime = row[1].value - average_velocity_U
                W_prime = row[3].value - average_velocity_W

                if U_prime > 0 and W_prime > 0:  # First Quadrant
                    Q1H0 = Q1H0 + U_prime * W_prime
                    if U_prime * W_prime >= threshold:
                        Q1H2 = Q1H2 + U_prime * W_prime

                elif U_prime < 0 and W_prime > 0:  # Second Quadrant
                    Q2H0 = Q2H0 + U_prime * W_prime
                    if U_prime * W_prime <= -threshold:
                        Q2H2 = Q2H2 + U_prime * W_prime

                elif U_prime < 0 and W_prime < 0:  # Third Quadrant
                    Q3H0 = Q3H0 + U_prime * W_prime
                    if U_prime * W_prime >= threshold:
                        Q3H2 = Q3H2 + U_prime * W_prime

                elif U_prime > 0 and W_prime < 0:  # Fouth Quadrant
                    Q4H0 = Q4H0 + U_prime * W_prime
                    if U_prime * W_prime <= -threshold:
                        Q4H2 = Q4H2 + U_prime * W_prime

                else:
                    print("One of the values is 0")

            Anisotropy = W_stdev / U_stdev

            fku_2d = (U_prime_sum_of_cubes / total_rows + U_prime_W_prime_W_prime / total_rows) * multiplying_factor_2d
            fkw_2d = (W_prime_sum_of_cubes / total_rows + U_prime_U_prime_W_prime / total_rows) * multiplying_factor_2d

            Fku_2d = fku_2d / (shear_velocity * shear_velocity * shear_velocity)
            Fkw_2d = fkw_2d / (shear_velocity * shear_velocity * shear_velocity)

            fku_3d = (
                             U_prime_sum_of_cubes / total_rows + U_prime_V_prime_V_prime / total_rows + U_prime_W_prime_W_prime / total_rows) * multiplying_factor_3d
            fkw_3d = (
                             U_prime_U_prime_W_prime / total_rows + V_prime_V_prime_W_prime / total_rows + W_prime_sum_of_cubes / total_rows) * multiplying_factor_3d

            Fku_3d = fku_3d / (shear_velocity * shear_velocity * shear_velocity)
            Fkw_3d = fkw_3d / (shear_velocity * shear_velocity * shear_velocity)

            TKE_3d = (U_variance + V_variance + W_variance) * multiplying_factor_3d

            m30 = 0
            m03 = 0
            m21 = 0
            m12 = 0

            M30 = 0
            M03 = 0
            M21 = 0
            M12 = 0

            U_cap = 0
            V_cap = 0
            W_cap = 0

            for i in range(3, first_sheet.nrows):
                row = first_sheet.row_slice(i)

                U_prime = row[1].value - average_velocity_U
                U_cap = U_prime / U_stdev

                W_prime = row[3].value - average_velocity_W
                W_cap = W_prime / W_stdev

                m30 = m30 + U_cap * U_cap * U_cap
                m03 = m03 + W_cap * W_cap * W_cap

                m21 = m21 + U_cap * U_cap * W_cap
                m12 = m12 + U_cap * W_cap * W_cap

            M30 = m30 / total_rows
            M03 = m03 / total_rows
            M21 = m21 / total_rows
            M12 = m12 / total_rows



            t, u, v, w = np.loadtxt(octant_file_name, dtype=float, delimiter=',',
                                    skiprows=2,
                                    usecols=(0, 1, 2, 3),
                                    unpack=True)

            # z_octant_module.plot_octant_graph(octant_file_name,u,v,w)

            freq_sorted, kurtosis_U_prime, kurtosis_V_prime, kurtosis_W_prime, skewness_U_prime, skewness_V_prime, skewness_W_prime = z_octant_module.compute_octant2(
                t, u, v, w)

            total = 0
            for ele in range(0, len(freq_sorted)):
                total = total + freq_sorted[ele]

            print("File name Read: %s" % (filename_read))

            print("U_avg: %0.10f" % (average_velocity_U))
            print("V_avg: %0.10f" % (average_velocity_V))
            print("W_avg: %0.10f" % (average_velocity_W))

            print("U_var: %0.10f" % (U_variance))
            print("V_var: %0.10f" % (V_variance))
            print("W_var: %0.10f" % (W_variance))


            print("Skewness U Prime",precision(skewness_U_prime))
            print("Skewness U Prime",precision(skewness_V_prime))
            print("Skewness U Prime",precision(skewness_W_prime))

            print("Kurtosis U Prime",precision(kurtosis_U_prime))
            print("Kurtosis V Prime",precision(kurtosis_V_prime))
            print("Kurtosis W Prime",precision(kurtosis_W_prime))


            print("U_stdev: %0.10f" % (U_stdev))
            print("V_stdev: %0.10f" % (V_stdev))
            print("W_stdev: %0.10f" % (W_stdev))

            print("Reynolds_stress uv: %0.10f" % (Reynolds_stress_uv))
            print("Reynolds_stress uw: %0.10f" % (Reynolds_stress_uw))
            print("Reynolds_stress vw: %0.10f" % (Reynolds_stress_vw))

            print("Anisotropy: %0.10f" % (Anisotropy))

            print("M30: %0.10f" % (M30))
            print("M03: %0.10f" % (M03))
            print("M21: %0.10f" % (M21))
            print("M12: %0.10f" % (M12))

            print("fku_2d: %0.10f" % (fku_2d))
            print("Fku_2d: %0.10f" % (Fku_2d))
            print("fkw_2d: %0.10f" % (fkw_2d))
            print("Fkw_2d: %0.10f" % (Fkw_2d))
            print("fku_3d: %0.10f" % (fku_3d))
            print("Fku_3d: %0.10f" % (Fku_3d))
            print("fkw_3d: %0.10f" % (fkw_3d))
            print("Fkw_3d: %0.10f" % (Fkw_3d))

            print("TKE_3d: %0.10f" % (TKE_3d))

            print("Q1H0: %0.10f" % (Q1H0 / all_quadrant))
            print("Q2H0: %0.10f" % (Q2H0 / all_quadrant))
            print("Q3H0: %0.10f" % (Q3H0 / all_quadrant))
            print("Q4H0: %0.10f" % (Q4H0 / all_quadrant))

            print("Q1H2: %0.10f" % (Q1H2 / all_quadrant))
            print("Q2H2: %0.10f" % (Q2H2 / all_quadrant))
            print("Q3H2: %0.10f" % (Q3H2 / all_quadrant))
            print("Q4H2: %0.10f" % (Q4H2 / all_quadrant))

            print("e: %0.10f" % (e))
            print("ED: %0.10f" % (ED))

            print("Octant_plus_1 = {}".format(freq_sorted[0]))
            print("Octant_minus_1 = {}".format(freq_sorted[1]))
            print("Octant_plus_2 = {}".format(freq_sorted[2]))
            print("Octant_minus_2 = {}".format(freq_sorted[3]))
            print("Octant_plus_3 = {}".format(freq_sorted[4]))
            print("Octant_minus_3 = {}".format(freq_sorted[5]))
            print("Octant_plus_4 = {}".format(freq_sorted[6]))
            print("Octant_minus_4 = {}".format(freq_sorted[7]))
            print("Total Octant Values in the sample = {}".format(total))



            # print("Nowopening file for writing ")
            fo = open("Parameters.csv", "a")
            fo.write("\n"
                     + str(filename_read) + ","
                     + str(depth_info) + ","
                     + str(precision(average_velocity_U)) + ","
                     + str(precision(average_velocity_V)) + ","
                     + str(precision(average_velocity_W)) + ","
                     + str(precision(U_variance)) + ","
                     + str(precision(V_variance)) + ","
                     + str(precision(W_variance)) + ","
                     + str(precision(skewness_U_prime)) + ","
                     + str(precision(skewness_V_prime)) + ","
                     + str(precision(skewness_W_prime)) + ","
                     + str(precision(kurtosis_U_prime)) + ","
                     + str(precision(kurtosis_V_prime)) + ","
                     + str(precision(kurtosis_W_prime)) + ","
                     + str(precision(U_stdev)) + ","
                     + str(precision(V_stdev)) + ","
                     + str(precision(W_stdev)) + ","
                     + str(precision(Reynolds_stress_uv, 10)) + ","
                     + str(precision(Reynolds_stress_uw, 10)) + ","
                     + str(precision(Reynolds_stress_vw, 10)) + ","
                     + str(precision(Anisotropy)) + ","
                     + str(precision(M30)) + ","
                     + str(precision(M03)) + ","
                     + str(precision(M12)) + ","
                     + str(precision(M21)) + ","
                     + str(precision(fku_2d, 10)) + ","
                     + str(precision(Fku_2d, 10)) + ","
                     + str(precision(fkw_2d, 10)) + ","
                     + str(precision(Fkw_2d, 10)) + ","
                     + str(precision(fku_3d, 10)) + ","
                     + str(precision(Fku_3d, 10)) + ","
                     + str(precision(fkw_3d, 10)) + ","
                     + str(precision(Fkw_3d, 10)) + ","
                     + str(precision(TKE_3d, 10)) + ","
                     + str(precision(Q1H0 / all_quadrant)) + ","
                     + str(precision(Q2H0 / all_quadrant)) + ","
                     + str(precision(Q3H0 / all_quadrant)) + ","
                     + str(precision(Q4H0 / all_quadrant)) + ","
                     + str(precision(Q1H2 / all_quadrant)) + ","
                     + str(precision(Q2H2 / all_quadrant)) + ","
                     + str(precision(Q3H2 / all_quadrant)) + ","
                     + str(precision(Q4H2 / all_quadrant)) + ","
                     + str(precision(e)) + ","
                     + str((ED)) + ","
                     + str((freq_sorted[0])) + ","
                     + str((freq_sorted[1])) + ","
                     + str((freq_sorted[2])) + ","
                     + str((freq_sorted[3])) + ","
                     + str((freq_sorted[4])) + ","
                     + str((freq_sorted[5])) + ","
                     + str((freq_sorted[6])) + ","
                     + str((freq_sorted[7])) + ","
                     + str((total)) + ","
                     + str(precision((freq_sorted[0]) / total)) + ","
                     + str(precision((freq_sorted[1]) / total)) + ","
                     + str(precision((freq_sorted[2]) / total)) + ","
                     + str(precision((freq_sorted[3]) / total)) + ","
                     + str(precision((freq_sorted[4]) / total)) + ","
                     + str(precision((freq_sorted[5]) / total)) + ","
                     + str(precision((freq_sorted[6]) / total)) + ","
                     + str(precision((freq_sorted[7]) / total)) + ","
                     + str((min(freq_sorted))) + ","
                     + str((max(freq_sorted))) + ","
                     )

            fo.close()
            # file2.close()
            print("File Written and Closed")
            print("-------------------------------------------------------------------\n")

except Exception as e:
    current = os.getcwd()
    dstDir = os.getcwd() + "\Logs"
    os.chdir(dstDir)
    logger = logging.getLogger(filename_read)
    logger.setLevel(logging.INFO)

    # Assign a file-handler to that instance
    fh = logging.FileHandler(filename_read + ".txt")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.exception(e)
    fh.close()
    os.chdir(current)

os.system('dir /b *Filtered_by_ALL*.dat > dat_files_list.txt')

#
# def plot(x, y, ylabel):
#     plt.scatter(y, x, label=ylabel, color="green", marker=".", s=30)
#     plt.ylabel('Depth')
#     # frequency label
#     plt.xlabel(ylabel)
#     # plot title
#     plt.title('Depth vs ' + ylabel)
#     # showing legend
#     plt.legend()
#
#     # function to show the plot
#     # plt.show()
#     plt.savefig('depth_' + ylabel + '_scatter.png')
#     plt.clf()
#
#
# def line_plot(x, y, ylabel):
#     plt.plot(y, x, label=ylabel, color="green")
#     # x-axis label
#
#     plt.ylabel('Depth')
#     # frequency label
#     plt.xlabel(ylabel)
#     # plot title
#     plt.title('Depth vs ' + ylabel)
#     # showing legend
#     plt.legend()
#
#     # function to show the plot
#     # plt.show()
#     plt.savefig('depth_' + ylabel + '_line.png')
#     plt.clf()
#
#
# import csv
#
# with open('foo.csv', 'r') as csvFile:
#     reader = csv.reader(csvFile)
#     # l=len(row)
#     R = [[]]
#     i = 0
#     for row in reader:
#         R.append([])
#         R[i].append(row)
#         i += 1
# csvFile.close()
# l = len(R[0][0])
# graph = 32
# current = os.getcwd()
# dstDir = os.getcwd() + "\Graphs"
# os.chdir(dstDir)
#
# #
# # import matplotlib.pyplot as plt
# #
# # # x-axis values
# # x = []
# # y_label = []
# # for j in range(2, i):
# #     x.append(R[j][0][0].split("_")[0])
# # for j in range(l):
# #     y_label.append(R[0][0][j])
# # x.sort()
# # col = 1
# # l_row = len(row)
# # for lenght in range(len(y_label)):
# #     y_label[lenght] = y_label[lenght].split('/')[0]
# # y_label.remove('filename_read')
# # for label in y_label:
# #     y = []
# #
# #     for c in range(2, i):
# #         y.append(R[c][0][col])
# #
# #     a = y
# #     b = x
# #     x = []
# #     y = []
# #     for he in a:
# #         y.append(float(he))
# #     for she in b:
# #         x.append(float(she))
# #
# #     plot(x, y, label)
# #     line_plot(x, y, label)
# #     col += 1
# #
# # os.chdir(current)
# #
# # os.system("del *.xls")
print("Program Ends: Check Parameters.csv :)")
# print("Have a good day! :)")
#
# end_time = time.time()
# print(("Elapsed time was %f seconds" % (end_time - start_time)))
