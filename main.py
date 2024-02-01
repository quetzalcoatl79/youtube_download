import re
import os
from pytube import Playlist, YouTube

#pip install pytube

YOUTUBE_STREAM_AUDIO = '140'
YOUTUBE_STREAM_VIDEO = '22'
YOUTUBE_STREAM_DEFAULT= '18'

# Vérification URL
def is_youtube_url(url):
    youtube_pattern = re.compile(r'(https?://)?(www\.)?youtube\.com/.*')
    return bool(re.match(youtube_pattern, url))

def replace_special_characters(title):
    # Remplacez les caractères spéciaux par des underscores
    return re.sub(r'[\\/:*?"<>|]', '_', title)

def is_playlist(url):
    try:
        # Essayez d'initialiser un objet Playlist
        playlist = Playlist(url)
        if not playlist:
            print(f"C'est une playlist vide !   ==> {playlist}")
            return False
        else:    
            print(f"C'est une playlist !   ==> {playlist}")
        return True
    except Exception as e:
        # Si une exception est levée, cela n'est pas une playlist
        print("Ce n'est pas une playlist !")
        return False

def creer_dossier_album(DOWNLOAD_DIR):
    # Obtenir le nom de l'album du chemin
    nom_album = DOWNLOAD_DIR.split('/')[-1]
    # Vérifiez si le dossier existe déjà
    if os.path.exists(DOWNLOAD_DIR):
        while True:
            wherefile = confirmation = input(f"Le dossier '{nom_album}' existe déjà. Voulez-vous le remplacer? (oui/non): ")
            if wherefile.lower() == "oui":
                print(f"Remplacement du dossier '{nom_album}'.")
                break  # Sortir de la boucle si le format est correct
            elif wherefile.lower() == "non":
                print(f"Opération annulée. Le dossier '{nom_album}' ne sera pas modifié.")
                return      
    else:
        os.makedirs(DOWNLOAD_DIR)
        print(f"Dossier '{nom_album}' créé avec succès.")

# Appel de la fonction
url = input('Colle ton URL : ')
if is_youtube_url(url):
    print("L'URL est une URL YouTube.")
else:
    print("L'URL n'est pas une URL YouTube.")


album = input('Nom de la playliste : ')
wherefile =""
while True:
    wherefile = input("Quel format désirez-vous (mp3/mp4): ")
    if wherefile.lower() == "mp3":
        DOWNLOAD_DIR = os.path.expanduser(f"~\\Music\\{album}")
        YOUTUBE_STREAM = YOUTUBE_STREAM_AUDIO
        break  # Sortir de la boucle si le format est correct
    elif wherefile.lower() == "mp4":
        DOWNLOAD_DIR = os.path.expanduser(f"~\\Videos\\{album}")
        YOUTUBE_STREAM = YOUTUBE_STREAM_VIDEO
        break  # Sortir de la boucle si le format est correct
    else:
        print("Format invalide. Veuillez entrer 'mp3' ou 'mp4'.")

      
creer_dossier_album(DOWNLOAD_DIR)

if not is_playlist(url):
    print(f"not is_playlist   {url}")
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(YOUTUBE_STREAM)
    if stream == None:
        stream = yt.streams.get_by_itag(YOUTUBE_STREAM_DEFAULT)
    titre = replace_special_characters(yt.title)    
    stream.download(output_path=DOWNLOAD_DIR, filename=f"{titre}.{wherefile}")
else:
    playlist = Playlist(url)
    for video in playlist.videos:
        stream = video.streams.get_by_itag(YOUTUBE_STREAM)
        if stream == None:
            stream = video.streams.get_by_itag(YOUTUBE_STREAM_DEFAULT)
        titre = replace_special_characters(video.title)
        stream.download(output_path=DOWNLOAD_DIR, filename=f"{titre}.{wherefile}")