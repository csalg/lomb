from flask import Blueprint, render_template, request

from mq.signals import new_word_to_learn_was_added
from .domain.domain import LibraryDomain
from .infrastructure.signals import new_word_to_learn_was_added_handler

library = Blueprint('library', __name__, template_folder='templates')
domain = LibraryDomain()
new_word_to_learn_was_added.connect(new_word_to_learn_was_added_handler)


@library.route('/upload')
def upload():
    return render_template('upload.html')


@library.route('/upload_file', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist("files")
    response_msg = ""
    for f in uploaded_files:
        domain.add_file(f.stream, f.filename)
    return response_msg if response_msg else 'file uploaded successfully'


@library.route('/texts')
def texts():
    return render_template('texts.html.j2', texts=domain.all_texts())


@library.route('/books')
def books():
    return render_template('books.html.j2', books=domain.all_books())


@library.route('/text/<id>')
def text(id):
    text_ = domain.get_text(id)
    if text_:
        return render_template('text.html.j2', **text_)
    return f'Id {id} not found!'

@library.route('/book/<id>/')
def book(id):
    book_ = domain.get_book_chapters(id)
    if book_:
        print(len(book_['chapters']))
        return render_template('book_chapters.html.j2', **book_)
    return f'Id {id} not found!'

@library.route('/book/<id>/<chapter>')
def book_chapter(id, chapter):
    chunks = domain.get_book_chapter(id, chapter)

    if chunks:
        print(chunks)
        return render_template('text.html.j2', chunks=list(chunks))
    return f'Id {id} not found!'

