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
                    # if some other node has it, fetch from it, else fetch from docker hub
                    pass
                else:
                    # fetch from docker hub
                    docker_hub.get(image)  # Increment the count for this image in DockerHub
                    self.images.append(image)


def status_update(nodes):
    for node in nodes:
        print(node)



# Example usage of a single node:
docker_hub = DockerHub()
workloads = ['ubuntu', 'nginx', 'nodejs','python-10.0']
# node.run(work_manager)
# print(node.lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs', 'python-10.0']
# print(docker_hub.counts)  # Outputs the dictionary with counts

allow_cross_node_fetching = True


# Creating 100 Node objects
nodes = []
if allow_cross_node_fetching:
    for i in range(1, 101):
        nodes.append(Node(i, all_nodes=nodes))

else:
    nodes = [Node(i) for i in range(1, 101)]

instances_per_workload = 5

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

# Randomly selecting a node and searching for a specific image
search_image = 'nginx'
random_node = random.choice(nodes)
if search_image in random_node.lookup():
    print(f"Image '{search_image}' found in Node {random_node.id}")
else:
    print(f"Image '{search_image}' not found in Node {random_node.id}")
