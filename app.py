from flask import Flask, request, render_template
import random
import re
from googleapiclient.discovery import build

# Replace with your own API key
youtube_api_key = 'AIzaSyDuIgB8PonxT3QTEMKmRspKW9IzVTyvu_E'

# Build a resource object for interacting with the YouTube API
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

app = Flask(__name__)

def get_playlist_titles(playlist_id):
    titles = []
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
    )

    while request:
        response = request.execute()
        for item in response['items']:
            titles.append(item['snippet']['title'])
        request = youtube.playlistItems().list_next(request, response)
    
    return titles

def clean_and_extract_words(titles):
    words = []
    for title in titles:
        cleaned_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        words.extend(cleaned_title.split())
    return words

def create_sentences(words, words_per_sentence=4):
    sentences = []
    random.shuffle(words)
    for i in range(0, len(words), words_per_sentence):
        sentence = ' '.join(words[i:i + words_per_sentence])
        sentences.append(sentence.capitalize() + '.')
    return sentences

def format_as_poem(sentences, sentences_per_line=2):
    poem_lines = []
    for i in range(0, len(sentences), sentences_per_line):
        line = ' '.join(sentences[i:i + sentences_per_line])
        poem_lines.append(line)
    return '\n'.join(poem_lines)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        playlist_url = request.form['playlist_url']
        playlist_id = playlist_url.split('list=')[-1].split('&')[0]
        titles = get_playlist_titles(playlist_id)
        words = clean_and_extract_words(titles)
        sentences = create_sentences(words)
        poem = format_as_poem(sentences)
        return render_template('index.html', poem=poem)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
