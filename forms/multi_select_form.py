from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField

class MigrateUsersForm(FlaskForm):
    multiselect = SelectMultipleField("Utilisateurs des anciennes campagne")
    multiselect_to = SelectMultipleField("Utilisateurs de la campagne en cours")
    submit = SubmitField('Valider')


    def __init__(self, *args, **kwargs):
        super(MigrateUsersForm, self).__init__(*args, **kwargs)
        self.multiselect.choices = [("py", "python"), ("rb", "ruby"), ("js", "javascript")]
        self.multiselect_to.choices = [("py", "python"), ("rb", "ruby"), ("js", "javascript")]