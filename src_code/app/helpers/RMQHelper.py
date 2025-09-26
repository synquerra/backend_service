import requests
from app.config.config import settings
from app.helpers.ErrorMessages import ErrorMessages
from app.helpers.ErrorCodes import ErrorCodes


class RMQHelper:
    """Helper class to send logs to RabbitMQ via HTTP API"""

    RMQ_API_URL = settings.LOG_RMQ_API_URL  # RabbitMQ API URL from settings

    def __init__(self):
        self.rmq_auth = settings.LOG_RMQ_AUTH  # Authorization token

    
    def send_log(self, queue_name: str, exchange_name: str, exchange_type: str, routing_key: str, data: dict):
        """Send error log to RabbitMQ queue via HTTP request"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"{self.rmq_auth}"
            }

            payload = {
                "queue_name": queue_name,  # Accepts queue_name explicitly
                "exchange_name": exchange_name,
                "exchange_type": exchange_type,
                "routing_key": routing_key,
                "data": data
            }

            response = requests.post(self.RMQ_API_URL, headers=headers, json=payload)
            
            if response.status_code == ErrorCodes.SUCCESS:
                return {
                    "status": ErrorMessages.SUCCESS,
                    "message": ErrorMessages.QUEUE_SUCCESSFUL_SENT,
                    "rmq_response": response.json()
                }
            else:
                return {
                    "status": ErrorMessages.ERROR,
                    "message": f"{ErrorMessages.ERROR_SENT_TO_QUEUE}: {response.text}"
                }
        except Exception as e:
            return {
                "status": ErrorMessages.ERROR,
                "message": f"{ErrorMessages.EXCEPTION_SENT_TO_QUEUE}: {str(e)}"
            }
