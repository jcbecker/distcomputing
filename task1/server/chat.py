from bottle import route, run, post, request

messages = []
@post('/chat/msg') # or @route('/login', method='POST')
def index():
    message = request.forms.get('message')
    nickname = request.forms.get('nickname')
    messages.append ("<b>"+nickname + ": </b>"  + message + "</br>")
    return messages
    
    
run(host='localhost', port=8080, debug=True)