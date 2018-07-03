"""app.py"""

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

@app.route('/health')
def health():
    return "healthy", 200

class CaptionGenerator(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument("date",
                                    required=True,
                                    location="json",
                                    type=str)

        super(CaptionGenerator, self).__init__()

    def post(self):
        return 'hello', 200

api.add_resource(CaptionGenerator, "/generate_caption")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug='True')
