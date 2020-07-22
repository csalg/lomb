from copy import copy


class MockMongoCollection:
    def __init__(self):
        self.items = []

    def create_index(self,query):
        pass

    def insert_one(self, item):
        self.items += [item, ]

    def find_one(self, query):
        for item in self.items:
            if MockMongoCollection.match_item(item,query):
                return copy(item)

    @staticmethod
    def match_item(item,query):
        item_validity = True
        for key, val in query.items():
            if not key in item:
                return False
            item_validity = item_validity and item[key] == val
        return item_validity

    def remove(self,query):
        for item in self.items:
            if MockMongoCollection.match_item(item,query):
                self.items.remove(item)
