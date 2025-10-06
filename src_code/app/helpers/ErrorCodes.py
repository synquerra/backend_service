class ErrorCodes:
   
   """
   ErrorCodes class to define unique error codes for the application.

    Instructions for developers:
    - Ensure each error code is unique and follows the format 'E_XXXX', 
    - where 'XXXX' is a four-digit identifier.
    - Do not reuse or redefine existing error codes to avoid conflicts.
    - New error codes should be added in sequential order to maintain readability.
    - Variable names should be in all caps to indicate constants and follows the format with page name 'MN_0001' for main.py.
    - Use descriptive names for better code understanding.
    - Review and update existing error codes as needed.
    - Check for any potential duplicate error codes if the class is modified.
    """
    
   # Common error codes
   SUCCESS = 200
   BAD_REQUEST = 400
   INTERNAL_SERVER_ERROR = 500
   NOT_FOUND = 404
   UNAUTHORIZED = 401
   TOO_MANY_REQUESTS = 429
   CONFLICT = 409
   UNPROCESSABLE_ENTITY = 422
   ACCEPTED = 202
   SERVICE_UNAVAILABLE = 503
   NOT_ALLOWED = 403