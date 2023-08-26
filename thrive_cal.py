import random
NEUTRAL_MOOD = 0


class CalendarEvent:
    def __init__(self, name, mood, start, end, negotiable=True):
        self.name = name
        self.mood = mood
        self.name = name
        self.mood = mood
        self.start = start
        self.end = end
        self.negotiable = negotiable

    def __repr__(self) -> str:
        return f"CalEvent(name='{self.name}', mood='{self.mood}', start='{self.start}', end='{self.end}', negotiable='{self.negotiable}')"


def get_mood_score(event, classifier):
    return event.mood + float(classifier(event.name))


class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def get_events_by_date(self, datetime_start, datetime_end):
        events_in_range = []
        for event in self.events:
            if datetime_start <= event.start <= datetime_end and \
               datetime_start <= event.end <= datetime_end:
                events_in_range.append(event)

        return events_in_range

    def get_events_by_length_and_mood(self, length, mood_lo, classifier):
        possible_events = []
        for event in self.events:
            dt = event.end - event.start
            sentiment_score = get_mood_score(event, classifier)
            if dt == length and sentiment_score >= mood_lo:
                possible_events.append(event)
        random.shuffle(possible_events)
        if len(possible_events) > 0:
            return possible_events
        else:
            return None

    def is_unique_event_in_schedule(self, schedule, event):
        for curr_event in schedule:
            if curr_event.name == event.name:
                return False
        return True

    def recommend_activity(self, datetime_start, datetime_end, classifier):
        day_score = 0  # Day score to balance things out if things get below a threshold
        schedule = []  # Final schedule
        negotiable_events = []  # These are negotiable events
        events_within_range = self.get_events_by_date(
            datetime_start, datetime_end)
        for event in events_within_range:
            sentiment_score = get_mood_score(event, classifier)
            # set the non negotiable ones and check mood
            if event.negotiable:
                negotiable_events.append((sentiment_score, event))
            else:
                day_score += sentiment_score
                schedule.append(event)

            # check the negotiable events
            sorted(negotiable_events)
            for _ in range(len(negotiable_events)):
                score, curr_event = negotiable_events.pop()
                if score < 0:
                    dt = curr_event.end - curr_event.start
                    # This event makes users mood lower than thresh
                    # So find a suitable swap from events list
                    results = self.get_events_by_length_and_mood(
                        dt,
                        NEUTRAL_MOOD, classifier)
                    if results is not None:
                        for res in results:
                            if self.is_unique_event_in_schedule(schedule=schedule, event=res):
                                schedule.append(CalendarEvent(
                                    name=res.name, mood=res.mood, start=curr_event.start, end=curr_event.end, negotiable=True))
                                day_score += get_mood_score(res, classifier)
                                break
                else:
                    # Unfortunate, user has not done previous activities of similar things
                    schedule.append(curr_event)
                    day_score += score
        # ###################################################
        # # Sorting by start time so we can check the gaps
        # schedule.sort(key=lambda event: event.start)
        # possible_event_times = []  # []
        # possible_reccs = []  # possible events we can recommend
        # fast_access_possible_recs = {}

        # # Dummy initialised so we can do O(n) walk through
        # max_gap_duration = 0
        # for i in range(len(schedule) - 1):
        #     # Going through all the events then making sure we got
        #     curr_event = schedule[i]
        #     next_event = schedule[i + 1]
        #     gap_duration = next_event.start - curr_event.end
        #     if gap_duration.total_seconds() >= 0:  # There's a gap between events
        #         max_gap_duration = max(gap_duration, max_gap_duration)
        #         possible_event_times.append[(curr_event.end, next_event.start)]

        # last_event = schedule[-1]
        # last_gap_duration = datetime_end - last_event.end
        # if last_gap_duration.total_seconds() >= 0:  # There's a gap between events
        #     max_gap_duration = max(last_gap_duration, max_gap_duration)
        #     possible_event_times.append[(curr_event.end, datetime_end)]
        # #####################################################
        # for i in range(max_gap_duration):
        #     results = self.get_events_by_length_and_mood(
        #         i, NEUTRAL_MOOD, classifier)
        #     fast_access_possible_recs.setdefault(i, [])
        #     if results is not None:
        #         for res in results:
        #             if self.is_unique_event_in_schedule(schedule, res) and self.is_unique_event_in_schedule(possible_reccs, res):
        #                 possible_reccs.append(res)
        #                 fast_access_possible_recs[i].append(res)

        # for gap_start, gap_end in possible_event_times:
        #     for i in range(1, gap_end - gap_start + 1):
        #         if len(fast_access_possible_recs[i]) > 0:
        #             possible_reccs.append(res)
        #             fast_access_possible_recs[i].append(res)
        return schedule

    def __repr__(self) -> str:
        return f"Calendar(events='{self.events}')"
