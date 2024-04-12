from flask import Flask, jsonify
import docker
from requests.exceptions import HTTPError

app = Flask(__name__)
installed_image_ids_registry = []


def fetch_container_ids(client, installed_images):
	# Driver code to check above generator function 
	for i in installed_images:  
		if i.tags == []:
			print(f"no tag for image {i.id}")
			continue
		try:
			# TODO: this is slow
			regdata = client.images.get_registry_data(i.tags[0])
			yield regdata.image_name
		except HTTPError:
			print(f"http error fetching image {i.id}")
			continue

		

@app.route("/dockerpull")
def list_images():
	global installed_image_ids_registry
	# return JSON that identifies the server and lists the image/layer IDs it can send
	return jsonify({
		"dockerpull_version": "0",
		"images" : installed_image_ids_registry
	})

@app.route("/dockerpull/image/<id>")
def download(id):
	return "<p>Hello, World!</p>"

if __name__ == '__main__':

	client = docker.from_env()
	installed_images = client.images.list()
	# installed_image_ids = [i.id for i in installed_images]
	installed_image_ids_registry = list(fetch_container_ids(client, installed_images))

	app.run(debug=True, host="0.0.0.0", port=5000)