import time
from flask import Flask, Response, render_template, abort, send_from_directory
from jinja2.exceptions import TemplateNotFound
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
    try:
        return render_template(title + '.html')
    except TemplateNotFound as e:
        abort(404)

@app.route('/stream/<title>')
def stream(title):
    cameras[title].poke()
    return Response(jpeg(cameras[title]), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/blog/<title>')
def blog(title):
    try:
        return render_template('blog/' + title + '.html')
    except TemplateNotFound as e:
        abort(404)



@app.errorhandler(404)
def not_found_error(error):
    return render_template('/error/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('/error/500.html'), 500

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----




