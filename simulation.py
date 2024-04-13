import threading
import random

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


def status_update(nodes):
    for node in nodes:
        print(node)

workloads = ['ubuntu', 'nginx', 'nodejs','python-10.0']
# node.run(work_manager)
# print(node.lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs', 'python-10.0']
# print(docker_hub.counts)  # Outputs the dictionary with counts

allow_cross_node_fetching = True
instances_per_workload = 5

# docker hub simulation to track downloads
docker_hub = DockerHub()

# Creating 100 Node objects
nodes = []
if allow_cross_node_fetching:
    for i in range(1, 101):
        nodes.append(Node(i, all_nodes=nodes))
else:
    nodes = [Node(i) for i in range(1, 101)]

# Running the first five nodes with some image pulls
for workload in workloads:
    for i in range(instances_per_workload):
        random_node = random.choice(nodes)
        print(f"starting workload {workload} on node {random_node.name}")
        random_node.run([workload])

# Check the lookup for node1 and node5
# print(nodes[0].lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs']
# print(nodes[4].lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs']
status_update(nodes)
# Checking updated DockerHub counts after running multiple nodes
print(docker_hub.counts)  # This will show updated counts reflecting multiple pulls by different nodes

