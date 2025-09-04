from py4web import action, request, abort, redirect, URL,response,Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A,TAG, XML
from pydal.validators import IS_IN_DB, IS_NOT_EMPTY,IS_IN_SET
from ..common import db, session, T, auth,flash
import time
import json
import uuid
from datetime import datetime
@action("book_page/index")
@action.uses("book_page/index.html",session,flash)
def index(id=None):
    
    sql = """
    SELECT * from book_page
    """
    users = db.executesql(sql, as_dict=True)
   
    return locals()

def validation_check_book_page(form):
    # proposal_date=request.forms.get('publish_date')
    # advertiser=request.forms.get('advertiser')
    # kam=request.forms.get('kam')
    errors=[]


@action("book_page/create", method=['GET', 'POST'])
@action.uses("book_page/create.html", session,auth,T)
def create(id=None):  

    today = datetime.today().strftime('%a').lower()
    today_date = datetime.today().date()

    daywise_items = db(db.assign_day[today] == True).select(db.assign_day.id, db.assign_day.news_supplement)
    news_items = db(db.assign_day.date_on == today_date).select(db.assign_day.id, db.assign_day.news_supplement)
    alldays_items =daywise_items + news_items
    
    news_supplement=db(db.news_supplement.status==1).select(db.news_supplement.id,db.news_supplement.name, orderby=db.news_supplement.name)
    supplement_page=db(db.supplement_page.status==1).select(db.supplement_page.id,db.supplement_page.page_name, orderby=db.supplement_page.page_name)
    additional_pricing=db(db.additional_pricing.status==1).select(db.additional_pricing.id,db.additional_pricing.policy_name,db.additional_pricing.type,db.additional_pricing.rate, orderby=db.additional_pricing.policy_name)
    utils_region=db(db.utils_region.status==1).select(db.utils_region.id,db.utils_region.name, orderby=db.utils_region.name)
    advertiser=db(db.advertiser.status==1).select(db.advertiser.id,db.advertiser.advertiser, orderby=db.advertiser.advertiser)
    adv_sectors=db(db.adv_sector.status==1).select(db.adv_sector.id,db.adv_sector.adv_sector, orderby=db.adv_sector.adv_sector)
    color_types=db(db.assign_page_type.status==1).select(db.assign_page_type.id,db.assign_page_type.color, orderby=db.assign_page_type.color)
    brands=db(db.brand.status==1).select(db.brand.id,db.brand.name, orderby=db.brand.name)
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

