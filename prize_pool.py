import requests
import locale


def get_prize_pool():
    url = "https://www.dota2.com/webapi/IDOTA2League/GetPrizePool/v001?league_id=11625"

    r = requests.get(url)
    prize_pool_json = r.json()
    prize_pool = prize_pool_json["prize_pool"]

    prize_pool_amount = "{:,}".format(prize_pool)
    prize_pool_amount = "[$" + prize_pool_amount + "]"

    return prize_pool_amount
