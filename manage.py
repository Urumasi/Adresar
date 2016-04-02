from flask import Flask, render_template, redirect, url_for, abort, flash, request
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.pymongo import PyMongo
from bson import ObjectId

from forms import ContactForm


app = Flask(__name__)
app.config.from_pyfile('config.py')

mongo = PyMongo(app)

if app.debug:
    debug = DebugToolbarExtension(app)


@app.context_processor
def inject_contacts():
    contacts = list(mongo.db.contacts.find({}).sort('firstname'))
    return dict(contacts=contacts)


@app.errorhandler(404)
def error_404(e):
    return "Error 404"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacts/<id>/view', endpoint='contact-view')
def contact_view(id):
    id_obj = ObjectId(id)
    contact = mongo.db.contacts.find_one({'_id': id_obj}) or abort(404)
    return render_template('contact-view.html', contact=contact)


@app.route('/contacts/<id>/delete', endpoint='contact-delete')
def contact_delete(id):
    id_obj = ObjectId(id)
    mongo.db.contacts.remove({'_id': id_obj})
    flash("Kontakt byl smazán.")
    return redirect(url_for('index'))


@app.route('/contacts/<id>/edit', endpoint='contact-edit', methods=['GET', 'POST'])
def contact_edit(id):
    id_obj = ObjectId(id)
    contact = mongo.db.contacts.find_one({'_id': id_obj}) or abort(404)
    form = ContactForm()

    if form.is_submitted() and not form.validate():
        flash("Chyba při vstupu dat", category="error")

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data

        print(firstname, lastname)

        id_obj = mongo.db.contacts.update_one({'_id': id_obj}, {"$set": {'firstname': firstname, 'lastname': lastname}})

        flash("Kontakt byl editován")
        return redirect(url_for('contact-view', id=id))


    form.firstname.data = contact['firstname']
    form.lastname.data = contact['lastname']

    return render_template('contact-edit.html', form=form)


@app.route('/contacts/add', endpoint='contacts-add', methods=['GET', 'POST'])
def contacts_add():
    form = ContactForm()

    if form.is_submitted() and not form.validate():
        flash("Chyba při vstupu dat", category="error")

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data

        id_obj = str(mongo.db.contacts.insert({'firstname': firstname, 'lastname': lastname}))

        flash("Kontakt byl přidán")
        return redirect(url_for('contact-view', id=id_obj))

    return render_template('contact-form.html', form=form)


if __name__ == '__main__':
    app.run()
