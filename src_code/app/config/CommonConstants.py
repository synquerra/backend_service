class CommonConstants:
    UDISE_DATA_CSV_FILENAME = "student_data.csv"
    UDISE_DATA_ZIP_FILENAME = "student_data.zip"
    UDISE_DATA_ZIP_CONTENTTYPE = "application/zip"
    UDISE_DATA_SOURCE = "in.school.udise"
    UDISE_DATA_FILE_PREFIX = "update_ekyc_apaar_"
    # Constants
    AES_KEY_LENGTH = 32  # AES-256 requires a 32-byte key
    VALID_GENDERS = {"M", "F", "T"}  # Allowed gender values
    DOB_FORMAT = "%d/%m/%Y"
    APAAR_ID_PATTERN = r"^(?!.*(\d)\1{10})\d{12}$"  # Prevents repeated digits over 10 times
    AADHAAR_NAME_PATTERN = r"^[a-zA-Z]+(?:[\s'\.]{1,2}[a-zA-Z]+)*$"  # Name validation regex
    DATE_FORMAT = "%d/%m/%Y"
    APPLICATION_XML = "application/xml"
    TEXT_PLAIN_MEDIA_TYPE = "text/plain"
    VALID_NAME_PATTERN = r"^[a-zA-Z]+(?:[\s'\.]{1,2}[a-zA-Z]+)*$"
