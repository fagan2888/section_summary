
# Section Summary Tool

This is a tool for quickly getting a summary of your section's performance, if you are a 61A TA.

To run the command,

 - log into okpy on chrome
 - get the [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg?hl=en) extension for chrome and download your cookies
 - copy your list of students from your section attendance into a file, comma/space/newline separated
 - clone this repo: `git clone https://github.com/kavigupta/section_summary.git`
 - run the command `python3 section_summary/main.py [cookies.txt] 173 [emails.txt]`. This will take a while, and then pop up a window in your browser summarizing your section's performance.
