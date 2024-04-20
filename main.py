from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.firefox.options import Options
from download_mp3 import Mp3_Class


def launch_driver():
    options = Options()
    options.add_argument('--headless') #It's used to hide the driver
    options.set_preference("media.volume_scale", "0.0")

    #driver.set_window_position(-10000,0) #You can also use this to hide the driver
    #service = Service(executable_path = 'geckodriver.exe') #You can utilize it to use a specific version of firefox

    driver = webdriver.Firefox(options = options)
    return driver


def start_search(driver):
    driver.get('https://www.youtube.com/')

    driver.implicitly_wait(10)
    time.sleep(1)

    for _ in range(3):
        try:
            search_box = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.NAME, 'search_query')))
            search_box.click()
            break

        except:
            driver.get('https://www.youtube.com/')
            driver.implicitly_wait(10)
            search_box = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.NAME, 'search_query')))
            search_box.click()

    '''searches = driver.find_elements(By.XPATH, '//*[@aria-label="Search"]')
       searches[0].click() #You can also use this one'''

    return search_box


def get_urls(driver, search_box):
    print('Finding Songs...')
    search_box.click()
    time.sleep(1)

    song_names = []
    with open(file='songs/song_names.txt', mode='r', encoding='utf-8') as m:
        for i in m:
            song_names.append(i.replace('\n', ''))

    #Fetching The Songs Here
    for song in song_names:
        search_box.send_keys(song, Keys.ENTER)
        driver.implicitly_wait(5)
        time.sleep(1)
        videos = driver.find_elements(By.XPATH, '//*[@id="video-title"]')

        for i in videos[:5]:
            if song in i.text:
                song_url = i.get_attribute('href')

                if song_url != None:
                    with open(file ='songs/song_urls.txt', mode ='a') as song_urls:
                        song_urls.write(song_url + '\n')

                break
        search_box.clear()

    driver.quit()


if __name__ == '__main__':
    try:
        with open(file='songs/song_urls.txt', mode='w') as w:
            w.write('')

        print("Launching Web Driver...")
        driver = launch_driver()
        search_box = start_search(driver)
        get_urls(driver, search_box)

        print('Downloading Songs...')
        song_urls = []

        with open(file='songs/song_urls.txt', mode='r') as s:
            for i in s:
                song_urls.append(i.replace('\n', ''))


        download_path = r'C:\YoutubeSongs'
        mp3_class = Mp3_Class(download_path)  # You can change this path as you wish

        for h in song_urls:
            mp3_class.download_video(video_url = h)
        print(f'Successfully downloaded songs to {download_path}')

    except Exception as error:
        print(error)
        print("An Error Occured Try Again!")
