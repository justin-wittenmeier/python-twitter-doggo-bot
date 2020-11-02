import requests
from PIL import Image
from io import BytesIO
import cv2
import tweepy
import time

# ------------------------------Doggo Bot------------------------------

#gets image from api
def dogImage():
    r = requests.get('https://dog.ceo/api/breeds/image/random')
    json_data = r.json()
    b = requests.get(json_data['message'])
    img = Image.open(BytesIO(b.content))
    img = img.convert('RGB')
    img.save(' {IMAGE FILE PATH} ', format = 'jpeg')

#checks if any faces are in image
def detectDoggoFace():
    check = cv2.imread(' {IMAGE FILE PATH} ')
    grey_scale = cv2.cvtColor(check, cv2.COLOR_BGR2GRAY)
    check_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    face_check = check_cascade.detectMultiScale(grey_scale, scaleFactor=1.1, minNeighbors=5)
    if len(face_check) == 0: return False
    return True

#post image to twitter
def makeDoggoTweet(post_number):
    auth = tweepy.OAuthHandler(' {TWITTER INFO} ',' {TWITTER INFO} ')
    auth.set_access_token(' {TWITTER INFO} ',' {TWITTER INFO} ')
    api = tweepy.API(auth, wait_on_rate_limit=True)
    api.update_with_media(' {IMAGE FILE PATH} ', status=f'Doggo Post: {post_number}\n#gooddog')

#run doggo bot
def doggoBot(post_number):
    dogImage()
    if detectDoggoFace(): doggoBot(post_number)
    else: makeDoggoTweet(post_number)

def likeTweets():
    bot_id = # Set this to the accounts ID to prevent it from liking its own tweets
    auth = tweepy.OAuthHandler(' {TWITTER INFO} ',' {TWITTER INFO} ')
    auth.set_access_token(' {TWITTER INFO} ',' {TWITTER INFO} ')
    api = tweepy.API(auth, wait_on_rate_limit=True)
    blacklist = ['k9', 'biden' , 'trump', 'police', 'officer']
    already_liked = []
    like_list = set()
    tag_list = ['#gooddog','#puppy','#dog']
 
    for x in range(1,3):
        for i in api.favorites(count = 75, page = x):
            already_liked.append(i.id)
        
        time.sleep(1)

    for x in tag_list:
        for i in api.search(x,count = 30):
            if i.user.id != bot_id and not any(x in i.text.lower().split(' ') for x in blacklist) and i.id not in already_liked:
                try:
                    api.create_favorite(i.id)
                    time.sleep(1)
                except tweepy.TweepError:
                    pass
    time.sleep(1)
#------------------------------------------------------------------------------------------------------------------------------------------------------

#get number from file and update file as + 1
def postCounter():
    with open(' {POST NUMBER FILE} ', 'r') as read_f: #You will need to create a .txt file with 0 as the starting number.
        x = read_f.read()
    x = int(x) + 1
    x = str(x)
    with open(' {POST NUMBER FILE} ', 'w') as write_f:
        write_f.write(x)
    return int(x)

#------------------------------------------------------------------------------------------------------------------------------------------------------
def runBot():
    x = postCounter()
    doggoBot(x)
    time.sleep(1)
    likeTweets()

runBot()
