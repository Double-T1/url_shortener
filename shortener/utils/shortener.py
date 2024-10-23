import random, string
from shortener.models import ShortenedUrl

# make sure it doesn't collide with existing short urls
def generate_short_url_hash():
    short_url = random_hash()
    while ShortenedUrl.has_short_url(short_url):
        short_url = random_hash()
    return short_url

def random_hash():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(7))