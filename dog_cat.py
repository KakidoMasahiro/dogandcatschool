from flask import Flask, redirect, request, jsonify, render_template
from flask_cors import CORS
from keras import models
from keras.models import load_model
from keras.backend import tensorflow_backend as backend
from PIL import Image, ImageFile
import keras
import numpy as np
import sys, os, io
import glob
import tensorflow as tf

ImageFile.LOAD_TRUNCATED_IMAGES = True
app = Flask(__name__)
CORS(app)

imsize = (64, 64)
keras_param = "./cnn.h5"

def load_image(path):
    img = Image.open(path)
    img = img.convert('RGB')
    img = img.resize(imsize)
    img = np.asarray(img)
    img = img / 255.0

    backend.clear_session()
    # 2回以上連続してpredictするために必要な処理

    # 学習済みモデル(cnn.h5)を読み込み
    model = load_model(keras_param)

    # 読み込んだ画像をnumpyの配列に変換
    prd = model.predict(np.array([img]))

    # 配列の最大要素のインデックスを返しprelabelに代入します
    prelabel = np.argmax(prd, axis=1)

    return prelabel