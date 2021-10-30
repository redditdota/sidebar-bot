## /r/Dota2 Sidebar bot

Despite being called the sidebar bot, this repo actually does all of the following:

* Update the sidebar with
    * Tournament and events from Google Calendar: `events.py`
    * Top twitch streams: `twitch.py`
    * Current played pro matches: `gosu.py`
    * Countdown until TI: `countdown.py`
    * Track TI prize pool: `prize_pool.py`
    * Update side

* Post weekly scheduled posts:
    * Battle cup: `battlecup.py`
    * Stupid questions: `stupidquestions.py`
    * Hero discussion: `discussions.py`
    * Item discussion: `item_discussion.py`

* Ping discord when there is new modmail: `modmail.py`

The entry point is `update_sidebar.py` and redesign specific code is `redesign.py`.


## Config.txt

The following fields in the config.txt file are required:
```
artifact_calendar_id = ?
artifact_email = ?
artifact_google_key = ?
bot_username = ?
client_id = ?
client_secret = ?
dota_calendar_id = ?
dota_email = ?
dota_google_key = ?
gosu_api_key = ?
stupid_questions_id = a number
hero_discussion_id = a number
artifact_stupid_questions_id = a number
twitch_client_id =
twitch_secret_id =
discord_token =
```