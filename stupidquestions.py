import praw

posttitle = "Weekly Stupid Questions Thread"

postbody = """
Ready the questions! Feel free to ask anything (no matter how seemingly moronic).

Other resources:

- The [Dota 2 Wiki](http://www.dota2wiki.com/wiki/Dota_2_Wiki) has tons of useful information.

- Old [Stupid Questions threads](http://www.reddit.com/r/DotA2/search?q=title%3A%22Weekly+Stupid+Questions%22&restrict_sr=on&sort=new&t=all) - and [](#begin last_week)[last week's](http://reddit.com/r/dota2/comments/59vj00)[](#end last_week) for convenience.

[](#hidden number 250)

> > When the frist hit strikes wtih desolator, the hit stirkes as if the - armor debuff had already been placed?

> yes
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
    submission.mod.flair(text="Questions")
    submission.mod.sticky()

def unstickyPost(r):
    submissions = r.redditor("VRCbot").submissions.new()
    submission = submissions.next()
    submission.mod.sticky(state=False)