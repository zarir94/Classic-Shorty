from flask import Flask, Blueprint, render_template, flash, request, redirect
from urllib.parse import quote_plus, unquote_plus
from requests import get
from pyperclip import copy

app=Flask(__name__)
app.config['SECRET_KEY']='iureyu48783d#8*#^37489xnhkc'
url=Blueprint('urls',__name__)

def copylink(string):
	copy(string)


@url.route('/',methods=['GET','POST'])
def shortener():
	if request.method=='POST':
		longurl=request.form.get('longurl')
		name=request.form.get('name')
		longurl=quote_plus('https://pm-redirector.blogspot.com/?url=' + unquote_plus(longurl))
		if name=='':
			api_url=f"https://cutt.ly/api/api.php?key=667cc3506cc77adad0b8503f2dfc8a2121930&short={longurl}"
		else:
			api_url=f'https://cutt.ly/api/api.php?key=667cc3506cc77adad0b8503f2dfc8a2121930&short={longurl}&name={name}'

		link=get(api_url).json()['url']
		linkstatus=link['status']
		if linkstatus==7:
			global shortlink
			shortlink=link['shortLink']
			title=link['title']
			return redirect(f'/result?title={title}&url={shortlink}')
		elif linkstatus==3:
			flash('Alias/Name is already taken','error')
		elif linkstatus==2:
			flash('URL is Invalid or not supported. Example: https://google.com','error')
		elif linkstatus==5:
			flash('Entered Alias/Name in not supported','error')
		else:
			flash('Something went wrong!','error')
		

	return render_template('index.html')


@url.route('/result')
def result():
	title=request.args.get('title')
	link=request.args.get('url')
	return render_template('result.html',title=title,link=link)




app.register_blueprint(url,url_prefix='/')
app.jinja_env.globals.update(copy=copylink)
if __name__=='__main__':
	app.run(debug=False,host='0.0.0.0',port=80)
