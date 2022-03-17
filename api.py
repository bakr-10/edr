from pymongo import MongoClient
from flask import Flask, request
from flask_restful import Resource, Api
from netmiko import ConnectHandler

client = MongoClient("mongodb+srv://bakrmo:0100_2967089Bm@cluster0.gg5rc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.edr

app = Flask(__name__)
api = Api(app)

class Machine(Resource):
    def post(self):
        data = request.get_json()
        inputs = {
            "device_type": "linux",
            "ip": data["ip"],
            "username": data["username"],
            "password": data["password"],
            "port": "22"
        }
        conn = ConnectHandler(**inputs)
        output = conn.send_command("find $PWD -type f -print | grep 'testfile'")
        intodb = {"path_of_specific_file": output, "ip_of_machine": data["ip"]}
        db.output.insert_one(intodb)

        return {"msg": "The machine has been added and commands have been sent"}

    def get(self):
        return db.output.find_one({}, { "_id":0 })

    def delete(self):
        data = request.get_json()
        db.output.delete_one({"ip_of_machine": data["ip"]})
        return {"msg": "The machine has been deleted"}


#class MachinesList(Resource):
    #def get(self, ip):
       # return db.output.find_one({ "ip_of_machine": ip }, { "_id":0 })


api.add_resource(Machine, '/edr') 
#api.add_resource(MachinesList, '/edr/<string:ip>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

#find specific file --->$ find $PWD -type f | grep "testfile", $ realpath "filename"
