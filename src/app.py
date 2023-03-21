import logging
import io
from PIL import UnidentifiedImageError
from flask import Flask, request
from models.plate_reader import PlateReader
from app_modules import *
import requests
from io import BytesIO


app = Flask(__name__)



# /readNumber <- img bin
# {"name": "a222a78"}
@app.route('/readNumber', methods=["POST"])
def read_number():
    body = request.get_data()
    im = io.BytesIO(body)
    return read_plate_function(im)

# /getNumber <- str
# ip.port/getNumber?id=12343
@app.route('/getNumber')
def get_number():
    id = request.args['id']
    return get_plate_function(id)

# посылаем все id через дефис
# /getNumbers <- str
# ip.port/getNumbers?id=12343-111111-6773
@app.route('/getNumbers')
def get_numbers():
    ids = list(request.args['ids'].split('-'))
    result = {}
    i = 0
    for id in ids:
        plate = get_plate_function(id)
        if  type(plate) is not dict:
            return {'error': f"id '{id}' not found"}, 400
        else:
            result[i] = plate
            i+=1
    return result



if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
