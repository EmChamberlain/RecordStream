from time import sleep
import os
import subprocess
import datetime
import ctypes



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

wait = None
p = None

def start_recording(cmd):
    try:
        global p
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        p.stdin.write(b"y\n")
        p.stdin.flush()
    except:
        pass

def stop_recording():
    try:
        p.stdin.write(b"q")
        p.stdin.flush()
        p.wait()
    except:
        pass

def click_large_play_button():
    try:
        large_play_button = wait.until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="fcplayer"]/button""")))
        large_play_button.click()
    except:
        pass

def click_small_play_button():
    try:
        small_play_button = wait.until(
            EC.presence_of_element_located((By.CLASS, """vjs-play-control vjs-control vjs-button vjs-playing""")))
        small_play_button.click()
    except:
        pass

def click_fullscreen_button():
    try:
        small_play_button = wait.until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="fcplayer"]/div[6]/button[2]""")))
        small_play_button.click()
    except:
        pass

def is_time():
    now = datetime.datetime.now()
    # now = now.replace(hour=9, minute=31)
    print(str(now.weekday()) + " " + str(now.hour) + ":" + str(now.minute))
    correct_day = now.weekday() == 0 or now.weekday() == 2
    after_start = (now.hour > 8) or (now.hour == 8 and now.minute >= 38)
    before_end = (now.hour < 10) or (now.hour == 10 and now.minute < 5)
    return correct_day and after_start and before_end
def main():

    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Please run with administrator priveleges")
        exit(1)
    command = """ffmpeg -f dshow -i video="UScreenCapture":audio="VoiceMeeter Output (VB-Audio VoiceMeeter VAIO)" captures/"""

    while True:
        if is_time():
            options = webdriver.ChromeOptions()
            # options.add_argument("user-data-dir=C:\\Users\\Matt\\AppData\\Local\\Google\\Chrome\\User Data")
            browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
            browser.maximize_window()
            browser.get("https://player.cloud.wowza.com/hosted/fffjqfv1/player.html")

            global wait
            wait = WebDriverWait(browser, 30)

            click_large_play_button()
            click_small_play_button()
            click_fullscreen_button()
            start_recording(command + datetime.datetime.now().strftime("%Y_%m_%d_%H-%M-%S") + ".mkv")
            while is_time():
                sleep(30)
            stop_recording()
            browser.quit()

        sleep(30)


if __name__ == '__main__':
    main()