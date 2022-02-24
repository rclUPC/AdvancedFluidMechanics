import csv, datetime, os, sys, glob, xlwt, time, timeit, math
import numpy as np
import itertools
import matplotlib.pyplot as plt


def calc_ak_bk(U, total_rows, k):
    ak = bk = 0
    j = 0
    for every_value in U:
        ak = ak + every_value * np.cos(2 * math.pi * (j / total_rows) * k)
        bk = bk + every_value * np.sin(2 * math.pi * (j / total_rows) * k)
        j += 1
    return ak / total_rows, bk / total_rows


def all_fourier_calculations(total_rows, U, V, W, M):
    U0 = np.mean(U)
    V0 = np.mean(V)
    W0 = np.mean(W)
#    print(("Total Rows in the file are %d and U0 = %d" % (total_rows, U0)))

    U_avg = []
    partial_sum_U = 0
    V_avg = []
    partial_sum_V = 0
    W_avg = []
    partial_sum_W = 0

    ak_list_U = []
    bk_list_U = []
    ak_list_V = []
    bk_list_V = []
    ak_list_W = []
    bk_list_W = []

#    print(M)

    for k in range(1, int((M - 1) / 2) + 1):
        ak_U, bk_U = calc_ak_bk(U, total_rows, k)
        ak_list_U.append(ak_U)
        bk_list_U.append(bk_U)
        ak_V, bk_V = calc_ak_bk(V, total_rows, k)
        ak_list_V.append(ak_V)
        bk_list_V.append(bk_V)
        ak_W, bk_W = calc_ak_bk(W, total_rows, k)
        ak_list_W.append(ak_W)
        bk_list_W.append(bk_W)

    # print ak_list_U, bk_list_U, ak_list_V, bk_list_V, ak_list_W, bk_list_W,

    for j in range(0, total_rows):
        # print "---------------\nIteration Number J = %d" %(j)
        for k in range(1, int((M - 1) / 2) + 1):
            # ak, bk = calc_ak_bk(U, total_rows, k)
            # print "Value of a%d  = %0.3f and b%d =  %0.3f" %(k, 2*ak, k, 2*bk)
            # partial_sum = partial_sum + ak*np.cos(2 * math.pi * (j / total_rows)*k) + bk*np.sin(2 * math.pi * (j / total_rows)*k)
            partial_sum_U = partial_sum_U + ak_list_U[k - 1] * np.cos(2 * math.pi * (j / total_rows) * k) + bk_list_U[
                k - 1] * np.sin(2 * math.pi * (j / total_rows) * k)
            partial_sum_V = partial_sum_V + ak_list_V[k - 1] * np.cos(2 * math.pi * (j / total_rows) * k) + bk_list_V[
                k - 1] * np.sin(2 * math.pi * (j / total_rows) * k)
            partial_sum_W = partial_sum_W + ak_list_W[k - 1] * np.cos(2 * math.pi * (j / total_rows) * k) + bk_list_W[
                k - 1] * np.sin(2 * math.pi * (j / total_rows) * k)
        U_j = 0.5 * U0 + partial_sum_U
        V_j = 0.5 * V0 + partial_sum_V
        W_j = 0.5 * W0 + partial_sum_W
        # print "U_avg = %f" %(U_j*2)  # Multiplied by 2 since Vishal had 2/n and  1 * a0
        partial_sum_U = 0
        partial_sum_V = 0
        partial_sum_W = 0
        U_avg.append(float('{:01.3f}'.format(U_j * 2)))
        V_avg.append(float('{:01.3f}'.format(V_j * 2)))
        W_avg.append(float('{:01.3f}'.format(W_j * 2)))

    return U_avg, V_avg, W_avg


