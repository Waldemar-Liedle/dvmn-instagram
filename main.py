"""
В ЭТОМ КОММЕНТАРИИ ВОПРОС К ПРЕПОДАВАТЕЛЮ. ПРИ ПРОШЛОЙ ПРОВЕРКЕ МОЙ ВОПРОС БЫЛ ПРОИГНОРИРОВАН.
Написал вчера через "Я в тупике. Помогите", но ответа не последовало, поэтому отправляю на проверку с ошибкой.
При загрузке картинок на Instagram загружает первую картинку, а потом выдаёт ошибку доступа к картинкам, мол, другой процесс уже использует файл.
Я не могу найти те места в коде, где я многократно обращаюсь к одному файлу.
Я не знаю, как решить эту проблему.
"""
import requests
import argparse
from os import getenv, makedirs, listdir
from instabot import Bot
from dotenv import load_dotenv

SPACEX_URL = "https://api.spacexdata.com/v3/launches/latest"
HUBBLE_IMAGE_URL = "http://hubblesite.org/api/v3/image"
HUBBLE_IMAGES_URL = "http://hubblesite.org/api/v3/images"
 
COMMAND_DOWNLOAD_IMAGES = "download"
COMMAND_UPLOAD_IMAGES = "upload"

def download_image(image_url, file_name):
  response = requests.get(image_url)
  response.raise_for_status()
  with open(file_name, 'wb') as file:
      file.write(response.content)

def fetch_spacex_last_launch(images_dir):
  links = []
  response = requests.get(SPACEX_URL)  
  response.raise_for_status()
  
  links = response.json()["links"]["flickr_images"]
   
  for index, url in enumerate(links):
    download_image(
	  url,
	  "{}/spacex{}.{}".format(images_dir, index, get_extension(url))
	)

def fetch_hubble_image_by_id(id, images_dir):
  links = []
  response = requests.get("{}/{}".format(HUBBLE_IMAGE_URL, id))
  response.raise_for_status()
  
  for image_file in response.json()["image_files"]:
    links.append(image_file["file_url"])
  
  last_index = len(links)-1
  url = links[last_index]
  download_image(
    url,
	"{}/hubble{}.{}".format(images_dir, id, get_extension(url))
  )

def get_extension(url):
  return url.split(".")[-1]

def fetch_hubble_images(collection_name, images_dir):
  response = requests.get(
    HUBBLE_IMAGES_URL, 
	{
      "page": "all",
      "collection_name": collection_name
    }
  )
  response.raise_for_status()
  for item in response.json():
    id = item["id"]
    fetch_hubble_image_by_id(id, images_dir)
	
def fetch_images(images_dir):
  collection_name = "spacecraft"  
  fetch_spacex_last_launch(images_dir)
  fetch_hubble_images(collection_name, images_dir)

def publish_image(bot, image):
  bot.upload_photo(image, caption = "Uploaded by Instabot!") 

def publish_images(images_dir):
  bot = get_bot()
  for file_name in listdir(images_dir):
    publish_image(bot, "{}/{}".format(images_dir, file_name))
	
def get_bot():
  bot = Bot() 
  bot.login(
	username = getenv("USER_INSTAGRAM"),
	password = getenv("PASS_INSTAGRAM"),
	proxy = None
  )
  return bot

def main():
  load_dotenv()
  images_dir = getenv("IMAGES_DIR")
  makedirs(images_dir, exist_ok = True)
  parser = argparse.ArgumentParser(description='Program description')  
  parser.add_argument('-command', help='Command to perform: "download" or "upload"')
  args = parser.parse_args()
  command = args.command
    
  if command == COMMAND_DOWNLOAD_IMAGES:
    try:
      fetch_images(images_dir)
    except requests.exceptions.HTTPError as error:
      exit(format(error))
  elif command == COMMAND_UPLOAD_IMAGES:
    publish_images(images_dir)
  else:
    print("Command not recognised. Use argument -h for help.")
  
  print("Exit program.")

if __name__ == "__main__":
  main()
