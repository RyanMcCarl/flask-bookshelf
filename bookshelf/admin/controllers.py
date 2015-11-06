from flask import Blueprint, render_template, flash
from flask import current_app, redirect, request, url_for
from bookshelf.admin.forms.author_forms import CreateAuthorForm
from bookshelf.data.models import Author, db
from sqlalchemy import exc


admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/')
def index():
    return render_template('admin_index.htm')


@admin.route('/author/create', methods=['GET', 'POST'])
def create_author():
    form = CreateAuthorForm(request.form)
    if request.method == 'POST' and form.validate():
        names = form.names.data
        current_app.logger.info('Adding a new author %s.', (names))
        author = Author(names)

        try:
            db.session.add(author)
            db.session.commit()
            flash('Author successfully created.')
        except exc.SQLAlchemyError as e:
            flash('Author was not created.')
            current_app.logger.error(e)

            return redirect(url_for('admin.create_author'))

        return redirect(url_for('main.display_authors'))

    return render_template('create_author.htm', form=form)
