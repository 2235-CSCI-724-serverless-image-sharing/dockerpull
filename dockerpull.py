# This is a script to more intelligently perform docker pull between machines on a network for the purposes of reducing bandwidth to external, or non-local networks.
import grequests
import argparse
import docker

parser = argparse.ArgumentParser(
    prog='dockerpull',
    description='Intelligent version of docker pull'
    )
parser.add_argument('images', help="a space separated list of images to download")
parser.add_argument('-t', '--targets', help="a comma-separated list of IP addresses to use to shortcut the network discovery process")
parser.add_argument('-p', '--port', type=int, default=5000, help="the port number to use when querying the server")
# parser.add_argument('-d', '--background', action='store_true', help="Runs the server component of the program")

parser.add_argument('-v', '--verbose', action='store_true', help="Output more verbosely")
parser.add_argument('-b', '--benchmark', action='store_true', help="Whether or not to collect benchmark timing data for the run")


args = parser.parse_args()

# Normal client operation

client = docker.from_env()

requested_images = args.images.split(" ") #[client.images.get(image) for image in ]

installed_images = client.images.list()
# installed_images_text = [i.tags[0] if i.tags != [] else i.id for i in installed_images]
installed_image_ids = [i.id for i in installed_images]

# needed_images

# Step 1: Figure out what other machines on the network support this new extension on existing docker functionality
targets = args.targets.split(",")

if targets is None:
    # Step 1a: Figure out what other machines exist on the network
    targets = []

# Step 1b: Figure out which of those machines are advertising support for this dockerpull protocol by running the server

urls_to_check = [f"http://{ip}:{args.port}/" for ip in targets]
# Create a set of unsent Requests:
rs = (grequests.get(u) for u in urls_to_check)

results = grequests.map(rs)

clients = zip(urls_to_check, results)
active_clients = filter(lambda r: r[1] is not None and r[1].status_code == 200, clients)

active_clients = map(lambda r: (r[0], r[1].json()), active_clients)

dockerpull_clients = filter(lambda r: r[1].get("dockerpull_version") is not None, active_clients)

images_by_client = map(lambda r: (r[0], set(r[1].get("images"))), dockerpull_clients)
images_by_client = list(images_by_client)

# Step 2: check if any of those other machines have any of the same image layers as the ones we need for the current pull operation

# Gets the registry data for an image.

registrydata = [client.images.get_registry_data(name) for name in requested_images]
requested_image_ids = set([d.id for d in registrydata])

clients_containing_image = filter(lambda c: len(requested_image_ids.intersection(c[1])) > 0, images_by_client)
clients_containing_image = list(clients_containing_image)

# Step 3: If they do, download them from that local source instead 

# Step 4: fetch any remaining layers from docker hub
client.images.pull(args.images)