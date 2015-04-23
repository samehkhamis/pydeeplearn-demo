import os, redis
from rq import get_current_job, Worker, Queue, Connection
from PIL import Image, ImageFilter
from io import BytesIO
import base64
import numpy as np
from pydeeplearn.net.cnn import CNN

pretrained_lenet = os.getenv('PRETRAINED_LENET', '/app/mnist.pkl')
cnn = CNN.load(pretrained_lenet)

def recognize(imb64):
    imb64 = imb64[imb64.find('base64,') + 7:]
    im = Image.open(BytesIO(base64.decodestring(imb64)))
    _, _, _, im = im.split()
    im.thumbnail((28, 28), Image.ANTIALIAS)
    arr = np.array(im)
    scores = cnn.predict(arr.reshape(arr.shape[0], arr.shape[1], 1))
    result = scores.argmax()
    
    # save the results
    job = get_current_job()
    job.meta['result'] = str(result)
    job.save()
    
    return True

listen = ['default']
redis_url = os.getenv('REDISCLOUD_URL', 'localhost')
redis_password = os.getenv('REDISCLOUD_PWD', 'password')
connection = redis.Redis(host=redis_url, port='12365', password=redis_password)

if __name__ == '__main__':
    with Connection(connection):
        worker = Worker(map(Queue, listen))
        worker.work()