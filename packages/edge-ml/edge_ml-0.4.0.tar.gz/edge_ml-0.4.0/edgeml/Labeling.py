class Labeling:
    def __init__(self):
        self._id = None
        self.labels = None
        self.name = None

    def parse(self, data):
        self._id = data["labelingId"]
        self.name = data["name"]
        self.labels = []
        for label in data["labels"]:
            tmp_label = Label()
            tmp_label.parse(label)
            self.labels.append(tmp_label)

    def __str__(self):
        return f"Labeling(_id={self._id}, labels={self.labels}, name={self.name})"

    def __repr__(self):
        return str(self)


class Label:
    def __init__(self):
        self._id = None
        self.start = None
        self.end = None
        self.type = None
        self.name = None

    def parse(self, data):
        self._id = data["_id"]
        self.start = data["start"]
        self.end = data["end"]
        self.type = data["type"]
        self.name = data["name"]

    def __str__(self):
        return f"Label(_id={self._id}, start={self.start}, end={self.end}, type={self.type}, name={self.name})"

    def __repr__(self):
        return str(self)
