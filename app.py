import json
from pprint import pprint

from dropbox_sign import \
    Configuration
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from werkzeug.utils import redirect

app = Flask(__name__)
CORS(app, support_credentials=True)
api = Api(app)

configuration = Configuration(
    # Configure HTTP basic authorization: api_key
    username="03c89a58d42b806ee55a4968f9af24382ae436f378a72d11e0f81651788cd326",

    # or, configure Bearer (JWT) authorization: oauth2
    # access_token="YOUR_ACCESS_TOKEN",
)

class DropboxSignIntegration(Resource):

    @app.route('/', methods=['GET'])
    @cross_origin(support_credentials=True)
    def helloWorld():

        # Replace the security_key with your own
        # gw = Gwapi()
        # gw.setLogin("checkout_public_wDb8q95zg479zA9GF3pGqr9U3TG2dm87")
        # gw.setBilling("John", "Smith", "Acme, Inc.", "123 Main St", "Suite 200", "Beverly Hills", "CA", "90210", "US",
        #               "555-555-5555", "555-555-5556", "support@example.com", "www.example.com")
        # gw.setShipping("Mary", "Smith", "na", "124 Shipping Main St", "Suite Ship", "Beverly Hills", "CA", "90210",
        #                "US", "support@example.com")
        # gw.setOrder("1234", "Big Order", 1, 2, "PO1234", "65.192.14.10")
        #
        # r = gw.doSale("5.00", "4111111111111111", "1212", '999')
        # print(gw.responses['response'])
        #
        # if int(gw.responses['response']) == 1:
        #     print("Approved")
        # elif int(gw.responses['response']) == 2:
        #     print("Declined")
        # elif int(gw.responses['response']) == 3:
        #     print("Error")

        return "Hello World"


    @app.route('/payment/callback', methods=['POST'])
    @cross_origin(support_credentials=True)
    def payment_callback():

        callback_data = json.loads(request.values['json'])
        pprint(callback_data)

        # Accessing the event data
        event_time = callback_data['event']['event_time']
        event_type = callback_data['event']['event_type'] # signature_request_sent
        event_hash = callback_data['event']['event_hash']
        reported_for_account_id = callback_data['event']['event_metadata']['reported_for_account_id']

        # Do something with the data, like logging it
        print("Received callback data:")
        print("Event Time:", event_time)
        print("Event Type:", event_type)
        print("Event Hash:", event_hash)
        print("Reported For Account ID:", reported_for_account_id)

        return "Hello API Event Received", 200


    @app.route('/checkout', methods=['GET'])
    def redirect_to_url():
        url = "https://collectcheckout.com/r/l7pyhm77gmg97udr8wd9dirxq2oxis"
        return redirect(url)

    @app.route("/checkout2", methods=['GET'])
    def collectCheckout():
        data = {}

        data['amount'] = 1000
        data['Customer'] = "Customer Name"
        data['sku'] = "0001"
        data['qty'] = 1
        return render_template('payment.html', data=data)


if __name__ == "__main__":
    api.add_resource(DropboxSignIntegration)
    app.run()