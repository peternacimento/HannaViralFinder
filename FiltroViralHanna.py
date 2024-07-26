import os
import time
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Configuração da API
api_key = 'SUA_API_KEY'  # Substitua pela sua API Key
youtube = build('youtube', 'v3', developerKey=api_key)

DIA_ATRAS = 60
QTD_INSCRITOS_CANAL_MIN = 0
QTD_INSCRITOS_CANAL_MAX = 90000
QTD_MIN_VIEWS = 100000
REQUEST_DELAY = 1  # Delay de 1 segundo entre as requisições para reduzir o risco de exceder a cota


def search_videos(query, max_results=50, published_after=None):
    print(f"Procurando vídeos para a palavra-chave: {query}")
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=max_results,
        publishedAfter=published_after
    ).execute()

    print(f"Encontrado {len(search_response['items'])} vídeos para a palavra-chave: {query}")
    time.sleep(REQUEST_DELAY)  # Aguarda REQUEST_DELAY segundos após a busca
    return search_response['items']


def get_video_details(video_id):
    print(f"Obtendo detalhes para o vídeo ID: {video_id}")
    video_response = youtube.videos().list(
        part='statistics,snippet',
        id=video_id
    ).execute()

    print(f"Detalhes obtidos para o vídeo ID: {video_id}")
    time.sleep(REQUEST_DELAY)  # Aguarda REQUEST_DELAY segundos após obter os detalhes do vídeo
    return video_response['items'][0]


def get_channel_details(channel_id):
    print(f"Obtendo detalhes para o canal ID: {channel_id}")
    channel_response = youtube.channels().list(
        part='statistics',
        id=channel_id
    ).execute()

    print(f"Detalhes obtidos para o canal ID: {channel_id}")
    time.sleep(REQUEST_DELAY)  # Aguarda REQUEST_DELAY segundos após obter os detalhes do canal
    return channel_response['items'][0]


def load_existing_video_ids(file_path):
    if not os.path.exists(file_path):
        return set()

    with open(file_path, 'r', encoding='latin-1') as file:
        lines = file.readlines()

    video_ids = set()
    for line in lines:
        if line.startswith("VideoID: "):
            video_id = line.strip().split(" ")[1]
            video_ids.add(video_id)

    print(f"Carregados {len(video_ids)} IDs de vídeos existentes.")
    return video_ids


def filter_videos(videos, existing_video_ids):
    filtered_videos = []
    with open('filtered_videos.txt', 'a', encoding='latin-1') as file:  # Abre o arquivo em modo append
        for video in videos:
            video_id = video['id']['videoId']
            if video_id in existing_video_ids:
                print(f"Vídeo {video_id} já existe no arquivo. Ignorando.")
                continue

            video_details = get_video_details(video_id)
            channel_id = video_details['snippet']['channelId']
            channel_details = get_channel_details(channel_id)

            view_count = int(video_details['statistics']['viewCount'])
            subscriber_count = int(channel_details['statistics']['subscriberCount'])
            publish_date = video_details['snippet']['publishedAt']
            print(f"Inscritos: {subscriber_count} | Views: {view_count}")

            if QTD_INSCRITOS_CANAL_MIN <= subscriber_count <= QTD_INSCRITOS_CANAL_MAX and view_count >= QTD_MIN_VIEWS:
                filtered_video = {
                    'title': video_details['snippet']['title'],
                    'channel': video_details['snippet']['channelTitle'],
                    'view_count': view_count,
                    'subscriber_count': subscriber_count,
                    'video_id': video_id,
                    'publish_date': publish_date
                }
                filtered_videos.append(filtered_video)
                existing_video_ids.add(video_id)  # Adiciona o ID do vídeo ao conjunto de IDs existentes

                # Grava no arquivo assim que o vídeo atende aos critérios
                file.write(f"VideoID: {video_id}\n")
                file.write(f"Title: {filtered_video['title']}\n")
                file.write(f"Channel: {filtered_video['channel']}\n")
                file.write(f"Views: {filtered_video['view_count']}\n")
                file.write(f"Subscribers: {filtered_video['subscriber_count']}\n")
                file.write(f"Published Date: {filtered_video['publish_date']}\n")
                file.write(f"Link: https://www.youtube.com/watch?v={filtered_video['video_id']}\n")
                file.write('-' * 50 + '\n')
                print(f"Vídeo salvo: {filtered_video['title']}")

    return filtered_videos


def read_keywords_from_file(file_path):
    print(f"Lendo palavras-chave do arquivo: {file_path}")
    with open(file_path, 'r', encoding='latin-1') as file:
        keywords = file.readlines()
    print(f"{len(keywords)} palavras-chave lidas")
    return [keyword.strip() for keyword in keywords]


def main():
    # Lê as palavras-chave do arquivo
    keywords = read_keywords_from_file('PalavrasChaves.txt')

    # Carrega IDs de vídeos existentes
    existing_video_ids = load_existing_video_ids('filtered_videos.txt')

    # Define a data de dois meses atrás
    one_month_ago = datetime.utcnow() - timedelta(days=DIA_ATRAS)
    published_after = one_month_ago.isoformat("T") + "Z"

    for query in keywords:
        print(f"Processando palavra-chave: {query}")
        videos = search_videos(query, published_after=published_after)
        filter_videos(videos, existing_video_ids)

    print("Processo concluído!")


if __name__ == '__main__':
    main()
