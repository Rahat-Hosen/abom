from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("page_type/index")
@action.uses("page_type/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from page_type
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_category(form):
    name=request.forms.get('name')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    category=request.forms.get('category')
    errors=[]

    if company=='':
        errors.append('Enter Company')  
    if segment=='':
        errors.append('Enter Segment')
    if category=='':
        errors.append('Enter Category')
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("page_type/create", method=['GET', 'POST'])
@action.uses("page_type/create.html", session,auth,T)
def create(id=None):  
    db.page_type.company.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)
    db.page_type.segment.requires=IS_IN_DB(db((db.segment.status==1)),db.segment.name,error_message='Select a value',zero='Select a value',orderby=db.segment.name)    
    db.page_type.category.requires=IS_IN_DB(db((db.category.status==1)),db.category.name,error_message='Select a value',zero='Select a value',orderby=db.category.name)    
    form = Form(db.page_type,
        fields=['name','company','segment','category','status'],   
        keep_values=True,
        validation=validation_check_category
    )
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'   
    if 'category' in form.custom.widgets:
        form.custom.widgets['category']['_class'] = 'select_custom'   
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('page_type','index'))          
    
    return locals()    
   
def edit_validation_check_category(form):
    name=request.forms.get('name')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    category=request.forms.get('category')
    errors=[]
    if name=='':
        errors.append('Enter name')     
    if company=='':
        errors.append('Enter Company')  
    if segment=='':
        errors.append('Enter Segment')  
    if category=='':
        errors.append('Enter Category')  
  
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("page_type/edit", method=['GET', 'POST'])
@action.uses("page_type/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.page_type(record_id) or redirect(URL('category', 'index'))    
    db.page_type.company.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)  
    db.page_type.segment.requires=IS_IN_DB(db((db.segment.status==1)),db.segment.name,error_message='Select a value',zero='Select a value',orderby=db.segment.name)  
    db.page_type.category.requires=IS_IN_DB(db((db.category.status==1)),db.category.name,error_message='Select a value',zero='Select a value',orderby=db.category.name)  
    form = Form(db.page_type,
                record=record,
                fields=['name','company','segment','status'],  
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_category
                )
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'
    if 'category' in form.custom.widgets:
        form.custom.widgets['category']['_class'] = 'select_custom'
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('page_type','index'))
    return locals()


@action("page_type/delete")
@action.uses("page_type/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.page_type.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('page_type', 'index')))

    return locals()


@action("page_type/get_data", method=['GET', 'POST'])
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
    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM category where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `page_type` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
