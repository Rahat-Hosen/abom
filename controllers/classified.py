from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY,IS_IN_SET
from ..common import db, session, T, auth,flash
import time
import json
from datetime import date,datetime

@action("classified/index")
@action.uses("classified/index.html",session,flash)
def index(id=None):
    
    sql = """
    SELECT * from book_page  where page_type = 'Classified'
    """
    users = db.executesql(sql, as_dict=True)
   
    return locals()

def validation_check_proposal(form):
    errors=[]
   
   
@action("classified/create", method=['GET', 'POST'])
@action.uses("classified/create.html", session,auth,T)
def create(id=None): 
    today = datetime.today().strftime('%a').lower()
    today_date = datetime.today().date()

    daywise_items = db(db.assign_day[today] == True).select(db.assign_day.id, db.assign_day.news_supplement)
    news_items = db(db.assign_day.date_on == today_date).select(db.assign_day.id, db.assign_day.news_supplement)
    alldays_items =daywise_items + news_items
    utils_region=db(db.utils_region.status==1).select(db.utils_region.id,db.utils_region.name, orderby=db.utils_region.name)
    news_supplement=db(db.news_supplement.status==1).select(db.news_supplement.id,db.news_supplement.name, orderby=db.news_supplement.name)
    supplement_page=db(db.supplement_page.status==1).select(db.supplement_page.id,db.supplement_page.page_name, orderby=db.supplement_page.page_name)
    additional_pricing=db(db.additional_pricing.status==1).select(db.additional_pricing.id,db.additional_pricing.policy_name,db.additional_pricing.type,db.additional_pricing.rate, orderby=db.additional_pricing.policy_name)
    page_type=db(db.page_type.status==1).select(db.page_type.id,db.page_type.name, orderby=db.page_type.name)
    page_name=db(db.supplement_page.status==1).select(db.supplement_page.id,db.supplement_page.page_name, orderby=db.supplement_page.page_name)
    advertiser=db(db.advertiser.status==1).select(db.advertiser.id,db.advertiser.advertiser, orderby=db.advertiser.advertiser)
    classified_category=db(db.classified_category.status==1).select(db.classified_category.id,db.classified_category.category, orderby=db.classified_category.category)
    customer_ids=db(db.customer.status==1).select(db.customer.id,db.customer.accpac_id, orderby=db.customer.accpac_id)
    customer_names=db(db.customer.status==1).select(db.customer.id,db.customer.name, orderby=db.customer.name)
    customer_types=db(db.customer_type.status==1).select(db.customer_type.id,db.customer_type.name, orderby=db.customer_type.name)
    return locals()

def get_bknid():
    # Fetch the last booking_id, assuming the format is always BKN-xxxxxxxx
    last_record = db().select(db.book_page.booking_id, orderby=~db.book_page.id, limitby=(0, 1)).first()
    
    if last_record and last_record.booking_id:
        # Extract the numeric part from 'BKN-xxxxxxxx' and increment it
        last_num = int(last_record.booking_id.split('-')[1])
        new_num = last_num + 1
    else:
        # If no records, start from 1
        new_num = 1
    
    # Return the new booking ID with leading zeros, formatted to 8 digits
    return f"BKN-{new_num:08d}"

