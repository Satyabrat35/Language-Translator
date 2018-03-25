from flask import Flask  , request , render_template ,url_for ,flash
import json
import requests
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator

app = Flask(__name__)

app.secret_key = '\xc9 \x1e\x8d\x04\xed(t\x01g\rN\xa0*G\xb4`\xca\xc5\xb4R\xd4\xa0\x98c\xfb\xbbP\xb5\xb8\xe0\xd9'

language_translator = LanguageTranslator (
	username = "<your_username>",
	password = "<your_password>"
	) 


@app.route('/')
def route():
	return render_template('lang.html')

@app.route('/trn')
def trns():
	data2 = {u'character_count': 0, u'translations': [{u'translation': u'Welcome!!'}], u'word_count': 1}
	return render_template('home.html',data2=data2)

@app.route('/dtc')
def dtcz():
	return render_template('home2.html')	

@app.route('/translate',methods=['POST'])
def trans():
	if request.method == 'POST':
		text = request.form.get('text_area')
		en_to = request.form.get('trans1')
		to_en = request.form.get('trans2')


	#print(text)
	#print(en_to)
	#print(to_en)

	text1 = text.encode('utf-8')

	if text1 == '':
		flash('Enter the text')
		return render_template('home.html')

	if en_to != 'null' and to_en != 'null':
		flash('Enter only one translation method')
		return render_template('home.html')

	if en_to == 'null' and to_en == 'null':
		flash('Enter one translation method')
		return render_template('home.html')

	if en_to != 'null':
		translation = language_translator.translate(
			text= str(text1),
			model_id= 'en-' + str(en_to))
		data = json.dumps(translation,indent=2,ensure_ascii=False)
		data2 = json.loads(data)
		txt = data2['translations'][0]['translation']
		return render_template('home.html',data2=data2)

	if to_en != 'null':
		translation = language_translator.translate(
			text=str(text1),
			model_id= str(to_en) + '-en')
		data = json.dumps(translation,indent=2,ensure_ascii=False)
		data2 = json.loads(data)
		flash("Translation: ")
		txt = data2['translations'][0]['translation']
		return render_template('home.html',data2=data2)
	

	return render_template('home.html')

@app.route('/detect',methods=['POST'])
def detection():
	if request.method == 'POST':
		text = request.form.get('text_area')

	text1 = text.encode('utf-8')	

	language = language_translator.identify(str(text1))
	data = json.dumps(language,indent=2)
	data2 = json.loads(data)

	data3 = data2['languages'][0]['language']

	url = "https://restcountries.eu/rest/v2/alpha/" + str(data3)
	resp = requests.request('GET',url)
	country_name = json.loads(resp.content)

	flash("The language is mostly {}".format(country_name['demonym']))
	return render_template('home2.html')

if __name__ == "__main__":
	app.run(debug=True)