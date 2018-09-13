
import re
import urllib
import urllib3, urllib3.util.ssl_
from subprocess import Popen, PIPE
import sys

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


def get_all_pages(course_number, cookie, *emails):
    ssl_context = urllib3.util.ssl_.create_urllib3_context()
    pool = urllib3.HTTPSConnectionPool("okpy.org", ssl_context=ssl_context)

    requests = {}
    for email in emails:
        requests[email] = pool.request(
            'GET',
            '/admin/course/%s/%s' % (course_number, email),
            headers={"connection" : "keep-alive", "cookie" : "session=" + cookie}
        )
    results = {}
    for email in emails:
        print("Downloading page corresponding to email", email, file=sys.stderr)
        results[email] = requests[email].data.decode('utf-8')
    return results

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
