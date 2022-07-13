from wsgiref.validate import PartialIteratorWrapper
from flask import Flask, request, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import sqlalchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from forms.multi_select_form import MigrateUsersForm

# Bokeh Part

from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure,show,output_file
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models.sources import ColumnDataSource



app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:////Users/tomi/Projects/Py/flasksqlalchemy/DVT Rigs_x8 copy.db'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:////Users/tomi/Projects/Py/flasksqlalchemy/DVT_Rigs_Database_Seed.db'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite://///syd-netapp-03/Lab-DVT-Results$/DVT_Results/DVT Rigs/DVT_Rigs_Database_Seed.db'


app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class Summary(db.Model):
    DateId = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String(50))
    RigName = db.Column(db.String(50))
    User = db.Column(db.String(50))
    PolOpt = db.Column(db.REAL(3))
    PM = db.Column(db.REAL(3))
    StartWL = db.Column(db.REAL(3))
    StopWL = db.Column(db.REAL(3))

    def __repr__(self):
        return '{},{},{},{},{},{},{}'.format(self.DateId,self.Date,self.RigName,self.User, self.PolOpt, self.PM, self.StartWL, self.StopWL)

class Refdata(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    DateId = db.Column(db.Integer)
    InSW = db.Column(db.Integer)
    SB = db.Column(db.Integer)
    OPM = db.Column(db.Integer)
    PolState = db.Column(db.Integer)
    WL = db.Column(db.REAL)
    Val = db.Column(db.REAL)  

    def __repr__(self):
        return '{},{},{},{},{},{},{}'.format(self.DateId,self.InSW,self.SB,self.OPM, self.PolState, self.WL, self.Val)
    

def summary_query():
    form = SummaryForm()
    return Summary.query

class SummaryForm(FlaskForm):
    DateId = QuerySelectField(query_factory=summary_query, allow_blank=False, get_label='DateId')
    Date = QuerySelectField(query_factory=summary_query, allow_blank=False, get_label='Date')
    RigName = QuerySelectField(query_factory=summary_query, allow_blank=False, get_label='RigName')
    User = QuerySelectField(query_factory=summary_query, allow_blank=False, get_label='User')
    PolOpt = QuerySelectField(query_factory=summary_query, allow_blank=False, get_label='PolOpt')
    PM = QuerySelectField(query_factory=summary_query, allow_blank=False, get_label='PM')
    StartWL = QuerySelectField(query_factory=summary_query, allow_blank=False, get_label='StartWL')
    StopWL = QuerySelectField(query_factory=summary_query, allow_blank=False, get_label='StopWL')


@app.route("/")
@app.route("/home")
def home():    
    summary = Summary.query.all()    

    return render_template('home.html', summary=summary)

@app.route("/refdata")
def refdata():    
    summary = Refdata.query.filter(Refdata.DateId==2)    
    # result_dict = [u.__dict__ for u in summary]
       

    return render_template('refdata.html', summary=summary)

# DropDownList
@app.route('/select', methods=["GET","POST"])
def select():
    form = SummaryForm()

    # you can set filter here
    form.Date.query = Summary.query.filter(Summary.Date == '2022-07-07')
    form.Date.query = Summary.query.all()
    # if form.validate_on_submit():
    if request.method == 'POST':
        print(form.PM.data)
        # return '<h1>{}</h1>'.format(form.RigName.data)
        return render_template('select.html', form=form)
    return render_template('select.html', form=form)

@app.route('/migrate', methods = ["GET", "POST"])
def migrate_users():
    form = MigrateUsersForm()
    if request.method == "POST" and form.validate_on_submit():
        multiselect = ', '.join(form.multiselect.data)
        # multiselect_to = ', '.join(form.multiselect_to.data)
        posted_data = {
            "multiselect": multiselect,
            # "multiselect_to": multiselect_to
        }
        return jsonify(posted_data)
    return render_template('simpler.html', form=form)

@app.route('/<Date>')
def dataByDate(Date):
    x= Summary.query.filter(Date == Date)
    y = Refdata.query.filter_by(DateId = 1)  
    return render_template('xx.html', y = y)

@app.route('/plot')
def plot():
    wl_query = Refdata.query.with_entities(Refdata.WL)
    val_query = Refdata.query.with_entities(Refdata.Val).filter(Refdata.DateId==1,Refdata.SB==1,Refdata.OPM ==77, Refdata.PolState == 0)
    
    wl = [u.WL for u in wl_query]
    wl = list(dict.fromkeys(wl))
    print(wl)
    y1 = [u.Val for u in val_query]
    y2 = [u.Val for u in val_query]

    source = ColumnDataSource(data=dict(
    x=wl,
    y1=y1,))
       
    print(y1)      
    print(y2)      
 
    p = figure(width=800, height=400)

    # add a line renderer
    p.vline_stack(['y1'],x='x', line_width=2, legend_label = str("Ch"),line_color="green",source = source)  
    p.xaxis.axis_label = "Wavelength[nm]"
    p.yaxis.axis_label = "power[dBm]"
    p.legend.location = "bottom_right"
   

    script, div = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files
   
    # return render_template('home.html', summary=summary)
    return render_template('Plot.html',script=script, div=div, cdn_css= cdn_css, cdn_js= cdn_js)

if __name__ == '__main__':
    app.run(debug=True)