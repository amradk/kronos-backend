from flask import Flask
from flask_restful import Resource, Api
from model import *

app = Flask(__name__)
api = Api(app)

class LocalityResource(Resource):
    def get(self, name):
        if name == '':
            return "Locality not found", 404
        query = Locality.select(Locality.id, Locality.type, Locality.guid, Locality.name, Locality.fedsubj_code, Locality.district).where(Locality.name == name)
        if len(query) > 0:
            localitys = []
            for l in query:
                localitys.append({
                    'Name':l.name,
                    'Type':l.type.type,
                    'GUID':l.guid,
                    'FedSubjCode':l.fedsubj_code.code,
                    'FedSubjType':l.fedsubj_code.type.type,
                    'FedSubjName':l.fedsubj_code.name,
                    'District':l.district.name,
                    'MSK_TZ':l.district.msk_tz,
                    'UTC_TZ':l.district.utc_tz,
                })
        else:
            return "Locality not found", 404

        return localitys

class LocalityInFedSubjResource(Resource):
    def get(self, code, name):
        if (name == '' or code == ''):
            return "Locality not found", 404
        if code != 0:
            code = abs(int(code))
        else:
            return "Locality not found", 404
        query = Locality.select(Locality.id, Locality.type, Locality.guid, Locality.name, 
                Locality.fedsubj_code, Locality.district).where((Locality.name == name) & (Locality.fedsubj_code == code))
        if len(query) > 0:
            localitys = []
            for l in query:
                localitys.append({
                    'Name':l.name,
                    'Type':l.type.type,
                    'GUID':l.guid,
                    'FedSubjCode':l.fedsubj_code.code,
                    'FedSubjType':l.fedsubj_code.type.type,
                    'FedSubjName':l.fedsubj_code.name,
                    'District':l.district.name,
                    'MSK_TZ':l.district.msk_tz,
                    'UTC_TZ':l.district.utc_tz,
                })
        else:
            return "Locality not found", 404

        return localitys

class FedSubjResource(Resource):
    def get(self, name):
        if name == '':
            return "FedSubj not found", 404
        if name.isnumeric():
            fedsubj_code = abs(int(name))
            if fedsubj_code != 0:
                query = FedSubj.select(FedSubj.id, FedSubj.guid, FedSubj.code, FedSubj.name, FedSubj.type).where(FedSubj.code == fedsubj_code)
            elif fedsubj_code == 0: 
                query = FedSubj.select(FedSubj.id, FedSubj.guid, FedSubj.code, FedSubj.name, FedSubj.type)
        else:
            query = FedSubj.select(FedSubj.id, FedSubj.guid, FedSubj.code, FedSubj.name, FedSubj.type).where(FedSubj.name == name)
        if len(query) > 0:
            fedsubjs = []
            for f in query:
                fedsubjs.append({
                    'Name':f.name,
                    'Type':f.type.type,
                    'GUID':f.guid,
                    'Code':f.code,
                })
        else:
            return "FedSubj not found", 404

        return fedsubjs

api.add_resource(LocalityResource, '/locality/<string:name>')
api.add_resource(LocalityInFedSubjResource, '/locality/<int:code>/<string:name>')
api.add_resource(FedSubjResource, '/fedsubj/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)
