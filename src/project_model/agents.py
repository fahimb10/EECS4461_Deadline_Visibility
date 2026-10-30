import mesa

class CourseItemAgent(mesa.Agent):
    def __init__(self, model, item_id, kind, post_day, due_day=None):
        super().__init__(model)
        self.item_id = item_id
        self.kind = kind                 # "assessment", "resource", or "announcement"
        self.post_day = post_day
        self.due_day = due_day
        
        self.posted = False
        self.urgent = False
        self.visible = False

    def step(self):
        # check if the item has appeared on the feed yet
        if self.model.day >= self.post_day:
            self.posted = True
        else:
            self.posted = False

        # an assessment is urgent if itt is posted and due within 0 to 3 days
        if self.kind == "assessment" and self.posted and self.due_day is not None:
            days_left = self.due_day - self.model.day
            self.urgent = (0 <= days_left <= 3)
        else:
            self.urgent = False

