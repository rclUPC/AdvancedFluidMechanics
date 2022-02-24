from scipy.stats import skew
from scipy.stats import kurtosis
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
import string , random
start_time = datetime.now()

def plot_octant_graph(input_filename,u,v,w):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    t, x,y,z  = np.loadtxt(input_filename, dtype=float, delimiter=',',
                                                                      skiprows=2,
                                                                      usecols=(0,4,5,6),
                                                                      unpack=True)



    ax.scatter(x, y, z, c='g', marker='o')

    ax.set_xlabel('U')
    ax.set_ylabel('V')
    ax.set_zlabel('W')
    input_filename = input_filename+  "_octant_graph_.pdf"
    plt.savefig(input_filename, dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format="pdf",
        transparent=False, bbox_inches="tight", pad_inches=0.1,
        frameon=None)
    # plt.show()
    plt.clf()


import sys
import numpy as np


# do your work here
def frequency(lis):
    # making dictionary with words and their frequency
    count = {}
    for i in lis:
        if i in count.keys():
            count[i] = count[i] + 1
        else:
            count[i] = 1
    return count


def mean(value):
    su, Total_count = 0, 0
    for i in value:
        su = su + i
        Total_count = Total_count + 1
    return float(su / Total_count)


def prime(vel, mean):
    prime = []
    for i in vel:
        prime.append(float(i - mean))
    return prime


def lis(x):
    lists = []
    for i in x:
        lists.append(i)
    return lists


def write_csv(csv_file, d, value):
    import csv
    from itertools import zip_longest
    export_data = zip_longest(*d, fillvalue='')
    with open(csv_file, 'w', encoding="ISO-8859-1", newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(value)
        wr.writerows(export_data)
    myfile.close()


def octane(u, v, w):
    if u >= 0 and v >= 0:
        if w >= 0:
            return 1
        else:
            return -1
    if u < 0 and v >= 0:
        if w >= 0:
            return 2
        else:
            return -2
    if u < 0 and v < 0:
        if w >= 0:
            return 3
        else:
            return -3
    if u > 0 and v < 0:
        if w >= 0:
            return 4
        else:
            return -4


#
# with open(sys.argv[1]) as filename:
#     fname = sys.argv[1]


def compute_octant2(t, u, v, w):
    # with open("Filtered.csv") as filename:
    T_seepage, U_seepage, V_seepage, W_seepage, = t, u, v, w

    # np.loadtxt(c, delimiter=',', usecols=(0, 2), unpack=True)
    u_mean, v_mean, w_mean = mean(U_seepage), mean(V_seepage), mean(W_seepage)
    # u_mean, v_mean, w_mean = list(u_mean),list(v_mean),list(w_mean)
    # T_seepage, U_seepage, V_seepage, W_seepage = list(T_seepage), list(U_seepage), list(V_seepage), list(W_seepage)
    # print(type(T_seepage), type(U_seepage), type(V_seepage), type(W_seepage))
    u_ = prime(U_seepage, u_mean)
    v_ = prime(V_seepage, v_mean)
    w_ = prime(W_seepage, w_mean)

    octan = []

    for u, v, w in zip(u_, v_, w_):
        octan.append(octane(u, v, w))
    value = ('Velocities', 'U', 'V', 'W', "u'", "v'", "w'", 'OCTANT ID')

    T_seepage = lis(T_seepage)
    U_seepage = lis(U_seepage)
    V_seepage = lis(V_seepage)
    W_seepage = lis(W_seepage)

    # octane ={}
    d = [T_seepage, U_seepage, V_seepage, W_seepage, u_, v_, w_, octan]
    # for i,j in zip(value,[T_seepage, U_seepage, V_seepage, W_seepage,u_,v_,w_,octan]):
    #    octane[i]=j
    #
    # filename = "detailed_octant.csv"
    # write_csv(filename, d, value)

    # print(T_seepage, U_seepage, V_seepage, W_seepage)
    freq = frequency(octan)

    values = [" ", "Frequency", "Total", "Probability"]
    Octane_ = ['Octane 1', 'Octane -1', 'Octane 2', 'Octane -2', 'Octane 3', 'Octane -3', 'Octane 4', 'Octane -4']
    freq_sorted = [freq[1], freq[-1], freq[2], freq[-2], freq[3], freq[-3], freq[4], freq[-4]]
    #print(freq_sorted, type(freq_sorted))

    kurtosis_U_prime = (kurtosis(u_))
    kurtosis_V_prime = (kurtosis(v_))
    kurtosis_W_prime = (kurtosis(w_))

    skewness_U_prime = (skew(u_))
    skewness_V_prime = (skew(v_))
    skewness_W_prime = (skew(w_))

    print("Kurtosis U_prime = {}".format(kurtosis_U_prime ))
    print("Kurtosis V_prime = {}".format(kurtosis_V_prime))
    print("Kurtosis W_prime = {}".format(kurtosis_W_prime))
    print("Skewness U_prime = {}".format(skewness_U_prime))
    print("Skewness V_prime = {}".format(skewness_V_prime))
    print("Skewness W_prime = {}".format(skewness_W_prime))

    return freq_sorted, kurtosis_U_prime, kurtosis_V_prime, kurtosis_W_prime ,  skewness_U_prime,skewness_V_prime,skewness_W_prime

    # Prob = []
    # Total_count = 0
    # for i in T_seepage:
    #     Total_count = Total_count + 1
    # Total = []
    # for i in Octane_:
    #     Total.append(Total_count)
    # for i in freq_sorted:
    #     Prob.append(i / Total_count)
    #
    # d = [Octane_, freq_sorted, Total, Prob]
    #
    # filename = "overall_octant_frequency.csv"
    # write_csv(filename, d, values)
    # return freq_sorted



#end_time = datetime.now()
#print('Duration: {}'.format(end_time - start_time))
