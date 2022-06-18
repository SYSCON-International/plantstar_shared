from django.core.signing import Signer


def is_valid_signed_string(*, signer_key, signed_string, unsigned_string, salt):
    if signed_string is None or salt is None:
        return False

    return Signer(key=signer_key, salt=salt).unsign(signed_string) == unsigned_string
