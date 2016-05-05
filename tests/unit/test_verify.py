from datetime import datetime, timedelta
import base64
import unittest

from mock import Mock, patch

from pylexa.exceptions import InvalidRequest
from pylexa.verify import (
    get_pubkey_from_cert,
    get_verifier,
    is_cert_chain_url_valid,
    is_within_time_tolerance,
    verify_request,
    verify_signature,
)


class TestIsCertChainUrlValid(unittest.TestCase):

    def should_require_https(self):
        self.assertFalse(is_cert_chain_url_valid('http://s3.amazonaws.com/echo.api/'))

    def should_require_amazon_hostname(self):
        self.assertFalse(is_cert_chain_url_valid('https://s3.elsewhere.com/echo.api/'))

    def should_require_echo_api_path(self):
        self.assertFalse(is_cert_chain_url_valid('https://s3.amazonaws.com/foo.api/'))
        self.assertTrue(is_cert_chain_url_valid('https://s3.amazonaws.com/echo.api/more'))

    def should_check_port(self):
        self.assertFalse(is_cert_chain_url_valid('https://s3.amazonaws.com:8000/echo.api/'))

    def should_return_True_for_valid_url(self):
        self.assertTrue(is_cert_chain_url_valid('https://s3.amazonaws.com/echo.api/'))
        self.assertTrue(is_cert_chain_url_valid('https://s3.amazonaws.com:443/echo.api/'))


class TestIsWithinTimeTolerance(unittest.TestCase):

    format_string = '%Y-%m-%dT%H:%M:%SZ'

    def should_return_False_for_old_timestamp(self):
        old_time = datetime.utcnow() - timedelta(seconds=151)
        old_timestamp = old_time.strftime(self.format_string)
        self.assertFalse(is_within_time_tolerance(old_timestamp))

    def should_return_True_for_valid_timestamp(self):
        valid_time = datetime.utcnow() - timedelta(seconds=149)
        valid_timestamp = valid_time.strftime(self.format_string)
        self.assertTrue(is_within_time_tolerance(valid_timestamp))


class TestGetPubkeyFromCert(unittest.TestCase):

    def setUp(self):
        self.cert_mock = {}
        self.cert_patcher = patch('pylexa.verify.DOWNLOADED_CERTS', new=self.cert_mock)
        self.cert_patcher.start()

    def tearDown(self):
        self.cert_patcher.stop()

    def should_return_downloaded_cert_if_exists(self):
        self.cert_mock['foo'] = Mock()
        self.assertEqual(get_pubkey_from_cert('foo'), self.cert_mock['foo'])

    @patch('pylexa.verify.requests')
    @patch('pylexa.verify.crypto')
    def should_fetch_cert_if_not_cached(self, crypto, requests):
        cert_chain_url = 'http://example.foo'

        pubkey = get_pubkey_from_cert(cert_chain_url)

        requests.get.assert_called_once_with(cert_chain_url)
        crypto.load_certificate.assert_called_once_with(
            crypto.FILETYPE_PEM, requests.get.return_value.text)
        self.assertEqual(pubkey, crypto.load_certificate.return_value.get_pubkey.return_value)
        self.assertEqual(self.cert_mock[cert_chain_url], pubkey)


class TestGetVerifier(unittest.TestCase):

    @patch('pylexa.verify.PKCS1_v1_5')
    @patch('pylexa.verify.RSA')
    @patch('pylexa.verify.DerSequence')
    @patch('pylexa.verify.crypto')
    def should_construct_pkcs1_verifier_from_key(self, crypto, der_sequence, rsa, pkcs1):
        pubkey = Mock()
        verifier = get_verifier(pubkey)
        crypto.dump_privatekey.assert_called_once_with(crypto.FILETYPE_ASN1, pubkey)
        pkcs1.new.assert_called_once_with(rsa.construct.return_value)
        self.assertEqual(verifier, pkcs1.new.return_value)


class TestVerifySignature(unittest.TestCase):

    @patch('pylexa.verify.SHA')
    @patch('pylexa.verify.get_verifier')
    @patch('pylexa.verify.get_pubkey_from_cert')
    def should_verify_signature_and_request_hash(self, get_pubkey_from_cert, get_verifier, sha):
        verifier = get_verifier.return_value
        signature = 'BEEF'
        request_body = '{"request": "foo"}'
        result = verify_signature(signature, Mock(), request_body)

        verifier.verify.assert_called_once_with(
            sha.new(request_body), base64.decodestring(signature))
        self.assertEqual(result, verifier.verify.return_value)


class TestVerifyRequest(unittest.TestCase):

    def setUp(self):
        self.request_patcher = patch('pylexa.verify.request')
        self.request_mock = self.request_patcher.start()
        self.cert_chain_url = Mock()
        self.signature = Mock()
        self.request_mock.headers = {
            'SignatureCertChainUrl': self.cert_chain_url,
            'Signature': self.signature
        }
        self.timestamp = Mock()
        self.request_mock.json = {
            'request': {
                'timestamp': self.timestamp,
            },
        }

        self.is_cert_chain_url_valid_patcher = patch('pylexa.verify.is_cert_chain_url_valid')
        self.is_cert_chain_url_valid = self.is_cert_chain_url_valid_patcher.start()

        self.is_within_time_tolerance_patcher = patch('pylexa.verify.is_within_time_tolerance')
        self.is_within_time_tolerance = self.is_within_time_tolerance_patcher.start()

        self.verify_signature_patcher = patch('pylexa.verify.verify_signature')
        self.verify_signature = self.verify_signature_patcher.start()

    def tearDown(self):
        self.request_patcher.stop()
        self.is_cert_chain_url_valid_patcher.stop()
        self.is_within_time_tolerance_patcher.stop()
        self.verify_signature_patcher.stop()

    def should_raise_error_if_cert_chain_invalid(self):
        self.is_cert_chain_url_valid.return_value = False
        with self.assertRaises(InvalidRequest):
            verify_request()
        self.is_cert_chain_url_valid.assert_called_once_with(self.cert_chain_url)

    def should_raise_error_if_timestamp_not_valid(self):
        self.is_within_time_tolerance.return_value = False
        with self.assertRaises(InvalidRequest):
            verify_request()
        self.is_within_time_tolerance.assert_called_once_with(self.timestamp)

    def should_raise_error_if_no_signature(self):
        self.request_mock.headers['Signature'] = None
        with self.assertRaises(InvalidRequest):
            verify_request()

    def should_raise_error_if_signature_not_verified(self):
        self.verify_signature.return_value = False
        with self.assertRaises(InvalidRequest):
            verify_request()
        self.verify_signature.assert_called_once_with(
            self.signature, self.cert_chain_url, self.request_mock.get_data.return_value)

    def should_not_raise_error_when_valid(self):
        try:
            verify_request()
        except InvalidRequest:
            self.fail('InvalidRequest exception should not have been raised')
