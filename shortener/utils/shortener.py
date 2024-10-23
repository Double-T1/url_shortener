import random
import string

from shortener.models import ShortenedUrl


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
    return f"http://{request.get_host()}/"
