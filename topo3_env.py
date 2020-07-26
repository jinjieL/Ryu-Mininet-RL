# -*- coding: utf-8 -*-
import numpy as np
import copy
import collections as col

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, Intf, TCLink, OVSLink
from mininet.topo import Topo

from topo3_rest_env import NetworkEnvRestAPI
import logging
import time
import os
from subprocess import Popen
from multiprocessing import Process
import pandas as pd


class MyTopo(Topo):
    """
    	Class of Topology.
    	h1-e0------e1-------->s1<-----e2------e0-h2
    """
    def __init__(self):
        # Init Topo
        Topo.__init__(self)

        # Add hosts and switches
        self.h1 = self.addHost( 'h1' )
        self.h2 = self.addHost( 'h2' )

        self.s1 = self.addSwitch( 's1' )

        # Add links
        self.addLink(self.h1, self.s1)
        self.addLink(self.h2, self.s1)

def makeHostList(net):
    HostIPList = []
    HostList = []
    HostNameIPMAC = {}
    # print net.keys()
    for hostStr in net.keys():
        if "h" in hostStr:
            host = net.get(hostStr)
            HostList.append(host)
            HostIPList.append(host.IP())
            HostNameIPMAC[hostStr] = (host.IP(), host.MAC())
    return HostList, HostIPList, HostNameIPMAC

def makeAccess_table(net, HostNameIPMAC):
    Access_table = {}
    nodes = net.values()
    for node in nodes:
        if "h" in node.name:
            # print node.name
            # print node.intfList()
            for intf in node.intfList():
                # print (' %s:' % intf)
                if intf.link:
                    # print intf.link
                    intfs = [intf.link.intf1, intf.link.intf2]
                    intfs.remove(intf)
                    dpid_port = str(intfs[0]).split('-')
                    Access_table[(dpid_port[0],dpid_port[1].replace('eth', ''))] = HostNameIPMAC[node.name]
    return Access_table

def run_ryu_rest():
    print 'ok'
    time.sleep(1)
    proc = Popen("ryu-manager rest_conf_switch.py rest_topology.py rest_qos.py ofctl_rest.py --observe-links", shell=True)
    # proc.wait()
    time.sleep(2)

class NetworkEnv(object):
    def __init__(self):


        self.CONTROLLER_IP = "127.0.0.1"
        self.CONTROLLER_PORT = 6653
        self.state_dim = 500
        self.action_dim = 27

        self.HostList  = []
        self.HostIPList = []

        self.FCT = 0
        self.DMR = 0

    def reset(self):
        os.system('sudo mn -c')
        os.system('sudo ovs-vsctl --all destroy qos')
        os.system('sudo ovs-vsctl --all destroy queue')

        topo = MyTopo()
        net = Mininet(topo=topo, link=Link, switch=OVSSwitch, controller=None, autoSetMacs=True)
        # add Controller
        net.addController(
            'controller', controller=RemoteController,
            ip=self.CONTROLLER_IP, port=self.CONTROLLER_PORT)
        net.start()

        self.HostList, self.HostIPList, self.HostNameIPMAC = makeHostList(net)

        self.Access_table = makeAccess_table(net, self.HostNameIPMAC)

        # CLI(net)
        # net.stop()

        p = Process(target=run_ryu_rest())
        p.start()
        p.join()

    def step(self,action):
        pass

    def get_state(self):
        headers = ['src', 'dst','flowtype', 'flowsize', 'FCT', 'meetrate']

        flownum = 100

        # data = pd.read_csv('1.csv', header=None)
        while True:
            data = pd.read_csv('1.csv',header=None)
            if data.shape[0] == flownum:
                break
        data.columns = headers

        # print data.groupby(['flowtype']).size()[1]
        MFnum = len(data[data.flowtype==1])
        MFmeetratenum = len(data[data.meetrate==True])
        data["Tput"] = data["flowsize"] / (data["FCT"] * 1000)


        self.FCT = data.FCT.sum()
        self.DMR = 1 - float(MFmeetratenum)/MFnum


        # Min-Max Normalization
        data_norm = (data - data.min()) / (data.max() - data.min())
        

        # data_norm.to_csv("2.csv", mode='w')
        # print data_norm

    def get_reward(self):
        pass

    def generate_trace(self):
        pass

    def initial_RandomAction(self):
        pass

    def read_trace(self):
        filename = 'result_gen500.txt'
        self.trace = []
        with open(filename, 'r') as f:
            for l in f.readlines():
                self.trace.append(([int(i) for i in str.split(l)]))
        # print(self.trace)

    def test_trace(self):
        for i, flow in enumerate(self.trace):
            time_interval = flow[0]  # (ms)
            time.sleep(time_interval / 1000)
            # time_interval_all += time_interval
            # print(time_interval)
            size = flow[1]
            # size_all += flow[1]

            type = flow[2]
            deadline = flow[3]
            src = self.HostList[flow[4] - 1]
            dst = self.HostList[flow[5] - 1]
            # print src.IP(),dst.IP()
            dsport = flow[6]

            s1 = time.time()
            dst.popen("python Mys2.py {}".format(dsport), shell=False)
            src.popen("python Myc2.py {} {} {}".format(dst.IP(), dsport, size), shell=False)




max_episode = 1000
max_step = 1000


env = NetworkEnv()
# envrest= NetworkEnvRestAPI()
# env.reset()
# s_dim = env.state_dim
# a_dim = env.action_dim

env.get_state()





