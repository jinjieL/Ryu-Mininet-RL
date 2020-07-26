
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, Intf, TCLink, OVSLink
from mininet.topo import Topo
from mininet.log import output


import logging
import os
import time
from subprocess import Popen
from multiprocessing import Process


class MyTopo(Topo):


    HostList = []

    def __init__(self):
        # Init Topo
        Topo.__init__(self)
        "Create custom topo."


        # Add hosts and switches
        # Add hosts and switches
        self.h1 = self.addHost( 'h1' )
        self.h2 = self.addHost( 'h2' )
        self.h3 = self.addHost( 'h3' )
        self.h4 = self.addHost( 'h4' )
        # self.h5 = self.addHost( 'h5' )
        # self.h6 = self.addHost( 'h6' )
        self.s1 = self.addSwitch( 's1' )
        self.s2 = self.addSwitch( 's2' )
        self.s3 = self.addSwitch('s3')
        self.s4 = self.addSwitch('s4')

        # Add links
        self.addLink(self.h1, self.s1)
        self.addLink(self.h2, self.s1)
        self.addLink(self.h3, self.s2)
        self.addLink(self.h4, self.s2)
        self.addLink(self.s1, self.s3)
        self.addLink(self.s1, self.s4)
        self.addLink(self.s2, self.s3)
        self.addLink(self.s2, self.s4)


        # self.addLink(self.h3, self.s1, bw=1000, max_queue_size=1000)
        # self.addLink(self.h4, self.s1, bw=1000, max_queue_size=1000)


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
    access_table = {}
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
                    access_table[(dpid_port[0],dpid_port[1].replace('eth', ''))] = HostNameIPMAC[node.name]
    return access_table



def main():
    CONTROLLER_IP = "127.0.0.1"
    CONTROLLER_PORT = 6653

    topo = MyTopo()
    net = Mininet(topo=topo, link=Link, switch=OVSSwitch, host=Host, controller=None, autoSetMacs=True)
    # add Controller
    net.addController(
        'controller', controller=RemoteController,
        ip=CONTROLLER_IP, port=CONTROLLER_PORT)
    net.start()


    HostList, HostIPList, HostNameIPMAC = makeHostList(net)
    # print HostNameIP

    Access_table = makeAccess_table(net, HostNameIPMAC)
    # print Access_table


    CLI(net)
    net.stop()




if __name__ == '__main__':
    os.system('sudo ovs-vsctl --all destroy qos')
    os.system('sudo ovs-vsctl --all destroy queue')
    os.system('sudo mn -c')
    setLogLevel('info')
    if os.getuid() != 0:
        logging.debug("You are NOT root")
    elif os.getuid() == 0:
        main()