@action("classified/submit", method=['GET', 'POST'])
@action.uses(flash, session, db)
def submit(id=None):
    ad_multi_json = request.forms.get('ad_multi')
    ad_multi_entries = json.loads(ad_multi_json)

    if ad_multi_entries and len(ad_multi_entries) > 0:
        bkn_id = get_bknid() 
        db.book_page.insert(
            booking_id=bkn_id,
            booking_date=request.forms.get('booking_date'),
            publish_date=request.forms.get('publish_date'),
            news_supplement=request.forms.get('news_supplement'),
            page_type=request.forms.get('page_type'),
            page_name=request.forms.get('page_name'),
            customer_id=request.forms.get('customer_id'),
            customer_type=request.forms.get('customer_type'),
            customer_name=request.forms.get('customer_name'),
            advertiser=request.forms.get('advertiser'),
            reference=request.forms.get('reference'),
            region=request.forms.get('region'),
            title=request.forms.get('title'),
            classified_category=request.forms.get('classified_category'),
            word=request.forms.get('word'),
            rate=request.forms.get('rate'),
            subtotal=request.forms.get('subtotal'),
            discount_percentage=request.forms.get('discount_percentage'),
            discount_amount=request.forms.get('discount_amount'),
            gross_total=request.forms.get('gross_total'),
            box=request.forms.get('box'),
            top=request.forms.get('top'),
            bold=request.forms.get('bold'),
            specific=request.forms.get('specific'),
            palo_box=request.forms.get('palo_box'),
            reversed=request.forms.get('reversed'),
            additional_charge=request.forms.get('additional_charge'),
            net_total=request.forms.get('net_total'),
            booking_state_status=request.forms.get('booking_state_status'),
            status=request.forms.get('status')
        )

        # Loop through each entry in the submitted form data if there are multiple entries
        for entry in ad_multi_entries:
            bkn_id = get_bknid()  # Generate a new unique booking ID for each entry
            
            # Extract fields from the current entry
            publish_date = entry.get('publish_date')
            news_supplement = entry.get('news_supplement')
            page_type = entry.get('page_type')
            page_name = entry.get('page_name')

            db.book_page.insert(
                booking_id=bkn_id,
                booking_date=request.forms.get('booking_date'),
                publish_date=publish_date,
                news_supplement=news_supplement,
                page_name=page_name,
                page_type=page_type,
                customer_id=request.forms.get('customer_id'),
                customer_type=request.forms.get('customer_type'),
                customer_name=request.forms.get('customer_name'),
                advertiser=request.forms.get('advertiser'),
                reference=request.forms.get('reference'),
                region=request.forms.get('region'),
                title=request.forms.get('title'),
                classified_category=request.forms.get('classified_category'),
                word=request.forms.get('word'),
                rate=request.forms.get('rate'),
                subtotal=request.forms.get('subtotal'),
                discount_percentage=request.forms.get('discount_percentage'),
                discount_amount=request.forms.get('discount_amount'),
                gross_total=request.forms.get('gross_total'),
                box=request.forms.get('box'),
                top=request.forms.get('top'),
                bold=request.forms.get('bold'),
                specific=request.forms.get('specific'),
                palo_box=request.forms.get('palo_box'),
                reversed=request.forms.get('reversed'),
                additional_charge=request.forms.get('additional_charge'),
                net_total=request.forms.get('net_total'),
                booking_state_status=request.forms.get('booking_state_status'),
                status=request.forms.get('status')
            )
    else:
        # Insert a single entry when there are no multiple entries
        bkn_id = get_bknid()  # Generate a new unique booking ID
        db.book_page.insert(
            booking_id=bkn_id,
            booking_date=request.forms.get('booking_date'),
            publish_date=request.forms.get('publish_date'),
            news_supplement=request.forms.get('news_supplement'),
            page_type=request.forms.get('page_type'),
            page_name=request.forms.get('page_name'),
            customer_id=request.forms.get('customer_id'),
            customer_type=request.forms.get('customer_type'),
            customer_name=request.forms.get('customer_name'),
            advertiser=request.forms.get('advertiser'),
            reference=request.forms.get('reference'),
            region=request.forms.get('region'),
            title=request.forms.get('title'),
            classified_category=request.forms.get('classified_category'),
            word=request.forms.get('word'),
            rate=request.forms.get('rate'),
            subtotal=request.forms.get('subtotal'),
            discount_percentage=request.forms.get('discount_percentage'),
            discount_amount=request.forms.get('discount_amount'),
            gross_total=request.forms.get('gross_total'),
            box=request.forms.get('box'),
            top=request.forms.get('top'),
            bold=request.forms.get('bold'),
            specific=request.forms.get('specific'),
            palo_box=request.forms.get('palo_box'),
            reversed=request.forms.get('reversed'),
            additional_charge=request.forms.get('additional_charge'),
            net_total=request.forms.get('net_total'),
            booking_state_status=request.forms.get('booking_state_status'),
            status=request.forms.get('status')
        )

    # ad_multi_json = request.forms.get('ad_multi')
    # ad_multi_entries = json.loads(ad_multi_json)

    # for entry in ad_multi_entries:
    #     publish_date = entry.get('publish_date')
    #     news_supplement = entry.get('news_supplement')
    #     page_type = entry.get('page_type')
    #     page_name = entry.get('page_name')
    #     bkn_id = get_bknid()
    #     db.book_page.insert(
    #         booking_id=bkn_id,
    #         booking_date=request.forms.get('booking_date'),
    #         publish_date=publish_date,
    #         agency_id=request.forms.get('agency_id'),
    #         agency_name=request.forms.get('agency_name'),
    #         news_supplement=news_supplement,
    #         page_name=page_name,
    #         page_type=page_type,
    #         advertiser=request.forms.get('advertiser'),
    #         title=request.forms.get('title'),
    #         customer_id=request.forms.get('customer_id'),
    #         customer_type=request.forms.get('customer_type'),
    #         customer_name=request.forms.get('customer_name'),
    #         confused_field=request.forms.get('confused_field'),
    #         brand=request.forms.get('brand'),
    #         color_type=request.forms.get('color_type'),
    #         reference=request.forms.get('reference'),
    #         payment_type=request.forms.get('payment_type'),
    #         credit_limit=request.forms.get('credit_limit'),
    #         outstanding=request.forms.get('outstanding'),
    #         availed=request.forms.get('availed'),
    #         vat=request.forms.get('vat'),
    #         specific=request.forms.get('specific'),
    #         fixed_rate=request.forms.get('fixed_rate'),
    #         region=request.forms.get('region'),
    #         options=request.forms.get('options'),
    #         booking_state_status=request.forms.get('booking_state_status'),
    #         status=request.forms.get('status')
    #     )
    
    # Commit to save changes
    db.commit()

    session.flash = {"msg_type": "success", "msg": "classified entries added successfully."}
    return dict(redirect(URL('classified', 'index')))

