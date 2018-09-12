
# Section Summary Tool

This is a tool for quickly getting a summary of your section's performance, if you are a 61A TA.

To run the command,

 - log into okpy on chrome
 - get the [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg?hl=en) extension for chrome and download your cookies (on some machines, you need to do this from a tab with okpy open)
 - copy your list of students from your section attendance into a file, comma/space/newline separated
 - clone this repo: `git clone https://github.com/kavigupta/section_summary.git`. If necessary, run `pip install -r requirements.txt` from the project folder
 - Find your course's number, it should be be the number in the link to your course (173 for fall 18): `https://okpy.org/admin/course/[course number]/assignments`
 - run the command `python3 section_summary/main.py [cookies.txt] [course_number] [emails.txt]`. This will take a while, and then pop up a window in your browser summarizing your section's performance.

## How to interpret the columns in the display

Most of the columns are self explanatory, corresponding to single assingments: these appear on the right of the display

 - score: the total raw score the student has in the course, without point adjustment or participation points.
 - midterm 1, midterm 2, final: the scores on the exams
 - proj, disc, lab, hw: the total score the student has in this category
 - recent effort: a score from 0-6 that represents how many of the most recent assignments a student has completed, 2 points are given for having attended the most recent discussion, 2 for the most recent lab, and 1 for each point on the most recent homework. This is intended as a measure of how much effort the student has been putting in recently, and will hopefully eventually be updated to include office hours.
