import speech_recognition as sr
import pyautogui
import pygetwindow as gw
import time
import pvporcupine
import struct
import pyaudio
import winsound
import picovoice_access_config

def switch_to_youtube_tab():

    print(gw.getWindowsWithTitle('Google Chrome'))
    # Get the active Chrome window
    chrome_windows = gw.getWindowsWithTitle('Google Chrome')
    yt=0
    for window in chrome_windows:
        if yt==1:
            break
    # Activate the Chrome window
        window.activate()
    # Bring the Chrome window to the front
       # window.maximize()
    # Wait for Chrome to be in focus
        time.sleep(1)
    # Simulate Ctrl+Tab key press
        pyautogui.hotkey('ctrl', 'tab')
        tab_list=[]
    # Loop until the YouTube tab is found
        while True:
            # Get the active tab's title
            active_tab_title = gw.getActiveWindow().title
            print(active_tab_title)
            if active_tab_title in tab_list:
                break
            tab_list.append(gw.getActiveWindow().title)
            # Check if the YouTube tab is open
            if 'YouTube' in active_tab_title:
                yt=1
                break
            # Simulate Ctrl+Tab key press to switch to the next tab
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(0.5)  # Wait for the tab to switch (adjust if needed)
        print("Switched to YouTube tab!")


def take_command():
    #takes command from user used as a helper function in do_command()

    r = sr.Recognizer()
    #below commented thresholds are not being used in this file as we have wake word to start listening
    #r.phrase_threshold=0.1
    #r.pause_threshold=0.5 #default 0.8
    #r.non_speaking_duration=0.1 #default 0.5
    #mic = sr.Microphone(device_index=1)
    mic = sr.Microphone()
    recognized_text=""
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(mic) #adjusts for ambient noise default duration 1sec i.e if we start speaking the first 1 sec will not be used by .listen()
        #beep_sound()
        #start=time.time()
        play_sound()
        #end= time.time()
        #print(end-start)
        audio = r.listen(source)
        try:
            recognized_text = r.recognize_google(audio).lower()
            print("Recognized:", recognized_text)
            if recognized_text is not None:
                return recognized_text
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Speech recognition service error:", str(e))

def beep_sound():
    # beep sound freq=600 Hz, duration=300 millsec
    winsound.Beep(600,300) 

def play_sound():
    #plays the system(windows) Welcome sound
    #flag SND_ASYNC make sure the sound plays asynchronously
    #better option as .Beep() does not work the first time we call for wake word
    winsound.PlaySound("SystemWelcome", winsound.SND_ASYNC) 

def do_command():
    #takes recognized command obtained from take_command() and does particular actions 

    while True:
        said = take_command()
        if said is not None:
            if "youtube" in said:
                switch_to_youtube_tab()
                break
            if "play" in said:
                pyautogui.press("playpause")
                break
            if "pause" in said:
                pyautogui.press("playpause")
                break
            if "back" in said:
                for i in range(int(said[-2:])//5):
                    pyautogui.press("left")
                break
            if "skip" in said:
                for i in range(int(said[-2:])//5):
                    pyautogui.press("right")
                break
            if "sleep" in said:
                print("stopping...")
                break
            
            break


def main():

    porcupine=None
    pa=None
    audio_stream=None

    print("Awaiting call... ")

    try:
        porcupine=pvporcupine.create(keywords=["computer"],access_key=picovoice_access_config.access_key)
        pa=pyaudio.PyAudio()
        audio_stream=pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        while True:
            pcm=audio_stream.read(porcupine.frame_length)
            pcm=struct.unpack_from("h"*porcupine.frame_length, pcm)
            keyword_index=porcupine.process(pcm)
            if keyword_index>=0:
                print("Wakeword Detected... ")
                time.sleep(1)
                do_command()
                print("Awaiting call... ")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()    


if __name__ == "__main__":
    main()      
