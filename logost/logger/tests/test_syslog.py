from django.test import TestCase

from logost.logger.models import SyslogLoggerServer


class SyslogLoggerServerTestCase(TestCase):
    def test_message_constructed_as_bytelike_object(self):
        """
        Test if constructed message is a byte-like object
        """
        logger = SyslogLoggerServer()
        message = logger._construct_message('this is a test', 0)

        self.assertIsInstance(message, bytes)

    def test_message_constructed_with_break_line(self):
        """
        Test if constructed message container a break line at the end
        """
        logger = SyslogLoggerServer()
        message = logger._construct_message('this is a test', 0)

        self.assertRegex(message.decode(), '\n$')
