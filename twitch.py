import requests, sys
r = requests.get('https://api.twitch.tv/kraken/streams?game=Dota 2', headers={'Client-ID': '59bfzzahzvq2haa6mo9kt3siak01w0s'})
data = r.json()

o = ''
for stream in data['streams'][:5]:
	o += (">>>#[" + stream['channel']['status'].strip() + "](" + stream['channel']['url'] + "#profile-twitch)\n>##\n>###" + str(stream['viewers']) + " @ " + stream['channel']['name'])
	o += '\n'

print(o)
# return o or some shit