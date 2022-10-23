import json
import time
import datetime

items = json.load(open("items.json"))

top_level = [
    "Core Heroes",
    "Situational Purchases",
    "Strong Versus",
    "Tips and Tricks",
]

top_level_comment_body = "**{text}**"
top_level_comment = "* [{comment}]({link})\n"

post_title = "Item Discussion of the Week: {item_name} ({date})"

post_body = """
## **[{item_name}](http://www.dota2wiki.com{link})**

**Ask/Answer/Comment anything related to {item_name}!**

Leave comments under these top level comments for more specific discussion about the item.

{comments}
"""

def get_item(num):
    return items[num]


def next_item_index(prev):
    return (prev + 1) % len(items)


def create_post(r, subname, num):
    item = get_item(num)
    title = post_title.format(item_name=item["item"], date=datetime.datetime.now().strftime("%B %d, %Y"))
    body = post_body.format(
        item_name=item["item"], link=item["link"], comments="{comments}"
    )

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

    x_post_title = "[X-Post from /r/Dota2] " + title

    time.sleep(8)
    r.subreddit("truedota2").submit(x_post_title, selftext=submission.url)
    #time.sleep(20)
    #r.subreddit("learndota2").submit(x_post_title, url=submission.url)
