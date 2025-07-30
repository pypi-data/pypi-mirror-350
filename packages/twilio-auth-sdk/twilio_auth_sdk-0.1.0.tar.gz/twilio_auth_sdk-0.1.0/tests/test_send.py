import unittest
import twilio_auth
from unittest.mock import patch, MagicMock

class TestSendWhatsApp(unittest.TestCase):
    
    @patch("twilio_auth.send_whatsapp.client.messages.create")
    def test_send_whatsapp_success(self, mock_create):
        # Arrange: Set up mock return value
        mock_message = MagicMock()
        mock_message.sid = "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        mock_create.return_value = mock_message

        # Act: Call the function
        twilio_auth.send_whatsapp.send_message(
            from_="whatsapp:+14155238886",
            to="whatsapp:+2348130000000",
            body="Your code is 123456")

        # Assert: Ensure the message was "sent"
        mock_create.assert_called_once_with(
            body="Your code is 123456",
            from_="whatsapp:+14155238886",
            to="whatsapp:+2348130000000"
        )

if __name__ == '__main__':
    unittest.main()
