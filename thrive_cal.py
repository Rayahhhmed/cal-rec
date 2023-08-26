

class GenericEvent:
    def __init__(self, name, mood):
        self.name = name
        self.mood = mood

    def __repr__(self) -> str:
        return f"GenericEvent(name='{self.name}', mood='{self.mood}')"


class CalendarEvent(GenericEvent):
    def __init__(self, name, mood, time_start, time_end):
        super().__init__(name, mood)
        self.name = name
        self.mood = mood
        self.time_start = time_start
        self.time_end = time_end

    def __repr__(self) -> str:
        return f"CalEvent(name='{super.name}', mood='{super.mood}')"


class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def recommend_activity(self, user_mood_preference, classifier):
        recommended_activity = None
        max_score = float('-inf')

        for event in self.events:
            sentiment_score = classifier.classify(event.name)
            sentiment_score = float(sentiment_score)

            score = user_mood_preference * event.mood_effect * sentiment_score

            if score > max_score:
                max_score = score
                recommended_activity = event

        return recommended_activity

    def __repr__(self) -> str:
        return f"Calendar(events='{self.events}')"
