from flask import current_app


def stop_learning_lemma_handler(controllers):
    def inner(stop_learning_lemma_event):
        current_app.logger.info('Inside tracking')
        controllers.ignore(stop_learning_lemma_event.username, stop_learning_lemma_event.lemma, stop_learning_lemma_event.source_language)
    return inner