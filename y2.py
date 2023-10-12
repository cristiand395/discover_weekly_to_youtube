from flask import Flask, redirect, request, render_template
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

app = Flask(__name__)

# Define el alcance de la API (en este caso, solo YouTube Data API).
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Lee las credenciales y el URI de redirección desde las variables de entorno.
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
REDIRECT_URI = "http://localhost:8080/"

YOUTUBE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
YOUTUBE_TOKEN_URI = "https://oauth2.googleapis.com/token"
YOUTUBE_AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"


# Variable para almacenar los tokens de autenticación
user_credentials = None

# Ruta para iniciar la autenticación


@app.route('/')
def authenticate():
    flow = InstalledAppFlow.from_client_config(
        client_config={
            "installed": {
                "client_id": YOUTUBE_CLIENT_ID,
                "client_secret": YOUTUBE_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "auth_uri": YOUTUBE_AUTH_URI,
                "token_uri": YOUTUBE_TOKEN_URI,
                "auth_provider_x509_cert_url": YOUTUBE_AUTH_PROVIDER_X509_CERT_URL
            }
        },
        scopes=SCOPES
    )
    authorization_url, _ = flow.authorization_url()
    return redirect(authorization_url)

# Ruta para recibir la redirección de Google


@app.route('/callback')
def callback():
    global user_credentials
    flow = InstalledAppFlow.from_client_config(
        client_config={
            "installed": {
                "client_id": YOUTUBE_CLIENT_ID,
                "client_secret": YOUTUBE_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "auth_uri": YOUTUBE_AUTH_URI,
                "token_uri": YOUTUBE_TOKEN_URI,
                "auth_provider_x509_cert_url": YOUTUBE_AUTH_PROVIDER_X509_CERT_URL
            }
        },
        scopes=SCOPES
    )
    flow.fetch_token(authorization_response=request.url)
    # Almacena los tokens de autenticación en una base de datos o realiza acciones con ellos
    user_credentials = flow.credentials
    return "Autenticación exitosa."

# Ruta para verificar la conexión y hacer una búsqueda


@app.route('/search')
def search():
    global user_credentials
    if user_credentials is None:
        return "Debes autenticarte primero."

    # Crea un objeto de servicio de la API de YouTube.
    youtube_service = build('youtube', 'v3', credentials=user_credentials)

    # Verifica la conexión haciendo una solicitud a la API de YouTube
    try:
        channel_info = youtube_service.channels().list(
            part="snippet",
            mine=True
        ).execute()

        # Realizar una búsqueda de videos en YouTube (cambiar la consulta según tus necesidades)
        search_response = youtube_service.search().list(
            q="Programming projects",  # Cambia la consulta si lo deseas
            type="video",
            part="id,snippet",
            maxResults=5
        ).execute()

        return render_template('results.html', channel_title=channel_info["items"][0]["snippet"]["title"], search_results=search_response.get("items", []))

    except Exception as e:
        return f"Error al conectar a la API de YouTube: {str(e)}"


app.run(debug=True, port=8080)
