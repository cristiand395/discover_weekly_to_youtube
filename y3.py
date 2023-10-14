import os
from flask import Flask, redirect, request, session, url_for, make_response
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

app = Flask(__name__)

# Configura las claves secretas para sesiones en Flask.
app.secret_key = 'tu_secreto'

# Define el alcance de la API (en este caso, solo YouTube Data API).
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Nombre del archivo JSON de credenciales descargado.
CREDENTIALS_FILE = 'client_secret.json'


@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    # Carga las credenciales desde la sesión.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    # Crea un objeto de servicio de la API de YouTube.
    youtube_service = build('youtube', 'v3', credentials=credentials)

    # Ahora puedes utilizar youtube_service para interactuar con la API de YouTube.

    # Ejemplo: Obtener la lista de tus videos.
    videos = youtube_service.search().list(
        part="snippet", type="video", maxResults=10).execute()

    return f'Tus videos: {videos}'


# @app.route('/authorize')
# def authorize():
#     flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
#     # flow.redirect_uri = url_for('oauth2callback', _external=True)
#     flow.redirect_uri = "http://localhost:8080/oauth2callback"
#     authorization_url, state = flow.authorization_url(access_type='offline')

#     # Guarda el estado en la sesión para verificarlo en la respuesta de OAuth2.
#     session['state'] = state

#     return redirect(authorization_url)


# @app.route('/oauth2callback')
# def oauth2callback():
#     state = session['state']
#     flow = InstalledAppFlow.from_client_secrets_file(
#         CREDENTIALS_FILE, SCOPES, state=state)
#     flow.redirect_uri = url_for('oauth2callback', _external=True)
#     authorization_response = request.url
#     flow.fetch_token(authorization_response=authorization_response)

#     # Guarda las credenciales en la sesión.
#     session['credentials'] = flow.credentials.to_json()

#     return redirect(url_for('index'))

@app.route('/authorize')
def authorize():
    print("Entro en la ruta /authorize")
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    flow.redirect_uri = "http://localhost:8080/oauth2callback"
    authorization_url, state = flow.authorization_url(access_type='offline')

    # Guarda el estado en una cookie.
    response = make_response(redirect(authorization_url))
    response.set_cookie('oauth_state', state)

    return response


# @app.route('/oauth2callback')
# def oauth2callback():
#     print("Entro en la ruta /oauth2callback")
#     # Recupera el estado de la cookie.
#     state = request.cookies.get('oauth_state')
#     if state is None:
#         return "Error: Estado no encontrado en la cookie."

#     # Resto del código para el flujo de OAuth2.

#     return redirect(url_for('index'))

@app.route('/oauth2callback')
def oauth2callback():
    state = request.cookies.get('oauth_state')
    if state is None:
        return "Error: Estado no encontrado en la cookie."

    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE, SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Guarda las credenciales en la sesión.
    session['credentials'] = flow.credentials.to_json()

    # Redirige al usuario a la página principal (ruta '/index').
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
