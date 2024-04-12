# This is a script to more intelligently perform docker pull between machines on a network for the purposes of reducing bandwidth to external, or non-local networks.
import grequests
import requests
import argparse
import docker
import ipaddress
import tempfile

parser = argparse.ArgumentParser(
    prog='dockerpull',
    description='Intelligent version of docker pull'
    )
parser.add_argument('images', help="a space separated list of images to download")
parser.add_argument('-t', '--targets', help="a comma-separated list of IP addresses, or a single address in CIDR notation denoting the network to use to shortcut the network discovery process")
parser.add_argument('-p', '--port', type=int, default=5000, help="the port number to use when querying the server")
# parser.add_argument('-d', '--background', action='store_true', help="Runs the server component of the program")

parser.add_argument('-v', '--verbose', action='store_true', help="Output more verbosely")
parser.add_argument('-b', '--benchmark', action='store_true', help="Whether or not to collect benchmark timing data for the run")


args = parser.parse_args()

# Normal client operation

client = docker.from_env()

requested_images = args.images.split(" ") #[client.images.get(image) for image in ]

print(f"Requested Docker Images: {requested_images}")
installed_images = client.images.list()
# installed_images_text = [i.tags[0] if i.tags != [] else i.id for i in installed_images]
installed_image_ids = [i.id for i in installed_images]

# needed_images

# Step 1: Figure out what other machines on the network support this new extension on existing docker functionality
if " " in args.targets:
    print("Spaces arent allowed in IP targets argument. please specify a comma,separated list of IP addresses, or a network ID in CIDR notation")
elif "," in args.targets:
    # this is a list of IPs
    targets = args.targets.split(",")
elif "/" in args.targets:
    # this is liekly a CIDR IP
    print("detecting hosts from network CIDR IP")
    net = ipaddress.ip_network(args.targets)
    
    targets = [str(h) for h in net.hosts()]
else:
    # single IP address
    targets=[args.targets]

# Step 1b: Figure out which of those machines are advertising support for this dockerpull protocol by running the server

print(f"{len(targets)} target IPs to check")
urls_to_check = [f"http://{ip}:{args.port}/dockerpull" for ip in targets]
# Create a set of unsent Requests:
rs = (grequests.get(u) for u in urls_to_check)

results = grequests.map(rs)

clients = zip(urls_to_check, results)
# clients = list(clients)

# print(clients)


active_clients = filter(lambda r: r[1] is not None and r[1].status_code == 200, clients)
# print(list(active_clients))

active_clients = map(lambda r: (r[0], r[1].json()), active_clients)

dockerpull_clients = filter(lambda r: r[1].get("dockerpull_version") is not None, active_clients)

images_by_client = map(lambda r: (r[0], set(r[1].get("images"))), dockerpull_clients)
images_by_client = list(images_by_client)
print(images_by_client)
# print(images_by_client)


# Step 2: check if any of those other machines have any of the same image layers as the ones we need for the current pull operation

# TODO: filter the requested images list to things we dont already have

# Gets the registry data for an image.

# registrydata = [client.images.get_registry_data(name) for name in requested_images]
requested_image_ids = requested_images#[d.image_name for d in registrydata]

def id_to_name(image_id):
    return requested_images[requested_image_ids.index(image_id)]

remote_source_map = list(zip(requested_image_ids, [None]*len(requested_image_ids)))
remote_source_map = {remote_source_map[i][0]: remote_source_map[i][1] for i in range(0, len(remote_source_map))}

for image, sources in remote_source_map.items():
    clients_containing_image = filter(lambda c: len(set([image]).intersection(c[1])) > 0, images_by_client)
    clients_containing_image = map(lambda r: r[0], clients_containing_image)

    if sources is not None:
        existing_values = sources
        existing_values.append(clients_containing_image)
        existing_values = list(set(existing_values))
        remote_source_map[image] = list(existing_values)
    else: 
        remote_source_map[image] = list(clients_containing_image)

print(remote_source_map)
# Step 3: If they do, download them from that local source instead 
local_download = {k: v for k, v in remote_source_map.items() if len(v) > 0}
docker_download = [id_to_name(k) for k, v in remote_source_map.items() if len(v) == 0]


for image, sources in local_download.items():
    # TODO: set up concurrent remote downloads from the sources
    print(image)
    with tempfile.TemporaryFile() as tmp:
        with requests.get(f"{sources[0]}/image/{image}", stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                tmp.write(chunk)
        tmp.seek(0)
        f = client.images.load(tmp.read())
        print(f)

for image in docker_download:
# Step 4: fetch any remaining images from docker hub
    print(f"Pulling image for {image}...")
    client.images.pull(image)