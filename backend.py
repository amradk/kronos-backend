from flask import Flask
from flask_restful import Resource, Api
from model import *

app = Flask(__name__)
api = Api(app)

class LocalityResource(Resource):
    def get(self, name):
        if name == '':
            return "Locality not found", 404
        query = Locality.select(Locality.id, Locality.type, Locality.name, Locality.fedsubj_code, Locality.district).where(Locality.name == name)
        if len(query) > 0:
            localitys = []
            for l in query:
                localitys.append({
                    'name':l.name,
                    'type':l.type.type,
                    'fedsubj':l.fedsubj_code.code,
                    'district':l.district.name,
                    'msk_tz':l.district.msk_tz,
                    'utc_tz':l.district.utc_tz,
                })
        else:
            return "Locality not found", 404

        return localitys

api.add_resource(LocalityResource, '/locality/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)