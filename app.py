
from thrive_cal import Calendar, CalendarEvent
import pickle
from flask import Flask, render_template, request, jsonify
from datetime import datetime
app = Flask(__name__)
format_string = "%Y-%m-%d %H:%M:%S.%f"
model = pickle.load(open('model.pkl', 'rb'))
user_calendar = Calendar()


def get_sentiment_score(sentence):
    res = model.polarity_scores(sentence)['compound']
    return res if res != 0 else 1  # res == 0 if its neutral


@app.route('/hc', methods=['GET'])
def health_check():
    return jsonify({'response': 'BE is working'})


@app.route('/data/event', methods=['POST'])
def post_cal_event():
    start = datetime.strptime(request.get_json()[
        'start'].replace('_', ' '), format_string)
    end = datetime.strptime(request.get_json()[
        'end'].replace('_', ' '), format_string)
    ce = CalendarEvent(
        request.get_json()['activity'], request.get_json()['mood'],  start,  end, request.get_json()['negotiable'])
    user_calendar.add_event(ce)
    return jsonify({'activity': ce.name, 'mood': ce.mood, 'start': ce.start, 'end': ce.end})


@app.route('/data/cal/<start>/<end>', methods=['GET'])
def get_reccomendation(start, end):
    start = datetime.strptime(start.replace('_', ' '), format_string)
    end = datetime.strptime(end.replace('_', ' '), format_string)

    sched = user_calendar.recommend_activity(
        start, end, classifier=get_sentiment_score)
    sched.sort(key=lambda event: event.start)
    resp = []
    for event in sched:
        resp.append({'name': event.name, 'mood': event.mood, 'start': event.start,
                    'end': event.end, 'negotiable': event.negotiable})

    return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True)