@action("book_page/submit", method=['GET', 'POST'])
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
            agency_id=request.forms.get('agency_id'),
            agency_name=request.forms.get('agency_name'),
            advertiser=request.forms.get('advertiser'),
            title=request.forms.get('title'),
            customer_id=request.forms.get('customer_id'),
            customer_type=request.forms.get('customer_type'),
            customer_name=request.forms.get('customer_name'),
            confused_field=request.forms.get('confused_field'),
            brand=request.forms.get('brand'),
            color_type=request.forms.get('color_type'),
            reference=request.forms.get('reference'),
            payment_type=request.forms.get('payment_type'),
            credit_limit=request.forms.get('credit_limit'),
            outstanding=request.forms.get('outstanding'),
            availed=request.forms.get('availed'),
            rate=request.forms.get('rate'),
            inch=request.forms.get('inch'),
            col=request.forms.get('col'),
            vat=request.forms.get('vat'),
            subtotal=request.forms.get('subtotal'),
            specific=request.forms.get('specific'),
            box=request.forms.get('box'),
            fixed_rate=request.forms.get('fixed_rate'),
            adv_sector=request.forms.get('adv_sector'),
            discount_percentage=request.forms.get('discount_percentage'),
            discount_amount=request.forms.get('discount_amount'),
            additional_charge=request.forms.get('additional_charge'),
            region=request.forms.get('region'),
            options=request.forms.get('options'),
            word=request.forms.get('word'),
            net_total=request.forms.get('net_total'),
            gross_total=request.forms.get('gross_total'),
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
                agency_id=request.forms.get('agency_id'),
                agency_name=request.forms.get('agency_name'),
                news_supplement=news_supplement,
                page_name=page_name,
                page_type=page_type,
                advertiser=request.forms.get('advertiser'),
                title=request.forms.get('title'),
                customer_id=request.forms.get('customer_id'),
                customer_type=request.forms.get('customer_type'),
                customer_name=request.forms.get('customer_name'),
                confused_field=request.forms.get('confused_field'),
                brand=request.forms.get('brand'),
                color_type=request.forms.get('color_type'),
                reference=request.forms.get('reference'),
                payment_type=request.forms.get('payment_type'),
                credit_limit=request.forms.get('credit_limit'),
                outstanding=request.forms.get('outstanding'),
                availed=request.forms.get('availed'),
                rate=request.forms.get('rate'),
                inch=request.forms.get('inch'),
                col=request.forms.get('col'),
                vat=request.forms.get('vat'),
                subtotal=request.forms.get('subtotal'),
                specific=request.forms.get('specific'),
                box=request.forms.get('box'),
                fixed_rate=request.forms.get('fixed_rate'),
                adv_sector=request.forms.get('adv_sector'),
                discount_percentage=request.forms.get('discount_percentage'),
                discount_amount=request.forms.get('discount_amount'),
                additional_charge=request.forms.get('additional_charge'),
                region=request.forms.get('region'),
                options=request.forms.get('options'),
                word=request.forms.get('word'),
                net_total=request.forms.get('net_total'),
                gross_total=request.forms.get('gross_total'),
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
            agency_id=request.forms.get('agency_id'),
            agency_name=request.forms.get('agency_name'),
            advertiser=request.forms.get('advertiser'),
            title=request.forms.get('title'),
            customer_id=request.forms.get('customer_id'),
            customer_type=request.forms.get('customer_type'),
            customer_name=request.forms.get('customer_name'),
            confused_field=request.forms.get('confused_field'),
            brand=request.forms.get('brand'),
            color_type=request.forms.get('color_type'),
            reference=request.forms.get('reference'),
            payment_type=request.forms.get('payment_type'),
            credit_limit=request.forms.get('credit_limit'),
            outstanding=request.forms.get('outstanding'),
            availed=request.forms.get('availed'),
            rate=request.forms.get('rate'),
            inch=request.forms.get('inch'),
            col=request.forms.get('col'),
            vat=request.forms.get('vat'),
            subtotal=request.forms.get('subtotal'),
            specific=request.forms.get('specific'),
            box=request.forms.get('box'),
            fixed_rate=request.forms.get('fixed_rate'),
            adv_sector=request.forms.get('adv_sector'),
            discount_percentage=request.forms.get('discount_percentage'),
            discount_amount=request.forms.get('discount_amount'),
            additional_charge=request.forms.get('additional_charge'),
            region=request.forms.get('region'),
            options=request.forms.get('options'),
            word=request.forms.get('word'),
            net_total=request.forms.get('net_total'),
            gross_total=request.forms.get('gross_total'),
            booking_state_status=request.forms.get('booking_state_status'),
            status=request.forms.get('status')
        )

    db.commit()

    session.flash = {"msg_type": "success", "msg": "Book page entries added successfully."}
    return dict(redirect(URL('book_page', 'index')))


def edit_validation_check(form):
    brand_name=request.forms.get('brand_name')
    rows_check=db((db.brand.brand_name==brand_name)&(db.brand.status==1)).select(db.brand.brand_name,limitby=(0,1))
    if rows_check:
        flash.set('Brand name already exist', 'warning')
    else:
        form.vars['brand_name']=brand_name

