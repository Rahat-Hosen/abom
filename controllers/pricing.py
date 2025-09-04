from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY,IS_IN_SET
from ..common import db, session, T, auth,flash

@action("pricing/index")
@action.uses("pricing/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from pricing
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_segment(form):
    segment=request.forms.get('segment')
    category=request.forms.get('category')
    news_supplement=request.forms.get('news_supplement')
    page_type=request.forms.get('page_type')
    color_type=request.forms.get('color_type')
    lmd=request.forms.get('lmd')
    unit_price =request.forms.get('unit_price')
    max_size =request.forms.get('max_size')
    label =request.forms.get('label')
    active_date =request.forms.get('active_date')
    errors=[]

    if segment=='':
        errors.append('Enter segment')  
    if category=='':
        errors.append('Enter category')  
    if news_supplement=='':
        errors.append('Enter news_supplement')  
    if page_type=='':
        errors.append('Enter page_type')  
    if color_type=='':
        errors.append('Enter color_type')  
    if lmd=='':
        errors.append('Enter lmd')  
    if unit_price=='':
        errors.append('Enter unit_price')  
    if max_size=='':
        errors.append('Enter max_size')  
    if label=='':
        errors.append('Enter label')  
    if active_date=='':
        errors.append('Enter active_date')  
    
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("pricing/create", method=['GET', 'POST'])
@action.uses("pricing/create.html", session,auth,T)
def create(id=None):  
    # xyz=db((db.company.status==1)).select().first()  //check the sql value
    # print(str(xyz))
    db.pricing.segment.requires = IS_IN_DB(db((db.segment.status == 1)), db.segment.name, error_message='Select a value', zero='Select a value', orderby=db.segment.name)
    db.pricing.category.requires = IS_IN_DB(db((db.category.status == 1)), db.category.name, error_message='Select a value', zero='Select a value', orderby=db.category.name)
    db.pricing.news_supplement.requires = IS_IN_DB(db((db.news_supplement.status == 1)), db.news_supplement.name, error_message='Select a value', zero='Select a value', orderby=db.news_supplement.name)
    db.pricing.page_type.requires = IS_IN_DB(db((db.page_type.status == 1)), db.page_type.name, error_message='Select a value', zero='Select a value', orderby=db.page_type.name)
    # db.pricing.color_type.requires = IS_IN_DB(db((db.assign_page_type.status == 1)), db.assign_page_type.color, error_message='Select a value', zero='Select a value', orderby=db.assign_page_type.color)
    db.pricing.page_name.requires = IS_IN_DB(db((db.supplement_page.status == 1)), db.supplement_page.page_name, error_message='Select a value', zero='Select a value', orderby=db.supplement_page.page_name)
    db.pricing.color_type.requires = IS_IN_SET(['Black & White', 'Color'], error_message='Select a value', zero='Select a value')
    form = Form(db.pricing,
        fields=['segment','category','news_supplement','page_type','color_type','lmd','unit_price','max_size','label','active_date'],  
        keep_values=True,
        validation=validation_check_segment
    )
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'
    if 'category' in form.custom.widgets:
        form.custom.widgets['category']['_class'] = 'select_custom'
    if 'news_supplement' in form.custom.widgets:
        form.custom.widgets['news_supplement']['_class'] = 'select_custom'
    if 'page_type' in form.custom.widgets:
        form.custom.widgets['page_type']['_class'] = 'select_custom'
    if 'color_type' in form.custom.widgets:
        form.custom.widgets['color_type']['_class'] = 'select_custom'
    if 'page_name' in form.custom.widgets:
        form.custom.widgets['page_name']['_class'] = 'select_custom'
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('pricing','index'))          
    
    return dict(form=form)  
   
def edit_validation_check_segment(form):
    segment=request.forms.get('segment')
    category=request.forms.get('category')
    news_supplement=request.forms.get('news_supplement')
    page_type=request.forms.get('page_type')
    color_type=request.forms.get('color_type')
    lmd=request.forms.get('lmd')
    unit_price =request.forms.get('unit_price')
    max_size =request.forms.get('max_size')
    label =request.forms.get('label')
    active_date =request.forms.get('active_date')
    errors=[]
    if segment=='':
        errors.append('Enter segment')  
    if category=='':
        errors.append('Enter category')  
    if news_supplement=='':
        errors.append('Enter news_supplement')  
    if page_type=='':
        errors.append('Enter page_type')  
    if color_type=='':
        errors.append('Enter color_type')  
    if lmd=='':
        errors.append('Enter lmd')  
    if unit_price=='':
        errors.append('Enter unit_price')  
    if max_size=='':
        errors.append('Enter max_size')  
    if label=='':
        errors.append('Enter label')  
    if active_date=='':
        errors.append('Enter active_date')      
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("pricing/edit", method=['GET', 'POST'])
@action.uses("pricing/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.pricing(record_id) or redirect(URL('pricing', 'index'))  
    db.pricing.segment.requires = IS_IN_DB(db((db.segment.status == 1)), db.segment.name, error_message='Select a value', zero='Select a value', orderby=db.segment.name)
    db.pricing.category.requires = IS_IN_DB(db((db.category.status == 1)), db.category.name, error_message='Select a value', zero='Select a value', orderby=db.category.name)
    db.pricing.news_supplement.requires = IS_IN_DB(db((db.news_supplement.status == 1)), db.news_supplement.name, error_message='Select a value', zero='Select a value', orderby=db.news_supplement.name)
    db.pricing.page_type.requires = IS_IN_DB(db((db.page_type.status == 1)), db.page_type.name, error_message='Select a value', zero='Select a value', orderby=db.page_type.name)
    db.pricing.color_type.requires = IS_IN_SET(['Black & White', 'Color'], error_message='Select a value', zero='Select a value')
    db.pricing.page_name.requires = IS_IN_DB(db((db.supplement_page.status == 1)), db.supplement_page.page_name, error_message='Select a value', zero='Select a value', orderby=db.supplement_page.page_name)
    form = Form(db.pricing,
                record=record,
                fields=['segment','category','news_supplement','page_type','color_type','lmd','unit_price','max_size','label','active_date'],    
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_segment
                )
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'
    if 'category' in form.custom.widgets:
        form.custom.widgets['category']['_class'] = 'select_custom'
    if 'news_supplement' in form.custom.widgets:
        form.custom.widgets['news_supplement']['_class'] = 'select_custom'
    if 'page_type' in form.custom.widgets:
        form.custom.widgets['page_type']['_class'] = 'select_custom'
    if 'color_type' in form.custom.widgets:
        form.custom.widgets['color_type']['_class'] = 'select_custom'
    if 'page_name' in form.custom.widgets:
        form.custom.widgets['page_name']['_class'] = 'select_custom'

    news_supplement_value = record.news_supplement if record else ""
    page_name_value = record.page_name if record else ""

    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('pricing','index'))
    return dict(form=form,record=record, news_supplement_value=news_supplement_value,page_name_value=page_name_value)

@action("pricing/delete")
@action.uses("pricing/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.segment.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('pricing', 'index')))

    return locals()


@action("pricing/get_data", method=['GET', 'POST'])
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
    SELECT * FROM `pricing` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
