import requests, cv2, tweepy, os
from PIL import Image
from io import BytesIO

class TwitterHandler:
    def __init__(self):
        self.__file_path=os.path.dirname(os.path.realpath(__file__))
        self.__oauth=["TWITTER-OAUTH", "TWITTER-OAUTH"]
        self.__token=["TWITTER-TOKEN","TWITTER-TOKEN"]
        self.__auth=tweepy.OAuthHandler(self.__oauth[0],self.__oauth[1])
        self.__auth.set_access_token(self.__token[0],self.__token[1])
        self.__api=tweepy.API(self.__auth, wait_on_rate_limit=True)
        self.__bot_id=self.__api.me().id

    def makeTweet(self):
        post_number=FileHandler()
        self.__api.update_with_media(os.path.join(self.__file_path, "dog_image.jpg"), status=f'Doggo Post: {post_number.count}\n#gooddog')

    def likeTweets(self):
        blacklist=['k9', 'biden' , 'trump', 'police', 'officer', 'feral', 'tits', 'furry', 'adidas', 'kpop', 'post:', 'furryart', 'artistontwitter']
        already_liked=[j.id for i in range(1,3) for j in self.__api.favorites(count=75,page=i)]
        tag_list = ['#gooddog','#puppy','#dog']
        for i in tag_list:
            for j in self.__api.search(i,count=30):
                if j.user.id!=self.__bot_id and not any(i in j.text.lower().split() for i in blacklist) and j.id not in already_liked:
                    try:
                        self.__api.create_favorite(j.id)
                    except Exception:
                        pass

        for i in self.__api.mentions_timeline(count=25):
            if i.user.id!=self.__bot_id and not any(i in j.text.lower().split() for i in blacklist):
                try:
                    self.__api.create_favorite(i.id)
                except Exception:
                    pass

class ImageHandler:
    def __init__(self):
        self.__file_path=os.path.dirname(os.path.realpath(__file__))
        self.__url="https://dog.ceo/api/breeds/image/random"

    def fetchImage(self):
        image_url=requests.get(self.__url).json()["message"]
        img=Image.open(BytesIO(requests.get(image_url).content))
        img=img.convert("RGB")
        img.save(os.path.join(self.__file_path, "dog_image.jpg"), format='jpeg')
        if self.detectFace():
            fetchImage()
        
    def detectFace(self):
        check = cv2.imread(os.path.join(self.__file_path, "dog_image.jpg"))
        grey_scale = cv2.cvtColor(check, cv2.COLOR_BGR2GRAY)
        check_cascade = cv2.CascadeClassifier(os.path.join(self.__file_path, 'haarcascade_frontalface_alt.xml'))
        face_check = check_cascade.detectMultiScale(grey_scale, scaleFactor=1.1, minNeighbors=5)
        if len(face_check) == 0: return False
        return True

class FileHandler:
    def __init__(self):
        self.__file_path=os.path.dirname(os.path.realpath(__file__))
        self.count = self.__fetchPostNumber()
    
    def __fetchPostNumber(self):
        with open(os.path.join(self.__file_path, "counter.txt"), 'r') as read_f:
            x = read_f.read()
        x = int(x) + 1
        x = str(x)
        with open(os.path.join(self.__file_path, "counter.txt"), 'w') as write_f:
            write_f.write(x)
        return int(x)

class Bot:
    def __init__(self):
        self.run()    

    def run(self):
        img=ImageHandler()
        img.fetchImage()
        tweet=TwitterHandler()
        tweet.makeTweet()
        tweet.likeTweets()

if __name__=="__main__":
    bot = Bot()