@action("book_page/edit", method=['GET', 'POST'])
@action.uses("book_page/edit.html", session,auth,T)
def edit(id=None):
    today = datetime.today().strftime('%a').lower()
    today_date = datetime.today().date()     
    record_id = request.query.get('id')

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
    utils_region=db(db.utils_region.status==1).select(db.utils_region.id,db.utils_region.name, orderby=db.utils_region.name)
    cause_cancels=db(db.cause_cancel.status==1).select(db.cause_cancel.id,db.cause_cancel.cause, orderby=db.cause_cancel.cause)
    supplement_page=db(db.supplement_page.status==1).select(db.supplement_page.id,db.supplement_page.page_name, orderby=db.supplement_page.page_name)
    additional_pricing=db(db.additional_pricing.status==1).select(db.additional_pricing.id,db.additional_pricing.policy_name,db.additional_pricing.type,db.additional_pricing.rate, orderby=db.additional_pricing.policy_name)
    page_type=db(db.page_type.status==1).select(db.page_type.id,db.page_type.name, orderby=db.page_type.name)
    page_name=db(db.supplement_page.status==1).select(db.supplement_page.id,db.supplement_page.page_name, orderby=db.supplement_page.page_name)
    advertiser=db(db.advertiser.status==1).select(db.advertiser.id,db.advertiser.advertiser, orderby=db.advertiser.advertiser)
    adv_sectors=db(db.adv_sector.status==1).select(db.adv_sector.id,db.adv_sector.adv_sector, orderby=db.adv_sector.adv_sector)
    color_types=db(db.assign_page_type.status==1).select(db.assign_page_type.id,db.assign_page_type.color, orderby=db.assign_page_type.color)
    brands=db(db.brand.status==1).select(db.brand.id,db.brand.name, orderby=db.brand.name)
    customer_ids=db(db.customer.status==1).select(db.customer.id,db.customer.accpac_id, orderby=db.customer.accpac_id)
    customer_names=db(db.customer.status==1).select(db.customer.id,db.customer.name, orderby=db.customer.name)
    customer_types=db(db.customer_type.status==1).select(db.customer_type.id,db.customer_type.name, orderby=db.customer_type.name)
    return locals()

@action("book_page/book_page_update", method=['GET', 'POST'])
@action.uses(flash, session, db)
def book_page_update(id=None):
    record_id = request.query.get('id')
    errors = []

    # Get form data without commas to avoid creating tuples
    booking_id = request.forms.get('booking_id')
    booking_date = request.forms.get('booking_date')
    publish_date = request.forms.get('publish_date')
    news_supplement = request.forms.get('news_supplement')  # Fixed: no comma
    page_name = request.forms.get('page_name')
    page_type = request.forms.get('page_type')
    advertiser = request.forms.get('advertiser')
    title = request.forms.get('title')
    customer_id = request.forms.get('customer_id')
    customer_type = request.forms.get('customer_type')
    customer_name = request.forms.get('customer_name')
    confused_field = request.forms.get('confused_field')
    brand = request.forms.get('brand')
    color_type = request.forms.get('color_type')
    reference = request.forms.get('reference')
    payment_type = request.forms.get('payment_type')
    credit_limit = request.forms.get('credit_limit')
    outstanding = request.forms.get('outstanding')
    availed = request.forms.get('availed')
    rate = request.forms.get('rate')
    inch = request.forms.get('inch')
    col = request.forms.get('col')
    vat = request.forms.get('vat')
    subtotal = request.forms.get('subtotal')
    specific = request.forms.get('specific')
    box = request.forms.get('box')
    fixed_rate = request.forms.get('fixed_rate')
    adv_sector = request.forms.get('adv_sector')
    discount_percentage = request.forms.get('discount_percentage')
    discount_amount = request.forms.get('discount_amount')
    additional_charge = request.forms.get('additional_charge')
    region = request.forms.get('region')
    net_total = request.forms.get('net_total')
    gross_total = request.forms.get('gross_total')
    status = request.forms.get('status')
    # Validation checks
    if not booking_id:
        errors.append('Booking ID is required.')
    if not booking_date:
        errors.append('Booking date is required.')
    if not publish_date:
        errors.append('Publish date is required.')
    if not news_supplement:
        errors.append('News supplement is required.')

    # If there are errors, flash them and redirect back
    if errors:
        msg = ' '.join(errors)
        flash.set(msg, 'warning')
        return dict(redirect(URL('book_page', 'create')))
    try:
        # Perform the update operation
        db(db.book_page.id == record_id).update(
            booking_date=booking_date,
            publish_date=publish_date,
            news_supplement=news_supplement,
            page_type=page_type,
            page_name=page_name,
            customer_id=customer_id,
            customer_name=customer_name,
            customer_type=customer_type,
            brand=brand,
            advertiser=advertiser,
            adv_sector=adv_sector,
            reference=reference,
            title=title,
            region=region,
            payment_type=payment_type,
            col=col,
            inch=inch,
            credit_limit=credit_limit,
            outstanding=outstanding,
            availed=availed,
            color_type=color_type,
            rate=rate,
            subtotal=subtotal,
            discount_amount=discount_amount,
            discount_percentage=discount_percentage,
            gross_total=gross_total,
            specific=specific,
            box=box,
            additional_charge=additional_charge,
            vat=vat,
            fixed_rate=fixed_rate,
            net_total=net_total,
            confused_field=confused_field,
            status=status
        )
        db.commit()
        session.flash = {"msg_type": "success", "msg": "Book page updated successfully."}
    except Exception as e:
        flash.set(f"An error occurred: {str(e)}", 'error')

    return dict(redirect(URL('book_page', 'index')))


