from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import time
from download_mp3 import Mp3_Class
from selenium.webdriver.chrome.options import Options


with open(file = 'songs/song_urls.txt', mode = 'w') as w:
    w.write('')


song_names = []
with open(file ='songs/song_names.txt', mode ='r', encoding ='utf-8') as m:
    for i in m:
        song_names.append(i.replace('\n', ''))


options = Options()
options.add_argument('headless=new') #It's used to hide the chrome
options.add_argument('--mute-audio')


driver = webdriver.Chrome(options = options)
#driver.set_window_position(-10000,0) #You can also use this to hide the chrome

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

search_box.click()
time.sleep(1)
print('Finding Songs...')


for song in song_names:
    search_box.send_keys(song, Keys.ENTER)
    driver.implicitly_wait(5)
    time.sleep(2)

    videos = driver.find_elements(By.XPATH, '//*[@class="style-scope ytd-video-renderer"]')

    for i in videos[:5]:
        if song in i.get_attribute('innerHTML'):
            i.click()
            time.sleep(1)
            with open(file ='songs/song_urls.txt', mode ='a') as song_urls:
                song_urls.write(driver.current_url + '\n')

            break

    search_box.clear()

driver.quit()
print('Downloading Songs...')
song_urls = []
with open(file = 'songs/song_urls.txt', mode = 'r') as s:
    for i in s:
        song_urls.append(i.replace('\n', ''))


mp3_class = Mp3_Class(download_path = r'C:\YoutubeSongs')#You can change this path as you wish

for h in song_urls:
    mp3_class.download_video(video_url = h)

print('Successfully downloaded songs!')
