from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("cause_cancel/index")
@action.uses("cause_cancel/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from cause_cancel
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_cause_cancel(form):
    cause=request.forms.get('cause')

    errors=[]
    if cause=='':
        errors.append('Enter Cause') 

    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("cause_cancel/create", method=['GET', 'POST'])
@action.uses("cause_cancel/create.html", session, auth, T)
def create(id=None):  
    form = Form(db.cause_cancel,
                fields=['cause', 'status'],   
                keep_values=True,
                validation=validation_check_cause_cancel
    )
   
    if form.accepted:

        flash.set('Record added successfully', 'success')
        redirect(URL('cause_cancel', 'index'))          
    
    return locals()    
   
def edit_validation_check_category(form):
    cause=request.forms.get('cause')
    errors=[]
    if cause=='':
        errors.append('Enter cause')     
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("cause_cancel/edit", method=['GET', 'POST'])
@action.uses("cause_cancel/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.cause_cancel(record_id) or redirect(URL('cause_cancel', 'index'))    

    form = Form(db.cause_cancel,
                record=record,
                fields=['cause','status'],  
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_category
                )
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('cause_cancel','index'))
    return locals()


@action("cause_cancel/delete")
@action.uses("cause_cancel/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.cause_cancel.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('cause_cancel', 'index')))

    return locals()


@action("cause_cancel/get_data", method=['GET', 'POST'])
def get_data():
  
    conditions = ""
  
    
    if  request.query.get('cause') != None and request.query.get('cause') !='':
        conditions += " and cause = '"+str(request.query.get('cause'))+"'"

    

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM cause_cancel where 1 "+conditions, as_dict=True))

    page = int(int(request.query.get('start'))/int(request.query.get('length')) +1 or 1)
    rows_per_page = int(request.query.get('length') or 15)
    if rows_per_page == -1:
        rows_per_page = total_rows
    start = (page - 1) * rows_per_page         
    end = rows_per_page
    ##Paginate End##

    #Ordering Start##
    sort_column_index = int(request.query.get('order[0][column]') or 0)
    sort_column_name = request.query.get('columns[' + str(sort_column_index) + '][data]') or 'id'
    sort_direction = request.query.get('order[0][dir]') or 'desc'
    #Ordering End##

    ##Querry Start##
    sql = """
    SELECT * FROM `cause_cancel` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
