# dvmn-instagram

Command line tool for the work with Instagram API. The program was created as an assigment for the course "[APIs of web services](https://dvmn.org/modules/web-api/)" from DevMan.

### Installation

After Python3 and pip are installed, run following command:

```pip install -r requirements.txt```

### Purpose

The program can be used to download images from Hubble and SpaceX and publish them on Instagram.

Valid commands are:

```python main.py -c download```

```python main.py -command download```

```python main.py -c upload```

```python main.py -command upload```

### Important note

In current state this program isn't working, because InstaBot library 0.26.0 has a bug (look at traceback):

```
2019-04-16 22:20:32,496 - INFO - Instabot Started
2019-04-16 22:20:33,527 - INFO - Logged-in successfully as 'DevmanTest'!
Analizing `images/hubble3804.jpg`
FOUND w:4288, h:2848, ratio=1.5056179775280898
Horizontal image
Resizing image
Saving new image w:1080 h:718 to `images/hubble3804.jpg.CONVERTED.jpg`
FOUND: w:1080 h:718 r:1.5041782729805013
Traceback (most recent call last):
  File "main.py", line 108, in <module>
    main()
  File "main.py", line 101, in main
    publish_images(images_dir)
  File "main.py", line 75, in publish_images
    publish_image(bot, "{}/{}".format(images_dir, file_name))
  File "main.py", line 70, in publish_image
    bot.upload_photo(image, caption = "Uploaded by Instabot!")
  File "C:\Users\###\Anaconda3\lib\site-packages\instabot\bot\bot.py", line 489, in upload_photo
    return upload_photo(self, photo, caption, upload_id, from_video)
  File "C:\Users\###\Anaconda3\lib\site-packages\instabot\bot\bot_photo.py", line 9, in upload_photo
    if self.api.upload_photo(photo, caption, upload_id, from_video):
  File "C:\Users\###\Anaconda3\lib\site-packages\instabot\api\api.py", line 266, in upload_photo
    return upload_photo(self, photo, caption, upload_id, from_video)
  File "C:\Users\###\Anaconda3\lib\site-packages\instabot\api\api_photo.py", line 120, in upload_photo
    rename(photo, "{}.REMOVE_ME".format(photo))
PermissionError: [WinError 32] Der Prozess kann nicht auf die Datei zugreifen, da sie von einem anderen Prozess verwendet wird: 'images/hubble3804.jpg.CONVERTED.jpg' -> 'images/hubble3804.jpg.CONVERTED.jpg.REMOVE_ME'
2019-04-16 22:20:43,765 - INFO - Bot stopped. Worked: 0:00:11.285040
2019-04-16 22:20:43,765 - INFO - Total requests: 5
```

You could use an older version (for example 0.4.5) to get it work.

```pip install --upgrade instabot==0.4.5```