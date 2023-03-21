import requests
from io import BytesIO
import time
from PIL import UnidentifiedImageError
import warnings


class PlateClient:
    def __init__(self, url: str):
        self.url = url
    
    def readNumber(self, im) -> str:
        res = requests.post(
            f'{self.url}/readNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im)
        return res.json()['name']
    
    def getNumber(self, id) -> str:
        res = requests.get(f'{self.url}/getNumber?id={id}')
        return res.json()
    
    def getNumbers(self, ids) -> str:
        res = requests.get(f'{self.url}/getNumbers?ids={ids}')
        return res.json()


if __name__ == '__main__':
    client = PlateClient('http://127.0.0.1:8080/')
    res = client.getNumbers('10022-9965')
    print(res)

# if __name__ == '__main__':
#     client = PlateClient('http://127.0.0.1:8080/')
#     res = client.getNumber('10022')
#     print(res)

# if __name__ == '__main__':
#     client = PlateClient('http://127.0.0.1:8080/')
#     with open('images/10022.jpg', 'rb') as im:
#         res = client.getNumber(im)
#     print(res)