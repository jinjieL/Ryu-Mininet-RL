# -*- coding: utf-8 -*-

import requests
import numpy as np
import json
import networkx as nx
import matplotlib.pyplot as plt


link_to_port = {}  # {(src_dpid,dst_dpid):(src_port,dst_port),}
access_table = {}  # {(sw,port):(ip, mac),} MAC地址表
switch_port_table = {}  # {dpid:set(port_num,),}
access_ports = {}  # {dpid:set(port_num,),}
interior_ports = {}  # {dpid:set(port_num,),}
switches = []  # self.switches = [dpid,]
shortest_paths = {}  # {dpid:{dpid:[[path],],},}
graph = nx.DiGraph()		# 创建有向图


##########################################
# 交换机id、端口信息
##########################################
url1 = 'http://localhost:8080/v1.0/topology/switches'
r1 = requests.get(url1)
# print(r1.encoding)
# r1.encoding = 'utf-8'
switchs_list = r1.json()
print switchs_list

for sw in switchs_list:
    id = int(str(sw['dpid']).lstrip("0"), 16)
    # print id
    switches.append(id)

    switch_port_table.setdefault(id, {})
    # switch_port_table is equal to interior_ports plus access_ports.
    # interior_ports.setdefault(dpid, {})
    # access_ports.setdefault(dpid, {})
    switch_port_table[id]['port'] = {}
    for port in sw['ports']:

        # print port
        port_no = str(port['port_no']).lstrip("0")
        # switch_port_table[dpid]['port'].setdefault(port_no, str(port['name']))
        switch_port_table[id]['port'][port_no] = str(port['name'])

    switch_port_table[id]['dpid'] = str(sw['dpid'])

print switch_port_table
print switches
# [1, 2, 3, 4]


#######################################
# 建立链路信息
#######################################
url = 'http://localhost:8080/v1.0/topology/links'
r = requests.get(url)
link_list = r.json()
# print len(link_list)

for link in link_list:
    # print link
    src_id = int(str(link['src']['dpid']).lstrip('0'), 16)
    src_port = int(str(link['src']['port_no']).lstrip('0'))
    dst_id = int(str(link['dst']['dpid']).lstrip('0'), 16)
    dst_port = int(str(link['dst']['port_no']).lstrip('0'))
    # print src_id,dst_id
    # print src_port,dst_port
    link_to_port[(src_id, dst_id)] = (src_port, dst_port)
# print link_to_port



#######################################
# 建立有向图
#######################################

def get_graph(link_list):
    """
    	Get Adjacency matrix from link_to_port.
    """
    _graph = graph.copy()
    for src in switches:
        for dst in switches:
            if src == dst:
                _graph.add_edge(src, dst, weight=0)
            elif (src, dst) in link_list:
                _graph.add_edge(src, dst, weight=1)
            else:
                pass
    return _graph


graph = get_graph(link_to_port.keys())
# nx.draw(graph, with_labels=True)
# plt.show()
# print('All the nodes in the figure: ', graph.nodes())
# print('The number of nodes in the figure:', graph.number_of_nodes())
# print('All the edges in the figure:', graph.edges())
# print('The number of edges in the figure:', graph.number_of_edges())


#################################
# 所有端点的k-path
#################################
def k_shortest_paths(graph, src, dst, weight='weight', k=5):
    """
        Creat K shortest paths from src to dst.
        generator produces lists of simple paths, in order from shortest to longest.
        创建从src到dst的K个最短路径。
        生成器按照从最短到最长的顺序生成简单路径列表。
    """
    generator = nx.shortest_simple_paths(graph, source=src, target=dst, weight=weight)
    shortest_paths = []
    try:
        for path in generator:
            if k <= 0:
                break
            shortest_paths.append(path)
            k -= 1
        return shortest_paths
    except:
        print ("No path between %s and %s" % (src, dst))

def all_k_shortest_paths(graph, weight='weight', k=5):
    """
    	Creat all K shortest paths between datapaths.
    	Note: We get shortest paths for bandwidth-sensitive
    	traffic from bandwidth-sensitive switches.
    	在数据路径之间创建所有K个最短路径。
    	注意：我们从带宽敏感交换机为带宽敏感流量获得最短路径。
    """
    _graph = graph.copy()
    paths = {}
    # Find k shortest paths in graph.
    for src in _graph.nodes():
        paths.setdefault(src, {src: [[src] for i in xrange(k)]})
        for dst in _graph.nodes():
            if src == dst:
                continue
            paths[src].setdefault(dst, [])
            paths[src][dst] = k_shortest_paths(_graph, src, dst, weight=weight, k=k)
    return paths


shortest_paths = all_k_shortest_paths(graph, weight='weight', k=2)
print(shortest_paths[1][2])



#######################################
# 接入ovsdb
#######################################
print switches
for i in switches:
    # print i
    url = 'http://127.0.0.1:8080/v1.0/conf/switches/000000000000000%d/ovsdb_addr'%(i)
    # print url
    payload = json.dumps("tcp:127.0.0.1:6632")
    r = requests.put(url,data=payload)



# url = 'http://localhost:8080/qos/queue/0000000000000002'
# param = {
# 	"port_name": "s2-eth1",
#     "type": "linux-htb",
#     "max_rate": "100000000",
#     "queues":
#         [
# 	        {"max_rate": "100000000"},
# 	        {"min_rate": "200000"},
# 	    	{"min_rate": "50000000"}
#         ]
# }
# payload = json.dumps(param)
# r = requests.post(url,data=payload)

