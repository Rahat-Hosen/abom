from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY,IS_IN_SET
from ..common import db, session, T, auth,flash

@action("assign_page_type/index")
@action.uses("assign_page_type/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from assign_page_type
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_news_supplement(form):
    # print("Form Data:", request.forms) 
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    category=request.forms.get('category')
    news_supplement=request.forms.get('news_supplement')
    color=request.forms.get('color')
    assign_page=request.forms.get('assign_page')
    page_type=request.forms.get('page_type')

    

    errors=[]
    # if name=='':
    #     errors.append('Enter name') 
    # else:
    #     rows_check=db((db.assign_page_type.name==name)).select(db.assign_page_type.name,limitby=(0,1))
    #     if rows_check:
    #         form.errors['name'] = ''
    #         errors.append('Name already exist') 

    if company=='':
        errors.append('Enter company')  
    if segment=='':
        errors.append('Enter segment')  
    if category=='':
        errors.append('Enter category')  
    if news_supplement=='':
        errors.append('Enter news/ supplement')  
    if color=='':
        errors.append('Enter color')  
    if assign_page=='':
        errors.append('Enter assign page')  
    if page_type=='':
        errors.append('Enter news page type')  
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("assign_page_type/create", method=['GET', 'POST'])
@action.uses("assign_page_type/create.html", session, auth, T)
def create(id=None):
    db.assign_page_type.company.requires = IS_IN_DB(db((db.company.status == 1)), db.company.name, error_message='Select a value', zero='Select a value', orderby=db.company.name)
    db.assign_page_type.segment.requires = IS_IN_DB(db((db.segment.status == 1)), db.segment.name, error_message='Select a value', zero='Select a value', orderby=db.segment.name)
    db.assign_page_type.category.requires = IS_IN_DB(db((db.category.status == 1)), db.category.name, error_message='Select a value', zero='Select a value', orderby=db.category.name)
    db.assign_page_type.page_type.requires = IS_IN_DB(db((db.page_type.status == 1)), db.page_type.name, error_message='Select a value', orderby=db.page_type.name)
    # db.assign_page_type.assign_page.requires = IS_IN_DB(db((db.supplement_page.status == 1)), db.supplement_page.page_name, error_message='Select a value', orderby=db.supplement_page.page_name)
    db.assign_page_type.color.requires = IS_IN_SET(['Black & White', 'Color'], error_message='Select a value', zero='Select a value')

     # Fetching the page names from the database
    # page_names = db((db.supplement_page.status == 1)).select(db.supplement_page.page_name,db.supplement_page.id, orderby=db.supplement_page.id)
    # assign_page = request.forms.get('assign_page')

# Check if assign_page is a list
    # if isinstance(assign_page, list):
    #     assign_page = ','.join(assign_page)  # Convert list to a comma-separated string
    # else:
    #     assign_page = str(assign_page)  # If it's not a list, just ensure it's a string

    # print(assign_page)  # This will print: 15,16,17

    # SELECT Name FROM news_supplement WHERE Category IN ('News');

    form = Form(db.assign_page_type,
            fields=['name', 'company', 'segment', 'category', 'color', 'assign_page', 'page_type', 'news_supplement', 'status'],
            keep_values=True,
            validation=validation_check_news_supplement)

    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'
    if 'category' in form.custom.widgets:
        form.custom.widgets['category']['_class'] = 'select_custom'
    if 'page_type' in form.custom.widgets:
        form.custom.widgets['page_type']['_class'] = 'select_custom'
    if 'color' in form.custom.widgets:
        form.custom.widgets['color']['_class'] = 'select_custom'
    if 'news_supplement' in form.custom.widgets:
        form.custom.widgets['news_supplement']['_class'] = 'select_custom'
    if 'assign_page' in form.custom.widgets:
        form.custom.widgets['assign_page']['_class'] = 'select_custom'
    if form.accepted:
        flash.set('Record added successfully', 'success')
        redirect(URL('assign_page_type', 'index'))
    return dict(form=form)  # Pass page_names to the template

def edit_validation_check_news_supplement(form):
    name=request.forms.get('name')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    category=request.forms.get('category')
    supp_category=request.forms.get('supp_category')
    no_of_pages=request.forms.get('no_of_pages')
    column_size=request.forms.get('column_size')
    inch_size=request.forms.get('inch_size')
    errors=[]
    if name=='':
        errors.append('Enter name')     
    if company=='':
        errors.append('Enter company')  
    if segment=='':
        errors.append('Enter segment')  
    if category=='':
        errors.append('Enter category')  
    if supp_category=='':
        errors.append('Enter supp_category')  
    if no_of_pages=='':
        errors.append('Enter no_of_pages')  
    if column_size=='':
        errors.append('Enter column_size')  
    if inch_size=='':
        errors.append('Enter inch_size')       
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("assign_page_type/edit", method=['GET', 'POST'])
@action.uses("assign_page_type/edit.html", session,auth,T)
def edit(id=None): 
    db.assign_page_type.company.requires = IS_IN_DB(db((db.company.status == 1)), db.company.name, error_message='Select a value', zero='Select a value', orderby=db.company.name)
    db.assign_page_type.segment.requires = IS_IN_DB(db((db.segment.status == 1)), db.segment.name, error_message='Select a value', zero='Select a value', orderby=db.segment.name)
    db.assign_page_type.category.requires = IS_IN_DB(db((db.category.status == 1)), db.category.name, error_message='Select a value', zero='Select a value', orderby=db.category.name)
    db.assign_page_type.page_type.requires = IS_IN_DB(db((db.page_type.status == 1)), db.page_type.name, error_message='Select a value', orderby=db.page_type.name)
    db.assign_page_type.color.requires = IS_IN_SET(['Black & White', 'Color'], error_message='Select a value', zero='Select a value')
    # db.assign_page_type.assign_page.requires = IS_IN_DB(db((db.supplement_page.status == 1)), db.supplement_page.page_name, error_message='Select a value', orderby=db.supplement_page.page_name)
    record_id = request.query.get('id')
    record= db.assign_page_type(record_id) or redirect(URL('assign_page_type', 'index'))    
    form = Form(db.assign_page_type,
                record=record,
                fields=['company','segment','category','news_supplement','page_type','color','assign_page','status'],    
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_news_supplement
                )
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom' 
    if 'category' in form.custom.widgets:
        form.custom.widgets['category']['_class'] = 'select_custom'  
    if 'page_type' in form.custom.widgets:
        form.custom.widgets['page_type']['_class'] = 'select_custom'
    if 'color' in form.custom.widgets:
        form.custom.widgets['color']['_class'] = 'select_custom'
    if 'news_supplement' in form.custom.widgets:
        form.custom.widgets['news_supplement']['_class'] = 'select_custom'
    if 'assign_page' in form.custom.widgets:
        form.custom.widgets['assign_page']['_class'] = 'select_custom'
        # Pass the news_supplement value to the template
    news_supplement_value = record.news_supplement if record else ""
    assign_page_value = record.assign_page if record else ""
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('assign_page_type','index'))
    return dict(form=form,record=record, news_supplement_value=news_supplement_value,assign_page_value=assign_page_value)


@action("assign_page_type/delete")
@action.uses("assign_page_type/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.assign_page_type.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('assign_page_type', 'index')))

    return locals()


@action("assign_page_type/get_data", method=['GET', 'POST'])
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
    total_rows = len(db.executesql( "SELECT * FROM assign_page_type where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `assign_page_type` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