def edit_validation_check(form):
    brand_name=request.forms.get('brand_name')
    rows_check=db((db.brand.brand_name==brand_name)&(db.brand.status==1)).select(db.brand.brand_name,limitby=(0,1))
    if rows_check:
        flash.set('Brand name already exist', 'warning')
    else:
        form.vars['brand_name']=brand_name

@action("classified/edit", method=['GET', 'POST'])
@action.uses("classified/edit.html", session,auth,T)
def edit(id=None):            
    record_id = request.query.get('id')
    today = datetime.today().strftime('%a').lower()
    today_date = datetime.today().date()  
    sql = """
    SELECT * from book_page where id ='{record_id}'
    """.format(record_id=record_id)

    head_record = db.executesql(sql, as_dict=True)
    head_record=head_record[0]
    details_sql = """
    SELECT * from book_page where book_page.id ='{record_id}'
    """.format(record_id=record_id)

    details_record = db.executesql(details_sql, as_dict=True)
    daywise_items = db(db.assign_day[today] == True).select(db.assign_day.id, db.assign_day.news_supplement)
    news_items = db(db.assign_day.date_on == today_date).select(db.assign_day.id, db.assign_day.news_supplement)
    alldays_items =daywise_items + news_items
    news_supplement=db(db.news_supplement.status==1).select(db.news_supplement.id,db.news_supplement.name, orderby=db.news_supplement.name)
    cause_cancels=db(db.cause_cancel.status==1).select(db.cause_cancel.id,db.cause_cancel.cause, orderby=db.cause_cancel.cause)
    utils_region=db(db.utils_region.status==1).select(db.utils_region.id,db.utils_region.name, orderby=db.utils_region.name)
    supplement_page=db(db.supplement_page.status==1).select(db.supplement_page.id,db.supplement_page.page_name, orderby=db.supplement_page.page_name)
    additional_pricing=db(db.additional_pricing.status==1).select(db.additional_pricing.id,db.additional_pricing.policy_name,db.additional_pricing.type,db.additional_pricing.rate, orderby=db.additional_pricing.policy_name)
    page_type=db(db.page_type.status==1).select(db.page_type.id,db.page_type.name, orderby=db.page_type.name)
    page_name=db(db.supplement_page.status==1).select(db.supplement_page.id,db.supplement_page.page_name, orderby=db.supplement_page.page_name)
    advertiser=db(db.advertiser.status==1).select(db.advertiser.id,db.advertiser.advertiser, orderby=db.advertiser.advertiser)
    option=db(db.advertiser.status==1).select(db.advertiser.id,db.advertiser.advertiser, orderby=db.advertiser.advertiser)
    classified_category=db(db.classified_category.status==1).select(db.classified_category.id,db.classified_category.category, orderby=db.classified_category.category)
    color_types=db(db.assign_page_type.status==1).select(db.assign_page_type.id,db.assign_page_type.color, orderby=db.assign_page_type.color)
    brands=db(db.brand.status==1).select(db.brand.id,db.brand.name, orderby=db.brand.name)
    customer_ids=db(db.customer.status==1).select(db.customer.id,db.customer.accpac_id, orderby=db.customer.accpac_id)
    customer_names=db(db.customer.status==1).select(db.customer.id,db.customer.name, orderby=db.customer.name)
    customer_types=db(db.customer_type.status==1).select(db.customer_type.id,db.customer_type.name, orderby=db.customer_type.name)
    return locals()

