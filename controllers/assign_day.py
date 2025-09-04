from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY,IS_IN_SET
from ..common import db, session, T, auth,flash

@action("assign_day/index")
@action.uses("assign_day/index.html",session,flash)
def index(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    sql = """
    SELECT * from assign_day
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_assign_day(form):
    news_supplement=request.forms.get('news_supplement')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    date_on=request.forms.get('date_on')
    # print(str(form.errors))
    errors=[]
    if news_supplement=='':
        errors.append('Enter News supplement') 
    # else:
    #     rows_check=db((db.assign_day.news_supplement==news_supplement)).select(db.assign_day.news_supplement,limitby=(0,1))
    #     if rows_check:
    #         form.errors['news_supplement'] = ''
    #         errors.append('News/Supp. already exist') 

    if company=='':
        errors.append('Enter company')  
    if segment=='':
        errors.append('Enter segment')  
    if date_on=='':
        errors.append('Enter Date On')  
     
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("assign_day/create", method=['GET', 'POST'])
@action.uses("assign_day/create.html", session,auth,T)
def create(id=None):
    # check the sql value
    # xyz=db((db.news_supplement.status==1)).select().first()  
    # print(str(xyz))  
    db.assign_day.news_supplement.requires=IS_IN_DB(db((db.news_supplement.status==1)),db.news_supplement.name,error_message='Select a value',zero='Select a value',orderby=db.news_supplement.name)    
    db.assign_day.company.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)
    db.assign_day.segment.requires=IS_IN_DB(db((db.segment.status==1)),db.segment.name,error_message='Select a value',zero='Select a value',orderby=db.segment.name)
     
   
    form = Form(db.assign_day,
        fields=['news_supplement','company','segment','date_on','status'],  
        keep_values=True,
        validation=validation_check_assign_day
    )
    
    if 'news_supplement' in form.custom.widgets:
        form.custom.widgets['news_supplement']['_class'] = 'select_custom'
    if 'date_on' in form.custom.widgets:
        form.custom.widgets['date_on']['_class'] = 'select_custom'
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom' 
   
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('assign_day','index'))          
    
    return locals()    
   
def edit_validation_check_assign_day(form):
    news_supplement=request.forms.get('news_supplement')
    company=request.forms.get('company')
    segment=request.forms.get('segment')
    date_on=request.forms.get('date_on')
    
    errors=[]
    if news_supplement=='':
        errors.append('Enter News supple')     
    if company=='':
        errors.append('Enter company')  
    if segment=='':
        errors.append('Enter segment')  
    if date_on=='':
        errors.append('Enter Date on')  
          
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("assign_day/edit", method=['GET', 'POST'])
@action.uses("assign_day/edit.html", session,auth,T)
def edit(id=None): 
    db.assign_day.news_supplement.requires=IS_IN_DB(db((db.news_supplement.status==1)),db.news_supplement.name,error_message='Select a value',zero='Select a value',orderby=db.news_supplement.name)    
    db.assign_day.company.requires=IS_IN_DB(db((db.company.status==1)),db.company.name,error_message='Select a value',zero='Select a value',orderby=db.company.name)
    db.assign_day.segment.requires=IS_IN_DB(db((db.segment.status==1)),db.segment.name,error_message='Select a value',zero='Select a value',orderby=db.segment.name)    
          
    record_id = request.query.get('id')
    record= db.assign_day(record_id) or redirect(URL('assign_day', 'index'))    
    form = Form(db.assign_day,
                record=record,
                 fields=['news_supplement','company','segment','date_on','status'],  
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_assign_day
                )
    if 'news_supplement' in form.custom.widgets:
        form.custom.widgets['news_supplement']['_class'] = 'select_custom'
    if 'company' in form.custom.widgets:
        form.custom.widgets['company']['_class'] = 'select_custom'
    if 'segment' in form.custom.widgets:
        form.custom.widgets['segment']['_class'] = 'select_custom' 
    if 'date_on' in form.custom.widgets:
        form.custom.widgets['date_on']['_class'] = 'select_custom'
    
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('assign_day','index'))
    return locals()


@action("assign_day/delete")
@action.uses("assign_day/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.assign_day.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('assign_day', 'index')))

    return locals()


@action("assign_day/get_data", method=['GET', 'POST'])
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""
    # if  request.query.get('cid') != None and request.query.get('cid') !='':
    #     cid = str(request.query.get('cid'))
    #     conditions += " and cid = '"+cid+"'"
    
    if  request.query.get('news_supplement') != None and request.query.get('news_supplement') !='':
        conditions += " and news_supplement = '"+str(request.query.get('news_supplement'))+"'"

    if  request.query.get('language') != None and request.query.get('language') !='':
        conditions += " and language = '"+str(request.query.get('language'))+"'"

    if  request.query.get('address') != None and request.query.get('address') !='':
        conditions += " and address = '"+str(request.query.get('address'))+"'"

    if  request.query.get('status') != None and request.query.get('status') !='':
        conditions += " and status = '"+str(request.query.get('status'))+"'"
    #Search End## 
    
    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM assign_day where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `assign_day` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)
