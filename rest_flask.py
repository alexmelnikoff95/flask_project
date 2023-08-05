import json

from flask import Flask, request
from pydantic import BaseModel
from werkzeug import Response

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///your_database.db')
Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)

class ResponseTestModel(Base):
    __tablename__ = 'response_tests'

    id = Column(Integer, primary_key=True)
    date = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, date, name):
        self.date = date
        self.name = name

class ResponseTest(BaseModel):
    date: int
    name: str

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        'date': 123,
        'name': 'aelx'
    }
    res = ResponseTest(**data)
    return Response(response=res.json(), content_type='application/json', status=200)

@app.route('/req', methods=['POST', 'GET'])
def req():
    if request.method == 'POST':
        data = request.json
        res = ResponseTest(**data)
        session = Session()
        session.add(ResponseTestModel(**data))
        session.commit()
        return Response(response=json.dumps({'ok': True}), content_type='application/json', status=200)
    return Response(response=json.dumps({'ok': True}), content_type='application/json', status=200)

if __name__ == '__main__':
    app.run(debug=True)
