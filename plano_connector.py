import requests

PLANO_BASE_URL="https://planorama.lacon.org"

# resp = requests.get("{}/conclar/schedule".format(PLANO_BASE_URL), verify=False)
# schedule = resp.text

# resp = requests.get("{}/conclar/participants".format(PLANO_BASE_URL), verify=False)
# people = resp.text

with open('lacon/participants.json', 'r') as f:
  people = f.readline()

with open('lacon/schedule.json', 'r') as f:
  schedule = f.readline()

with open('plano-lacon.jsonp', 'w') as f:
  f.write("var program={}\n".format(schedule))
  f.write("var people={}".format(people))
