import os
import cv2
import json
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from tensorflow.keras.layers import Conv2D, Activation, BatchNormalization
from tensorflow.keras.layers import UpSampling2D, Input, Concatenate
from tensorflow.keras.models import Model , load_model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.metrics import Recall, Precision
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam

def UNet(height, width, n_channels):
    inputs = Input(shape=(height, width, 3), name="input_image")#(IMG_SIZE, IMG_SIZE, 3), name="input_image")

    encoder = MobileNetV2(input_tensor=inputs, weights="imagenet", include_top=False, alpha=0.50)
    skip_connection_list = ["input_image", "block_1_expand_relu", "block_3_expand_relu", "block_6_expand_relu"]
    encoder_output = encoder.get_layer("block_13_expand_relu").output

    fil = [48, 64, 96, 128]
    xt = encoder_output
    for i in range(1, len(skip_connection_list)+1, 1):
        xt_skip = encoder.get_layer(skip_connection_list[-i]).output
        xt = UpSampling2D((2, 2))(xt)
        xt = Concatenate()([xt, xt_skip])

        xt = Conv2D(fil[-i], (3, 3), padding="same")(xt)
        xt = BatchNormalization()(xt)
        xt = Activation("relu")(xt)

        xt = Conv2D(fil[-i], (3, 3), padding="same")(xt)
        xt = BatchNormalization()(xt)
        xt = Activation("relu")(xt)

    xt = Conv2D(1, (1, 1), padding="same")(xt)
    xt = Activation("sigmoid")(xt)

    model = Model(inputs, xt)
    return model

# 加载模型
model = UNet(height=256, width=256, n_channels=3)
model.load_weights(r'E:\\work\\unet语义分割\\DRRMSAN_NOTEBOOKS-main\\UNet\\LUNG\\models\\modelW_UNet_lung.h5')
print(model)

import numpy as np
X = []
Y = []


img = cv2.imread('./data/2d_images/ID_0002_Z_0162.tif', cv2.IMREAD_COLOR)
resized_img = cv2.resize(img,(256, 256), interpolation = cv2.INTER_CUBIC)
X.append(resized_img)

X = np.array(X)

yp = model.predict(x=X, batch_size=2, verbose=1)
yp = np.round(yp, 0)[0]


plt.figure(figsize=(20,10))
plt.subplot(1,3,1)
plt.imshow(X[0])
plt.title('Input')
plt.subplot(1,3,2)
plt.imshow(yp.reshape(yp.shape[0],yp.shape[1]))
plt.title('Prediction')
plt.show()
