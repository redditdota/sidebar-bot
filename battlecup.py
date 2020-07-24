import praw

import datetime
import calendar

posttitle = "Find a Party"

postbody = """
This thread is dedicated to recruitment for the weekly battle cup, Aghanim's Labyrinth, guilds, etc

____

Suggested Format:

**Steam ID / Guild Name & Tag:**

**Server:**

**Language:**

**Rank/Tier:**

**Preferred Heroes/Role:**

**Other Information:** Any other info that you would like your new mates to know

____

If you start to love playing with a premade and in a competitive setting please check out our friends at https://www.reddit.com/r/compDota2

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
