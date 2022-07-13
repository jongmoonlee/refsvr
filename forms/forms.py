from wtforms import Form, StringField, SelectField
class SearchForm(Form):
    choices = [('Serial_Number', 'Serial_Number'),
               ('Part_Number', 'Part_Number')
               ]
    default = 'select all'
    select = SelectField('Search for unit:', choices=choices)
    search = StringField('Type SN or PN',default = default)



class OutboundForm(Form):
    choices = [('R&D', 'R&D'),
               ('Marketing', 'Marketing'),
               ('Production', 'Production'),
               ('Reliability', 'Reliability'),
               ('OtherDept', 'OtherDept')
               ]
    default = 'type sn..'
    name = 'name..'
    select = SelectField('Kidnapper:', choices=choices)
    snToGo = StringField('Serial Number',default = default)
    name = StringField('Name',default = name)