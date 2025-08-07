import phonenumbers

def parse_phone_number( phoneNumber, default_region=None):
    parsedNumber= phonenumbers.parse(phoneNumber, default_region)
    return phonenumbers.format_number(parsedNumber, phonenumbers.PhoneNumberFormat.E164)
