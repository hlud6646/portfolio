import time
from flask import Flask, Response, render_template
from cameras.base_camera import Camera
from cameras import lasers, game_of_life, three_body, odes


# ---- Camera utilities and setup. - ---- ---- ---- ---- ---- ---- ----
def jpeg(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

cameras = { 'lasers':       Camera(lasers.gen,          fps=30),
            'game_of_life': Camera(game_of_life.gen,    fps=10),
            'three_body':   Camera(three_body.gen,      fps=80),
            'odes':         Camera(odes.gen,            fps=100)}
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

 

# ---- Flask setup. - ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<title>')
def page(title):
    return render_template(title + '.html')

@app.route('/stream/<title>')
def stream(title):
    cameras[title].poke()
    return Response(jpeg(cameras[title]), 
        mimetype='multipart/x-mixed-replace; boundary=frame')
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----




