import threading
import random

import argparse

class DockerHub:
    def __init__(self):
        self.counts = {}
        
    def get(self, key):
        if key in self.counts:
            self.counts[key] += 1
        else:
            self.counts[key] = 1
        return True

    def bandwidth_by_workload(self, bytes_per_workload={}, format=None):
        bandwidth_per_workload = {}
        for key,value in self.counts.items():
            bandwidth = bytes_per_workload.get(key,0)
            if format is not None:
                bandwidth_per_workload[key] = format(bandwidth*value)
            else:
                bandwidth_per_workload[key] = bandwidth*value
        return bandwidth_per_workload


class Node:

    @property
    def name(self):
        return f"node{self.id:04d}"

    def __init__(self, unique_id, all_nodes=None):
        # all_nodes is a list of other nodes in the system it if is a list of other node objects, then fetching from other nodes is allowed
        self.id = unique_id
        self.images = []
        self.nodelist = all_nodes
    
    def __str__(self):
        variables = dict(vars(self))
        del variables["nodelist"]
        return str(variables)

    def lookup(self):
        # Return the list of images stored in this Node
        return self.images

    def run(self, workload):
        # 'work_manager' is a list of image names to pull
        for image in workload:
            if image not in self.images:
                
                if self.nodelist is not None:
                    tmplist = list(self.nodelist)
                    tmplist = filter(lambda n: n.id != self.id, tmplist)
                    tmplist = filter(lambda n: workload in n.lookup(), tmplist)
                    tmplist = list(tmplist)
                    # if some other node has it, fetch from it, else fetch from docker hub
                    if len(tmplist) > 0:
                        selected_node = tmplist[0]
                        # pretend we did a local fetch here
                        self.images.append(image)
                    else:
                        # fetch from docker hub
                        docker_hub.get(image)  # Increment the count for this image in DockerHub
                        self.images.append(image)
                else:
                    # fetch from docker hub
                    docker_hub.get(image)  # Increment the count for this image in DockerHub
                    self.images.append(image)

# http://stackoverflow.com/questions/1094841/ddg#1094933
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

MB = 1024*1024 

workloads = {
    'ubuntu:20.04': 63.2*MB,
    # 'nginx': 0,
    # 'node:bullseye': 0,
    'maven:3.6.1-jdk-8': 499*MB,
    'python:3.10': 1024*MB,
}
workload_names = workloads.keys()

parser = argparse.ArgumentParser(description='Simulate docker stuff.')
parser.add_argument('--ipw', type=int, default=5, help='number of instances for each workload')
parser.add_argument('--internode', action="store_true", help='whether to allow cross-node fetching')
parser.add_argument('--nodes', type=int, default = 100, help='how many nodes to use')
parser.add_argument('--stats', action="store_true", help='whether to print stats of the run')
parser.add_argument('--verbose', action="store_true", help='whether to print stats of the run')



args = parser.parse_args()



# docker hub simulation to track downloads
docker_hub = DockerHub()

# Creating 100 Node objects
nodes = []
if args.internode:
    for i in range(1, args.nodes):
        nodes.append(Node(i, all_nodes=nodes))
else:
    nodes = [Node(i) for i in range(1, args.nodes)]

for workload in workload_names:
    for i in range(args.ipw):
        random_node = random.choice(nodes)
        print(f"starting workload {workload} on node {random_node.name}")
        random_node.run([workload])


if args.stats:

    # Check the lookup for node1 and node5
    # print(nodes[0].lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs']
    # print(nodes[4].lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs']
    if args.verbose:
        for node in nodes:
            print(node)
        
        
    # Checking updated DockerHub counts after running multiple nodes
    print(docker_hub.counts)  # This will show updated counts reflecting multiple pulls by different nodes

    print(docker_hub.bandwidth_by_workload(workloads, format=sizeof_fmt))
