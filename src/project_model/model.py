import mesa
from .agents import CourseItemAgent

class CourseFeedModel(mesa.Model):
    def __init__(self, rule="baseline", volume="low"):
        super().__init__()
        self.rule = rule
        self.volume = volume
        self.day = 0
        self.total_days = 30
        
        self.feed = []
        self.displaced_count = 0

        # 1. setup the 6 fixed assessments (post_day, due_day)
        assessment_schedule = [
            (1, 7), (5, 12), (10, 16), (12, 17), (19, 25), (23, 29)
        ]
        for i, (p_day, d_day) in enumerate(assessment_schedule, start=1):
            CourseItemAgent(self, f"A{i}", "assessment", p_day, d_day)

        # 2. setup the 10 regular resources (posted every 3 days)
        resource_days = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]
        for i, p_day in enumerate(resource_days, start=1):
            CourseItemAgent(self, f"R{i}", "resource", p_day, None)

        # 3. setup synthetic announcements based on volume condition
        notice_days = []
        if volume == "low":
            notice_days = list(range(1, 31, 5))          # 6 items
        elif volume == "medium":
            notice_days = list(range(1, 31, 2))          # 15 items
        elif volume == "high":
            for d in range(1, 31):                       # 60 items (2 per day)
                notice_days.extend([d, d])

        for i, p_day in enumerate(notice_days, start=1):
            CourseItemAgent(self, f"N{i}", "announcement", p_day, None)

        # mesa datacollector tracking our daily numbers
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Day": lambda m: m.day,
                "Urgent_Eligible": lambda m: len([a for a in m.agents if getattr(a, "urgent", False)]),
                "Urgent_Visible": lambda m: len([a for a in m.feed if getattr(a, "urgent", False)]),
                "Displaced_Announcements": lambda m: m.displaced_count
            }
        )

    def get_baseline_feed(self):
        # sort posted items newest first; break ties by item_id reverse
        posted_items = [a for a in self.agents if getattr(a, "posted", False)]
        posted_items.sort(key=lambda a: (a.post_day, a.item_id), reverse=True)
        return posted_items[:5]

    def get_alternative_feed(self, default_feed):
        # find all currently urgent assessments
        urgent_items = [a for a in self.agents if getattr(a, "urgent", False)]
        if not urgent_items:
            return list(default_feed)

        # Pick the one with the nearest deadline (tie breaker: item_id)
        urgent_items.sort(key=lambda a: (a.due_day, a.item_id))
        nearest = urgent_items[0]

        # if it is already in the top 5, leave the feed as is
        if nearest in default_feed:
            return list(default_feed)

        # otherwise reserve slot 0: take top 4 and put nearest at the front
        alt = default_feed[:4]
        alt.insert(0, nearest)
        return alt

    def step(self):
        self.day += 1
        self.agents.do("step")

        base_items = self.get_baseline_feed()

        if self.rule == "baseline":

            self.feed = base_items
            self.displaced_count = 0
        elif self.rule == "alternative":
            alt_items = self.get_alternative_feed(base_items)
            self.feed = alt_items

            # count how many announcements that would have been visible got pushed out
            lost_notices = 0
            for item in base_items:
                if item.kind == "announcement" and item not in alt_items:
                    lost_notices += 1
            self.displaced_count = lost_notices

        # update visibility flag on all agents
        for a in self.agents:
            a.visible = (a in self.feed)

        self.datacollector.collect(self)

        if self.day >= self.total_days:
            self.running = False

