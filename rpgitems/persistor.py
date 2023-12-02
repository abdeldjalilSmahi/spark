import json


class Persistor:
    def __init__(self, filename="rpg_items_final.json"):
        self.filename = filename

    def load_items(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_items(self, items):
        with open(self.filename, 'w') as file:
            json.dump(items, file)

    def add_rpg_item(self, rpg_item):
        items = self.load_items()
        items.append(rpg_item.__dict__)
        self.save_items(items)
