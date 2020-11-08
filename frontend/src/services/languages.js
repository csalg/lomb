export const LANGUAGE_NAMES = {
    'en': 'English',
    'de': 'German',
    'es': 'Spanish',
    'fr': 'French',
    'it': 'Italian',
    'nl': 'Dutch',
    'pl': 'Polish',
    'ru': 'Russian',
    'jp': 'Japanese',
    'zh': 'Chinese',
    'da': 'Danish',
}
export const LEARNING_LANGUAGES = ['en', 'de', 'es', 'fr', 'it', 'nl', 'pl', 'ru', 'da']
export const KNOWN_LANGUAGES = ['en', 'de', 'es', 'fr', 'it', 'nl', 'pl', 'ru', 'jp', 'zh', 'da']
LEARNING_LANGUAGES.sort((a,b) => LANGUAGE_NAMES[a]>LANGUAGE_NAMES[b])
KNOWN_LANGUAGES.sort((a,b) => LANGUAGE_NAMES[a]>LANGUAGE_NAMES[b])
