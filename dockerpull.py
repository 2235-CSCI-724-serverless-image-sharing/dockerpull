
import argparse

parser = argparse.ArgumentParser(
    prog='dockerpull',
    description='Intelligent version of docker pull'
    )
parser.add_argument('image')
# parser.add_argument('-c', '--count')      # option that takes a value
# parser.add_argument('-d', '--background', action='store_true', help="Runs the server component of the program")

parser.add_argument('-v', '--verbose', action='store_true', help="Output more verbosely")
parser.add_argument('-b', '--benchmark', action='store_true', help="Whether or not to collect benchmark timing data for the run")


args = parser.parse_args()

# Normal client operation

