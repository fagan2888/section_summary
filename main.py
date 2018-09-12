
from sys import argv

import webbrowser
import tempfile

from user_summary import get_scores_for_all_emails
from visualize import visualize

all_scores = get_scores_for_all_emails(argv[1], int(argv[2]), open(argv[3]).read().split())
f = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False)
html, csv = visualize(all_scores)
f.write(html)
print(csv)
webbrowser.open_new_tab('file://%s' % f.name)
