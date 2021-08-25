# load and evaluate a saved model
import numpy as np
from keras.models import load_model
 
# load model
model = load_model('mymodel2.h5')
# summarize model.
# model.summary()
# load dataset
for i in range(-381, 381, 50):
    for j in range(-381, 381, 50):
        print(i, j)
        x_test = np.reshape([0, 0, i, j], (1, 4))
        pred = model.predict(x_test)
        print(np.argmax(pred[0]))
