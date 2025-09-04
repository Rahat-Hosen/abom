from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY,IS_IN_SET
from ..common import db, session, T, auth,flash

@action("additional_pricing/index")
@action.uses("additional_pricing/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from additional_pricing
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_segment(form):
    segment=request.forms.get('segment')
    company=request.forms.get('company')
    form_type=request.forms.get('form_type')
    errors=[]

    if segment=='':
        errors.append('Enter segment')  
    if company=='':
        errors.append('Enter company')  
    if form_type=='':
        errors.append('Enter form_type')  
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("additional_pricing/create", method=['GET', 'POST'])
@action.uses("additional_pricing/create.html", session,auth,T)
def create(id=None):  
    # xyz=db((db.company.status==1)).select().first()  //check the sql value
    # print(str(xyz))
    db.additional_pricing.segment.requires = IS_IN_DB(db((db.segment.status == 1)), db.segment.name, error_message='Select a value', zero='Select a value', orderby=db.segment.name)
    db.additional_pricing.company.requires = IS_IN_DB(db((db.company.status == 1)), db.company.name, error_message='Select a value', zero='Select a value', orderby=db.company.name)
    db.additional_pricing.form_type.requires = IS_IN_SET(
        ['Classified Page','Booking Page'], error_message='Select a value',zero='Select a value'
    )
    db.additional_pricing.policy_name.requires = IS_IN_SET(
        ['Bold','Box','Palo Box','Reverse','Specific','Top'], error_message='Select a value',zero='Select a value'
    )
    db.additional_pricing.type.requires = IS_IN_SET(
        ['Percentage(%)','Fixed Amount'], error_message='Select a value',zero='Select a value'
    )
    form = Form(db.additional_pricing,
        fields=['segment','company','form_type','policy_name','type','rate'],  
        keep_values=True,
        validation=validation_check_segment
    )
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'form_type' in form.custom.widgets:
        form.custom.widgets['form_type']['_class'] = 'select_custom'
    if 'policy_name' in form.custom.widgets:
        form.custom.widgets['policy_name']['_class'] = 'select_custom'
    if 'type' in form.custom.widgets:
        form.custom.widgets['type']['_class'] = 'select_custom'
    
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('additional_pricing','index'))          
    
    return dict(form=form)  
   
def edit_validation_check_segment(form):
    segment=request.forms.get('segment')
    company=request.forms.get('company')
   
    errors=[]
    if segment=='':
        errors.append('Enter segment')  
    if company=='':
        errors.append('Enter company')  
   
        errors.append('Enter active_date')      
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("additional_pricing/edit", method=['GET', 'POST'])
@action.uses("additional_pricing/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.additional_pricing(record_id) or redirect(URL('additional_pricing', 'index'))  
    db.additional_pricing.segment.requires = IS_IN_DB(db((db.segment.status == 1)), db.segment.name, error_message='Select a value', zero='Select a value', orderby=db.segment.name)
    db.additional_pricing.company.requires = IS_IN_DB(db((db.company.status == 1)), db.company.name, error_message='Select a value', zero='Select a value', orderby=db.company.name)
    db.additional_pricing.form_type.requires = IS_IN_SET(
        ['Classified Page','Booking Page'], error_message='Select a value',zero='Select a value'
    )
    db.additional_pricing.policy_name.requires = IS_IN_SET(
        ['Bold','Box','Palo Box','Reverse','Specific','Top'], error_message='Select a value',zero='Select a value'
    )
    db.additional_pricing.type.requires = IS_IN_SET(
        ['Percentage(%)','Fixed Amount'], error_message='Select a value',zero='Select a value'
    )
    form = Form(db.additional_pricing,
                record=record,
                fields=['segment','company'],    
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_segment
                )
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom'
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'form_type' in form.custom.widgets:
        form.custom.widgets['form_type']['_class'] = 'select_custom'
    if 'policy_name' in form.custom.widgets:
        form.custom.widgets['policy_name']['_class'] = 'select_custom'
    if 'type' in form.custom.widgets:
        form.custom.widgets['type']['_class'] = 'select_custom'
   
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('additional_pricing','index'))
    return locals()

@action("additional_pricing/delete")
@action.uses("additional_pricing/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.segment.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('additional_pricing', 'index')))

    return locals()


@action("additional_pricing/get_data", method=['GET', 'POST'])
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
    SELECT * FROM `additional_pricing` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
