
import re
import sys
import functools
from multiprocessing.pool import ThreadPool

try: import urllib.request as urllib_request  # Python 3
except ImportError: import urllib2 as urllib_request  # Python 2

def urlopen(url, *args, **kwargs):
    cookie = kwargs.pop('cookie', None)
    opener = urllib_request.build_opener()
    if cookie is not None: opener.addheaders.append(('Cookie', cookie))
    return opener.open(url, *args, **kwargs)

def get_okpy_cookie(cookies_path):
    with open(cookies_path) as f:
        for line in f:
            columns = line.split()
            if len(columns) < 4:
                continue
            site, *_, cookie_name, cookie = columns
            if site == "okpy.org" and cookie_name == "session":
                return cookie
    assert False, "cookie not found"

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

def request(course_number, cookie, email):
    print("Downloading page corresponding to email", email, file=sys.stderr)
    response = urlopen('https://okpy.org/admin/course/%s/%s' % (course_number, email), cookie="session=" + cookie)
    return email, response.read().decode('utf-8')

def get_all_pages(course_number, cookie, *emails):

    function = functools.partial(request, course_number, cookie)
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
    cookie = get_okpy_cookie(cookies_path)
    result = {}
    all_pages = get_all_pages(course_number, cookie, *emails)
    for email in emails:
        name, scores = get_scores(all_pages[email], email)
        if scores is not None:
            result[name] = scores
    return result
