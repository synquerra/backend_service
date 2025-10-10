class ErrorMessages:
    # Common Messages
    INVALID_REQUEST = 'Invalid Request'
    INVALID_URL = 'Invalid URL provided.'
    HEALTH_CHECK = 'Health Check, OK'
    INVALID_RESPONSE = 'Invalid response.'
    INVALID_RESPONSE_ELK = 'Invalid response from Elasticsearch.'
    NO_RESPONSE_ELK = 'No response from Elasticsearch.'
    NOT_FOUND = 'The requested resource was not found.'
    PLEASE_TRY_AGAIN = 'Please try again later.'
    EXCEPTION_TRY_AGAIN = 'An unexpected error occurred. Please try again later.'
    NO_RECORD_EXIST = 'No records found'
    SUCCESS = 'Success'
    ERROR = 'Error'
    HMAC_EXPIRED = 'HMAC EXPIRED'
    HMAC_MISMATCHED = 'HMAC MISMATCHED'
    QUEUE_SUCCESSFUL_SENT = 'Data has been successfully inserted into the queue'
    ERROR_SENT_TO_QUEUE = 'Error inserting data into the queue'
    EXCEPTION_SENT_TO_QUEUE = 'Error inserting data into the queue'
    INVALID_SECRET_KEY = 'SECRET_KEY must be 32 bytes long for AES-256'
    RECORD_FOUND = 'Record found'
    
    ## 
    EMAIL_EXIST = "Email already registered"
    MOBILE_EXIST = "Mobile number already registered"
    USER_REGISTERED_SUCCESS = "User registered successfully"
    LOGIN_SUCCESS = "Login successful"
    LOGIN_FAILED = "Invalid email or password"
    