from flask import Flask, request
app = Flask(__name__)

event_types = ['EXPOSURE', 'REVIEW']

@app.route('/log', methods=['POST'])
def hello():
    print(request.is_json)

    content = request.get_json()

    if 'event' not in content:
        return 'Wrong format!'
    
    if content['event'] not in event_types:
        return 'Wrong event type!'  
    
    if content['event'] == 'EXPOSURE':
        log_exposure(content['word'], content['payload'])
        return
    
    if content['event'] == 'REVIEW':
        log_review(content['word'], content['payload'])
        return

    return 'ok'


