from unittest import TestCase
from heaserver.service.db import awsservicelib
from botocore.exceptions import ClientError

import heaserver.service.db.aws


class TestAWSServiceLib(TestCase):

    def test_handle_client_error_404(self):
        c = ClientError(error_response={'Error': {'Code': heaserver.service.db.aws.CLIENT_ERROR_404}}, operation_name='foo')
        self.assertEqual(404, awsservicelib.handle_client_error(c).status)

    def test_handle_client_error_no_such_bucket(self):
        c = ClientError(error_response={'Error': {'Code': heaserver.service.db.aws.CLIENT_ERROR_NO_SUCH_BUCKET}}, operation_name='foo')
        self.assertEqual(404, awsservicelib.handle_client_error(c).status)

    def test_handle_client_error_unknown(self):
        c = ClientError(error_response={'Error': {'Code': "It's wrecked"}},
                        operation_name='foo')
        self.assertEqual(500, awsservicelib.handle_client_error(c).status)

