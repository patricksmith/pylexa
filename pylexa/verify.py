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


def is_cert_chain_url_valid(url):
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


def is_within_time_tolerance(timestamp):
    tolerance = 150
    try:
        request_time = parser.parse(timestamp)
    except (AttributeError, ValueError) as ex:
        return False
    now = datetime.now(tz.tzutc())
    return now - request_time < timedelta(seconds=tolerance)


def get_pubkey_from_cert(cert_chain_url):
    if cert_chain_url in DOWNLOADED_CERTS:
        return DOWNLOADED_CERTS[cert_chain_url]

    st_cert = requests.get(cert_chain_url).text
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, st_cert)
    pubkey = cert.get_pubkey()
    DOWNLOADED_CERTS[cert_chain_url] = pubkey
    return pubkey


def get_verifier(pubkey):
    src = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pubkey)
    pub_der = DerSequence()
    pub_der.decode(src)
    key = RSA.construct((long(pub_der._seq[1]), long(pub_der._seq[2])))
    return PKCS1_v1_5.new(key)


def verify_signature(signature, cert_chain_url, request_body):
    pubkey = get_pubkey_from_cert(cert_chain_url)
    verifier = get_verifier(pubkey)

    decoded_signature = base64.decodestring(signature)

    request_hash = SHA.new(request_body)
    return verifier.verify(request_hash, decoded_signature)


def verify_request():
    cert_chain_url = request.headers.get('SignatureCertChainUrl')
    if not is_cert_chain_url_valid(cert_chain_url):
        raise InvalidRequest('Cert chain URL not valid.')

    timestamp = request.json.get('request', {}).get('timestamp')
    if not is_within_time_tolerance(timestamp):
        raise InvalidRequest('Request timestamp too old')

    try:
        signature = request.headers.get('Signature')
        request_body = request.get_data()
        if not signature or not verify_signature(signature, cert_chain_url, request_body):
            raise InvalidRequest('Could not verify request signature')
    except Exception as ex:
        raise InvalidRequest('Could not verify request signature')
