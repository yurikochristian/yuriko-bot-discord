import youtube_dl
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import wikipedia
import random
def chat(pesan):
    url = "https://wsapi.simsimi.com/190410/talk"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': os.getenv('simi_token')
    }
    data = """
    {
                "utext": "%s",
                "lang": "id"
        }
    """
    res = requests.post(url, data=data % (pesan), headers=headers)
    data = res.json()
    
    return "Dah abis gan"

def knowledge(thing):
    return wikipedia.summary(thing)

def search(arg):
    YDL_OPTIONS = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            requests.get(arg)
        except:
            video = ydl.extract_info(f"ytsearch:{arg}",
                                     download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)
    print(video['webpage_url'])
    return video['webpage_url']

def kerang_ajaib(question):
    num = random.randint(1,1000)%3
    if(num == 0):
        return "Iya"
    elif(num == 1):
        return "Nggak"
    else:
        return "Hm, mungkin..."