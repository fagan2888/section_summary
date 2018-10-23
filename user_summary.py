import os
import re
import ssl
import sys
import functools
from multiprocessing.pool import ThreadPool

try: import urllib.request as urllib_request  # Python 3
except ImportError: import urllib2 as urllib_request  # Python 2

HTTPS_VERIFY_ENVVAR = 'PYTHONHTTPSVERIFY'
OKPY_DOMAIN_NAME = "okpy.org"

def urlopen(url, *args, **kwargs):
    cookie = kwargs.pop('cookie', None)
    headers = []
    if not sys.flags.ignore_environment and os.environ.get(HTTPS_VERIFY_ENVVAR) in ('0', 'no', 'false', 'False', 'disable', 'Disable'):
        headers.append(urllib_request.HTTPSHandler(context=ssl._create_unverified_context()))
    opener = urllib_request.build_opener(*headers)
    if cookie is not None: opener.addheaders.append(('Cookie', cookie))
    result = None
    try:
        result = opener.open(url, *args, **kwargs)
    except urllib_request.URLError as ex:
        if isinstance(ex.reason, ssl.SSLError):
            msg = "Error verifying the host's SSL certificate. You can bypass SSL verification AT YOUR OWN RISK by setting the environment variable %s=%s." % (HTTPS_VERIFY_ENVVAR, 0)
            raise ex.reason.__class__(ex.reason.errno, msg) from ex
        raise
    return result

def get_okpy_cookies(cookies_path):
    result = []
    with open(cookies_path) as f:
        for line in f:
            columns = line.split()
            if len(columns) < 4:
                continue
            site, *_, cookie_name, cookie = columns
            if site == OKPY_DOMAIN_NAME:
                result.append((cookie_name, cookie))
    assert len(result) > 0, "cookie not found"
    return result

def get_scripts(output):
    scripts = []

    current_script = None

    for line in output.split('\n'):
        if "<script" in line:
            if "</script>" in line:
                continue
            assert current_script == None
            current_script = []
        elif "</script>" in line:
            assert current_script != None
            scripts.append("\n".join(current_script))
            current_script = None
        elif current_script is not None:
            current_script.append(line.strip())
    return scripts

def request(course_number, cookies, email):
    print("Downloading page corresponding to email", email, file=sys.stderr)
    assert all(map(lambda cookie: len(cookie) == 2, cookies)), "cookies must be (name, value) pairs"
    response = urlopen('https://%s/admin/course/%s/%s' % (OKPY_DOMAIN_NAME, course_number, email), cookie="; ".join(map(lambda cookie: "=".join(cookie), cookies)))
    return email, response.read().decode('utf-8')

def get_all_pages(course_number, cookies, *emails):

    function = functools.partial(request, course_number, cookies)
    with ThreadPool(min(len(emails), 20)) as p:
        return dict(p.map(function, emails))

def get_scores(page_contents, email):

    scripts = get_scripts(page_contents)

    all_scores = [x for x in scripts if "allScores" in x]

    if all_scores == []:
        print(email, "does not exist", file=sys.stderr)
        return None, None

    name = re.search(r'<h3 class="widget-user-username">([^<]*)</h3>', page_contents).group(1)

    assert len(all_scores) == 1
    all_scores, = all_scores
    all_scores = all_scores[:-1]
    return name, eval("{" + "".join(all_scores.split("\n")[1:]))

def get_scores_for_all_emails(cookies_path, course_number, emails):
    cookies = get_okpy_cookies(cookies_path)
    result = {}
    all_pages = get_all_pages(course_number, cookies, *emails)
    for email in emails:
        name, scores = get_scores(all_pages[email], email)
        if scores is not None:
            result[name] = scores
    return result
