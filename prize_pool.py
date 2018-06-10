import requests
import locale

def get_prize_pool():
    url = 'http://www.dota2.com/webapi/ITournaments/GetLeaguePrizePool/v001?league_id=9870'

    r = requests.get(url)
    prize_pool_json = r.json()
    prize_pool = prize_pool_json["prize_pool"]
    
    prize_pool_amount = "{:,}".format(prize_pool)
    prize_pool_amount = "[$" + prize_pool_amount + "]"

    return prize_pool_amount
