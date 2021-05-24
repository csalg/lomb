from lib.db import get_db
from slices.texts.controllers import create_controllers_with_mongo_repositories

controllers = create_controllers_with_mongo_repositories(get_db())

# def new_lemma_was_added_handler(new_lemma_to_learn : LemmaShouldBeLearnt):
#     current_app.logger.info(new_lemma_to_learn)
#     user, lemma, source_language, support_language = new_lemma_to_learn.user, new_lemma_to_learn.lemma, new_lemma_to_learn.source_language, new_lemma_to_learn.support_language
#     try:
#         examples, frequency = controllers.find_examples(user, lemma, source_language, support_language)
#         LemmaExamplesWereFoundEvent(user,lemma,source_language,support_language, frequency, examples).dispatch()
#     except Exception as e:
#         current_app.logger.error(e)

