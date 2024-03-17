from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def list_images():
	# return JSON that identifies the server and lists the image/layer IDs it can send
    return jsonify({
		"dockerpull_version": "0",
		"images" : []
	})

@app.route("/image/<id>")
def download(id):
    return "<p>Hello, World!</p>"

if __name__ == '__main__':

    app.run(debug=True, port=5000)