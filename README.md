
# Section Summary Tool

This is a tool for quickly getting a summary of your section's performance, if you are a 61A TA.

To run the command,

 - log into okpy on chrome
 - get the [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg?hl=en) extension for chrome and download your cookies
 - copy your list of students from your section attendance into a file, comma/space/newline separated
 - clone this repo: `git clone https://github.com/kavigupta/section_summary.git`
 - Find your course's number, it should be be the number in the link to your course (173 for fall 18): `https://okpy.org/admin/course/[course number]/assignments`
 - run the command `python3 section_summary/main.py [cookies.txt] [course_number] [emails.txt]`. This will take a while, and then pop up a window in your browser summarizing your section's performance.
