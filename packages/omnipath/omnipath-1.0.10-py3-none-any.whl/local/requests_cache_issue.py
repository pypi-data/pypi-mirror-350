from requests import Request, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from io import BytesIO
from tqdm import tqdm
import logging

#logging.getLogger().setLevel(logging.DEBUG)
#logging.getLogger('urllib3').setLevel(logging.DEBUG)
#logging.getLogger('requests').setLevel(logging.DEBUG)

import requests_cache
#logging.getLogger('requests_cache').setLevel(logging.DEBUG)
requests_cache.install_cache('foobar')

def do_a_request():

    url = 'https://omnipathdb.org/about'
    session = Session()
    retries = Retry(
        total = 1,
        redirect = 5,
        status_forcelist = [413,429,500,502,503,504],
        backoff_factor = 1,
    )
    adapter = HTTPAdapter(max_retries = retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    request = Request(
        'GET',
        url,
        params = {'format': 'text'},
        headers = {'User-Agent': 'omnipathdb-user'},
    )

    prequest = session.prepare_request(request)
    handle = BytesIO()

    with session.send(prequest, stream = True, timeout = (1, 3)) as response:

        response.raise_for_status()
        total = response.headers.get('content-length', None)

        with tqdm(
            unit = 'B',
            unit_scale = True,
            miniters = 1,
            unit_divisor = 1024,
            total = total if total is None else int(total),
        ) as t:
            for chunk in response.iter_content(chunk_size = 1024):
                t.update(len(chunk))
                handle.write(chunk)

        handle.flush()
        handle.seek(0)


    print(handle.read(100))

do_a_request()


import omnipath as op
print(op)


do_a_request()
