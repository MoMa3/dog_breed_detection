from flask import Flask, request, jsonify, render_template, send_from_directory, url_for
import os
from yolo_inference import get_most_confident_prediction

app = Flask(__name__)

UPLOAD_FOLDER = 'upload_folder'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_prediction', methods=['GET', 'POST'])
def get_breed_prediction():
    if request.method == 'POST':
        if 'my_image' not in request.files:
            return jsonify(error="No file part"), 400

        img = request.files['my_image']

        if img.filename == '':
            return jsonify(error="No selected file"), 400

        if img and allowed_file(img.filename):
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
            img.save(img_path)
            prediction = get_most_confident_prediction(img_path)
            image_url = url_for('uploaded_file', filename=img.filename)
            return jsonify(prediction=prediction, image_url=image_url)
        else:
            return jsonify(error="File not allowed"), 400

    return '''
    <!doctype html>
    <title>Upload an Image</title>
    <h1>Upload an image for prediction</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=my_image>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# main driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)