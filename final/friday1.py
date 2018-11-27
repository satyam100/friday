import ctypes
import speech_recognition as sr
import os
from playsound import playsound
import webbrowser
import random


speech=sr.Recognizer()
greting_dict={'hello':'hello','hi':'hi'}
open_launch_dict={'open':'open','launch':'launch'}
google_searches_dict={'what':'what','why':'why','who':'who','which':'which'}
social_media_dict={'facebook':'https://www.facebook.com','twitter':'https://www.twitter.com'}
social_post_dict={'post':'post'}

mp3_thankyou_list=['mp3/friday/thankyou_1.mp3','mp3/friday/thankyou_2.mp3']
mp3_listening_problem_list=['mp3/friday/listening_problem_1.mp3','mp3/friday/listening_problem_2.mp3']
mp3_struggling_list=['mp3/friday/struggling_1.mp3']
mp3_google_search=['mp3/friday/google_search_1.mp3','mp3/friday/google_search_2.mp3']
mp3_greeting_list=['mp3/friday/greeting_accept.mp3','mp3/friday/greeting_accept_2.mp3']
mp3_open_launch_list=['mp3/friday/open_1.mp3','mp3/friday/open_3.mp3','mp3/friday/open_2.mp3']
mp3_bye_list=['mp3/friday/bye.mp3']

error_occurence = 0

def is_valid_google_search(phrase):
    if(google_searches_dict.get(phrase.split(' ')[0])== phrase.split(' ')[0]):
        return True

def play_sound(mp3_list):
    mp3=random.choice(mp3_list)
    playsound(mp3)

def read_voice_cmd():
    voice_text = ''
    print('Listening....')

    global error_occurence

    try:

        with sr.Microphone() as source:
            audio = speech.listen(source=source, timeout=10, phrase_time_limit=5)
        voice_text = speech.recognize_google(audio)
    except sr.UnknownValueError:

        if error_occurence==0:
            play_sound(mp3_listening_problem_list)
            error_occurence+=1
        elif error_occurence==1:
            play_sound(mp3_struggling_list)
            error_occurence+=1

    except sr.RequestError as e:
        print('Network error')
    except sr.WaitTimeoutError:
        if error_occurence == 0:
            play_sound(mp3_listening_problem_list)
            error_occurence += 1
        elif error_occurence == 1:
            play_sound(mp3_struggling_list)
            error_occurence += 1

    return voice_text

def is_valid_note(greet_dict,voice_note):
    for key,value in greet_dict.iteritems():
        #'Hello Friday'
        try:
            if value==voice_note.split(' ')[0]:
                return True
                break
            elif key==voice_note.split(' ')[1]:
                return True
                break
        except IndexError:
            pass
    return False


if __name__ == '__main__':

    playsound('mp3/friday/greeting.mp3')

    while True:

        voice_note = read_voice_cmd().lower()
        print('cmd:{}'.format(voice_note))

        if is_valid_note(greting_dict,voice_note):
            print('In greeting...')
            play_sound(mp3_greeting_list)
            continue
        elif is_valid_note(open_launch_dict,voice_note):
            print('In open...')
            play_sound(mp3_open_launch_list)
            if(is_valid_note(social_media_dict,voice_note)):
                #Launch Facebook
                key=voice_note.split(' ')[1]
                webbrowser.open(social_media_dict.get(key))
            else:
                os.system('explorer C:\\"{}"'.format(voice_note.replace('open ', '')))
            continue
        elif is_valid_google_search(voice_note):
            print('in google search.....')
            play_sound(mp3_google_search)
            webbrowser.open('https://www.google.co.in/search?q={}'.format(voice_note))
            continue
        elif 'thank you' in voice_note:
            play_sound(mp3_thankyou_list)
            continue
        elif 'cmd' in voice_note:
            os.system("cmd")
            playsound('mp3/friday/open_3.mp3')
        elif 'lock' in voice_note:
            for value in['pc','system','windows']:
                ctypes.windll.user32.LockWorkStation()

        elif 'goodbye' in voice_note:
            playsound('mp3/friday/bye.mp3')
            exit()
