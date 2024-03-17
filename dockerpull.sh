#!/bin/bash

# This is a script to more intelligently perform docker pull between machines on a network for the purposes of reducing bandwidth to external, or non-local networks.

# Step 1: Figure out what other machines on the network support this new extension on existing docker functionality

# Step 2: check if any of those other machines have any of the same image layers as the ones we need for the current pull operation

# Step 3: If they do, download them from that local source instead 

# Step 4: fetch any remaining layers from docker hub

docker pull "$1"