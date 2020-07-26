# -*- coding: utf-8 -*-
'''
generate the traffic trace

#Trace format: <flow_id, time_interval, flow_size(KB), flow_type, src, dst>

'''

import os
import sys
import string
import time
import random
import math
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from time import sleep, time


# parser = ArgumentParser(description="This script is used to generate flow workloads for mixedflow project")
# parser.add_argument('--CDF', '-c',
#             help="Directory to store outputs",
#             default="outputs/")
# parser.add_argument('--traffic', '-t',
#             help="Type of traffic, use: 'web' or 'data'",
#             required=True)
# parser.add_argument('--cong','-c',
#             help="Type of congestion control, use: 'tcp', 'mintcp', or 'none'(udp)",
#             required=True)
# parser.add_argument('--kary', '-k',
#             help="Size of K for fat tree topology, default = 3",
#             type=int,
#             default=3)
# parser.add_argument('--hosts', '-n',
#             help="Number of hosts to use for star topology, default = 54",
#             type=int,
#             default=54)
# parser.add_argument('--time',
#             help="Time for each sender to send flows",
#             type=int,
#             default=180)
# parser.add_argument('--topo',
#             help="Type of topology to use for network: 'star' or 'fattree', default = star",
#             default="star")
#
# args = parser.parse_args()
#
# if args.cong not in ['tcp', 'mintcp', 'none']:
#     parser.error('Wrong congestion method, use: tcp, mintcp, or none')
# if args.traffic not in ['web','data']:
#     parser.error('Wrong traffic type, use: web or data')
# if args.kary < 1 or args.kary > 3:
#     parser.error('Value of k must be between 1 and 3')
# if args.hosts < 1:
#     parser.error('Number of hosts must be at least 1')
# if args.time < 60:
#     parser.error('Runtime too short')
# if args.topo not in ['star','fattree']:
#     parser.error('Wrong network topology, use: star or fattree')



#This function is to print usage of this script
def usage():
    sys.stderr.write('This script is used to generate dynamic flow workloads for mixedflow project:\n')
    sys.stderr.write('generator.py [CDF file] [load] [link capacity (Mbps)] [flow number] [host number] [output file]\n')



# """ This function is taken from http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/ """
def weightedChoice(flowWeights):
    totals = []
    runningTotal = 0

    for w in flowWeights:
        runningTotal += w
        totals.append(runningTotal)

    rnd = random.random() * runningTotal
    for i, total in enumerate(totals):
        if rnd < total:
            return i

def randomSize(flowSizes,flowWeights):
    index = weightedChoice(flowWeights)
    flowsize = flowSizes[index]
    if flowsize <= 7:
        flowtype = 1
    else:
        flowtype = random.randint(2,3)
    return [flowsize, flowtype]


#http://preshing.com/20111007/how-to-generate-random-timings-for-a-poisson-process/
#Return next time interval (ms)
def nextTime(rateParameter):
    #We use round function to get a integer
    return round(-math.log(1.0 - random.random()) / rateParameter)


def main():
    # main function
    if len(sys.argv) != 7:
        usage()
    else:
        cdf_filename=sys.argv[1]
        load = float(sys.argv[2])
        capacity = float(sys.argv[3])
        flow_num = int(sys.argv[4])
        host_num = int(sys.argv[5])
        output_filename = sys.argv[6]

        # print(cdf_filename,load,capacity,flow_num,host_num,output_filename)

        flowCDF = []
        with open(cdf_filename, 'r') as f:
            for l in f.readlines():
                flowCDF.append(([float(i) for i in str.split(l)]))
        flowType = cdf_filename.split('.')[0]
        # print(flowType)
        # print(flowCDF)

        flowSizes= []
        flowWeights = []
        prev = 0
        for size in flowCDF:
            flowSizes.append(int(size[0]))
            flowWeights.append(size[2] - prev)
            prev = size[2]
        # print(flowSizes)
        # print(flowWeights)

        flows = []
        for i in range(flow_num):
            flows.append(randomSize(flowSizes,flowWeights))
        # print(flows)

        # num=0
        # for s, i in flows:
        #     if s == 666667:
        #         num +=1
        # print(num)
        # print(num/flow_num)


        # Get average throughput
        throughput = load * capacity
        # Get average flow size
        total_size = 0
        for flow in flows:
            total_size += flow[0]
        avg = total_size / len(flows)

        # Get average number of requests per second
        num = throughput * 1024 * 1024 / (avg * 1024 * 8)
        # Get average request rate (number of requests every 1 ms)
        rate = num / 1000
        # print(rate)

        hostlist = range(1, host_num+1)

        # Generate time interval
        times = []
        for i in range(flow_num):
            # Get time interval (sleep time)
            times.append(nextTime(rate))

        # Write trace results into output file
        # Trace format: <time_interval, flow_size(KB), flow_type, deadline(ms), src, dst>
        output_file = open(output_filename, 'w')

        for i in range(flow_num):
            flow_size = flows[i][0]
            flow_type = flows[i][1]

            # choose src and dit randomly
            hostslice = random.sample(hostlist, 2)  # 从list中随机获取5个元素，作为一个片断返回
            host_src = hostslice[0]
            host_dst = hostslice[1]
            dsport = random.randint(49152, 65535)

            deadline = 0
            # Type 1 flows
            if flow_type == 1:
                # Calculate ideal FCT (ms)
                ideal_fct = 0.2 + flow_size * 8 * 1024 / (capacity * 1024 * 1024) * 1000
                # Deadline is assigned to
                deadline = int(math.ceil(2 * ideal_fct))
            output_file.write(str(times[i]) + ' ' + str(flow_size) + ' ' + str(flow_type) + ' ' +
                              str(deadline) + ' ' + str(host_src) + ' ' + str(host_dst) + ' ' + str(dsport) +'\n')

        output_file.close()

        print('Auto generate ' + str(len(flows)) + ' flows:')
        print('The total flow size: ' + str(total_size) + 'KB')
        print('The average flow size: ' + str(avg) + ' KB')
        print('The average request speed: ' + str(num) + ' requests/second')
        print('Dynamic flow emulation will last for about ' + str(len(flows) / num) + ' mseconds')
        print('Done')



if __name__ == '__main__':
    main()

