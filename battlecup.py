import praw

import datetime
import calendar

posttitle = "Guild Recruitment Megathread"

postbody = """
Suggested Format:

**Steam ID / Guild Name & Tag:**

**Server:**

**Language:**

**Required Rank:**

**What makes your guild cool, unique, fun, etc:**

Have fun!

"""

def createPost(r, subname):
    title = posttitle + " | " + calendar.month_name[datetime.datetime.today().month] + " " + str(datetime.datetime.today().day)
    submission = r.subreddit(subname).submit(title, selftext=postbody)
    submission.disable_inbox_replies()
    submission.mod.flair(text="Other")
    submission.mod.suggested_sort('new')
    submission.mod.sticky()

def unstickyPost(r):
    submissions = r.redditor("VRCbot").submissions.new()
    submission = submissions.next()
    submission.mod.sticky(state=False)
