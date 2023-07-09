import speech_recognition as sr
import pyautogui
import pygetwindow as gw
import time

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

# Call the function to switch to the YouTube tab
switch_to_youtube_tab()


r = sr.Recognizer()
r.phrase_threshold=0.1
r.pause_threshold=0.5 #default 0.8
r.non_speaking_duration=0.1 #default 0.5
mic = sr.Microphone(device_index=1)
#mic = sr.Microphone()

play_commands = ["play", "resume"]
pause_commands = ["pause", "stop"]
rewind_commands = ["rewind 10", "rewind 20", "rewind 30"]
skip_commands = ["skip 10", "skip 20", "skip 30"]
vol_commands = ["volume up", "volume down"]

while True:
    start=time.time()
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(mic)
        audio = r.listen(source, phrase_time_limit=2)

    try:
        recognized_text = r.recognize_google(audio).lower()
        print("Recognized:", recognized_text)
        end=time.time()
        print(end-start)

        if recognized_text in play_commands:
            # Perform play action
            pyautogui.press("playpause")
        elif recognized_text in pause_commands:
            # Perform pause action
            pyautogui.press("playpause")
        elif recognized_text in vol_commands:
            if recognized_text[-2:]=="up":
                pyautogui.press("volumeup")
            else:
                pyautogui.press("volumedown")    
        elif recognized_text in rewind_commands:
            # Perform rewind action
            for i in range(int(recognized_text[-2:])//5):
                pyautogui.press("left")
        elif recognized_text in skip_commands:
            # Perform skip action
            for i in range(int(recognized_text[-2:])//5):
                pyautogui.press("right")
                
        else:
            # Handle unrecognized commands
            print("Command not recognized.")

    except sr.UnknownValueError:
        print("Could not understand audio.")
        end1=time.time()
        print(end1-start)
    except sr.RequestError as e:
        print("Speech recognition service error:", str(e))



