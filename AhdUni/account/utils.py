import re

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    pass

generate_token = TokenGenerator()

def is_valid_enrollment(enrollment_number):
    match = re.match("^[0-9]*$", enrollment_number)
    if match and len(enrollment_number) == 7:
        return True
    else:
        return False

def is_valid_contact(contact_number):
    match = re.match("^[0-9]*$", contact_number)
    if match and len(contact_number) == 10:
        return True
    else:
        return False

# def is_valid_email(email):
#     if email.endswith('ahduni.edu.in'):
#         return True
#     else:
#         return False
