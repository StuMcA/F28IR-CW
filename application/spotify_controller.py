import base64
import webbrowser
from urllib.parse import urlencode

from application import app
import requests


def get_auth_token():
    client_id = app.config["client_id"]

    return {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:5000/callback",
        "scope": "user-library-read"
    }


def fetch_access_token(code):
    auth_url = app.config["auth_url"]
    client_id = app.config["client_id"]
    client_secret = app.config["client_secret"]
    auth_code = code
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "http://localhost:5000/callback"
    }
    return requests.post(
        auth_url,
        data=token_data,
        headers=token_headers
    ).content


def fetch_artist_id(artist):
    find_artist_url = app.config["base_url"] + "/search?q={artist}&type=artist&limit=1".format(artist=artist)
    artist_headers = {
        "Authorization": "Bearer " + app.config.get("access_token")
    }
    return requests.get(
        find_artist_url,
        headers=artist_headers
    ).json()["artists"]["items"][0]["id"]


def fetch_tracks(artist, country_code):
    tracks_url = app.config["base_url"] + "/artists/{id}/top-tracks?market={country_code}" \
        .format(id=artist, country_code=country_code)
    tracks_headers = {
        "Authorization": "Bearer " + app.config.get("access_token")
    }
    return requests.get(
        tracks_url,
        headers=tracks_headers
    ).content
