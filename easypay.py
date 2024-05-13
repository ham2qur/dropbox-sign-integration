import requests as requests

class Gwapi:

    def __init__(self):
        self.login = {}
        self.order = {}
        self.billing = {}
        self.shipping = {}
        self.responses = {}

    def setLogin(self, security_key):
        self.login['security_key'] = security_key

    def setOrder(self, orderid, orderdescription, tax, shipping, ponumber, ipadress):
        self.order['orderid'] = orderid
        self.order['orderdescription'] = orderdescription
        self.order['shipping'] = '{0:.2f}'.format(float(shipping))
        self.order['ipaddress'] = ipadress
        self.order['tax'] = '{0:.2f}'.format(float(tax))
        self.order['ponumber'] = ponumber

    def setBilling(self, firstname, lastname, company, address1, address2, city, state, zip, country, phone, fax, email, website):
        self.billing['firstname'] = firstname
        self.billing['lastname'] = lastname
        self.billing['company'] = company
        self.billing['address1'] = address1
        self.billing['address2'] = address2
        self.billing['city'] = city
        self.billing['state'] = state
        self.billing['zip'] = zip
        self.billing['country'] = country
        self.billing['phone'] = phone
        self.billing['fax'] = fax
        self.billing['email'] = email
        self.billing['website'] = website

    def setShipping(self, firstname, lastname, company, address1, address2, city, state, zipcode, country, email):
        self.shipping['firstname'] = firstname
        self.shipping['lastname'] = lastname
        self.shipping['company'] = company
        self.shipping['address1'] = address1
        self.shipping['address2'] = address2
        self.shipping['city'] = city
        self.shipping['state'] = state
        self.shipping['zip'] = zipcode
        self.shipping['country'] = country
        self.shipping['email'] = email

    def doSale(self, amount, ccnumber, ccexp, cvv=''):
        url = "https://secure.easypaydirectgateway.com/api/transact.php"
        query = {
            'security_key': self.login['security_key'],
            'ccnumber': ccnumber,
            'ccexp': ccexp,
            'amount': '{0:.2f}'.format(float(amount)),
            'type': 'sale'
        }
        if cvv:
            query['cvv'] = cvv

        query.update(self.order)
        query.update(self.billing)
        query.update(self.shipping)

        response = requests.post(url, data=query)
        response_data = response.text.split('&')
        for item in response_data:
            key, value = item.split('=')
            self.responses[key] = value
        return self.responses['response']