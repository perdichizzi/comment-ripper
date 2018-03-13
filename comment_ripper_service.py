import os
import comment_ripper
import pymysql
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/code'
ALLOWED_EXTENSIONS = {'txt', 'c', 'cpp', 'cbl', 'ini'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

host = os.environ.get('HOST', '0.0.0.0')
port = int(os.environ.get('PORT', 5000))

mysql_host = os.environ.get('MYSQL_HOST', 'mysql-comment')
mysql_user = os.environ.get('MYSQL_USER', 'root')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'password')
mysql_database = os.environ.get('MYSQL_DATABASE', 'comments')


def init_configuration():
    # Create folder if it doesn't exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + '/output',
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            app.logger.warning("File not selected, please provide a file.")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            app.logger.warning("File not selected, please provide a file.")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            language = "COBOL"

            language_config = comment_ripper.ConfigFile().get_language_config(language)
            if language_config is None:
                raise Exception("'%s' is not a valid language" % language)

            parser = comment_ripper.CommentParserAction(language_config)
            parser.start(comment_ripper.File(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

            # DATA QUERY - START
            conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_database)
            # conn = pymysql.connect(host="127.0.0.1:3308", user="root", password="password", db="comments")

            with conn.cursor() as cur:
                sql = 'INSERT INTO files (name) VALUES (%s);'

                try:
                    cur.execute(sql, (filename))
                    conn.commit()
                except:
                    conn.rollback()

            conn.close()
            # DATA QUERY - END

            return redirect(url_for('uploaded_file',
                                    filename=filename))
        if file and not allowed_file(file.filename):
            app.logger.warning("Extension not valid, please select another file.")
            return redirect(request.url)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1> 
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    # Start general configurations (folders, connection information, etc.)
    init_configuration()

    # Bind to port if defined, otherwise default to 5000
    app.run(host=host, port=port)
