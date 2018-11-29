import praw

posttitle = "Weekly Stupid Questions Thread"

postbody = """
Ready the questions! Feel free to ask anything (no matter how seemingly moronic).

Other resources:

- The [Dota 2 Wiki](http://www.dota2wiki.com/wiki/Dota_2_Wiki) has tons of useful information.

> > When the first hit strikes wtih desolator, the hit stirkes as if the - armor debuff had already been placed?

> yes
"""
artifact_postbody = """
Ready the questions! Feel free to ask anything (no matter how seemingly moronic).

> > When the first hit strikes wtih desolator, the hit stirkes as if the - armor debuff had already been placed?

> There's no desolator in this game yet.
"""

def createPost(r, subname, num):
    threadnum = ""
    if(num[-1] == "1"):
        threadnum = num + "st"
    elif(num[-1] == "2"):
        threadnum = num + "nd"
    elif(num[-1] == "3"):
        threadnum = num + "rd"
    else:
        threadnum = num + "th"

    title = "The " + threadnum + " " + posttitle
    submission = r.subreddit(subname).submit(title, selftext=postbody)
    submission.disable_inbox_replies()
    submission.mod.flair(text="Question")
    submission.mod.suggested_sort('new')
    submission.mod.sticky()

def unstickyPost(r):
    submissions = r.redditor("VRCbot").submissions.new()
    submission = submissions.next()
    submission.mod.sticky(state=False)

def artifact_createPost(r, subname, num):
    threadnum = ""
    if(num[-1] == "1"):
        threadnum = num + "st"
    elif(num[-1] == "2"):
        threadnum = num + "nd"
    elif(num[-1] == "3"):
        threadnum = num + "rd"
    else:
        threadnum = num + "th"

    title = "The " + threadnum + " " + posttitle
    submission = r.subreddit(subname).submit(title, selftext=artifact_postbody)
    submission.disable_inbox_replies()
    submission.mod.flair(text="Question")
    submission.mod.suggested_sort('new')
    submission.mod.sticky()

def artifact_unstickyPost(r):
    submissions = r.redditor("VRCbot").submissions.new()
    submission = submissions.next()
    submission.mod.sticky(state=False)
