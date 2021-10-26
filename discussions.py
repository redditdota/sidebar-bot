import json
import time
import datetime

heroes = json.load(open("heroes.json"))

top_level = [
    "Skill Build",
    "Item Build",
    "Hero Synergies",
    "Hero Counters",
    "Aghanim's Scepter/Shard",
    "Tips and Tricks",
]
top_level_comment_body = "**{text}**"
top_level_comment = "* [{comment}]({link})\n"

post_title = "Hero Discussion of the Week: {hero_name} ({date})"

post_body = """
## **[{hero_name}](http://www.dota2wiki.com{link})**

**Ask/Answer/Comment anything related to {hero_name}!**

Leave comments under these top level comments for more specific discussion about the hero

{comments}

&nbsp;

#### Previous Hero Discussions

{previous}
"""

def get_hero(num):
    return heroes[num]

def next_hero_index(prev):
    return (prev + 1) % len(heroes)

def create_post(r, subname, num):
    hero = get_hero(num)
    title = post_title.format(hero_name=hero["hero"], date=datetime.datetime.now().strftime("%B %d, %Y"))
    body = post_body.format(hero_name=hero["hero"], link=hero["link"], comments="{comments}", previous=get_prev_posts(r))

    submission = r.subreddit(subname).submit(title, selftext=body)
    submission.mod.flair(text="Discussion", css_class="discussion")
    submission.mod.sticky()

    top_level_comments = []

    for top in top_level:
        time.sleep(8)
        top_level_comments.append(
            submission.reply(top_level_comment_body.format(text=top)).permalink
        )

    formatted_comment = ""

    for i in range(len(top_level)):
        formatted_comment += top_level_comment.format(
            comment=top_level[i], link=top_level_comments[i]
        )

    body = body.format(comments=formatted_comment)
    submission.edit(body)

def get_prev_posts(r):
    posts = []
    iterations = 0
    for post in r.redditor("VRCbot").submissions.new():
        if "Hero Discussion" in post.title:
            posts.append((post.title, post.url))

        if len(posts) >= 3:
            break

        if iterations > 200:
            break
        iterations += 1

    template = "* [{title}]({url})\n"
    post_body = ""

    for post in posts:
        post_body += template.format(title=post[0], title=post[1])
    
    return post_body