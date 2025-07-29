import logging

from zeep import Client

from .currencies import GPAY_CURRENCIES

_log = logging.getLogger("pygestpay")

GPAY_S2S_PRODUCTION_URL = "https://ecomms2s.sella.it/gestpay/gestpayws/WSs2s.asmx?WSDL"
GPAY_S2S_TEST_URL = "https://sandbox.gestpay.net/gestpay/gestpayws/WSs2s.asmx?WSDL"

GPAY_CD_PRODUCTION_URL = (
    "https://ecommS2S.sella.it/gestpay/GestPayWS/WsCryptDecrypt.asmx?wsdl"
)
GPAY_CD_TEST_URL = (
    "https://sandbox.gestpay.net/gestpay/GestPayWS/WsCryptDecrypt.asmx?wsdl"
)

GPAY_PAYMENT_PAGE_PRODUCTION_URL = (
    "https://ecomm.sella.it/pagam/pagam.aspx?a={shop_login}&b={crypted_string}"
)
GPAY_PAYMENT_PAGE_TEST_URL = (
    "https://sandbox.gestpay.net/pagam/pagam.aspx?a={shop_login}&b={crypted_string}"
)

GPAY_DEFAULT_CURRENCY = GPAY_CURRENCIES["EUR"]["UICCode"]


class GestpayException(Exception):
    pass


