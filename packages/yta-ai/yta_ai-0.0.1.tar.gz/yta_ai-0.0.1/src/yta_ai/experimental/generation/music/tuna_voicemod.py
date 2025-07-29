from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from yta_general_utils.experimental.chrome_scrapper import start_chrome, go_to_and_wait_loaded
from random import randrange

import time
import glob
import shutil
import os


URL = 'https://tuna.voicemod.net/text-to-song/?utm_source=LandingTTSong&utm_medium=LandingTTSong&utm_campaign=TTSongCreateLanding&utm_id=TTSongCreateLanding'
DOWNLOADS_ABSOLUTE_PATH = 'C:/Users/dania/Downloads/'
PROJECT_ABSOLUTE_PATH = os.getenv('PROJECT_ABSOLUTE_PATH')

def generate_song(lyrics, output_filename):
    try:
        cookies = [
            {
                'name': 'vm_userId',
                'value': '06755a97-1896-4856-9709-8203d1c1befc'
            },
            {
                'name': 'session',
                'value': '236gerx18e3xb82k3m81xcvnporuxysqaeqrrrs97nqp8gvv1fxspb0q3v5q4z3pnbsv1w6',
            },
            {
                'name': 'vm_refresh_token',
                'value': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDk0ODgwMzksImV4cCI6MTcxMjA4MDAzOSwic3ViIjoiMDY3NTVhOTctMTg5Ni00ODU2LTk3MDktODIwM2QxYzFiZWZjIiwiYXVkIjoid2ViIiwic2NvcGUiOiJyZWFkIHdyaXRlIn0.NWfF78CNbBQakZyofsWEYN4B7BDzGrYhZtFVPblrKNdRtCaQ6OZEvoTJGkjsbklUfzYzEcU71lqZWAdktAjjLgnEGwHKkNT0gnqm5wyw2m-VmX9K1FJcvYxrDuLSGgj4cXVknewmN7rJmNvV9m0VsI46bNX09Pd0lPcAevqouyb2G2W0yEyIyUNHxuPTrhXiBt15xIh7g7yffRJk33gRVOzwcu9xNutk32Ml-zHPcY1YhSEjXYRtDPdAmOzfXy1vNJSpI5T2BEH4NtZuegs2V3CRLoSCKFWd5mZKA3NKrEsfQjKnLIRE27VvNpNVM6PXltuI8rEgxeVlDeF4yechJQ'
            },
            {
                'name': 'vm_mparticle_device_id',
                'value': 'd533e2bc-9f88-4b47-f5bd-aa16779a6b26'
            },
            {
                'name': 'vm_initial_referrer',
                'value': 'aHR0cHM6Ly9hY2NvdW50LnZvaWNlbW9kLm5ldC8='
            },
            {
                'name': 'vm_initial_url',
                'value': 'aHR0cHM6Ly93d3cudm9pY2Vtb2QubmV0Lw=='
            },
            {
                'name': 'vm_access_token',
                'value': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDk0ODgwMzksImV4cCI6MTcwOTU3NDQzOSwic3ViIjoiMDY3NTVhOTctMTg5Ni00ODU2LTk3MDktODIwM2QxYzFiZWZjIiwiYXVkIjoid2ViIiwic2NvcGUiOiJyZWFkIHdyaXRlIn0.RVBc-3jRUlx03ulDyR7HoXW1c4ir6AdDFWqnSmMahVM2QM76zy2YY85r4n2ynvECKl5ylu7MhM4PwjyzYLISCCMgkQTkALexGJZXELBAdQTkKVhG4EuqU91VOHvYCLugaB6HkA12U9VGvbh-bgTxnRxB2dnDfOBSIUZUVx-tCNEmhpHILbKY_C4bo_UEpeC8nBLvdle2SnLZbuUNrlCIb3rFsLEdPCnAsBXeGqxQEBVKEOE-TCHwF0VvPSEo-HZo97I-yGindxpXvty2BZkbfXhurMed8Gl6UKV_rQ4deBxyl-SL1B1XFc-rzGVot_L0VyUeF10LKwK-Hwq4xzPmpQ'
            }
        ]

        driver = start_chrome(True, True, True, [])
        go_to_and_wait_loaded(driver, 'https://tuna.voicemod.net/text-to-song')
        for cookie in cookies:
            driver.add_cookie(cookie)
        go_to_and_wait_loaded(driver, URL)
        time.sleep(2)

        music_style_ids = ['DarkTrap', 'Levitate', 'LazerBeam', 'StayWithMe', 'MoveYourBody', 'BreakIsOver', 'HappyBirthday', 'Hallelujah', 'JingleBells', 'WeWishYou', 'SilentNight', 'DeckTheHalls', 'HolidayTunes', 'Joy', 'AngelsSing']
        music_style_element = driver.find_element(By.ID, music_style_ids[randrange(len(music_style_ids))])
        music_style_element.click()
        #music_style_elements = driver.find_elements(By.CLASS_NAME, 'song-preview-card')
        #music_style_elements[0].click()

        time.sleep(2)

        buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Next')]")
        buttons[0].click()

        time.sleep(2)

        music_style_elements = driver.find_elements(By.CLASS_NAME, 'step-singer-card')
        music_style_element = music_style_elements[randrange(len(music_style_elements))]
        music_style_element.click()
        #music_style_elements[0].click()

        time.sleep(2)

        buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Next')]")
        buttons[0].click()

        time.sleep(2)

        textarea = driver.find_element(By.TAG_NAME, 'textarea')
        textarea.send_keys(lyrics)

        time.sleep(2)

        buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Create song')]")
        buttons[0].click()

        time.sleep(2)

        # Check which one is the latest file
        list_of_files = glob.glob(DOWNLOADS_ABSOLUTE_PATH + '*.mp4')
        latest_file = max(list_of_files, key = os.path.getctime)

        element_present = EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Download')]"))
        element = WebDriverWait(driver, 60).until(element_present)
        # wait Button aria-label 'Download'
        element.click()
        time.sleep(2)

        # Now we need 2 ALT + SPACE
        actions = ActionChains(driver)
        for i in range(2):
            actions.send_keys(Keys.TAB)
        actions.perform()
        actions.send_keys(Keys.SPACE)
        actions.perform()

        cont = 0
        while cont < 60:
            list_of_files = glob.glob(DOWNLOADS_ABSOLUTE_PATH + '*.mp4')
            tmp_latest_file = max(list_of_files, key = os.path.getctime)
            if tmp_latest_file != latest_file:
                latest_file = tmp_latest_file
                cont = 60
            time.sleep(1)
            cont += 1

        shutil.move(latest_file, os.path.join(output_filename))
        print('Song downloaded successfully')
        
        """
        tabs_to_next = 16

        # Styles start at 5th tab
        actions = ActionChains(driver)
        for i in range(7):
            actions.send_keys(Keys.TAB)
        actions.perform()
        time.sleep(1)
        actions.send_keys(Keys.SPACE)
        actions.perform()
        time.sleep(1)

        for i in range(tabs_to_next - 7):
            actions.send_keys(Keys.TAB)
        actions.perform()
        time.sleep(1)
        actions.send_keys(Keys.SPACE)
        actions.perform()
        time.sleep(1)
        """
    except Exception as e:
        print(e)
    finally:
        driver.close()