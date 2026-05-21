from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Jenkins CI/CD Pipeline!</h1><p>DevOps Project 05</p>'

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
