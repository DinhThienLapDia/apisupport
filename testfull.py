'''
Created on Jun 11, 2016

@author: admin
'''
from flask import Flask, request, Response, jsonify, json
import pymongo
from bson import ObjectId
import datetime

app = Flask(__name__)
client = pymongo.MongoClient()
db = client.testdatabase

@app.route('/newticket', methods=["POST"])
def newticket():
    try:
        data = request.form["user"].encode("utf-8")
        print data
        jsondata = json.loads(data)
        print jsondata
        #user = jsondata["user"]
        #text = jsondata["text"]
        time_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        replies = []
        #file = request.file("image")
        status = 0
        jsondata.update({"time_created":time_created,"status":status, "replies":replies})
        db.supportticket.insert(jsondata)
        return jsonify({"status":0})
    except Exception as e:
        return jsonify({"error":str(e)})

@app.route('/listticket', methods=["POST"])
def listticket():
    data = request.form["user"]
    print data
    jsondata = json.loads(data)
    print jsondata
    ticketlist = []
    cursor = db.supportticket.find(jsondata)
    for document in cursor:
        str_id = str(document["_id"])
        document["_id"]= str_id
        ticketlist.append(document)
    print ticketlist
    return jsonify({"tickets":ticketlist})
@app.route('/updateticket', methods=["POST"])
def updateticket():
    data = request.form["ticket"]
    print data
    jsondata = json.loads(data)
    print jsondata
    ticketid = ObjectId(jsondata["_id"])
    print ticketid
    ticket = db.supportticket.find_one({"_id":ticketid})
    print ticket
    replies_current = []
    if ticket["replies"] is not None:
        replies_current = ticket["replies"]
    else:
        replies_current = []
    print replies_current
    new_reply = json.loads(request.form["reply"])
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_reply.update({"time_replies":current_time})
    print new_reply
    replies_current.append(new_reply)
    print replies_current
    result = db.supportticket.update({"_id":ticketid}, {"$set":{"replies":replies_current}})
    if result:
        return jsonify({"return_code":0})
    else:
        return jsonify({"return_code":1})
@app.route('/closeticket', methods =['POST'])
def closeticket():
    data = request.form["ticket"]
    jsondata = json.loads(data)
    print jsondata
    ticketid = ObjectId(jsondata["_id"])
    print ticketid
    ticket = db.supportticket.find_one({"_id":ticketid})
    print ticket
    result = db.supportticket.update({"_id":ticketid}, {"$set":{"status":1}})
    if result:
        return jsonify({"return_code":0})
    else:
        return jsonify({"return_code":1})

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8287,debug=True, threaded=True)