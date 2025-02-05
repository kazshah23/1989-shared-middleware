from dotenv import load_dotenv
load_dotenv()

import requests
import time
import base64
import os
import uuid
from flask import Flask, jsonify, render_template, request

mg_ports = {}

app = Flask(__name__)

@app.route("/", methods=["GET"])
def GET_index():
    """Route for "/" (frontend)"""
    return render_template("index.html")


@app.route("/addMMG", methods=["PUT"])
def PUT_addMMG():
    """Add a mosaic microservice generator"""
    name = request.form["name"]
    url = request.form["url"]
    author = request.form["author"]

    mg_ports[name] = (url, author)
    print(f"Added {name}: {url} by {author}")
    return "Success :)", 200


@app.route("/makeMosaic", methods=["POST"])
def POST_makeMosaic():
    """Route to generate mosaic"""
    response = []
    try:
        start_time = time.time()
        print("Reading in base file")
        input_file = request.files["image"]
        image_data = input_file.read()

        for idx, (theme, mg_url) in enumerate(mg_ports.items(), 1):
            print(f"Generating {theme} mosiac ({idx}/{len(mg_ports)})")
            req = requests.post(
                f'{mg_url}?tilesAcross={request.form["tilesAcross"]}&renderedTileSize={request.form["renderedTileSize"]}',
                files={"image": image_data}
            )
            response += req.json()

        print(
            f"Spent {time.time() - start_time} seconds to generate {len(mg_ports)} images"
        )

    except KeyError as e:
        response.append({"error": "Please upload an image file."})
    except requests.exceptions.RequestException as e:
        response.append({"error": "Failed to connect to remote server."})
    except Exception as e:
        with open("static/favicon.png", "rb") as f:
            buffer = f.read()
            b64 = base64.b64encode(buffer)
            response.append({"image": "data:image/png;base64," + b64.decode("utf-8")})
      print(f"Generating {theme} mosaic ({idx}/{len(mg_ports)})")
      response += req.json()
  except requests.exceptions.ConnectionError:
    mg_ports.pop(theme)
    with open("static/favicon.png", "rb") as f:
        buffer = f.read()
        b64 = base64.b64encode(buffer)
        response.append({"image": "data:image/png;base64," + b64.decode("utf-8")})
  except:
    with open("static/favicon.png", "rb") as f:
        buffer = f.read()
        b64 = base64.b64encode(buffer)
        response.append({"image": "data:image/png;base64," + b64.decode("utf-8")})
    
  return jsonify(response)

@app.route("/serverList", methods=["GET"])
def GET_serverList():
  """Route to get connected servers"""
  return render_template("servers.html", data=mg_ports)
    