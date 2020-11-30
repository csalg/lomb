from collections import defaultdict

import mongomock
import pytest
from bson import ObjectId

from config import LIBRARY_CHUNKS_COLLECTION_NAME
from services.library.domain.entities import Chunk, Textfile
from services.library.repositories import ChunksRepository, TextfileRepository


@pytest.fixture
def db():
    return defaultdict(lambda: mongomock.MongoClient().db.collection)

def test_ChunksRepository(db):
    textfile_id = ObjectId()
    chunks = [
        Chunk(textfile_id, "some_text", "some_support_text", ["a", "another_lemma"], "en", "es"),
        Chunk(textfile_id, "another sentence", "translation", ["lemma", "b"], "en", "es"),
        Chunk(textfile_id, "last sentence", "translation", ["c", "another_lemma"], "en", "es")
    ]

    repository = ChunksRepository(db)

    # add
    repository.add(chunks)
    assert len(list(db[LIBRARY_CHUNKS_COLLECTION_NAME].find({}))) == 3

    # find_chunks
    assert len(list(repository.find_chunks('a', 'en', 'es'))) == 1

    # find_chunks with textfile_ids
    assert len(list(repository.find_chunks('a', 'en', 'es', textfile_ids=[textfile_id, ObjectId(), ObjectId()]))) == 1
    with pytest.raises(Exception, match=".*lemma.*"):
        repository.find_chunks('a', 'en', 'es', textfile_ids=[ObjectId(), ObjectId()])

    # delete_text
    repository.delete_text(textfile_id)
    with pytest.raises(Exception, match=".*lemma.*"):
        repository.find_chunks('a', 'en', 'es')

def test_TextfileRepository(db):
    repository = TextfileRepository(db)
    id = repository.get_next_id()
    textfile = Textfile(id,"title", "en", "es", "filename.html")

    # Sanity check
    repository.add(textfile)

    assert len(repository.all_filtered_by_language(['en'], ['es'])) == 1
    assert len(repository.all_filtered_by_language(['en', 'es', 'de'], ['es', 'ro'])) == 1
    assert len(repository.all_filtered_by_language(['es', 'de'], ['es', 'ro'])) == 0

    repository.delete(textfile.id)
    assert len(repository.all_filtered_by_language(['en'], ['es'])) == 0