class GestPAY(object):
    def __init__(self, shop_login, test=False, debug=False, apikey=None):
        self.debug = debug
        self.ws_s2s_url = GPAY_S2S_TEST_URL if test else GPAY_S2S_PRODUCTION_URL
        self.ws_cd_url = GPAY_CD_TEST_URL if test else GPAY_CD_PRODUCTION_URL
        self.payment_page_url = (
            GPAY_PAYMENT_PAGE_TEST_URL if test else GPAY_PAYMENT_PAGE_PRODUCTION_URL
        )
        self.shop_login = shop_login
        self.apikey = apikey

        try:
            self.s2s_client = Client(self.ws_s2s_url)
        except Exception as e:
            raise Exception(
                "GestPay WsS2S Endpoint not reachable: {} {}".format(self.ws_s2s_url, e)
            )

        try:
            self.cd_client = Client(self.ws_cd_url)
        except Exception as e:
            raise Exception(
                "GestPay WsCD Endpoint not reachable: {} {}".format(self.ws_cd_url, e)
            )

    def _prepare_request(self):
        data = {}
        data["shopLogin"] = self.shop_login

        return data

    #######################################################
    ## Crypt/Decrypt Methods
    #######################################################

    def encrypt(
        self,
        amount,
        transaction_id,
        buyer_name=None,
        buyer_email=None,
        language_id=None,
        info=None,
        order_details=None,
        trans_details=None,
        currency=GPAY_DEFAULT_CURRENCY,
    ):
        data = self._prepare_request()
        data["amount"] = amount
        data["shopTransactionId"] = transaction_id
        data["uicCode"] = currency

        if buyer_name:
            data["buyerName"] = buyer_name
        if buyer_email:
            data["buyerEmail"] = buyer_email
        if language_id:
            data["languageId"] = language_id
        if order_details:
            data["orderDetails"] = order_details
        if trans_details:
            data["transDetails"] = trans_details

        if self.debug:
            _log.info("GESTPAY: Encrypt")
            _log.info(data)

        return self.make_cd_request("Encrypt", data)

    def decrypt(self, crypted_string):
        data = self._prepare_request()
        data["CryptedString"] = crypted_string

        if self.debug:
            _log.info("GESTPAY: Decrypt")
            _log.info(data)

        return self.make_cd_request("Decrypt", data)

    def _generate_payment_page_url(self, crypted_string):
        data = {"shop_login": self.shop_login, "crypted_string": crypted_string}
        return self.payment_page_url.format(**data)

    def get_payment_page_url(self, **kwargs):
        data = self.encrypt(**kwargs)

        if data["TransactionResult"] == "OK":
            crypted_string = data["CryptDecryptString"]
            return self._generate_payment_page_url(crypted_string)

        raise GestpayException(data)

    #######################################################
    ## S2S Method
    #######################################################

    def card_transaction(
        self,
        amount,
        transaction_id,
        card_number,
        exp_month,
        exp_year,
        currency=GPAY_DEFAULT_CURRENCY,
        buyer_name=None,
        buyer_email=None,
        trans_details=None,
    ):
        data = self._prepare_request()
        data["amount"] = amount
        data["shopTransactionId"] = transaction_id
        data["cardNumber"] = card_number
        data["expiryMonth"] = exp_month
        data["expiryYear"] = exp_year
        data["uicCode"] = currency

        if buyer_name:
            data["buyerName"] = buyer_name
        if buyer_email:
            data["buyerEmail"] = buyer_email
        if trans_details:
            data["transDetails"] = trans_details

        if self.debug:
            _log.info("GESTPAY: Card Transaction")
            _log.info(data)

        return self.make_s2s_request("callPagamS2S", data)

    def token_transaction(
        self,
        amount,
        transaction_id,
        token,
        currency=GPAY_DEFAULT_CURRENCY,
        buyer_name=None,
        buyer_email=None,
        trans_details=None,
    ):
        data = self._prepare_request()
        data["amount"] = amount
        data["shopTransactionId"] = transaction_id
        data["tokenValue"] = token
        data["uicCode"] = currency

        if buyer_name:
            data["buyerName"] = buyer_name
        if buyer_email:
            data["buyerEmail"] = buyer_email
        if trans_details:
            data["transDetails"] = trans_details

        if self.debug:
            _log.info("GESTPAY: Token Transaction")
            _log.info(data)

        return self.make_s2s_request("callPagamS2S", data)

    def read_transaction(self, transaction_id, bank_transaction_id=False):
        data = self._prepare_request()
        data["shopTransactionId"] = transaction_id
        if bank_transaction_id:
            data["bankTransactionId"] = bank_transaction_id

        if self.debug:
            _log.info("GESTPAY: Read Transaction")
            _log.info(data)

        return self.make_s2s_request("CallReadTrxS2S", data)

    def delete_transaction(self, transaction_id, bank_transaction_id=False):
        data = self._prepare_request()
        data["shopTransactionId"] = transaction_id
        if bank_transaction_id:
            data["bankTransactionId"] = bank_transaction_id

        return self.make_s2s_request("CallDeleteS2S", data)

    def refund_transaction(
        self,
        amount,
        transaction_id,
        bank_transaction_id,
        currency=GPAY_DEFAULT_CURRENCY,
        **kwargs
    ):
        data = self._prepare_request()
        data["amount"] = amount
        data["shopTransactionId"] = transaction_id
        data["bankTransactionId"] = bank_transaction_id
        data["uicCode"] = currency

        for key, value in kwargs.items():
            data[key] = value

        if self.debug:
            _log.info("GESTPAY: Refund Transaction")
            _log.info(data)

        return self.make_s2s_request("CallRefundS2S", data)

    def settle_transaction(
        self,
        amount,
        transaction_id,
        bank_transaction_id=False,
        currency=GPAY_DEFAULT_CURRENCY,
    ):
        data = self._prepare_request()
        data["amount"] = amount
        data["uicCode"] = currency
        data["shopTransID"] = transaction_id
        if bank_transaction_id:
            data["bankTransID"] = bank_transaction_id

        if self.debug:
            _log.info("GESTPAY: Settle Transaction")
            _log.info(data)

        return self.make_s2s_request("CallSettleS2S", data)

    def verify_card(
        self, card_number, exp_month, exp_year, cvv=False, transaction_id=False
    ):
        data = self._prepare_request()
        data["cardNumber"] = card_number
        data["expMonth"] = exp_month
        data["expYear"] = exp_year
        if cvv:
            data["CVV2"] = cvv
        if transaction_id:
            data["shopTransactionId"] = transaction_id

        if self.debug:
            _log.info("GESTPAY: Verify Card")
            _log.info(data)

        return self.make_s2s_request("callVerifycardS2S", data)

    def check_card(
        self,
        card_number,
        exp_month,
        exp_year,
        cvv=False,
        transaction_id=False,
        card_auth="N",
    ):
        data = self._prepare_request()
        data["cardNumber"] = card_number
        data["expMonth"] = exp_month
        data["expYear"] = exp_year
        if cvv:
            data["CVV2"] = cvv
        if transaction_id:
            data["shopTransactionId"] = transaction_id

        data["withAuth"] = card_auth

        if self.debug:
            _log.info("GESTPAY: Check Card")
            _log.info(data)

        return self.make_s2s_request("callCheckCartaS2S", data)

    def check_token(self, card_token, transaction_id=False, card_auth="N"):
        data = self._prepare_request()
        data["tokenValue"] = card_token
        if transaction_id:
            data["shopTransactionId"] = transaction_id
        data["withAuth"] = card_auth

        if self.debug:
            _log.info("GESTPAY: Check Token")
            _log.info(data)

        return self.make_s2s_request("callCheckCartaS2S", data)

    def update_token(self, card_token, exp_month, exp_year, card_auth="N"):
        data = self._prepare_request()
        data["token"] = card_token
        data["expiryMonth"] = exp_month
        data["expiryYear"] = exp_year
        data["withAut"] = card_auth

        if self.debug:
            _log.info("GESTPAY: Update Token")
            _log.info(data)

        return self.make_s2s_request("CallUpdateTokenS2S", data)

    def request_token(self, card_number, exp_month, exp_year, cvv=False, card_auth="N"):
        data = self._prepare_request()
        data["requestToken"] = "MASKEDPAN"
        data["cardNumber"] = card_number
        data["expiryMonth"] = exp_month
        data["expiryYear"] = exp_year

        if cvv:
            data["cvv"] = cvv

        data["withAuth"] = card_auth

        if self.apikey:
            data["apikey"] = str(self.apikey).strip()

        if self.debug:
            _log.info("GESTPAY: Request Token")
            _log.info(data)

        return self.make_s2s_request("CallRequestTokenS2S", data)

    def delete_token(self, card_token):
        data = self._prepare_request()
        data["tokenValue"] = card_token

        if self.debug:
            _log.info("GESTPAY: Delete Token")
            _log.info(data)

        return self.make_s2s_request("callDeleteTokenS2S", data)

    def make_s2s_request(self, method, data):
        return self.make_request(self.s2s_client, "GestPayS2S", method, data)

    def make_cd_request(self, method, data):
        return self.make_request(self.cd_client, "GestPayCryptDecrypt", method, data)

    def make_request(self, client, key, method, data):
        try:
            response_data = getattr(client.service, method)(**data)
            response = elem2dict(response_data)
            if not response:
                raise Exception("%s key does not exist in response" % key)
        except Exception as e:
            response = {
                "TransactionResult": "KO",
                "TransactionType": "",
                "ErrorCode": "-1",
                "ErrorDescription": "Token service not available ({})".format(e),
            }

        if self.debug:
            _log.info("GESTPAY: Response %s" % method)
            _log.info(response)

        return response


def elem2dict(node):
    """
    Convert an lxml.etree node tree into a dict.
    """
    d = {}
    for e in node.iterchildren():
        key = e.tag.split("}")[1] if "}" in e.tag else e.tag
        value = e.text if e.text else elem2dict(e)
        d[key] = value
    return d
