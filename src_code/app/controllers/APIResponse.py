from abc import ABC, abstractmethod
from app.libraries.Logger import Logger
from app.helpers.CommonHelper import CommonClass
from datetime import datetime
import json
from app.config.config import settings
from typing import Dict, Any, Optional

class APIResponseBase(ABC):
    """Abstract base class for API responses."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Returns the API response as a dictionary."""
        ...

    @staticmethod
    @abstractmethod
    def error(msg: str, code: int = 401, msg_code: Optional[str] = None) -> Dict[str, Any]:
        """Creates an error API response."""
        ...

    @staticmethod
    @abstractmethod
    def success(msg: str, data: Optional[Any] = None, code: int = 200, msg_code: Optional[str] = None) -> Dict[str, Any]:
        """Creates a success API response."""
        ...


class APIResponse(APIResponseBase):
    """Concrete class for API responses."""

    def __init__(self, status: str, code: int, msg: str, data: Optional[Any] = None, msg_code: Optional[str] = None, date_time: Optional[str] = None, txn_id: Optional[int] = None, client_id: Optional[str] = None):
        self.status = status
        self.code = code
        self.msg = msg
        self.msg_code = msg_code
        self.timestamp = CommonClass.current_time()
        self.request_id = Logger.get_instance().uuid
        self.encryption_required_client_ids = settings.ENCRYPTION_REQUIRED_CLIENT_IDS.split('|') if settings.ENCRYPTION_REQUIRED_CLIENT_IDS else []
        self.client_id = client_id
        self.data = self._encrypt_data(data) if data is not None else None
        self.now = datetime.now()
        self.formatted_now = self.now.strftime("%d/%m/%Y %H:%M:%S")
        self.date_time = date_time
        self.txn_id = txn_id


    def _encrypt_data(self, data: Optional[Any], client_id: Optional[str] = None) -> Optional[str]:
        """Encrypts the data if encryption is enabled."""
        if isinstance(data, (dict, list, int, float, bool)):
            data_str = json.dumps(data)
        elif isinstance(data, str): #handle string input as well
            data_str = data
        else:
            data_str = str(data)
        
        if settings.API_ENCRYPTED:
            return CommonClass.encrypt_aes(data_str)
        elif self.client_id in self.encryption_required_client_ids and self.client_id is not None:
            return CommonClass.encrypt_aes(data_str)
        else:
            return data

    def to_dict(self) -> Dict[str, Any]:
        """Returns the API response as a dictionary."""
        response_dict = {
            'status': self.status,
            'code': self.code,
            'request_id': self.request_id
        }
        
        if self.status == 'success':
            response_dict['secure'] = settings.API_ENCRYPTED or False
            response_dict['message'] = self.msg
        else:
            response_dict['error_description'] = self.msg

        if self.msg_code:
            response_dict['response_code'] = self.msg_code

        if self.date_time:
            response_dict['date_time'] = self.formatted_now
        else:
            response_dict['timestamp'] = self.timestamp

        if self.txn_id:
            response_dict['txn_id'] = self.txn_id

        if self.status != 'error' and self.data is not None:
            response_dict['data'] = self.data

        return response_dict


    @staticmethod
    def error(msg: str, code: int = 401, msg_code: Optional[str] = None, date_time: Optional[bool] = None, txn_id: Optional[int] = None) -> Dict[str, Any]:
        """Creates an error API response."""
        response = APIResponse(
            status='error',
            code=code,
            msg_code=msg_code,
            msg=msg,
            txn_id=txn_id,
            date_time=date_time
        )
        logger = Logger.get_instance()
        logger.log_critical(response.to_dict())
        return response.to_dict()

    @staticmethod
    def success(msg: str, data: Optional[Any] = None, code: int = 200, msg_code: Optional[str] = None, date_time: Optional[bool] = None, return_only_data: bool = False, txn_id: Optional[int] = None, client_id: Optional[str] = None) -> Dict[str, Any]:
        """Creates a success API response."""
        response = APIResponse(
            status='success',
            code=code,
            msg_code=msg_code,
            msg=msg,
            txn_id=txn_id,
            data=data,
            date_time=date_time,
            client_id=client_id
        )
        # Check if only the 'data' field should be returned
        if return_only_data:
            return response.to_dict().get("data", {})
        return response.to_dict()