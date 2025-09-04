from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("receipt_mode/index")
@action.uses("receipt_mode/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from receipt_mode
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_category(form):
    receipt_mode=request.forms.get('receipt_mode')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    errors=[]
    if receipt_mode=='':
        errors.append('Enter receipt_mode') 
    else:
        rows_check=db((db.receipt_mode.receipt_mode==receipt_mode)).select(db.receipt_mode.receipt_mode,limitby=(0,1))
        if rows_check:
            form.errors['receipt_mode'] = ''
            errors.append('receipt_mode already exist') 

    if company=='':
        errors.append('Enter Company')  
    if segment=='':
        errors.append('Enter Segment')
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("receipt_mode/create", method=['GET', 'POST'])
@action.uses("receipt_mode/create.html", session,auth,T)
def create(id=None):  
    db.receipt_mode.company.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)
    db.receipt_mode.segment.requires=IS_IN_DB(db((db.segment.status==1)),db.segment.name,error_message='Select a value',zero='Select a value',orderby=db.segment.name)    
    form = Form(db.receipt_mode,
        fields=['receipt_mode','company','segment','status'],   
        keep_values=True,
        validation=validation_check_category
    )
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'   
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('receipt_mode','index'))          
    
    return locals()    
   
def edit_validation_check_category(form):
    receipt_mode=request.forms.get('receipt_mode')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    errors=[]
    if receipt_mode=='':
        errors.append('Enter receipt_mode')     
    if company=='':
        errors.append('Enter Company')  
    if segment=='':
        errors.append('Enter Segment')  
  
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("receipt_mode/edit", method=['GET', 'POST'])
@action.uses("receipt_mode/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.receipt_mode(record_id) or redirect(URL('receipt_mode', 'index'))    
    db.receipt_mode.company.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)  
    db.receipt_mode.segment.requires=IS_IN_DB(db((db.segment.status==1)),db.segment.name,error_message='Select a value',zero='Select a value',orderby=db.segment.name)  
    form = Form(db.receipt_mode,
                record=record,
                fields=['receipt_mode','company','segment','status'],  
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_category
                )
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('receipt_mode','index'))
    return locals()


@action("receipt_mode/delete")
@action.uses("receipt_mode/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.receipt_mode.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('receipt_mode', 'index')))

    return locals()


@action("receipt_mode/get_data", method=['GET', 'POST'])
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

    if  request.query.get('language') != None and request.query.get('language') !='':
        conditions += " and language = '"+str(request.query.get('language'))+"'"

    if  request.query.get('address') != None and request.query.get('address') !='':
        conditions += " and address = '"+str(request.query.get('address'))+"'"

    if  request.query.get('phone_no') != None and request.query.get('phone_no') !='':
        conditions += " and phone_no = '"+str(request.query.get('phone_no'))+"'"

    if  request.query.get('website') != None and request.query.get('website') !='':
        conditions += " and website = '"+str(request.query.get('website'))+"'"

    if  request.query.get('email') != None and request.query.get('email') !='':
        conditions += " and email = '"+str(request.query.get('email'))+"'"

    if  request.query.get('fax') != None and request.query.get('fax') !='':
        conditions += " and fax = '"+str(request.query.get('fax'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM receipt_mode where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `receipt_mode` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
