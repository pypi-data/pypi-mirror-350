from werkzeug.exceptions import Unauthorized


def get_ga_token(header):
    if not header:
        raise Unauthorized('No header found')

    return header
