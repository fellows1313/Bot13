#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


rentOptions = []

class RentOptions:
    def __init__(self, rentType, rentDescription):
        self.rentType = rentType
        self.rentDescription = rentDescription

rentOptions.append(RentOptions("DayPass", "Join us for a day for only $10.00!"))
rentOptions.append(RentOptions("HotDesk", "Come and go as you please for $75.00 a month"))
rentOptions.append(RentOptions("DedicatedDesk", "Your own personal desk available anytime for $300.00 a month"))
rentOptions.append(RentOptions("OfficeSpace", "Need a home for your startup? Office space starting as low as $500.00 a month"))


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = processRequest(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

# Process the request and generate the appropriate response based on the action
def processRequest(req):
    if req.get("result").get("action") != "displayRentInfo":
        return {}

    res = generateResult(req)
    return res

# Generate the result and return it in proper API.ai formatting
def generateResult(req):
    result = req.get("result")
    parameters = result.get("parameters")
    rentType = parameters.get("RentOptions") # This would be your value DayPass, HotDesk, etc.

    # Find the matching type in our array of rentOptions
    speechResponse = "Issue finding info about " + rentType
    textResponse = "Issue finding info about " + rentType
    for rentOption in rentOptions:
        if (rentOption.rentType == rentType):
            speechResponse = rentOption.rentType + " " + rentOption.rentDescription
            textResponse = rentOption.rentType + " - " + rentOption.rentDescription
            break


    return {
        "speech": speechResponse,
        "displayText": textResponse,
        # "data": {"slack": text},
        # "data": {"facebook": text},
        "source": "Bot13"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    app.run(debug=False, port=port, host='0.0.0.0')
