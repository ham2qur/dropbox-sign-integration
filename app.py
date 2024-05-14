import json
from pprint import pprint

from dropbox_sign import \
    Configuration
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from werkzeug.utils import redirect

from easypay import Gwapi

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
        """
            Step 1: Dropship sign will redirect the user to this endpoint after successful signing
            Step 2: This endpoint will render our checkout form.
        """

        # ye koi id aye gi dropbox sign se
        # id = request.data['id']

        # isko hum dropbox sign sdk se document fetch krna
        # document = dropbox.document(id)
        # amount = document['amount']

        # if document.status == 'signed':
        #   then only process payment


        data = {}

        data['amount'] = 1000
        # data['Customer'] = "Customer Name"
        data['sku'] = "1"
        data['qty'] = 1
        return render_template('payment.html', data=data)

    @app.route('/collect/payment', methods=['POST'])
    @cross_origin(support_credentials=False)
    def collect_payment():
        """
            Step 3: After submission from payment.html user would be submit to this form.
            Step 4: Call easypay to process payment with details received from the submitted form.
            Step 5: On success payment store the details to zapier.
            Step 6: Redirect back user to dropbox sign. (In step 1 maintain the incoming url.)
        """

        payment_data = request.form

        # Replace the security_key with your own
        gw = Gwapi()
        gw.setLogin("JDb8ggQzHTp34RKaFZEBpjfeaSVkjrH4")
        r = gw.doSale(payment_data['amount'], "4111111111111111", "1224", "999")
        print(gw.responses['response'])

        if int(gw.responses['response']) == 1:
            print("Approved")
            # Successfully payment hogyi
            # yahan zapier ki api call kr ke payment details save krdo
        elif int(gw.responses['response']) == 2:
            print("Declined")
        elif int(gw.responses['response']) == 3:
            print("Error")

        return redirect("https://www.hellosign.com")



if __name__ == "__main__":
    api.add_resource(DropboxSignIntegration)
    app.run()