from flask import Flask
#from Master import Master

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/regist', methods=['POST'])
def regist():
    print()

if __name__ == '__main__':
    #Process To System
    app.run(debug=True)