@action("classified/classified_update", method=['GET', 'POST'])
@action.uses(flash, session, db)
def proposal_update(id=None):  
    record_id = request.query.get('id')
    errors=[]
    booking_id=request.forms.get('booking_id')
    booking_date=request.forms.get('booking_date')
    publish_date=request.forms.get('publish_date')
    news_supplement=request.forms.get('news_supplement')
    customer_id=request.forms.get('customer_id')
    customer_name=request.forms.get('customer_name')
    customer_type=request.forms.get('customer_type')
    additional_pricing=request.forms.get('additional_pricing')    
    page_type=request.forms.get('page_type')    
    page_name=request.forms.get('page_name')    
    advertiser=request.forms.get('advertiser')    
    color_type=request.forms.get('color_type')    
    reference=request.forms.get('reference')    
    title=request.forms.get('title')      
    brand=request.forms.get('brand')    
    payment_type=request.forms.get('payment_type')    
    credit_limit=request.forms.get('credit_limit')    
    outstanding=request.forms.get('outstanding')    
    availed=request.forms.get('availed')    
    rate=request.forms.get('rate')      
    vat=request.forms.get('vat')    
    subtotal=request.forms.get('subtotal')    
    specific=request.forms.get('specific')    
    box=request.forms.get('box')    
    fixed_rate=request.forms.get('fixed_rate')    
    classified_category=request.forms.get('classified_category')   
    discount_percentage=request.forms.get('discount_percentage')    
    discount_amount=request.forms.get('discount_amount')    
    additional_charge=request.forms.get('additional_charge')    
    options=request.forms.get('options')    
    region=request.forms.get('region')    
    word=request.forms.get('word')      
    net_total=request.forms.get('net_total')    
    gross_total=request.forms.get('gross_total')    
    booking_state_status=request.forms.get('booking_state_status')    
    status=request.forms.get('status')
    # Blank check
    if booking_id == "":
        errors.append('booking_id date is required')  

    if booking_date == "":
        errors.append('booking_date is required')  

    if publish_date =="":
        errors.append('publish_date time is required.')

    if news_supplement == "":
        errors.append('news_supplement is required.')

    if additional_pricing == "":
        errors.append('additional_pricing is required.')
    
    if page_type == "":
        errors.append('page_type is required.')

    if page_name == "":
        errors.append('page_name is required.')

    if advertiser == "":
        errors.append('advertiser is required.')
    if customer_type == "":
        errors.append('customer type is required.')
    if customer_name == "":
        errors.append('customer name is required.')

    if classified_category == "":
        errors.append('classified_category is required.')
    if color_type == "":
        errors.append('color_type is required.')
    if discount_percentage == "":
        errors.append('discount_percentage is required.')
    if discount_amount == "":
        errors.append('discount_amount is required.')
    if additional_charge == "":
        errors.append('additional_charge is required.')
    if options == "":
        errors.append('options is required.')
    if region == "":
        errors.append('region is required.')
    if word == "":
        errors.append('word is required.')
    if region == "":
        errors.append('region is required.')
    if subtotal == "":
        errors.append('subtotal is required.')
    if net_total == "":
        errors.append('net_total is required.')
    if gross_total == "":
        errors.append('gross_total is required.')
    if booking_state_status == "":
        errors.append('booking_state_status is required.')
    # Check row & duplicate
   
    if errors:
        msg = ''
        for item in errors:
            msg = msg + item + 'rdrdrd'
        flash.set(msg, 'warning')
        return  dict(redirect(URL('classified','create')))
    
    if booking_id:
        db(db.book_page.id == record_id).update(
        booking_id=booking_id,
        booking_date=booking_date,
        publish_date=publish_date,
        news_supplement=news_supplement,
        additional_pricing=additional_pricing,
        page_name=page_name,
        page_type=page_type,
        advertiser=advertiser,
        title=title,
        customer_id=customer_id,
        customer_type=customer_type,
        customer_name=customer_name,
        brand=brand,
        color_type=color_type,
        reference=reference,
        payment_type=payment_type,
        credit_limit=credit_limit,
        outstanding=outstanding,
        availed=availed,
        rate=rate,
        vat=vat,
        subtotal=subtotal,
        specific=specific,
        box=box,
        fixed_rate=fixed_rate,
        classified_category=classified_category,
        discount_percentage=discount_percentage,
        discount_amount=discount_amount,    
        additional_charge=additional_charge,
        region=region,
        options=options,
        word=word,
        net_total=net_total,
        gross_total=gross_total,
        booking_state_status=booking_state_status,
        status=status     
    )
    # return len(brand)
    # Prepare details for bulk insert
    pro_details_list = []
    dict_data={}
    
    
    # Perform the bulk insert
    # db.proposal_details.bulk_insert(pro_details_list)
    
    # Commit to save changes
    db.commit()

    session.flash = {"msg_type":"success","msg":"classified added succesfully."}
    return  dict(redirect(URL('classified','index')))

