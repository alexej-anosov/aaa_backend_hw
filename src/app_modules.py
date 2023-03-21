import logging
import io
from PIL import UnidentifiedImageError
from flask import Flask, request
from models.plate_reader import PlateReader
import requests
from io import BytesIO

plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')

def read_plate_function(im):
    try:
        res = plate_reader.read_text(im)
    except UnidentifiedImageError:
        return {'error': 'invalid image'}, 400
    return {"plate": res}

def get_plate_function(id):
    res = requests.get(f'http://51.250.83.169:7878/images/{id}', timeout=3)
    if res.status_code < 400:
        print(res.status_code)
        im = BytesIO(res.content)
        plate = read_plate_function(im)['plate']
        return {id: plate}
    elif res.reason == 'NOT FOUND':
        return {'error': 'invalid id'}, 400
