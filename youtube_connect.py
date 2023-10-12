import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Define el alcance de la API (en este caso, solo YouTube Data API).
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Lee las credenciales y el URI de redirección desde las variables de entorno.
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('YOUTUBE_REDIRECT_URI')

YOUTUBE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
YOUTUBE_TOKEN_URI = "https://oauth2.googleapis.com/token"
YOUTUBE_AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
# YOUTUBE_PROJECT_ID = os.getenv('YOUTUBE_PROJECT_ID')
# YOUTUBE_AUTH_URI = os.getenv
# YOUTUBE_TOKEN_URI = os.getenv('YOUTUBE_TOKEN_URI')
# YOUTUBE_AUTH_PROVIDER_X509_CERT_URL = os.getenv(
#     'YOUTUBE_AUTH_PROVIDER_X509_CERT_URL')

# Crea un flujo de autenticación.
flow = InstalledAppFlow.from_client_config(
    client_config={
        "installed": {
            "client_id": YOUTUBE_CLIENT_ID,
            "client_secret": YOUTUBE_CLIENT_SECRET,
            "redirect_uris": [REDIRECT_URI],
            "auth_uri": YOUTUBE_AUTH_URI,
            "token_uri": YOUTUBE_TOKEN_URI,
            "auth_provider_x509_cert_url": YOUTUBE_AUTH_PROVIDER_X509_CERT_URL,
        }
    },
    scopes=SCOPES
)

# Autenticación del usuario (si no se han guardado tokens previamente).
credentials = flow.run_local_server(port=8080)

# Crea un objeto de servicio de la API de YouTube.
youtube_service = build('youtube', 'v3', credentials=credentials)

# Ahora puedes utilizar youtube_service para interactuar con la API de YouTube.
# Imprimir información de la cuenta
channel_info = youtube_service.channels().list(
    part="snippet",
    mine=True
).execute()

print("Nombre del canal asociado a tu cuenta:")
print(channel_info["items"][0]["snippet"]["title"])

# Realizar una búsqueda de videos en YouTube (cambiar la consulta según tus necesidades)
search_response = youtube_service.search().list(
    q="Python programming",  # Cambia la consulta si lo deseas
    type="video",
    part="id,snippet",
    maxResults=5
).execute()

print("\nVideos encontrados:")
for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        print(f"Titulo: {search_result['snippet']['title']}")
        print(f"Video ID: {search_result['id']['videoId']}\n")
