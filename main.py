import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder='assets', template_folder='templates')



@app.route('/')
def index():
    # video_list = get_video_list()
    # return render_template('index.html', video_list=video_list)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
