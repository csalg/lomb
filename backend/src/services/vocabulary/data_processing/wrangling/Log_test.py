import pytest

from services.tracking.domain import TEXT__WORD_HIGHLIGHTED
from services.vocabulary.data_processing.wrangling.domain import Log

invalid_logs = [
    (TypeError,
     {
         'user': 'user',
         'lemma': 'lemma',
         'timestamp': '1000',
         'message': TEXT__WORD_HIGHLIGHTED
     }),
    (ValueError,
     {
         'user': 'user',
         'lemma': 'lemma',
         'timestamp': 1000,
         'message': 'MESSAGE_THAT_SHOULD_FAIL'
     })
]


def test_Log():

    # Log objects should not be possible to create with invalid data
    for invalid_log in invalid_logs:
        error_type, log = invalid_log
        with pytest.raises(error_type):
            Log.from_dictionary(log)