@action("book_page/delete")
@action.uses("book_page/index.html",session,flash)
def delete(id=None):
    # if session['status']!='success':
    #     return 'Access Denied'
    record_id = request.query.get('id')
    if record_id:
        db(db.book_page.id == record_id).delete()

        flash.set('Record Delete successfully', 'error')        
        return dict(redirect(URL('book_page', 'index')))

    return locals()

@action("book_page/get_data", method=['GET', 'POST'])
def get_data():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""

   

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
    sql = """ 
    SELECT * FROM `book_page` WHERE page_type != 'Classified'
    """ + conditions + """
    ORDER BY """ + sort_column_name + """ """ + sort_direction + """
    LIMIT """ + str(start) + "," + str(end) + """;
    """
    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)


@action("book_page/get_data_details", method=['GET', 'POST'])
def get_data_details():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    #Search Start##
    conditions = ""

    # sql = """
    # SELECT h.proposal_sl,h.proposal_date, d.brand_name,d.campaign_duration,d.content_placement,d.ad_position,d.ad_size,d.ad_type,d.geo_target from book_page h, proposal_details d where h.proposal_sl=d.proposal_sl
    # """

    ##Paginate Start##
    total_rows = len(db.executesql( "SELECT * FROM proposal_details where 1"+conditions, as_dict=True))
    
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
    sql = """
    SELECT * FROM `proposal_details` where 1"""+conditions+""" ORDER BY """+sort_column_name+""" """+sort_direction+""" LIMIT """+str(start)+""","""+str(end)+""";
    """
    data = db.executesql(sql, as_dict=True)
    
    return dict(data=data, total_rows=total_rows,recordsFiltered=total_rows,recordsTotal=total_rows,sort_column_name=sort_column_name)
    # return json.dumps(data)

@action("book_page/proposal_list_preview", method=['GET', 'POST'])
@action.uses("book_page/proposal_list_preview.html",session,flash)
def proposal_list_preview():
    # if session.status=="" or session.status==None:
    #   redirect(URL(c='login',f='index'))
    record_id = request.query.get('id')

    sql = """
    SELECT * from book_page where id ='{record_id}'
    """.format(record_id=record_id)

    head_record = db.executesql(sql, as_dict=True)
    head_record=head_record[0]
    
    details_sql = """
    SELECT * from proposal_details where proposal_head_id ='{record_id}'
    """.format(record_id=record_id)

    details_record = db.executesql(details_sql, as_dict=True)
    
    
    return locals()

@action("book_page/book_cancel", method=['GET', 'POST'])
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

    session.flash = {"msg_type":"success","msg":"book_page added succesfully."}
    return  dict(redirect(URL('book_page','index')))
