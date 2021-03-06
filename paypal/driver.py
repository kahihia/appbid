# -*- coding: utf-8 -*-

# Pluggable PayPal NVP (Name Value Pair) API implementation for Django.
# This file includes the PayPal driver class that maps NVP API methods to such simple functions.

# Feel free to distribute, modify or use any open or closed project without any permission.

# Author: Ozgur Vatansever
# Email: ozgurvt@gmail.com


import urllib
from django.conf import settings
import urlparse
import collections
import httplib

# Exception messages
TOKEN_NOT_FOUND_ERROR = "PayPal error occured. There is no TOKEN info to finish performing PayPal payment process. We haven't charged your money yet."
NO_PAYERID_ERROR = "PayPal error occured. There is no PAYERID info to finish performing PayPal payment process. We haven't charged your money yet."
GENERIC_PAYPAL_ERROR = "There occured an error while performing PayPal checkout process. We apologize for the inconvenience. We haven't charged your money yet."
GENERIC_PAYMENT_ERROR = "Transaction failed. Check out your order details again."
GENERIC_REFUND_ERROR = "An error occured, we can not perform your refund request"


class PayPal(object):
    """
    Pluggable Python PayPal Driver that implements NVP (Name Value Pair) API methods.
    There are simply 3 main methods to be executed in order to finish the PayPal payment process.
    You explicitly need to define PayPal username, password and signature in your project's settings file.
    
    Those are:
    1) SetExpressCheckout
    2) GetExpressCheckoutDetails (optional)
    3) DoExpressCheckoutPayment
    """
    
    def __init__(self, debug=False):
        # PayPal Credientials
        
        # You can use the following api credientials for DEBUGGING. (in shell)

        # First step is to get the correct credientials.
        if debug or getattr(settings, "PAYPAL_DEBUG", False):
            self.username = "me_api1.rulong.org"
            self.password = "1380869543"
            self.sign = "A2vypYAyoKWCr5HKJHXEzqAil0rBANhDLrGYeKZ-H8Wjmb.OShNvkwhY"
            self.AP_APPLICATION_ID = "APP-80W284485P519543T"
            self.AP_REDIRECTURL = "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_ap-payment&paykey="
            self.AP_ENDPOINT = "svcs.sandbox.paypal.com"
        else:
            self.username = getattr(settings, "PAYPAL_USER", None)
            self.password = getattr(settings, "PAYPAL_PASSWORD", None)
            self.sign = getattr(settings, "PAYPAL_SIGNATURE", None)
            self.AP_APPLICATION_ID = getattr(settings, "PAYPAL_AP_APPLICATION_ID", None)
            self.AP_REDIRECTURL = "https://www.paypal.com/webscr?cmd=_ap-payment&paykey="
            self.AP_ENDPOINT = "svcs.paypal.com"

        self.credientials = {
            "USER": self.username,
            "PWD": self.password,
            "SIGNATURE": self.sign,
            "VERSION": "53.0",
        }
        # Second step is to set the API end point and redirect urls correctly.
        if debug or getattr(settings, "PAYPAL_DEBUG", False):
            self.NVP_API_ENDPOINT = "https://api-3t.sandbox.paypal.com/nvp"
            self.PAYPAL_REDIRECT_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token="

        else:
            self.NVP_API_ENDPOINT = "https://api-3t.paypal.com/nvp"
            self.PAYPAL_REDIRECT_URL = "https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token="

        # initialization
        self.signature = urllib.urlencode(self.credientials) + '&'
        self.setexpresscheckouterror = None
        self.getexpresscheckoutdetailserror = None
        self.doexpresscheckoutpaymenterror = None
        self.refundtransactionerror = None
        self.apierror = None
        self.api_response = None
        self.token = None
        self.response = None
        self.refund_response = None

    def _get_value_from_qs(self, qs, value):
        """
        Gets a value from a querystring dict
        This is a private helper function, so DO NOT call this explicitly.
        """
        raw = qs.get(value)
        if type(raw) == list:
            try:
                return raw[0]
            except KeyError:
                return None
        else:
            return raw

    def paypal_url(self, token=None):
        """
        Returns a 'redirect url' for PayPal payments.
        If token was null, this function MUST NOT return any URL.
        """
        token = token if token is not None else self.token
        if not token:
            return None
        return self.PAYPAL_REDIRECT_URL + token

    def SetExpressCheckout(self, amount, currency, return_url, cancel_url, **kwargs):
        """
        To set up an Express Checkout transaction, you must invoke the SetExpressCheckout API
        to provide sufficient information to initiate the payment flow and redirect to PayPal if the
        operation was successful.

        @currency: Look at 'https://cms.paypal.com/us/cgi-bin/?cmd=_render-content&content_ID=developer/e_howto_api_nvp_currency_codes'
        @amount : should be string with the following format '10.00'
        @return_url : should be in the format scheme://hostname[:uri (optional)]
        @cancel_url : should be in the format scheme://hostname[:uri (optional)]

        @returns bool

        If you want to add extra parameters, you can define them in **kwargs dict. For instance:
         - SetExpressCheckout(10.00, US, http://www.test.com/cancel/, http://www.test.com/return/, **{'SHIPTOSTREET': 'T Street', 'SHIPTOSTATE': 'T State'})
        """
        initParam = kwargs.get('initParam')
        parameters = {
            'METHOD': 'SetExpressCheckout',
            'NOSHIPPING': 0,#no need shipping address
            # 'PAYMENTACTION': 'Sale',
            'PAYMENTACTION': 'Sale',
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
            'AMT': amount,
            # 'PAYMENTREQUEST_0_AMT': amount,
            'CURRENCYCODE': currency,
            'DESC': initParam.get('DESC', ''),
            # 'INVNUM': '1000'  #invoice number
            # 'ALLOWNOTE': 1,
            # 'SOLUTIONTYPE'=Sole
            # 'order': 'Appswalk service fee',
            # 'L_PAYMENTREQUEST_0_NUMBER0': 10001,
            'PAYMENTREQUEST_0_DESC': initParam.get('PAYMENTREQUEST_0_DESC', ''),
            # 'L_PAYMENTREQUEST_0_AMT0':30,
            'ITEMAMT': initParam.get('ITEMAMT', amount),

            # &PAYMENTREQUEST_0_SHIPPINGAMT=3.00
            'L_NAME0': initParam.get('L_NAME0', ''),
            'L_DESC0': initParam.get('L_DESC0', ''),
            'L_AMT0': initParam.get('L_AMT0', amount),
            # 'L_PAYMENTREQUEST_0_NUMBER0':'10100',
            'L_QTY0': initParam.get('L_QTY0', '1'),
            'L_PAYMENTREQUEST_0_ITEMCATEGORY0': 'Digital',
            # &PAYMENTREQUEST_0_SHIPDISCAMT=-3.00
            # &PAYMENTREQUEST_0_INSURANCEAMT=1.00
        }
        
        parameters.update(kwargs)
        query_string = self.signature + urllib.urlencode(parameters)
        response = urllib.urlopen(self.NVP_API_ENDPOINT, query_string).read()
        response_dict = urlparse.parse_qs(response)
        self.api_response = response_dict
        state = self._get_value_from_qs(response_dict, "ACK")
        if state in ["Success", "SuccessWithWarning"]:
            self.token = self._get_value_from_qs(response_dict, "TOKEN")
            return True

        self.setexpresscheckouterror = GENERIC_PAYPAL_ERROR
        self.apierror = self._get_value_from_qs(response_dict, "L_LONGMESSAGE0")
        return False

    """
    If SetExpressCheckout is successfull use TOKEN to redirect to the browser to the address BELOW:
    
     - https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=TOKEN (for development only URL)

    """

    def GetExpressCheckoutDetails(self, return_url, cancel_url, token=None):
        """
        This method performs the NVP API method that is responsible from getting the payment details.
        This returns True if successfully fetch the checkout details, otherwise returns False.
        All of the parameters are REQUIRED.

        @returns bool
        """
        token = self.token if token is None else token
        if token is None:
            self.getexpresscheckoutdetails = TOKEN_NOT_FOUND_ERROR
            return False

        parameters = {
            'METHOD': "GetExpressCheckoutDetails",
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
            'TOKEN': token,
        }
        query_string = self.signature + urllib.urlencode(parameters)
        response = urllib.urlopen(self.NVP_API_ENDPOINT, query_string).read()
        response_dict = urlparse.parse_qs(response)
        self.api_response = response_dict
        state = self._get_value_from_qs(response_dict, "ACK")
        if not state in ["Success", "SuccessWithWarning"]:
            self.getexpresscheckoutdetailserror = self._get_value_from_qs(response_dict, "L_SHORTMESSAGE0")
            self.apierror = self.getexpresscheckoutdetailserror
            return False
        return True

    def DoExpressCheckoutPayment(self, currency, amount, token=None, payerid=None):
        """
        This method performs the NVP API method that is responsible from doing the actual payment.
        All of the parameters are REQUIRED.
        @currency: Look at 'https://cms.paypal.com/us/cgi-bin/?cmd=_render-content&content_ID=developer/e_howto_api_nvp_currency_codes'
        @amount : should be string with the following format '10.00'
        @token : token that will come from the result of SetExpressionCheckout process.
        @payerid : payerid that will come from the url when PayPal redirects you after SetExpressionCheckout process.
        @returns bool
        """
        if token is None:
            self.doexpresscheckoutpaymenterror = TOKEN_NOT_FOUND_ERROR
            return False

        if payerid is None:
            self.doexpresscheckoutpaymenterror = NO_PAYERID_ERROR
            return False

        parameters = {
            'METHOD': "DoExpressCheckoutPayment",
            'PAYMENTACTION': 'Sale',
            'TOKEN': token,
            'AMT': amount,
            'CURRENCYCODE': currency,
            'PAYERID': payerid,
        }
        query_string = self.signature + urllib.urlencode(parameters)
        response = urllib.urlopen(self.NVP_API_ENDPOINT, query_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
        for key in response_tokens.keys():
            response_tokens[key] = urllib.unquote(response_tokens[key])

        state = self._get_value_from_qs(response_tokens, "ACK")
        self.response = response_tokens
        self.api_response = response_tokens
        if not state in ["Success", "SuccessWithWarning"]:
            self.doexpresscheckoutpaymenterror = GENERIC_PAYMENT_ERROR
            self.apierror = self._get_value_from_qs(response_tokens, "L_LONGMESSAGE0")
            return False
        return True

    def RefundTransaction(self, transid, refundtype, currency=None, amount=None, note="Dummy note for refund"):
        """
        Performs PayPal API method for refund.
        
        @refundtype: 'Full' or 'Partial'

        Possible Responses:
         {'ACK': 'Failure', 'TIMESTAMP': '2009-12-13T09:51:19Z', 'L_SEVERITYCODE0': 'Error', 'L_SHORTMESSAGE0':
         'Permission denied', 'L_LONGMESSAGE0': 'You do not have permission to refund this transaction', 'VERSION': '53.0',
         'BUILD': '1077585', 'L_ERRORCODE0': '10007', 'CORRELATIONID': '3d8fa24c46c65'}

         or
    
         {'REFUNDTRANSACTIONID': '9E679139T5135712L', 'FEEREFUNDAMT': '0.70', 'ACK': 'Success', 'TIMESTAMP': '2009-12-13T09:53:06Z',
         'CURRENCYCODE': 'AUD', 'GROSSREFUNDAMT': '13.89', 'VERSION': '53.0', 'BUILD': '1077585', 'NETREFUNDAMT': '13.19',
         'CORRELATIONID': '6c95d7f979fc1'}
        """

        if not refundtype in ["Full", "Partial"]:
            self.refundtransactionerror = "Wrong parameters given, We can not perform your refund request"
            return False
        
        parameters = {
            'METHOD': "RefundTransaction",
            'TRANSACTIONID': transid,
            'REFUNDTYPE': refundtype,
        }
        
        if refundtype == "Partial":
            extra_values = {
                'AMT': amount,
                'CURRENCYCODE': currency,
                'NOTE': note
            }
            parameters.update(extra_values)

        query_string = self.signature + urllib.urlencode(parameters)
        response = urllib.urlopen(self.NVP_API_ENDPOINT, query_string).read()
        response_tokens = {}
        for token in response.split('&'):
            response_tokens[token.split("=")[0]] = token.split("=")[1]
            
        for key in response_tokens.keys():
            response_tokens[key] = urllib.unquote(response_tokens[key])

        state = self._get_value_from_qs(response_tokens, "ACK")
        self.refund_response = response_tokens
        self.api_response = response_tokens
        if not state in ["Success", "SuccessWithWarning"]:
            self.refundtransactionerror = GENERIC_REFUND_ERROR
            return False
        return True

    def GetPaymentResponse(self):
        return self.response

    def GetRefundResponse(self):
        return self.refund_response

    #add new method to return details info
    def GetExpressCheckoutDetailsInfo(self, return_url, cancel_url, token=None):
        """
        This method performs the NVP API method that is responsible from getting the payment details.
        This returns True if successfully fetch the checkout details, otherwise returns False.
        All of the parameters are REQUIRED.

        @returns bool
        """
        token = self.token if token is None else token
        if token is None:
            self.getexpresscheckoutdetails = TOKEN_NOT_FOUND_ERROR
            return False

        parameters = {
            'METHOD': "GetExpressCheckoutDetails",
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
            'TOKEN': token,
        }
        query_string = self.signature + urllib.urlencode(parameters)
        response = urllib.urlopen(self.NVP_API_ENDPOINT, query_string).read()
        response_dict = urlparse.parse_qs(response)
        self.api_response = response_dict
        state = self._get_value_from_qs(response_dict, "ACK")
        return response_dict

    #method to handle adaptive payment
    def setAPCall(self, currency, return_url, cancel_url, action_type='PAY', **kwargs):
    #Set our headers
        initParam = kwargs.get('initParam')
        headers = {
            'X-PAYPAL-SECURITY-USERID': self.username,
            'X-PAYPAL-SECURITY-PASSWORD': self.password,
            'X-PAYPAL-SECURITY-SIGNATURE': self.sign,
            'X-PAYPAL-APPLICATION-ID': self.AP_APPLICATION_ID,
            'X-PAYPAL-SERVICE-VERSION': '1.1.0',
            'X-PAYPAL-REQUEST-DATA-FORMAT': 'NV',
            'X-PAYPAL-RESPONSE-DATA-FORMAT': 'NV'
        }

        ###################################################################
        # In the above $headers declaration, the USERID, PASSWORD and
        # SIGNATURE need to be replaced with your own.
        ###################################################################

        #Set our POST Parameters
        params = collections.OrderedDict()
        params['requestEnvelope.errorLanguage'] = 'en_US'
        params['requestEnvelope.detailLevel'] = 'ReturnAll'
        # params['reverseAllParallelPaymentsOnError'] = 'true'
        params['returnUrl'] = return_url
        params['cancelUrl'] = cancel_url
        params['actionType'] = action_type
        params['currencyCode'] = currency
        params['feesPayer'] = 'EACHRECEIVER'
        params['receiverList.receiver(0).email'] = initParam.get('appsWalk_account')
        params['receiverList.receiver(0).amount'] = initParam.get('appsWalk_amount')
        #  params['receiverList.receiver(1).primary'] = 'true'

        params['receiverList.receiver(1).email'] = initParam.get('seller_account')
        params['receiverList.receiver(1).amount'] = initParam.get('seller_amount')


        #Add Client Details
        params['clientDetails.ipAddress'] = '127.0.0.1'
        params['clientDetails.deviceId'] = 'mydevice'
        params['clientDetails.applicationId'] = 'PayNvpDemo'
        enc_params = urllib.urlencode(params)

        #Connect to sand box and POST.
        conn = httplib.HTTPSConnection(self.AP_ENDPOINT)
        conn.request("POST", "/AdaptivePayments/Pay/", enc_params, headers)
        #Check the response - should be 200 OK.
        response = conn.getresponse()

        #Get the reply and print it out.
        data = response.read()
        response_dic = urlparse.parse_qs(data)
        return response_dic

    def check_ap_payment_status(self, paykey):
        headers = {
            'X-PAYPAL-SECURITY-USERID': self.username,
            'X-PAYPAL-SECURITY-PASSWORD': self.password,
            'X-PAYPAL-SECURITY-SIGNATURE': self.sign,
            'X-PAYPAL-APPLICATION-ID': self.AP_APPLICATION_ID,
            'X-PAYPAL-SERVICE-VERSION': '1.1.0',
            'X-PAYPAL-REQUEST-DATA-FORMAT': 'NV',
            'X-PAYPAL-RESPONSE-DATA-FORMAT': 'NV'
        }

        ###################################################################
        # In the above $headers declaration, the USERID, PASSWORD and
        # SIGNATURE need to be replaced with your own.
        ###################################################################

        #Set our POST Parameters
        params = collections.OrderedDict()
        params['payKey'] = paykey
        params['requestEnvelope.errorLanguage'] = 'en_US'
        enc_params = urllib.urlencode(params)

        #Connect to sand box and POST.
        conn = httplib.HTTPSConnection(self.AP_ENDPOINT)
        conn.request("POST", "/AdaptivePayments/PaymentDetails/", enc_params, headers)
        #Check the response - should be 200 OK.
        response = conn.getresponse()

        #Get the reply and print it out.
        data = response.read()
        response_dic = urlparse.parse_qs(data)
        result = response_dic
        return result

    def paypal_ap_url(self, pay_key=None):
        """
        Returns a 'redirect url' for PayPal pay.
        If pay_key was null, this function MUST NOT return any URL.
        """
        if not pay_key:
            return None
        return self.AP_REDIRECTURL + pay_key