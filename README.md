# pydeeplearn-demo
## Introduction
Online CNN demo on handwritten digits using HTML5 canvas and server-side job queueing (and long polling). Might still be here: http://pydeeplearn-demo.herokuapp.com/
## Requirements
* Numpy and Cython
* Pillow
* Flask, gevent, and gunicorn
* rq and redis (for the job queue)
* and of course pydeeplearn (and a pre-trained mnist.pkl)
