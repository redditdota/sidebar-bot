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