import praw

import datetime
import calendar

posttitle = "Find Your Battle Cup Party"

postbody = """
This thread is dedicated for you guys to find a party for weekly Battle Cup.
____
**During the event all posts about finding/forming a team will be removed to avoid spam.** 

**This thread is only for people looking for a team, if you are forming a team simply reply to or PM anyone looking for a team that suits what you're looking for and invite them.**

If you've already found a team please edit your post saying so or delete your post so no one will keep contacting you.

##Sort by new to find people who just posted and is looking for a party.

____

Suggested Format:

**Steam ID:** 

**Server:** 

**Tier:** What tier do you want to play on?

**Preferred Role** What positions you're comfortable playing with.

**Other Information** Any other info that you would like your party mates to know

---

If you start to love playing with a premade and in a competitive setting please check out our friends at https://www.reddit.com/r/compDota2 and/or https://playerbase.gg

Have fun!

"""

def createPost(r, subname):
    title = posttitle + " | " + calendar.month_name[datetime.datetime.today().month] + " " + datetime.datetime.today().day
    submission = r.subreddit(subname).submit(title, selftext=postbody)
    submission.disable_inbox_replies()
    submission.mod.flair(text="Other")
    submission.mod.suggested_sort('new')
    submission.mod.sticky()

def unstickyPost(r):
    submissions = r.redditor("VRCbot").submissions.new()
    submission = submissions.next()
    submission.mod.sticky(state=False)
