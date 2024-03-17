
from flask import Flask
import argparse

app = Flask(__name__)

@app.route("/")
def list_images():
    return "<p>Hello, World!</p>"

@app.route("/image/<id>")
def download(id):
    return "<p>Hello, World!</p>"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='dockerpull',
        description='Intelligent version of docker pull'
        )
    # parser.add_argument('filename')           # positional argument
    # parser.add_argument('-c', '--count')      # option that takes a value
    parser.add_argument('-d', '--background', action='store_true', help="Runs the server component of the program")

    parser.add_argument('-v', '--verbose', action='store_true', help="Output more verbosely")
    parser.add_argument('-b', '--benchmark', action='store_true', help="Whether or not to collect benchmark timing data for the run")


    args = parser.parse_args()


    app.run(debug=True, port=5000)

