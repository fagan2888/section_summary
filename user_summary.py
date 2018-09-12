
import urllib
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


def get_scores(cookies_path, course_number, email):
    print("Downloading page corresponding to email", email, file=sys.stderr)
    p = Popen(['curl', '-H', 'cookie:session=' + get_okpy_cookie(cookies_path), 'https://okpy.org/admin/course/%s/%s' % (course_number, email)], stdout=PIPE, stderr=PIPE)

    stdout, _ = p.communicate()

    scripts = get_scripts(stdout.decode('utf-8'))

    all_scores = [x for x in scripts if "scores" in x]

    if all_scores == []:
        print(email, "does not exist in https://okpy.org/admin/course/%s" % course_number, file=sys.stderr)
        return None

    assert len(all_scores) == 1
    all_scores, = all_scores
    all_scores = all_scores[:-1]
    return eval("{" + "".join(all_scores.split("\n")[1:]))

def get_scores_for_all_emails(cookies_path, course_number, emails):
    result = {}
    for email in emails:
        scores = get_scores(cookies_path, course_number, email)
        if scores is not None:
            result[email] = scores
    return result
