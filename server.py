from flask import Flask, jsonify
import docker

app = Flask(__name__)

@app.route("/dockerpull")
def list_images():
	client = docker.from_env()
	installed_images = client.images.list()
	installed_image_ids = [i.id for i in installed_images]
	installed_images_text = [i.tags[0] if i.tags != [] else i.id for i in installed_images]

	registrydata = [client.images.get_registry_data(name) for name in installed_images_text]
	installed_image_ids_registry = [d.id for d in registrydata]
	# return JSON that identifies the server and lists the image/layer IDs it can send
	return jsonify({
		"dockerpull_version": "0",
		"images" : installed_image_ids_registry
	})

@app.route("/dockerpull/image/<id>")
def download(id):
	return "<p>Hello, World!</p>"

if __name__ == '__main__':

	app.run(debug=True, host="0.0.0.0", port=5000)