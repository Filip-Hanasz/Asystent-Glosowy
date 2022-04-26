import speech_recognition as sr
import webbrowser
import playsound
import os
import random
from gtts import gTTS
from google_trans_new import google_translator

# Stworzenie obiektu r służącego do rozpoznawania głosu oraz translatora do jego tłumaczenia

r = sr.Recognizer()
translator = google_translator()

# Poniższe funkcje służą do pobierania próbki dźwiękowej z mikrofonu domyślnego urządzenia oraz kontroli błędów

# Funkcja do trzymania assystenta w stanie spoczynku. Rozpoznawanie mowy w języku polskim z wyłączoną kontrolą błędów

def record_audio_on_hold(ask = False):
    with sr.Microphone() as source:
        if ask:
            maniek_voice(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language='pl')
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
        return voice_data.lower()

# Funkcja do pobierania próbki dźwiękowej w języku angielskim potrzebnej do tłumaczenia
# słów z języka angielskiego na polski

def record_audioen(ask = False):
    with sr.Microphone() as source:
        if ask:
            maniek_voice(ask)
        print('powiedz coś...')
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language='en')
        except sr.UnknownValueError:
            maniek_voice('przepraszam, nie rozumiem co mówisz')
        except sr.RequestError:
            maniek_voice('teraz nie działam')
        return voice_data.lower()

# Funkcja do pobierania próbki w języku polskim ze zwracaniem informacji o błędzie, braku zrozumienia próbki
# Lub braku działania funkcji

def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:  # sprawdzanie czy w argumencie nie zostało przekazane dodatkowe zapytanie
            maniek_voice(ask)
        print('powiedz coś...')
        audio = r.listen(source)  # Pobranie próbki z mikrofonu
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language='pl')  # Rozpoznanie próbki za pomocą google API
        except sr.UnknownValueError:
            maniek_voice('nie zrozumiałem')
        except sr.RequestError:
            maniek_voice('teraz nie działam')
        return voice_data.lower()

# Funkcja reprezentująca głos assystenta (mańka) zamieniająca napis na plik dźwiękowy za pomocą
# google text to speech. Zapisuje plik z próbką w pliku mp3 w katalogu projektu oraz kasuje go
# po zakończeniu odtwarzania. Playsound używany do odtwarzania pliku mp3
    
def maniek_voice(audio_string):
    tts = gTTS(text = audio_string, lang='pl', tld='pn')  #Przetwarzania textu na mp3
    r = random.randint(1, 10000000)  # Losowość nazwy pliku
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)  # Zapisanie pliku mp3
    playsound.playsound(audio_file)  # Odtworzenie pliku mp3
    print(audio_string)
    os.remove(audio_file)  # Usunięcie pliku mp3

# Funkcja z zaprogramowanymi komendami dla assystenta. Po wywołaniu sprawdza czy w argumencie znajduje się jeden
# z podanych zwrotów i wykonuje zgodnie z nim przyjęte działanie

def respond(voice_data):
    if 'jak się nazywasz' in voice_data:
        maniek_voice('nazywam się Maniek')
    elif 'szukaj'in voice_data:
        maniek_voice('Co chcesz żebym znalazł?')
        search = record_audio()
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)  # wywołanie wyszukiwania danego zwrotu na podanym url
        maniek_voice('Proszę, oto twoje wyniki wyszukiwania')
    elif 'zamknij się' in voice_data:
        maniek_voice("zamykam")
        exit()
    elif 'przetłumacz' in voice_data:  # tłumacz, tylko ang - pl
        maniek_voice('Co mam przetłumaczyć?')
        slowo = record_audioen()
        wynik = translator.translate(slowo, lang_tgt='pl')  # tłumaczenie slowa w translatorze na polski
        maniek_voice(slowo + " po polsku znaczy " + wynik)

# Zatrzymanie i czekanie na komende wywołującą odrazu po odpaleniu programu
# Działa do momentu wypowiedzenia w komendzie "zamknij się"

while True:
    voice_data = record_audio_on_hold()
    print(voice_data)
    if 'maniek' in voice_data:
        maniek_voice('Jak ci mogę pomóc?')
        voice_data = record_audio()
        print(voice_data)
        respond(voice_data)

# Do uruchomienia i zadania pierwszej komendy trzeba wezwać zwrotem zawierającym jego imie ("Maniek")
