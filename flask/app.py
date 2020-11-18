# import the necessary packages
from flask import Flask, render_template,  request, redirect
from flask_pymongo import PyMongo
import gridfs

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://jh:4110@cluster0.ju4sq.mongodb.net/playlist?retryWrites=true&w=majority'
mongo = PyMongo(app)

class State:
    def __init__(self):
        self.confirm = False
        self.fn = None

    def setConfirm(self, confirm):
        self.confirm = confirm

    def setFn(self, fn):
        self.fn =fn

    def getConfirm(self):
        return self.confirm

    def getFn(self):
        return self.fn

state = State()

@app.route('/', methods=['GET', 'POST'])
def index():
    state.setFn(None)
    return render_template('index.html', confirm=state.getConfirm())

@app.route('/file/<filename>')
def file(filename):
    mongo.send_file(filename)
    return mongo.send_file(filename)

@app.route('/profile/<filename>', methods=['GET', 'POST'])
def profile(filename):
    state.setFn(filename)
    name = mongo.db.list.find_one({'filename':filename})['name']
    fileid = mongo.db.fs.files.find_one({'filename':filename})['_id']
    n = name.find('초')
    if request.method == 'POST':
        if request.form.get('submit') == 'delete':
            if state.getConfirm() == True:
                fs = gridfs.GridFS(mongo.db)
                fs.delete(fileid)
                mongo.db.list.delete_one({'filename':filename})
                return redirect('/')
            else:
                return render_template('video.html', filename=filename,name=name[:n+1],name2=name[n+1:], confirm=state.getConfirm(), message='권한없음')

    return render_template('video.html', filename=filename,name=name[:n+1],name2=name[n+1:], confirm=state.getConfirm())

@app.route('/search', methods=['POST'])
def search():
    flist = []
    name = request.form['name'].lower()

    list = mongo.db.list.find({'name': {'$regex': name}})
    for file in list:
        flist.append([file['filename'], file['name']])
    return {'data' : flist}

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('submit') == 'login':
            search_id = mongo.db.manager.find_one({'uid':request.form.get('id')})
            if search_id == None:
                return render_template('login.html', message='id가 존재하지 않습니다.', fn=state.getFn())
            else:
                if search_id['pwd'] == request.form.get('pw'):
                    state.setConfirm(True)
                    if state.getFn() != None:
                        return redirect('/profile/'+state.getFn())
                    else:
                        return redirect('/')
                else:
                    return render_template('login.html', message='비밀번호가 틀렸습니다.', fn=state.getFn())
    return render_template('login.html', fn=state.getFn())

@app.route('/logout')
def logout():
    state.setConfirm(False)
    if state.getFn() != None:
        return redirect('/profile/' + state.getFn())
    else:
        return redirect('/')

if __name__ == '__main__':
    # defining server ip address and port
    app.run()