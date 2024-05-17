# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,render_template, flash, request, redirect, url_for,Response,send_file
import os
from werkzeug.utils import secure_filename
import cv2


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS_IMAGE = {'png','webp','jpg','jpeg','jfif'}
ALLOWED_EXTENSIONS_VIDEO = {'mp4'}

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


#function to check for the correct file format
def allowed_file_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE
           
def allowed_file_video(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_VIDEO
           
def process_image(filename,opt):
    print(f"the operation is {opt} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match opt:
        case '1':
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
        case '2':
            imgProcessed = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
        case '3':
            imgProcessed = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            _, imgProcessed = cv2.threshold(imgProcessed, 80, 255, cv2.THRESH_TOZERO)
    newFilename = "static/images/result.jpg"
    cv2.imwrite(newFilename, imgProcessed)
    os.remove(os.path.join("uploads",filename))
    return newFilename


# Creating routes

#home page route
@app.route('/')
def home():
    return render_template("index.html")


#About page route
@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/image_edit')
def image_edit():
    option = [
    "Convert to GrayScale",
    "Convert to HSV",
    "Enhance Image"
    ]
    return render_template("imageedit.html",option = option)


#creating the image edit action route to return the edited image
@app.route('/editimage',methods = ['POST','GET'])
def editimage():
    if request.method == 'POST':
        operation = request.form.get("operation")
    #check if file is passed or not
    if 'file' not in request.files:
        flash('No file part')
        return 'error'
    # Reading the file
    file = request.files['file']
    if file.filename == '':
            flash('No selected file')
            return redirect('/image_edit')
    if file and allowed_file_image(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = process_image(filename, operation)
            flash(f"Your image has been processed")
            return redirect('/image_edit')
    
    

@app.route('/video_edit')
def video_edit():
    return render_template("videoedit.html")

@app.route('/downloadimage',methods = ['GET','POST'])
def downloadimg():
    path = os.path.join("static","images","result.jpg")
    return send_file(path, as_attachment=True)


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True, port=5001)