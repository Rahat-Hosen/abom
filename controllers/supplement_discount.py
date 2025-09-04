from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("supplement_discount/index")
@action.uses("supplement_discount/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from supplement_discount
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_category(form):
    discount=request.forms.get('discount')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    category=request.forms.get('category')
    news_supplement=request.forms.get('news_supplement')
    page_type=request.forms.get('page_type')
    errors=[]
    

    if company=='':
        errors.append('Enter Company')  
    if discount=='':
        errors.append('Enter discount')  
    if segment=='':
        errors.append('Enter Segment')
    if category=='':
        errors.append('Enter Category')
    if page_type=='':
        errors.append('Enter page_type')
    if news_supplement=='':
        errors.append('Enter news_supplement')
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("supplement_discount/create", method=['GET', 'POST'])
@action.uses("supplement_discount/create.html", session,auth,T)
def create(id=None):  
    db.supplement_discount.company.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)
    db.supplement_discount.segment.requires=IS_IN_DB(db((db.segment.status==1)),db.segment.name,error_message='Select a value',zero='Select a value',orderby=db.segment.name)    
    db.supplement_discount.category.requires=IS_IN_DB(db((db.category.status==1)),db.category.name,error_message='Select a value',zero='Select a value',orderby=db.category.name)    
    db.supplement_discount.page_type.requires=IS_IN_DB(db((db.page_type.status==1)),db.page_type.name,error_message='Select a value',zero='Select a value',orderby=db.page_type.name)    
    db.supplement_discount.news_supplement.requires=IS_IN_DB(db((db.news_supplement.status==1)),db.news_supplement.name,error_message='Select a value',zero='Select a value',orderby=db.news_supplement.name)    
    form = Form(db.supplement_discount,
        fields=['discount','company','segment','category','page_type','news_supplement','status'],   
        keep_values=True,
        validation=validation_check_category
    )
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'   
    if 'category' in form.custom.widgets:
        form.custom.widgets['category']['_class'] = 'select_custom'   
    if 'page_type' in form.custom.widgets:
        form.custom.widgets['page_type']['_class'] = 'select_custom'   
    if 'news_supplement' in form.custom.widgets:
        form.custom.widgets['news_supplement']['_class'] = 'select_custom'   
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('supplement_discount','index'))          
    
    return locals()    
   
def edit_validation_check_category(form):
    discount=request.forms.get('discount')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    category=request.forms.get('category')
    page_type=request.forms.get('page_type')
    news_supplement=request.forms.get('news_supplement')
    errors=[]
    if discount=='':
        errors.append('Enter discount')     
    if company=='':
        errors.append('Enter Company')  
    if segment=='':
        errors.append('Enter Segment')  
    if category=='':
        errors.append('Enter Category')  
    if page_type=='':
        errors.append('Enter page_type')  
    if news_supplement=='':
        errors.append('Enter news_supplement')  
  
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("supplement_discount/edit", method=['GET', 'POST'])
@action.uses("supplement_discount/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.supplement_discount(record_id) or redirect(URL('category', 'index'))    
    db.supplement_discount.company.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)  
    db.supplement_discount.segment.requires=IS_IN_DB(db((db.segment.status==1)),db.segment.name,error_message='Select a value',zero='Select a value',orderby=db.segment.name)  
    db.supplement_discount.category.requires=IS_IN_DB(db((db.category.status==1)),db.category.name,error_message='Select a value',zero='Select a value',orderby=db.category.name)  
    db.supplement_discount.page_type.requires=IS_IN_DB(db((db.page_type.status==1)),db.page_type.name,error_message='Select a value',zero='Select a value',orderby=db.page_type.name)  
    db.supplement_discount.news_supplement.requires=IS_IN_DB(db((db.news_supplement.status==1)),db.news_supplement.name,error_message='Select a value',zero='Select a value',orderby=db.news_supplement.name)  
    form = Form(db.supplement_discount,
                record=record,
                fields=['discount','company','segment','page_type','news_supplement','status'],  
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
    if 'page_type' in form.custom.widgets:
        form.custom.widgets['page_type']['_class'] = 'select_custom'
    if 'news_supplement' in form.custom.widgets:
        form.custom.widgets['news_supplement']['_class'] = 'select_custom'
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('supplement_discount','index'))
    return locals()


@action("supplement_discount/delete")
@action.uses("supplement_discount/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.supplement_discount.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('supplement_discount', 'index')))

    return locals()


@action("supplement_discount/get_data", method=['GET', 'POST'])
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('discount') != None and request.query.get('discount') !='':
        conditions += " and discount = '"+str(request.query.get('discount'))+"'"
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
    SELECT * FROM `supplement_discount` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
