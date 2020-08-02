DEBUG=True
MAXIMUM_SECONDS = 150*24*60*60 # Otherwise difficult to scale.
LANGUAGE_NAMES = {
    'en': 'English',
    'de': 'German',
    'es': 'Spanish',
    'fr': 'French',
    'it': 'Italian',
    'nl': 'Dutch',
    'pl': 'Polish',
    'ru': 'Russian',
    'jp': 'Japanese',
    'zh': 'Chinese'
}
LEARNING_LANGUAGES = ['en', 'de', 'es', 'fr', 'it', 'nl', 'pl', 'ru']
KNOWN_LANGUAGES = ['en', 'de', 'es', 'fr', 'it', 'nl', 'pl', 'ru', 'jp', 'zh']
MAXIMUM_EXAMPLES_PER_TEXT = 50
MAXIMUM_LEMMA_RANK = 20000
TRANSLATABLE_EXTENSIONS = ['txt','epub']

MINIMUM_PASSWORD_LENGTH = 8
MAXIMUM_PASSWORD_LENGTH = 40

MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION = 3

UPLOADS_FOLDER = '/uploads'

# COLLECTION NAMES
LIBRARY_CHUNKS_COLLECTION_NAME      = 'library_chunks'
LIBRARY_TEXTFILE_COLLECTION_NAME    = 'library_textfiles'
LIBRARY_FREQUENCY_LIST_COLLECTION_NAME = 'library_frequency_lists'
LIBRARY_LEMMA_RANK_COLLECTION_NAME = 'library_lemma_ranks'
VOCABULARY_LOGS_COLLECTION_NAME     = 'vocabulary_logs'
IGNORE_LEMMAS_COLLECTION_NAME       = 'vocabulary_ignore'
LEARNING_LEMMAS_COLLECTION_NAME     = 'learning_lemmas'

USERS_COLLECTION_NAME = 'users'
USER_CREDENTIALS_COLLECTION_NAME = 'user_credentials'
USER_PREFERENCES_COLLECTION_NAME = 'user_preferences'
