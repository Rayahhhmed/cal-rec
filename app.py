
from thrive_cal import Calendar, CalendarEvent, GenericEvent
import pickle
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
user_calendar = Calendar()


def get_sentiment_score(sentence):
    return model.polarity_scores(sentence)


@app.route("/hc", methods=["GET"])
def health_check():
    return jsonify({"response": "BE is working"})


@app.route("/data/generic", methods=["POST"])
def post_generic_event():
    ge = GenericEvent(
        request.get_json()["activity"], request.get_json()["mood"])
    user_calendar.add_event(ge)
    print(user_calendar)
    return jsonify({"activity": ge.name, "mood": ge.mood, "sentiment_score":  get_sentiment_score(ge.name)})


@app.route("/data/cal", methods=["POST"])
def post_cal_event():
    ce = CalendarEvent(
        request.get_json()["activity"], request.get_json()["mood"],  request.get_json()["time_start"],  request.get_json()["time_end"])
    user_calendar.add_event(ce)
    print(user_calendar)
    return jsonify({"activity": ce.name, "mood": ce.mood, "time_start": ce.time_start, "time_end": ce.time_end})


@app.route("/data/cal", methods=["GET"])
def get_reccomendation():
    pass


if __name__ == "__main__":
    app.run(debug=True)
