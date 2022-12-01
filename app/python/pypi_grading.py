import requests
import re
import json

package_name = "flask"
r = requests.get("https://pypi.org/project/{}/".format(package_name))
x = re.search('https:\/\/api.github.com\s*([^"]*)', r.text)
url = (x.group(0))
r = requests.get(url)
url_text = json.loads(r.text)
print(url_text["stargazers_count"])
print("this is not my name")