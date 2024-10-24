import random
import string

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from shortener.models import ShortenedUrl


def url_is_valid(url):
    validator = URLValidator()
    try:
        validator(url)
        return True
    except ValidationError:
        return False


# make sure it doesn't collide with existing short urls
def generate_short_code():
    short_code = random_code()
    while ShortenedUrl.has_short_code(short_code):
        short_code = random_code()
    return short_code


def random_code():
    return "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(7)
    )


def get_host(request):
    return f"http://{request.get_host()}/redirect/"
