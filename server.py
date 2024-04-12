from flask import Flask, jsonify, request
import docker
from requests.exceptions import HTTPError
import time

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

@app.before_request
def log_before():
    print(f"request initiated for {request.url} at: {time.time()} ")

@app.after_request
def log_after(response):
	# print(resp)
	print(f"request completed for {request.url} at: {time.time()} ")
	return response



@app.route("/dockerpull")
def list_images():
	global installed_image_ids_registry
	# return JSON that identifies the server and lists the image/layer IDs it can send
	return jsonify({
		"dockerpull_version": "0",
		"images" : installed_image_ids_registry
	})

@app.route("/dockerpull/image/<identifier>")
def download(identifier):
	try:
		client = docker.from_env()
		image = client.images.get(identifier)
		print(image)

		# https://flask.palletsprojects.com/en/2.3.x/patterns/streaming/
		return app.response_class(image.save(), mimetype='application/x-tar')
	except docker.errors.ImageNotFound:
		return "Not found", 404

if __name__ == '__main__':

	client = docker.from_env()
	installed_images = client.images.list()
	# installed_image_ids = [i.id for i in installed_images]
	installed_image_ids_registry = [image.tags[0] if len(image.tags) > 0 else "" for image in installed_images]
	installed_image_ids_registry = list(filter(lambda d: d != "", installed_image_ids_registry))

	app.run(debug=True, host="0.0.0.0", port=5000)