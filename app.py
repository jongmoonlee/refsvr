from wsgiref.validate import PartialIteratorWrapper
from flask import Flask, request, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import sqlalchemy
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
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



def refdata_query():
    form = RefdataForm()
    return Refdata.query


class RefdataForm(FlaskForm):
    DateId = QuerySelectField(query_factory=refdata_query, allow_blank=False, get_label='DateId')
    InSW = QuerySelectMultipleField(query_factory=refdata_query, allow_blank=False, get_label='InSW')
    SB = QuerySelectMultipleField(query_factory=refdata_query, allow_blank=False, get_label='SB')
    OPM = QuerySelectMultipleField(query_factory=refdata_query, allow_blank=False, get_label='OPM')
    PolState = QuerySelectMultipleField(query_factory=refdata_query, allow_blank=False, get_label='PolState')
    WL = QuerySelectMultipleField(query_factory=refdata_query, allow_blank=False, get_label='WL')
    Val = QuerySelectField(query_factory=refdata_query, allow_blank=False, get_label='Val')




@app.route("/")
@app.route("/home")
def home():    
    summary = Summary.query.all()    

    return render_template('home.html', summary=summary)

@app.route("/refdata")
def refdata():    
    summary = Refdata.query.filter(Refdata.DateId==2) 

    return render_template('refdata.html', summary=summary)

# DropDownList
@app.route("/<Date>", methods=["GET","POST"])
def Date(Date):
    DateIdQuery = Summary.query.with_entities(Summary.DateId).filter(Summary.Date ==Date)
    DateId = [u.InSW for u in DateIdQuery]  
    id = DateId[0]
    print("Xid")
    print(id)

    inSW_query = Refdata.query.with_entities(Refdata.InSW).distinct().filter(Refdata.DateId == id)    
    inSW = [u.InSW for u in inSW_query]  

    sb_query = Refdata.query.with_entities(Refdata.SB).distinct().filter(Refdata.DateId == id)       
    sb = [u.SB for u in sb_query]

    opm_query = Refdata.query.with_entities(Refdata.OPM).distinct().filter(Refdata.DateId == id)       
    opm = [u.OPM for u in opm_query]

    pol_query = Refdata.query.with_entities(Refdata.PolState).distinct().filter(Refdata.DateId == id)       
    pol = [u.PolState for u in pol_query]

    if request.method == 'POST':
        print("xxxxxx")
        print(id)
       
        inSW = request.form.get('inSW')
        SB = request.form.get('SB')
        OPM = request.form.get('OPM')
        PolState = request.form.get('PolState')
        print(inSW)
        print(SB)
        print(OPM)
        print(PolState)
        # return '<h1>{}</h1>'.format(form.RigName.data)
        return plot(2, inSW,SB,OPM,0)
    return render_template('select.html', pol=pol, inSW = inSW, sb=sb, opm=opm)

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



@app.route('/plot')
def plot(DateId,InSW,SB,OPM,PolState):
    wl_query = Refdata.query.with_entities(Refdata.WL).filter(Refdata.DateId==DateId,Refdata.InSW==InSW,Refdata.SB==SB,Refdata.OPM ==OPM, Refdata.PolState == PolState)
    val_query = Refdata.query.with_entities(Refdata.Val).filter(Refdata.DateId==DateId,Refdata.InSW==InSW,Refdata.SB==SB,Refdata.OPM ==OPM, Refdata.PolState == PolState)
    
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