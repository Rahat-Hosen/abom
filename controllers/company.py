from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("company/index")
@action.uses("company/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from company
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_company(form):
    name=request.forms.get('name')
    language=request.forms.get('language')
    address=request.forms.get('address')
    phone_no=request.forms.get('phone_no')
    website=request.forms.get('website')
    email=request.forms.get('email')
    fax=request.forms.get('fax')
    errors=[]
    if name=='':
        errors.append('Enter name') 
    else:
        rows_check=db((db.company.name==name)).select(db.company.name,limitby=(0,1))
        if rows_check:
            form.errors['name'] = ''
            errors.append('Name already exist') 

    if language=='':
        errors.append('Enter language')  
    if address=='':
        errors.append('Enter address')  
    if phone_no=='':
        errors.append('Enter phone number')  
    if website=='':
        errors.append('Enter website')  
    if email=='':
        errors.append('Enter email')  
    if fax=='':
        errors.append('Enter fax')  
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("company/create", method=['GET', 'POST'])
@action.uses("company/create.html", session,auth,T)
def create(id=None):  
    form = Form(db.company,
        fields=['name','language','address','phone_no','website','email','fax','status'],  
        keep_values=True,
        validation=validation_check_company
    )
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('company','index'))          
    
    return locals()    
   
def edit_validation_check_company(form):
    name=request.forms.get('name')
    language=request.forms.get('language')
    address=request.forms.get('address')
    phone_no=request.forms.get('phone_no')
    website=request.forms.get('website')
    email=request.forms.get('email')
    fax=request.forms.get('fax')
    errors=[]
    if name=='':
        errors.append('Enter name')     
    if language=='':
        errors.append('Enter language')  
    if address=='':
        errors.append('Enter address')  
    if phone_no=='':
        errors.append('Enter phone number')  
    if website=='':
        errors.append('Enter website')  
    if email=='':
        errors.append('Enter email')  
    if fax=='':
        errors.append('Enter fax')          
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("company/edit", method=['GET', 'POST'])
@action.uses("company/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.company(record_id) or redirect(URL('company', 'index'))    
    form = Form(db.company,
                record=record,
                fields=['name','language','address','phone_no','website','email','fax','status'],  
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_company
                )
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('company','index'))
    return locals()


@action("company/delete")
@action.uses("company/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.company.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('company', 'index')))

    return locals()


@action("company/get_data", method=['GET', 'POST'])
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
    total_rows = len(db.executesql( "SELECT * FROM company where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `company` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
