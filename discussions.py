import json
import time

heroes = json.load(open('heroes.json'))

top_level = ["Skill Build", "Item Build", "Hero Synergies", "Hero Counters", "Aghanim's Scepter/Shard", "Tips and Tricks"]
top_level_comment_body = "**{text}**"
top_level_comment = "* [{comment}]({link})\n"

post_title = "Hero Discussion of the Week: {hero_name}"

post_body = """
## **[{hero_name}](http://www.dota2wiki.com{link})**

**Ask/Answer/Comment anything related to {hero_name}!**

Leave comments under these top level comments for more specific discussion about the hero

{comments}
"""

def get_hero(num):
	return heroes[num]

def next_hero_index(prev):
    return (prev + 1) % len(heroes)

def create_post(r, subname, num):
	hero = get_hero(num)
	title = post_title.format(hero_name = hero['hero'])
	body = post_body.format(hero_name = hero['hero'], link = hero['link'], comments = "{comments}")

	submission = r.subreddit(subname).submit(title, selftext=body)
	submission.mod.flair(text="Discussion")
	submission.mod.sticky()

	top_level_comments = []

	for top in top_level:
		time.sleep(8)
		top_level_comments.append(submission.reply(top_level_comment_body.format(text = top)).permalink)

	formatted_comment = ""

	for i in range(len(top_level)):
		formatted_comment += top_level_comment.format(comment = top_level[i], link = top_level_comments[i])

	body = body.format(comments = formatted_comment)
	submission.edit(body)


