# This is a script to more intelligently perform docker pull between machines on a network for the purposes of reducing bandwidth to external, or non-local networks.
import argparse
import docker

parser = argparse.ArgumentParser(
    prog='dockerpull',
    description='Intelligent version of docker pull'
    )
parser.add_argument('images')
parser.add_argument('-t', '--targets', help="a comma-separated list of IP addresses to use to shortcut the network discovery process")
parser.add_argument('-p', '--port', type=int, default=5000, help="the port number to use when querying the server")
# parser.add_argument('-d', '--background', action='store_true', help="Runs the server component of the program")

parser.add_argument('-v', '--verbose', action='store_true', help="Output more verbosely")
parser.add_argument('-b', '--benchmark', action='store_true', help="Whether or not to collect benchmark timing data for the run")


args = parser.parse_args()

# Normal client operation

client = docker.from_env()

# Step 1: Figure out what other machines on the network support this new extension on existing docker functionality

# Step 2: check if any of those other machines have any of the same image layers as the ones we need for the current pull operation

# Step 3: If they do, download them from that local source instead 

# Step 4: fetch any remaining layers from docker hub
client.images.pull(args.images)