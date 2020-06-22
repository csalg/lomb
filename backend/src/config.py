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
SOURCE_LANGUAGES = ['en', 'de', 'es', 'fr', 'it', 'nl', 'pl', 'ru']
SUPPORT_LANGUAGES = ['en', 'de', 'es', 'fr', 'it', 'nl', 'pl', 'ru', 'jp', 'zh']

MINIMUM_PASSWORD_LENGTH = 8
MAXIMUM_PASSWORD_LENGTH = 40

UPLOADS_FOLDER = '/uploads'

# COLLECTION NAMES
LIBRARY_CHUNKS_COLLECTION_NAME = 'library_chunks'
LIBRARY_METADATA_COLLECTION_NAME = 'library_metadata'
