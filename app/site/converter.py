import re
from flask import url_for
from werkzeug.utils import escape

def text2html(text, path=None):
    text = escape(text)
    pattern = re.compile('\[img \w+\.\w{3,4}\]')
    for pic in re.findall(pattern, text):
        filename = pic.replace("[img ", "").replace("]", "")
        img_url = url_for('static', filename = path + filename)
        text = text.replace(pic, '<img src="{}">'.format(img_url))
    text = text.replace("[i]", "<i>").replace("[/i]", "</i>")
    text = text.replace("[b]", "<b>").replace("[/b]", "</b>")
    text = text.replace("\n", "<br />")
    return text