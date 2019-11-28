from apiclient.discovery import build
from PIL import Image
import requests
from io import BytesIO

class googleSearch(object):
    
    def __init__(self):
        self.service = build("customsearch", "v1", developerKey="developerKey")
        pass
    def searchObj(self, obj):
        res = self.service.cse().list(
            q=obj,
            cx='cx',
            searchType='image',
            num=1,
            fileType='jpeg',
            safe= 'off'
        ).execute()

        if not 'items' in res:
            print ('No result !!')
        else:
            for item in res['items']:
                response = requests.get(item['link'])
                img = Image.open(BytesIO(response.content))
                img.show()
        pass
