from urllib.parse import urlencode

from application import app
from flask import render_template, request, json, redirect
import pycountry
from application import spotify_controller


@app.route("/")
def index():
    # Get data from db
    auth_headers = spotify_controller.get_auth_token()
    return redirect("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))


@app.route("/callback")
def callback():
    response = spotify_controller.fetch_access_token(request.args.get("code"))
    app.config.update({"access_token": json.loads(response.decode('utf-8'))["access_token"]})
    return render_template("index.html", callback=True, login=False, countries=pycountry.countries)


@app.route("/fetch", methods=["POST"])
def fetch():
    artist = request.form["artist"]
    country = request.form["country"]
    artist_id = spotify_controller.fetch_artist_id(artist)
    tracks = spotify_controller.fetch_tracks(artist_id, country)
    decoded_tracks = json.loads(tracks.decode('utf-8'))
    return render_template("fetch.html", callback=False, login=True, countries=pycountry.countries, tracks=decoded_tracks["tracks"][:10])