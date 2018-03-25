import json
import requests
import request
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator

language_translator = LanguageTranslator (
	username = "<your_username>",
	password = "<your_password>"
	) 

translation = language_translator.translate(
	text='Hello',
	model_id='es-en')

data = json.dumps(translation,indent=2,ensure_ascii=False)
print(data)
data2 = json.loads(data)
print(data2)
print(data2['translations'][0]['translation'])

language = language_translator.identify('Gracias')
data3 = json.dumps(language,indent=2)
data4 = json.loads(data3)
print(data4['languages'][0]['language'])
data5 = data4['languages'][0]['language']

url = "https://restcountries.eu/rest/v2/alpha/" + str(data5)
resp = requests.request("GET",url)
cname = json.loads(resp.content)
print(cname['demonym'])