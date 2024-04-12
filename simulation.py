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
    def __init__(self, unique_id, other_nodes=None):
        # other_nodes is a list of other nodes in the system it if is a list of other node objects, then fetching from other nodes is allowed
        self.id = unique_id
        self.images = []
        self.nodelist = other_nodes

    def lookup(self):
        # Return the list of images stored in this Node
        return self.images

    def run(self, work_manager):
        # 'work_manager' is a list of image names to pull
        for image in work_manager:
            if image not in self.images:
                self.images.append(image)
                docker_hub.get(image)  # Increment the count for this image in DockerHub

# Example usage of a single node:
docker_hub = DockerHub()
node = Node(0)
work_manager = ['ubuntu', 'nginx', 'nodejs','python-10.0']
node.run(work_manager)
print(node.lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs', 'python-10.0']
print(docker_hub.counts)  # Outputs the dictionary with counts

# Creating 100 Node objects
nodes = [Node(i) for i in range(1, 101)]

# Running the first five nodes with some image pulls
for i in range(5):
    nodes[i].run(['ubuntu', 'nginx', 'nodejs'])

# Check the lookup for node1 and node5
# print(nodes[0].lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs']
# print(nodes[4].lookup())  # Outputs: ['ubuntu', 'nginx', 'nodejs']

# Checking updated DockerHub counts after running multiple nodes
print(docker_hub.counts)  # This will show updated counts reflecting multiple pulls by different nodes

# Randomly selecting a node and searching for a specific image
search_image = 'nginx'
random_node = random.choice(nodes)
if search_image in random_node.lookup():
    print(f"Image '{search_image}' found in Node {random_node.id}")
else:
    print(f"Image '{search_image}' not found in Node {random_node.id}")
