import numpy as np
import csv, os, datetime, sys

COUNT = 0


def process_uvw_correlation_thresholding(t, X, cor_X, threshold=70):
    X = list(X)
    cor_X = list(cor_X)
    bit_X = bit_generator(cor_X, threshold)
    universal_first_index = global_min_index(bit_X)
    universal_last_index = global_max_index(bit_X)
    correlation_fixer(X, cor_X, bit_X, universal_first_index, universal_last_index)
    # print("Total Non Confirming Values:", COUNT)
    # print(X[:10])
    # print(cor_X[:10])
    return X, cor_X


def increment():
    global COUNT
    COUNT = COUNT + 1


def bit_generator(input_list,threshold):
    """This function is a bit generator. If correlation threshold is set to 70, all those points having correlation less than 70 are marked as 1, and those having
     correlation greater than equal to 70 are marked as 0. So we get a list of bit in 0,1s for the input velocity list. """
    #threshold = 70 # int(input("Enter the threshold for Correlation (default 70) : ") or "70")
    bit_vector = []
    for i in input_list:
        bit_vector.append(0) if i >= threshold else bit_vector.append(1)

    return bit_vector


def correlation_fixer(velocity_i, correlation_velocity_i, bit_vector_velocity_i, universal_first_index,
                      universal_last_index):
    """This function uses the information obtained from the function bit_generator (bit array) and then fixes the values that are
    less than correlation threshold. It will update both the original velocity and the correlation value. At a given time, it
    works on a single velocity column."""

    index = 0
    new_velocity_i = []  # To get the new velocity vector with fixed correlation values
    new_correlation_velocity_i = []  # To get the new correlation vector with fixed correlation values
    for i in bit_vector_velocity_i:
        """i = 0 indicates that the bit_vector has 0 for this position. It indicates the correlation is above or equal to threshold.
        So we just ignore it and add to a new list """
        if i == 0:
            new_velocity_i.append(velocity_i[index])
            new_correlation_velocity_i.append(correlation_velocity_i[index])
        # """Now there is a value that does not confirm to the coorelation values. So we need to fix it"""
        else:
            # print("Value of correlation {}. Issues with co-relation value".format(correlation_velocity_i[index]))
            increment()
            prev, next = location_of_non_spikes(index, bit_vector_velocity_i, universal_first_index,
                                                universal_last_index)
            # print("The values of prev {} and next {}".format(prev, next))

            correlation_velocity_i[index] = (correlation_velocity_i[prev] + correlation_velocity_i[next]) / 2
            velocity_i[index] = (velocity_i[prev] + velocity_i[next]) / 2

            new_velocity_i.append(velocity_i[index])
        index += 1
    # return bit
    # print(new_velocity_i)
    # print(new_correlation_velocity_i)


def global_min_index(bit_vector_velocity_i):
    first_index = 0
    for item in bit_vector_velocity_i:
        if item == 0:
            break
            # last_index = input_list.index(item)
        else:
            first_index += 1
    # print("The first index that conforms to the corelation threshold is:  ", first_index)
    return first_index


def global_max_index(bit_vector_velocity_i):
    last_index = len(bit_vector_velocity_i) - 1  # Because indexing is 1 less
    for item in bit_vector_velocity_i[::-1]:
        if item == 0:
            break
            # last_index = input_list.index(item)
        else:
            last_index -= 1
    # print("The last index that conforms to the corelation threshold is:  ", last_index)
    return last_index


def location_of_non_spikes(index, bit_vector_velocity_i, universal_first_index, universal_last_index):
    """This function will get the two indexes prev and next that are non spike, or confirm to the correlation threshold. """
    prev = universal_first_index  # Some global minima index of 1 from start
    next = universal_last_index  # Some global maxima, index of 1 from last
    input_index_backup = index  # for other spike we need to preserve this value
    flag = 0

    # print("Index Causing Corelation Issue is at :", index)

    # First we find the lower index of the bit_vector where bit is set to 0 from the current index. Hence index-=1.
    while (bit_vector_velocity_i[index] != 0):
        index -= 1
        if bit_vector_velocity_i[
            index] == 0 and index >= 0:  # index>0 so that we dont reach -1 in the previous step which is last index
            prev = index
            flag = 1  # We have got a point
            break
        else:
            prev = universal_first_index
            # Should come when 1st value is not satisfying the corelation

    if flag == 1:  # It means we did locate a point. So no issues
        pass
    else:  # It means we could not locate a previous point that conforms to the correlation threshold. So we need a global minima
        prev = universal_first_index

    index = input_index_backup  # Restore from backup
    flag = 0

    # Now the higher index that conforms to accleration threshold. Hence index+=1.

    if index == len(bit_vector_velocity_i) - 1:
        pass
        # print("Its the last value baby")
    try:
        while (bit_vector_velocity_i[index] != 0):
            index += 1
            if bit_vector_velocity_i[index] == 0:
                next = index
                flag = 1  # We have got a point
                break
    except:
        next = universal_last_index
        # print("Error at index {}. Should come here if some error has occured. last value is spike", index)

    if flag == 1:  # It means we did locate a point. So no issues
        pass
    else:  # It means we could not locate a previous point that conforms to the correlation threshold. So we need a global maxima
        next = universal_last_index

    # print(prev, next)
    return prev, next