@action("classified/delete")
@action.uses("classified/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.book_page.id == record_id).delete()

        flash.set('Record Delete successfully', 'error')        
        return dict(redirect(URL('classified', 'index')))

    return locals()

@action("classified/get_data", method=['GET', 'POST'])
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""

    # sql = """
    # SELECT h.proposal_sl,h.proposal_date, d.brand_name,d.campaign_duration,d.content_placement,d.ad_position,d.ad_size,d.ad_type,d.geo_target from classified h, proposal_details d where h.proposal_sl=d.proposal_sl
    # """

    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM book_page where 1"+conditions, as_dict=True))
    
    page = int(request.query.get('page') or 1)
    rows_per_page = int(request.query.get('rows_per_page') or 15)
    if rows_per_page == -1:
        rows_per_page = total_rows
    start = (page - 1) * rows_per_page         
    end = rows_per_page
    ##Paginate End##

    #Ordering Start##
    sort_column_index = int(request.query.get('order[0][column]') or 0)
    if sort_column_index == 0:
            sort_column_index = 0 #defult sorting column define
    sort_column_name = request.query.get('columns[' + str(sort_column_index) + '][data]')
    sort_direction = request.query.get('order[0][dir]')
    #Ordering End##

    ##Querry Start##
    sql = """ SELECT * FROM `book_page` WHERE page_type = 'Classified'
""" + conditions + """ ORDER BY """ + sort_column_name + """ """ + sort_direction + """
LIMIT """ + str(start) + "," + str(end) + """;
"""

    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)





@action("classified/book_cancel", method=['GET', 'POST'])
@action.uses(flash, session, db)
def book_cancel(id=None):  
    booking_id=request.forms.get('booking_id')
    booking_date=request.forms.get('booking_date')
    cause = request.forms.get('cause') 

    booking_record = db(db.book_page.booking_id == booking_id).select().first()
    if booking_record:
        booking_record.update_record(booking_cancel_status=1)
        db.commit()

    if booking_id and cause:
        cancel_date = datetime.today().date()
        cancel_time = datetime.now().strftime('%H:%M:%S')
       
        db.book_cancel.insert(
            booking_id=booking_id,
            cause=cause,
            booking_date=booking_date,
            cancel_date=cancel_date,
            cancel_time=cancel_time,
        )
    # Commit to save changes
    db.commit()

    session.flash = {"msg_type":"success","msg":"classified added succesfully."}
    return  dict(redirect(URL('classified','index')))
