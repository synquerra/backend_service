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

   # MN Prefix for main.py (main.py)
   MN_0001 = 'MNP001'
   MN_0002 = 'MNP002'
   MN_0003 = 'MNP003'
   MN_0004 = 'MNP004'
   MN_0005 = 'MNP005'
   MN_0006 = 'MNP006'
   MN_0007 = 'MNP007'
   MN_0008 = 'MNP008'
   MN_0009 = 'MNP009'
   MN_0010 = 'MNP010'

   # SA Prefix for StudentAccounts.py file
   SA_0001 = 'SA0001'
   SA_0002 = 'SA0002'

   # UE Prefix for UdiseEkyc.py file
   UE_0001 = 'UE0001'
   UE_0002 = 'UE0002'
   UE_0003 = 'UE0003'
   UE_0004 = 'UE0004'
   UE_0005 = 'UE0005'
   UE_0006 = 'UE0006'
   UE_0007 = 'UE0007'

   # UE Prefix for VerifyApaar.py file
   VA_0001 = 'VA0001'
   VA_0002 = 'VA0002'
   VA_0003 = 'VA0003'
   VA_0004 = 'VA0004'
   VA_0005 = 'VA0005'
   VA_0006 = 'VA0006'
   VA_0007 = 'VA0007'
   VA_0008 = 'VA0008'
   VA_0009 = 'VA0009'
   VA_0010 = 'VA0010'
   VA_0011 = 'VA0011'
   VA_0012 = 'VA0012'
   VA_0013 = 'VA0013'
   VA_0014 = 'VA0014'
   VA_0015 = 'VA0015'

   # CSC Prefix for CSCServiceByApaar.py file

   CSC_0001 = 'CSC0001'
   CSC_0002 = 'CSC0002'
   CSC_0003 = 'CSC0003'
   CSC_0004 = 'CSC0004'
   CSC_0005 = 'CSC0005'
   CSC_0006 = 'CSC0006'
   CSC_0007 = 'CSC0007'
   CSC_0008 = 'CSC0008'
   CSC_0009 = 'CSC0009'
   CSC_0010 = 'CSC0010'
   CSC_0011 = 'CSC_0011'
   CSC_0012 = 'CSC_0012'
   CSC_0013 = 'CSC_0013'

   # PEN ID Search Prefix for ApaarPenIdSearch.py file

    # APAAR Creation Prefix for ApaarCreation.py file
    
   APAAR0000 = 'E-005'
   APAAR0001 = 'E-331'
   APAAR0003 = 'E-004'
   APAAR0004 = 'E-339'
   APAAR0005 = 'E-313'
   APAAR0006 = 'E-312'
   APAAR0007 = 'E-300'
   APAAR0008 = 'E-301'
   APAAR0009 = 'E-302'
   APAAR0010 = 'E-303'
   APAAR0011 = 'E-304'
   APAAR0012 = 'E-305'
   APAAR0013 = 'E-306'
   APAAR0014 = 'E-307'
   APAAR0015 = 'E-308'
   APAAR0016 = 'E-316'
   APAAR0017 = 'E-336'
   APAAR0018 = 'E-310'
   APAAR0019 = 'E-311'  # new
   APAAR0020 = 'S-101'
   APAAR0021 = 'E-337'
   APAAR0022 = 'E-322'  # new
   APAAR0023 = 'E-323'  # new
   APAAR0024 = 'E-324'  # new
   APAAR0025 = 'E-325'  # new
   APAAR0026 = 'E-326'  # new
   APAAR0027 = 'C-302'  
   APAAR0028 = 'C-305'
   APAAR0029 = 'C-306'
   APAAR0030 = 'C-307'
   APAAR0031 = 'C-308'
   APAAR0032 = 'E-309'
   APAAR0033 = 'E-339'
   APAAR0034 = 'S-101'
   APAAR0035 = 'S-100'
   APAAR0036 = 'E-315'
   APAAR0037 = 'E-500'
   APAAR0038 = 'E-334'
   APAAR0039 = 'E-333'
   APAAR0040 = 'E-999'
   APAAR0041 = 'C-303'
   APAAR0042 = 'E-888'
    
    # APAAR Update Prefix for UpdateRequestByABCId.py file
    
   UPDATE0001 = 'Update-001'
   UPDATE0002 = 'Update-002'
   UPDATE0003 = 'Update-003'
   UPDATE0004 = 'Update-004'
   UPDATE0005 = 'Update-005'
   UPDATE0006 = 'Update-006'
   UPDATE0007 = 'Update-007'
   UPDATE0008 = 'Update-008'
   UPDATE0009 = 'Update-009'
   UPDATE0010 = 'Update-010'
   UPDATE0011 = 'Update-011'
   UPDATE0012 = 'Update-012'
   UPDATE0013 = 'Update-013'
   UPDATE0014 = 'Update-014'
   UPDATE0015 = 'Update-015'
   UPDATE0016 = 'Update-016'
   UPDATE0017 = 'Update-017'
    
       # APAAR Update Prefix for DeleteController.py file
    
   DELETE0001 = 'Delete-001'
   DELETE0002 = 'Delete-002'
   DELETE0003 = 'Delete-003'
   DELETE0004 = 'Delete-004'
   DELETE0005 = 'Delete-005'
   DELETE0006 = 'Delete-006'
   DELETE0007 = 'Delete-007'
   DELETE0008 = 'Delete-008'
   DELETE0009 = 'Delete-009'
   DELETE0010 = 'Delete-010'
   DELETE0011 = 'Delete-011'
   DELETE0012 = 'Delete-012'
   DELETE0013 = 'Delete-013'
   DELETE0014 = 'Delete-014'
   DELETE0015 = 'Delete-015'
   DELETE0016 = 'Delete-016'
   DELETE0017 = 'Delete-017'
   DELETE0018 = 'Delete-018'
   DELETE0019 = 'Delete-019'
    
    
       # APAAR Get Prefix for SelectApaarData.py file
    
   SELECT0001 = 'Select-0001'
   SELECT0002 = 'Select-0002'
   SELECT0003 = 'Select-0003'
   SELECT0004 = 'Select-0004'
   SELECT0005 = 'Select-0005'
   SELECT0006 = 'Select-0006'
   SELECT0007 = 'Select-0007'
   SELECT0008 = 'Select-0008'
   SELECT0009 = 'Select-0009'
   SELECT0010 = 'Select-0010'
   SELECT0011 = 'Select-0011'
   SELECT0012 = 'Select-0012'
   SELECT0013 = 'Select-0013'
    
    # APAAR Generate Prefix for GenerateABCId.py file
    
   GENERATE0001 = 'Generate-001'
   GENERATE0002 = 'Generate-002'
   GENERATE0003 = 'Generate-003'
    
    # APAAR Check Prefix for ApaarController.py file
    
   CHECK0000 = "Check-000"
   CHECK0001 = 'Check-001'
   CHECK0002 = 'Check-002'
    
    # LOCKER Check Prefix for ApaarController.py file
     
   LOCKERCHECK0000 = 'LockerCheck-000'
   LOCKERCHECK0001 = 'LockerCheck-001'
   LOCKERCHECK0002 = 'LockerCheck-002'
    
    # Error code for ABCIdByLocker.py file
    
   INSERT0000 = 'Insert-0000'
   INSERT0001 = 'Insert-0001'
   INSERT0002 = 'Insert-0002'
   INSERT0003 = 'Insert-0003'
   INSERT0004 = 'Insert-0004'
   INSERT0005 = 'Insert-0005'
   INSERT0006 = 'Insert-0006'
   INSERT0007 = 'Insert-0007'
   INSERT0008 = 'Insert-0008'
   INSERT0009 = 'Insert-0009'
   INSERT0010 = 'Insert-0010'
   INSERT0011 = 'Insert-0011'
   INSERT0012 = 'Insert-0012'
   INSERT0013 = 'Insert-0013'
   INSERT0014 = 'Insert-0014'
   INSERT0015 = 'Insert-0015'
   INSERT0016 = 'Insert-0016'
   INSERT0017 = 'Insert-0017'
   INSERT0018 = 'Insert-0018'
   OLD0001 = 'O-0001'
   OLD0002 = 'O-0002'
   NEW0001 = 'N-0001'
   
   APAAR_CHECK_LOCKER_ID = 'Check-Locker-0001'
    
