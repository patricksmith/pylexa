from datetime import datetime, timedelta
from urlparse import urlparse
import base64

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence
from dateutil import parser, tz
from flask import request
from OpenSSL import crypto
import requests

from pylexa.exceptions import InvalidRequest


DOWNLOADED_CERTS = {}


def is_cert_chain_url_valid():
    url = request.headers.get('SignatureCertChainUrl')
    if not url:
        return False
    parsed_url = urlparse(url)
    if parsed_url.scheme.lower() != 'https':
        return False
    if parsed_url.hostname.lower() != 's3.amazonaws.com':
        return False
    if not parsed_url.path.startswith('/echo.api/'):
        return False
    if parsed_url.port and parsed_url.port != 443:
        return False
    return True


def is_within_time_tolerance():
    timestamp = request.json.get('request', {}).get('timestamp')
    tolerance = 150
    try:
        request_time = parser.parse(timestamp)
    except (AttributeError, ValueError):
        return False
    now = datetime.now(tz.tzutc())
    return now - request_time < timedelta(seconds=tolerance)


def verify_signature():
    headers = request.headers
    if 'signature' not in headers:
        return False

    cert_url = headers.get('SignatureCertChainUrl')
    pubkey = DOWNLOADED_CERTS.get(cert_url)
    if not pubkey:
        print 'downloading cert at', cert_url
        st_cert = requests.get(headers.get('SignatureCertChainUrl')).text
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, st_cert)
        pubkey = cert.get_pubkey()
        DOWNLOADED_CERTS[cert_url] = pubkey

    encoded_signature = headers.get('signature')
    decoded_signature = base64.decodestring(encoded_signature)

    src = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pubkey)
    pub_der = DerSequence()
    pub_der.decode(src)
    key = RSA.construct((long(pub_der._seq[1]), long(pub_der._seq[2])))

    request_body = request.get_data()
    h = SHA.new(request_body)

    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, decoded_signature)


def verify_request():
    if not is_cert_chain_url_valid():
        raise InvalidRequest('Cert chain URL not valid.')
    if not is_within_time_tolerance():
        raise InvalidRequest('Request timestamp too old')
    try:
        if not verify_signature():
            raise InvalidRequest('Could not verify request signature')
    except Exception:
        raise InvalidRequest('Unknown error verifying request signature')
