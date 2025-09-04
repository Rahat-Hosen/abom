from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("segment/index")
@action.uses("segment/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from segment
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_segment(form):
    name=request.forms.get('name')
    company_name=request.forms.get('company_name')
    errors=[]
    if name=='':
        errors.append('Enter name')
    else:
        rows_check=db((db.segment.name==name)&(db.segment.status==1)).select(db.segment.name,limitby=(0,1))
        if rows_check:
            form.errors['name'] = ''
            errors.append('Name already exist') 

    if company_name=='':
        errors.append('Enter Company')  
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("segment/create", method=['GET', 'POST'])
@action.uses("segment/create.html", session,auth,T)
def create(id=None):  
    # xyz=db((db.company.status==1)).select().first()  //check the sql value
    # print(str(xyz))
    db.segment.company_name.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)
    form = Form(db.segment,
        fields=['name','company_name'],  
        keep_values=True,
        validation=validation_check_segment
    )
    if 'company_name' in form.custom.widgets:
        form.custom.widgets['company_name']['_class'] = 'select_custom'
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('segment','index'))          
    
    return locals()    
   
def edit_validation_check_segment(form):
    name=request.forms.get('name')
    company_name=request.forms.get('company_name')
    errors=[]
    if name=='':
        errors.append('Enter name')     
    if company_name=='':
        errors.append('Enter Company')          
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("segment/edit", method=['GET', 'POST'])
@action.uses("segment/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.segment(record_id) or redirect(URL('segment', 'index'))  
    db.segment.company_name.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)  
    form = Form(db.segment,
                record=record,
                fields=['name','company_name','status'],  
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_segment
                )
    if 'company_name' in form.custom.widgets:
        form.custom.widgets['company_name']['_class'] = 'select_custom'
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('segment','index'))
    return locals()

@action("segment/delete")
@action.uses("segment/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.segment.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('segment', 'index')))

    return locals()


@action("segment/get_data", method=['GET', 'POST'])
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('name') != None and request.query.get('name') !='':
        conditions += " and name = '"+str(request.query.get('name'))+"'"

    if  request.query.get('company_name') != None and request.query.get('company_name') !='':
        conditions += " and company_name = '"+str(request.query.get('company_name'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM segment where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `segment` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
