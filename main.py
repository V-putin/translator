import speech_recognition as sr
from googletrans import Translator
import eel

lang1 = 'en'
lang2 = 'ru'

def translate(text):
    try:
        global lang1, lang2

        translator = Translator(service_urls=['translate.google.com'])
        translation = translator.translate(text, dest=lang2, src=lang1)

        return translation.text
    except Exception as ex:
        return ex

@eel.expose
def listen():
    # Создаем объект для распознавания речи
    r = sr.Recognizer()
    r.pause_threshold = 0.5

    while True:
        # Запускаем прослушивание микрофона
        with sr.Microphone() as source:
            audio = r.listen(source)

            try:
                global lang1
                # Преобразуем аудио в текст
                text = r.recognize_google(audio, language=lang1)
                #print("Вы сказали: " + text)

                return translate(text)
            except sr.UnknownValueError:
                return "Голос не распознан"
            except sr.RequestError as e:
                return "Ошибка сервиса распознавания речи; {0}".format(e)

eel.init('web')
eel.start('index.html', size=(500, 1000))