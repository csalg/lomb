from lib.mocks import MockMongoCollection


def test_MockMongoCollection():
    collection = MockMongoCollection()
    # Sanity check. Can insert and retrieve item
    item = {'key': 'someValue'}
    collection.insert_one(item)
    result = collection.find_one(item)
    assert result == item
    # Result should be a copy
    result['newKey'] = result.pop('key')
    assert result != item
    assert collection.find_one(item) == item
    # Doesn't return item if wrong key or value
    assert not collection.find_one({'key': 'someOtherValue'})
    assert not collection.find_one({'someOtherKey': 'someValue'})
    # Item gets deleted
    collection.remove(item)
    assert not collection.find_one(item)