def process_unsteady_files(input_filename):
    try:
        Timezero, U, V, W = np.loadtxt(input_filename, dtype=float, delimiter=',', skiprows=1, usecols=(0, 1, 2, 3),
                                       unpack=True)  # np.loadtxt(c, delimiter=',', usecols=(0, 2), unpack=True)
        total_rows = min(len(U), len(V), len(W), len(Timezero))
    except:
        print("File not found, {}".format(input_filename))
        return

    M = int(input("Enter the value of k, i.e. # of Fourier Components : "))
    while (M % 2 != 1):
        print("The Value of k should be strictly odd")
        M = int(input("Enter the value of k, i.e. # of Fourier Components : "))
    output_filename = str(input_filename.split('.')[0]) + "_k_" + str(M) + "_" + "Component_" + str(
        (M - 1) / 2) + ".xls"
    print(output_filename)
    U_avg, V_avg, W_avg = all_fourier_calculations(total_rows, U, V, W, M)

    U_prime = []
    V_prime = []
    W_prime = []
    U_prime_U_prime = []
    V_prime_V_prime = []
    W_prime_W_prime = []
    U_prime_V_prime = []
    V_prime_W_prime = []
    W_prime_U_prime = []

    for a, b, c, d, e, f in zip(U, U_avg, V, V_avg, W, W_avg):
        U_prime.append(float('{:01.3f}'.format(a - b)))
        V_prime.append(float('{:01.3f}'.format(c - d)))
        W_prime.append(float('{:01.3f}'.format(e - f)))
        U_prime_U_prime.append(float('{:01.3f}'.format((a - b) * (a - b))))
        V_prime_V_prime.append(float('{:01.3f}'.format((c - d) * (c - d))))
        W_prime_W_prime.append(float('{:01.3f}'.format((e - f) * (e - f))))
        U_prime_V_prime.append(float('{:01.3f}'.format((a - b) * (c - d))))
        V_prime_W_prime.append(float('{:01.3f}'.format((c - d) * (e - f))))
        W_prime_U_prime.append(float('{:01.3f}'.format((e - f) * (a - b))))

    U_prime_U_prime_Average, V_prime_V_prime_Average, W_prime_W_prime_Average = all_fourier_calculations(total_rows,
                                                                                                         U_prime_U_prime,
                                                                                                         V_prime_V_prime,
                                                                                                         W_prime_W_prime,
                                                                                                         M)
    U_prime_V_prime_Average, V_prime_W_prime_Average, W_prime_U_prime_Average = all_fourier_calculations(total_rows,
                                                                                                         U_prime_V_prime,
                                                                                                         V_prime_W_prime,
                                                                                                         W_prime_U_prime,
                                                                                                         M)

    TKE = []
    for a, b, c in zip(U_prime_U_prime_Average, V_prime_V_prime_Average, W_prime_W_prime_Average):
        TKE.append(float('{:01.3f}'.format((a + b + c) / 2)))

    import xlwt
    from tempfile import TemporaryFile
    book = xlwt.Workbook()


    Timezero = Timezero.tolist()
    Timezero.insert(0, "Timezero")

    U = U.tolist()
    U.insert(0, "U")

    V = V.tolist()
    V.insert(0, "V")

    W = W.tolist()
    W.insert(0, "W")

    U_avg.insert(0, "U_avg")
    V_avg.insert(0, "V_avg")
    W_avg.insert(0, "W_avg")



    fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
    # z='red'
    # marker symbol
    axs[0, 0].scatter(Timezero[1:], U[1:], s=2, c='r', marker=">")
    axs[0, 0].set_title("RAW U Velocities")

    # marker from TeX
    axs[0, 1].scatter(Timezero[1:], V[1:], s=2, c='g', marker=r'$\alpha$')
    axs[0, 1].set_title("RAW V Velocities")

    # marker from path
    # verts = [[-1, -1], [1, -1], [1, 1], [-1, -1]]
    axs[0, 2].scatter(Timezero[1:], W[1:], s=2, c='b', marker=r'$\alpha$')
    axs[0, 2].set_title("RAW W Velocities")

    # regular polygon marker
    axs[1, 0].scatter(Timezero[1:], U_avg[1:], s=2, c='r', marker=(5, 0))
    axs[1, 0].set_title("Fourier Averaged \n U Velocities k= {}".format(M))

    # regular star marker
    axs[1, 1].scatter(Timezero[1:], V_avg[1:], s=2, c='g', marker=(5, 1))
    axs[1, 1].set_title("Fourier Averaged \n V Velocities k= {}".format(M))

    # regular asterisk marker
    axs[1, 2].scatter(Timezero[1:], W_avg[1:], s=2, c='b', marker=(5, 2))
    axs[1, 2].set_title("Fourier Averaged \n W Velocities k= {}".format(M))

    plt.tight_layout()
    plt.savefig(output_filename + ".jpg")
    # plt.show()
    plt.clf()

    U_prime.insert(0, "u'")
    V_prime.insert(0, "v'")
    W_prime.insert(0, "w'")
    U_prime_U_prime.insert(0, "u'u'")
    V_prime_V_prime.insert(0, "v'v'")
    W_prime_W_prime.insert(0, "w'w'")
    U_prime_V_prime.insert(0, "u'v'")
    V_prime_W_prime.insert(0, "v'w'")
    W_prime_U_prime.insert(0, "u'w'")
    U_prime_U_prime_Average.insert(0, "u'u'_Avg")
    V_prime_V_prime_Average.insert(0, "v'v'_Avg")
    W_prime_W_prime_Average.insert(0, "w'w'_Avg")
    U_prime_V_prime_Average.insert(0, "u'v'_Avg")
    V_prime_W_prime_Average.insert(0, "v'w'_Avg")
    W_prime_U_prime_Average.insert(0, "u'w'_Avg")
    TKE.insert(0, "TKE")

    sheet1 = book.add_sheet('Fourier Components')
    for i, e in enumerate(Timezero):
        sheet1.write(i, 0, e)

    for i, e in enumerate(U):
        sheet1.write(i, 1, e)

    for i, e in enumerate(V):
        sheet1.write(i, 2, e)

    for i, e in enumerate(W):
        sheet1.write(i, 3, e)

    for i, e in enumerate(U_avg):
        sheet1.write(i, 4, e)

    for i, e in enumerate(V_avg):
        sheet1.write(i, 5, e)

    for i, e in enumerate(W_avg):
        sheet1.write(i, 6, e)

    for i, e in enumerate(U_prime):
        sheet1.write(i, 7, e)

    for i, e in enumerate(V_prime):
        sheet1.write(i, 8, e)

    for i, e in enumerate(W_prime):
        sheet1.write(i, 9, e)

    for i, e in enumerate(U_prime_U_prime):
        sheet1.write(i, 10, e)

    for i, e in enumerate(V_prime_V_prime):
        sheet1.write(i, 11, e)

    for i, e in enumerate(W_prime_W_prime):
        sheet1.write(i, 12, e)

    for i, e in enumerate(U_prime_V_prime):
        sheet1.write(i, 13, e)

    for i, e in enumerate(V_prime_W_prime):
        sheet1.write(i, 14, e)

    for i, e in enumerate(W_prime_U_prime):
        sheet1.write(i, 15, e)

    for i, e in enumerate(U_prime_U_prime_Average):
        sheet1.write(i, 16, e)

    for i, e in enumerate(V_prime_V_prime_Average):
        sheet1.write(i, 17, e)

    for i, e in enumerate(W_prime_W_prime_Average):
        sheet1.write(i, 18, e)

    for i, e in enumerate(U_prime_V_prime_Average):
        sheet1.write(i, 19, e)

    for i, e in enumerate(V_prime_W_prime_Average):
        sheet1.write(i, 20, e)

    for i, e in enumerate(W_prime_U_prime_Average):
        sheet1.write(i, 21, e)

    for i, e in enumerate(TKE):
        sheet1.write(i, 22, e)

    book.save(output_filename)
    book.save(TemporaryFile())

    # plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    # plt.scatter(Timezero,U)
    # plt.show(block = True)


def main():
    start_time1 = datetime.datetime.now()

    if __name__ == "__main__":

        # os.system("del_filter_files.bat")
        os.system('mkdir Logs')

        # from datetime import datetime
        start_time = datetime.datetime.now()

        with open("input_ensemble_files.txt", 'r') as f:
            lines = f.readlines()

            for line in lines:
                print("Processing File {}".format(line))
                process_unsteady_files(line.strip())


main()