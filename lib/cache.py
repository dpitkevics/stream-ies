import pyfscache

from settings import CACHE_DIR

cache_it = pyfscache.FSCache(CACHE_DIR, days=1)