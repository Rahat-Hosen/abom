from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY
from ..common import db, session, T, auth,flash

@action("customer/index")
@action.uses("customer/index.html",session,flash)
def index(id=None):
    sql = """
    SELECT * from customer
    """
    users = db.executesql(sql, as_dict=True)
        
    return locals()

def validation_check_customer(form):
    accpac_id=request.forms.get('accpac_id')
    name=request.forms.get('name')
    start_date=request.forms.get('start_date')
    address=request.forms.get('address')
    phone_no=request.forms.get('phone_no')
    website=request.forms.get('website')
    email=request.forms.get('email')
    fax=request.forms.get('fax')
    vat=request.forms.get('vat')
    accpac_code=request.forms.get('accpac_code')
    accpac_status=request.forms.get('accpac_status')
    errors=[]
    if name=='':
        errors.append('Enter name') 
    else:
        rows_check=db((db.customer.name==name)).select(db.customer.name,limitby=(0,1))
        if rows_check:
            form.errors['name'] = ''
            errors.append('Name already exist') 

    if accpac_id=='':
        errors.append('Enter accpac_id')  
    if start_date=='':
        errors.append('Enter start_date')  
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
    if vat=='':
        errors.append('Enter vat')  
    if accpac_code=='':
        errors.append('Enter accpac_code')  
    if accpac_status=='':
        errors.append('Enter accpac_status')  
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("customer/create", method=['GET', 'POST'])
@action.uses("customer/create.html", session,auth,T)
def create(id=None):  
    form = Form(db.customer,
        fields=['name','accpac_id','start_date','address','phone_no','website','email','fax','vat','accpac_code','accpac_status','status'],  
        keep_values=True,
        validation=validation_check_customer
    )
    if form.accepted:
        flash.set('Record added successfully', 'success')
        
        redirect(URL('customer','index'))          
    
    return locals()    
   
def edit_validation_check_customer(form):
    name=request.forms.get('name')
    accpac_id=request.forms.get('accpac_id')
    start_date=request.forms.get('start_date')
    address=request.forms.get('address')
    phone_no=request.forms.get('phone_no')
    website=request.forms.get('website')
    email=request.forms.get('email')
    fax=request.forms.get('fax')
    vat=request.forms.get('vat')
    accpac_code=request.forms.get('accpac_code')
    accpac_status=request.forms.get('accpac_status')
    errors=[]
    if name=='':
        errors.append('Enter name')     
    if accpac_id=='':
        errors.append('Enter accpac_id')  
    if start_date=='':
        errors.append('Enter start_date')  
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
    if vat=='':
        errors.append('Enter vat')  
    if accpac_code=='':
        errors.append('Enter accpac_code')  
    if accpac_status=='':
        errors.append('Enter accpac_status')            
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')

@action("customer/edit", method=['GET', 'POST'])
@action.uses("customer/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    record= db.customer(record_id) or redirect(URL('customer', 'index'))    
    form = Form(db.customer,
                record=record,
                fields=['name','accpac_id','start_date','address','phone_no','website','email','fax','vat','accpac_code','accpac_status''status'],  
                keep_values=True,
                deletable=True,
                validation=edit_validation_check_customer
                )
    if form.accepted:
        flash.set('Record Updated Successfully', 'success')        
        redirect(URL('customer','index'))
    return locals()


@action("customer/delete")
@action.uses("customer/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.customer.id == record_id).delete()
        
        flash.set('Record Delete successfully', 'error')      
        return dict(redirect(URL('customer', 'index')))

    return locals()


@action("customer/get_data", method=['GET', 'POST'])
def get_data():
 
    conditions = ""
    
    if  request.query.get('name') != None and request.query.get('name') !='':
        conditions += " and name = '"+str(request.query.get('name'))+"'"

    if  request.query.get('accpac_id') != None and request.query.get('accpac_id') !='':
        conditions += " and accpac_id = '"+str(request.query.get('accpac_id'))+"'"
    if  request.query.get('start_date') != None and request.query.get('start_date') !='':
        conditions += " and start_date = '"+str(request.query.get('start_date'))+"'"

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
    total_rows = len(db.executesql( "SELECT * FROM customer where 1 "+conditions, as_dict=True))

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
    SELECT * FROM `customer` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)

# API endpoint to sync customer data
@action("customer/sync", method=['GET', 'POST'])
def customer_sync():
    try:
        if request.json:
            customer_data = request.json  
            
            for customer in customer_data:
                existing_customer = db(db.customer.accpac_id == customer['accpac_id']).select().first()

                if existing_customer:
                    existing_customer.update_record(
                        cid=customer['cid'],
                        name=customer['name'],
                        start_date=customer['start_date'],
                        address=customer['address'],
                        phone_no=customer['phone_no'],
                        website=customer['website'],
                        email=customer['email'],
                        fax=customer['fax'],
                        vat=customer['vat'],
                        accpac_code=customer['accpac_code'],
                        accpac_status=customer['accpac_status'],
                        status=customer['status'],
                        updated_at=customer['updated_at']
                    )
                else:
                    db.customer.insert(
                        cid=customer['cid'],
                        accpac_id=customer['accpac_id'],
                        name=customer['name'],
                        start_date=customer['start_date'],
                        address=customer['address'],
                        phone_no=customer['phone_no'],
                        website=customer['website'],
                        email=customer['email'],
                        fax=customer['fax'],
                        vat=customer['vat'],
                        accpac_code=customer['accpac_code'],
                        accpac_status=customer['accpac_status'],
                        status=customer['status'],
                        updated_at=customer['updated_at']
                    )

            db.commit()
            
            return dict(success=True, message="Customer data synced successfully")
        else:
            return dict(success=False, message="No customer data received")
    except Exception as e:
        return dict(success=False, message=str(e))
