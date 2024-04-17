import json
import time
import datetime

SUBREDDIT = "Dota2"
USERNAME = "VRCBot"
HEROES = json.load(open("heroes.json"))

post_title = "Hero Discussion of the Week: {hero_name} ({date})"
post_body = """
## **[{hero_name}](https://www.liquipedia.net/dota2game{link})**

**Ask/Answer/Comment anything related to {hero_name}!**

Leave comments under these top level comments for more specific discussion about the hero

{comments}
"""

temp = """
&nbsp;

#### Previous Hero Discussions

{previous}
"""

top_level = [
    "Skill Build",
    "Item Build",
    "Hero Synergies",
    "Hero Counters",
    "Aghanim's Scepter/Shard",
    "Tips and Tricks",
    "Lore",
    "Favorite Cosmetics"
]
top_level_comment_body = "**{text}**"
top_level_comment = "* [{comment}]({link})\n"


def get_hero(num):
    try:
        hero = HEROES[num]
    except IndexError:
        # Everyone has been done, modulo
        num = num % len(HEROES)
        hero = HEROES[num]
    return hero

def create_post(r, num):
    hero = get_hero(num)
    title = post_title.format(hero_name=hero["hero"], date=datetime.datetime.now().strftime("%B %d, %Y"))
    body = post_body.format(hero_name=hero["hero"], link=hero["link"], comments="{comments}")

    submission = r.subreddit(SUBREDDIT).submit(title, selftext=body)
    submission.mod.flair(text="Discussion", css_class="discussion")
    submission.mod.sticky()

    top_level_comments = []
    for top in top_level:
        time.sleep(8)
        top_level_comments.append(submission.reply(top_level_comment_body.format(text=top)).permalink)

    formatted_comment = ""
    for index, _ in enumerate(top_level):
        formatted_comment += top_level_comment.format(comment=top_level[index], link=top_level_comments[index])

    body = body.format(comments=formatted_comment)
    submission.edit(body)

    x_post_title = "[X-Post from /r/Dota2] " + title

    time.sleep(8)
    r.subreddit("truedota2").submit(x_post_title, selftext=submission.url)
    #time.sleep(20)
    #r.subreddit("learndota2").submit(x_post_title, url=submission.url)


def count_prev_posts(r):
    submissions = r.redditor(USERNAME).submissions.new()
    prev_posts = [post for post in submissions if "Hero Discussion" in post.title]
    return len(prev_posts)

def get_prev_posts(r):
    posts = []
    iterations = 0

    for post in r.redditor('VRCbot').submissions.new():
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
        post_body += template.format(title=post[0], url=post[1])

    return post_body
