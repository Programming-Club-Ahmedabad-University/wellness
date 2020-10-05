import re

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """
        To create a token for email activation and password rest
    """
    pass


generate_token = TokenGenerator()


# Funtions for validating registration data
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


def is_valid_email(email):
    if email.endswith('ahduni.edu.in'):
        return True
    else:
        return False
