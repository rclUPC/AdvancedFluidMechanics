import numpy as np
import datetime, csv
import functools
import sys

def process_uvw_acceleration_thresholding(t, x,lambda_v=1):

    loop_counter = 0
    max_execution_limit = 10
    acceleration = compute_acceleration(t, x)
    bit_u, spike_counter = bit_generator_acceleration(acceleration, -1,lambda_v)
    universal_first_index = global_min_index(bit_u)
    universal_last_index = global_max_index(bit_u)

    while spike_counter != 0:

        backup_u = x
        x = acceleration_fixer(x, bit_u, universal_first_index, universal_last_index)

        acceleration = compute_acceleration(t, x)
        bit_u, spike_counter = bit_generator_acceleration(acceleration, -1,lambda_v)

        # print(spike_counter)

        print("*" * loop_counter)
        loop_counter += 1
        if loop_counter == max_execution_limit:
            break

    # For positive acceleration

    loop_counter = 0

    acceleration = compute_acceleration(t, x)
    bit_u, spike_counter = bit_generator_acceleration(acceleration, 1,lambda_v)
    universal_first_index = global_min_index(bit_u)
    universal_last_index = global_max_index(bit_u)

    while spike_counter != 0:

        backup_u = x
        x = acceleration_fixer(x, bit_u, universal_first_index, universal_last_index)
        acceleration = compute_acceleration(t, x)
        bit_u, spike_counter = bit_generator_acceleration(acceleration, 1,lambda_v)

        # print(t[:10])
        # print(x[:10])
        # print(acceleration[:10])
        # print(bit_u[:10])
        # print(spike_counter)

        # filename = str(datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f")) + "_positive_loop_" + str(
        #     x) + '_' + str(
        #     loop_counter) + ".csv"
        #
        # with open(filename, 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(zip(t, x, acceleration))

        print("#" * loop_counter)
        loop_counter += 1
        if loop_counter == max_execution_limit:
            break

    # print("In Function process uvw - {}", x[:20])
    return x


def checking_identical(current_list, previous_list):
    # initializing lists

    current_list = [int(i * 1000) for i in current_list]
    previous_list = [int(i * 1000) for i in previous_list]

    # import pandas as pd
    # data = pd.read_csv('Filtered.csv').apply(
    #     lambda col: (col * 1000).astype(int) if col.name in ['u', 'v', 'w'] else col)
    # print((data['v'] == data['v']).all())
    #

    # print("Current List for comparison {}".format(current_list[:25]))
    # print("Previous List for comparison {}".format(previous_list[:25]))
    # printing lists
    # print("The first list is : " + str(current_list))
    # print("The second list is : " + str(previous_list))

    # using map() + reduce() to check if
    # lists are equal
    if functools.reduce(lambda i, j: i and j, map(lambda m, k: m == k, current_list, previous_list), True):
        # print("The lists are identical")
        return 1
    else:
        # print("The lists are not identical")
        return 0


def list_precision_controller(input_list, precision=4):
    input_list = [round(elem, precision) for elem in input_list]
    return input_list


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


def compute_acceleration(time_vector, input_list):
    index = 0
    acceleration = []
    for t, u in zip(time_vector, input_list):
        if index == 0:
            acceleration.append(
                (input_list[index] - input_list[index - 1]) / (
                        time_vector[index] - time_vector[index - 1]))  # delta change
        else:
            acceleration.append(
                (input_list[index] - input_list[index - 1]) / (time_vector[index] - time_vector[index - 1]))
        index += 1
    acceleration = list_precision_controller(acceleration)
    return acceleration


def bit_generator_acceleration(acceleration, magnitude,lambda_v):
    bit_vector = []
    spike_counter = 0
    g = 9.80
    # lambda_v = 1
    if magnitude == 1:  # Positive spike_counter
        threshold = lambda_v * g * magnitude

        for i in acceleration:
            if i >= threshold:  # >9.8, so spike
                bit_vector.append(1)
                spike_counter += 1
            else:
                bit_vector.append(0)

        # print("+ve Spikes", spike_counter)
        return bit_vector, spike_counter

    else:
        threshold = lambda_v * g * magnitude

        for i in acceleration:
            if i <= threshold:  # <9.8, so spike
                bit_vector.append(1)
                spike_counter += 1
            else:
                bit_vector.append(0)

        # print("-ve Spikes", spike_counter)
        return bit_vector, spike_counter


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
        # print("Error at index {}. Should come here if some error has occured. last value is spike".format(index))

    if flag == 1:  # It means we did locate a point. So no issues
        pass
    else:  # It means we could not locate a previous point that conforms to the correlation threshold. So we need a global maxima
        next = universal_last_index

    # print(prev, next)
    return prev, next


def acceleration_fixer(velocity_i, bit_vector_velocity_i, universal_first_index,
                       universal_last_index):
    """This function uses the information obtained from the function bit_generator (bit array) and then fixes the values that are
    less than correlation threshold. It will update both the original velocity and the correlation value. At a given time, it
    works on a single velocity column."""

    flag=0
    index = 0
    backup_velocity_i = velocity_i
    new_vt = []  # To get the new velocity vector with fixed correlation values
    new_snr_velocity_i = []  # To get the new correlation vector with fixed correlation values
    for i in bit_vector_velocity_i:
        """i = 0 indicates that the bit_vector has 0 for this position. It indicates the correlation is above or equal to threshold.
        So we just ignore it and add to a new list """
        if i == 0:
            new_vt.append(velocity_i[index])
            # new_snr_velocity_i.append(round(correlation_velocity_i[index], decimal_granularity))
        # """Now there is a value that does not confirm to the coorelation values. So we need to fix it"""
        else:
            # print("Value of correlation {}. Issues with co-relation value".format(velocity_i[index]))

            prev, next = location_of_non_spikes(index, bit_vector_velocity_i, universal_first_index,
                                                universal_last_index)
            # print("The values of prev {} and next {}".format(prev, next))
            #
            # correlation_velocity_i[index] = round((correlation_velocity_i[prev] + correlation_velocity_i[next]) / 2,
            #                                       decimal_granularity)
            velocity_i[index] = ((velocity_i[prev] + velocity_i[next]) / 2)

            new_vt.append(velocity_i[index])
        index += 1

    new_vt = list_precision_controller(new_vt)
    # flag = checking_identical(new_vt,backup_velocity_i)
    # print("The value of flag is : {}".format(flag))
    return new_vt

