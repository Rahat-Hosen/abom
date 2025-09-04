from py4web import action, request, abort, redirect, URL, response, Session
from py4web.utils.form import Form, FormStyleDefault
from yatl.helpers import A
from ..common import db, session, T, auth, flash
import json

@action("index")
@action.uses("index.html", session, flash)
def index():
    return dict(redirect(URL('login', 'index')))




# KAM section search start
@action("default/get_kam", method=['GET', 'POST'])
def get_kam():
    value = request.query.get('q')
    sql = """
    SELECT kam_name as id, kam_name as text FROM `kam` where kam_name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

@action("default/get_brand", method=['GET', 'POST'])
def get_brand():
    value = request.query.get('q')
    sql = """
    SELECT brand_name as id, brand_name as text FROM `brand` where brand_name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Ad size section search start
@action("default/get_adsize", method=['GET', 'POST'])
def get_adsize():
    value = request.query.get('q')
    sql = """
    SELECT adsize as id, adsize as text FROM `adsize` where adsize like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Inventory type section search start
@action("default/get_inventory_type", method=['GET', 'POST'])
def get_inventory_type():
    value = request.query.get('q')
    sql = """
    SELECT inventory_name as id, inventory_name as text FROM `inventory_type` where inventory_name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)

    sql = """
    SELECT acc_pac_id as id, acc_pac_id as text FROM `inventory_type` where acc_pac_id like '%{}%'
    """.format(value)
    data2 = db.executesql(sql, as_dict=True)
    return dict(results=data, results2=data2)

# Client section search start
@action("default/get_client", method=['GET', 'POST'])
def get_client():
    value = request.query.get('q')
    sql = """
    SELECT name as id, name as text FROM `client` where name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Company section search start
@action("default/get_company", method=['GET', 'POST'])
def get_company():
    value = request.query.get('q')
    sql = """
    SELECT company as id where company like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Agency name section search start
@action("default/get_agency_name", method=['GET', 'POST'])
def get_agency_name():
    value = request.query.get('q')
    sql = """
    SELECT agency_name as id, agency_name as text FROM `agency_contact` where agency_name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Site Section Searching

# Site_section search start
@action("default/get_site_section", method=['GET', 'POST'])
def get_site_section():
    value = request.query.get('q')
    sql = """
    SELECT section_name as id, section_name as text FROM `site_section` where section_name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Price_site_section search start
@action("default/get_price", method=['GET', 'POST'])
def get_price():
    value = request.query.get('q')
    sql = """
    SELECT site_section as id, site_section as text FROM `price` where site_section like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Price_inventory_type section search start
@action("default/get_price_inv", method=['GET', 'POST'])
def get_price_inv():
    value = request.query.get('q')
    sql = """
    SELECT inventory_type as id, inventory_type as text FROM `price` where inventory_type like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Industry section search start
@action("default/get_industry", method=['GET', 'POST'])
def get_industry():
    value = request.query.get('q')
    sql = """
    SELECT industry_name as id, industry_name as text FROM `industry` where industry_name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# GEO name section search start
@action("default/get_geo_target", method=['GET', 'POST'])
def get_geo_target():
    value = request.query.get('q')
    sql = """
    SELECT geo_name as id, geo_name as text FROM `geo_target` where geo_name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Segment section search start
@action("default/get_segment", method=['GET', 'POST'])
def get_segment():
    value = request.query.get('q')
    sql = """
    SELECT name as id, name as text FROM `segment` where name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Contact name section search start
@action("default/get_contact_name", method=['GET', 'POST'])
def get_contact_name():
    value = request.query.get('q')
    sql = """
    SELECT name as id, name as text FROM `contact` where name like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Contact designation section search start
@action("default/get_contact_designation", method=['GET', 'POST'])
def get_contact_designation():
    value = request.query.get('q')
    sql = """
    SELECT designation as id, designation as text FROM `contact` where designation like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Contact email section search start
@action("default/get_contact_email", method=['GET', 'POST'])
def get_contact_email():
    value = request.query.get('q')
    sql = """
    SELECT email as id, email as text FROM `contact` where email like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

# Contact no section search start
@action("default/get_contact_no", method=['GET', 'POST'])
def get_contact_no():
    value = request.query.get('q')
    sql = """
    SELECT contact_no as id, contact_no as text FROM `contact` where contact_no like '%{}%'
    """.format(value)
    data = db.executesql(sql, as_dict=True)
    return dict(results=data)

@action("default/get_proposal", method=['GET', 'POST'])
def get_proposal():
    value = request.query.get('q')
    agency_info = ''
    
    sql2 = """
    SELECT proposal_sl, client_id, segment, net_amount, vat, net_payable FROM `proposal_head` where proposal_sl = '{proposal_sl}' 
    """.format(proposal_sl=value)
    proposal_head = db.executesql(sql2, as_dict=True)
    
    sql = """
    SELECT client_id, name, address, second_address, email, city, contact_person, phone_number, po_number FROM `client` where id = '{client_id}' 
    """.format(client_id=proposal_head[0]['client_id'])
    client_info = db.executesql(sql, as_dict=True)
    
    if client_info[0]['name']:
        sql3 = """
        SELECT agency_name, contact_no, agency_email FROM `agency_contact` where company like '%{}%'
        """.format(client_info[0]['name'].strip())
        agency_info1 = db.executesql(sql3, as_dict=True)
        if len(agency_info1) > 0:  
            agency_info = agency_info1  
    
    details_sql = """
    SELECT brand_name, campaign_duration, content_placement, ad_position, ad_size, ad_type, geo_target, device, publication, qty_imp, cpm, cpm_amount, cpm_discount, cpm_discount_amount 
    FROM `proposal_details` where proposal_sl = '{proposal_sl}' 
    """.format(proposal_sl=value)
    proposal_details = db.executesql(details_sql, as_dict=True)
    
    combined_results = {
        'client_info': client_info,
        'proposal_info': proposal_head,
        'agency_info': agency_info,        
        'proposal_details_info': proposal_details,        
    }

    return dict(results=combined_results)

@action("default/get_inventory_wise_rate", method=['GET', 'POST'])
def get_inventory_wise_rate():
    ad_type = request.query.get('ad_type')
    site_section = request.query.get('site_section_name_val')
    # if ad_type is None or site_section is None:
    #     return dict(results=[])
         
    sql = """
    SELECT rate FROM `price` where inventory_type = '{inventory_type}' 
    """.format(inventory_type=ad_type)
    inventory_wise_rate = db.executesql(sql, as_dict=True)
    
    return dict(results=inventory_wise_rate)

@action("default/get_news_supplement", method=['GET', 'POST'])
def get_news_supplement():
    category = request.query.get('category')
         
    sql = """
    SELECT name FROM `news_supplement` where category = '{category}' 
    """.format(category=category)
    news_supplement_rec= db.executesql(sql, as_dict=True)
    
    return dict(results=news_supplement_rec)


@action("default/get_page_type", method=['GET', 'POST'])
def get_page_type():
    news_supplement = request.query.get('news_supplement')
    
    sql1 = """
    SELECT page_type FROM assign_page_type WHERE news_supplement = '{news_supplement}'
    """.format(news_supplement=news_supplement)
    page_types = db.executesql(sql1, as_dict=True)

    return dict(results=page_types)


@action("default/get_page_name", method=['GET', 'POST'])
def get_page_name():
    page_type = request.query.get('page_type')

    sql = """
    SELECT assign_page  FROM assign_page_type WHERE page_type = '{page_type}'
    """.format(page_type=page_type)
    
    page_names = db.executesql(sql, as_dict=True)
    
    return dict(results=page_names)


@action("default/get_supplement_page_name", method=['GET', 'POST'])
def get_supplement_page_name():
    supplement = request.query.get('supplement')

    sql = """
    SELECT page_name FROM supplement_page  WHERE supplement = '{supplement}'
    """.format(supplement=supplement)
    
    supplement_page_name = db.executesql(sql, as_dict=True)

    return dict(results=supplement_page_name)

@action("default/get_advertiser", method=['GET', 'POST'])
def get_advertiser():
    brand = request.query.get('brand')

    sql = """
    SELECT advertiser  FROM brand WHERE name = '{brand}'
    """.format(brand=brand)
    
    advertisers = db.executesql(sql, as_dict=True)
    
    return dict(results=advertisers)


@action("default/get_adv_sector", method=['GET', 'POST'])
def get_adv_sector():
    advertiser = request.query.get('advertiser')

    sql = """
    SELECT sub_adv_sector FROM advertiser WHERE advertiser = '{advertiser}'
    """.format(advertiser=advertiser)
    sub_adv_sector = db.executesql(sql, as_dict=True)[0]['sub_adv_sector']

    sql2 = """
    SELECT adv_sector FROM sub_adv_sector WHERE sub_adv_sector = '{sub_adv_sector}'
    """.format(sub_adv_sector=sub_adv_sector)
    adv_sectors = db.executesql(sql2, as_dict=True)
    return dict(results=adv_sectors)


@action("default/confirm_booking", method=['POST'])
def confirm_booking():

    booking_id = request.POST.get('booking_id')
    if not booking_id:
        response.status = 400
        return dict(status='error', message='No booking ID provided.')
    
    booking_record = db(db.book_page.booking_id == booking_id).select().first()


    if booking_record:
        booking_record.update_record(confirm=1)
        db.commit()

        return dict(status='success', message='Booking confirmed successfully.')
    else:
        response.status = 404
        return dict(status='error', message='Booking not found.')
    
@action("default/hold_booking", method=['POST'])
def hold_booking():

    booking_id = request.POST.get('booking_id')
    if not booking_id:
        response.status = 400
        return dict(status='error', message='No booking ID provided.')
    
    booking_record = db(db.book_page.booking_id == booking_id).select().first()


    if booking_record:
        booking_record.update_record(hold=1)
        db.commit()

        return dict(status='success', message='Booking holded successfully.')
    else:
        response.status = 404
        return dict(status='error', message='Booking not found.')

@action("default/get_unit_price", method=["GET", "POST"])
def get_unit_price():
    # Get parameters from the AJAX request
    news_supplement = request.query.get('news_supplement')
    page_type = request.query.get('page_type')
    page_name = request.query.get('page_name')
    color_type = request.query.get('color_type')

    # Perform SQL query to get the unit price from the Pricing table
    sql = """
    SELECT Unit_Price
    FROM Pricing
    WHERE 
        News_Supplement = %s AND 
        Page_Type = %s AND
        Page_Name = %s AND 
        Color_Type = %s
    """

    try:
        result = db.executesql(sql, (news_supplement, page_type, page_name, color_type), as_dict=True)
        if result:
            unit_price = result[0]['Unit_Price']
            return json.dumps({'unit_price': unit_price})
        else:
            return json.dumps({'error': 'Price not found'})
    
    except Exception as e:
        return json.dumps({'error': str(e)})
    


@action('default/get_specific_rate', method=["GET", "POST"])
@action.uses(db)
def get_specific_rate():
    form_type = 'Booking Page'
    policy_name = 'Specific'
    row = db((db.additional_pricing.form_type == form_type) &
             (db.additional_pricing.policy_name == policy_name)).select().first()
    if row:
        return dict(rate=row.rate)
    else:
        return dict(rate=None)
    
@action('default/get_box_rate', method=["GET", "POST"])
@action.uses(db)
def get_specific_rate():
    form_type = 'Booking Page'
    policy_name = 'Box'
    row = db((db.additional_pricing.form_type == form_type) &
             (db.additional_pricing.policy_name == policy_name)).select().first()
    if row:
        return dict(rate=row.rate)
    else:
        return dict(rate=None)
    
@action('default/get_box_rate_cls', method=["GET", "POST"])
@action.uses(db)
def get_specific_rate():
    form_type = 'Classified Page'
    policy_name = 'Box'
    row = db((db.additional_pricing.form_type == form_type) &
             (db.additional_pricing.policy_name == policy_name)).select().first()
    if row:
        return dict(rate=row.rate)
    else:
        return dict(rate=None)
    
@action('default/get_top_rate_cls', method=["GET", "POST"])
@action.uses(db)
def get_specific_rate():
    form_type = 'Classified Page'
    policy_name = 'Top'
    row = db((db.additional_pricing.form_type == form_type) &
             (db.additional_pricing.policy_name == policy_name)).select().first()
    if row:
        return dict(rate=row.rate)
    else:
        return dict(rate=None)
@action('default/get_palo_box_rate_cls', method=["GET", "POST"])
@action.uses(db)
def get_specific_rate():
    form_type = 'Classified Page'
    policy_name = 'Palo Box'
    row = db((db.additional_pricing.form_type == form_type) &
             (db.additional_pricing.policy_name == policy_name)).select().first()
    if row:
        return dict(rate=row.rate)
    else:
        return dict(rate=None)
@action('default/get_bold_rate_cls', method=["GET", "POST"])
@action.uses(db)
def get_specific_rate():
    form_type = 'Classified Page'
    policy_name = 'Bold'
    row = db((db.additional_pricing.form_type == form_type) &
             (db.additional_pricing.policy_name == policy_name)).select().first()
    if row:
        return dict(rate=row.rate)
    else:
        return dict(rate=None)
@action('default/get_reversed_rate_cls', method=["GET", "POST"])
@action.uses(db)
def get_specific_rate():
    form_type = 'Classified Page'
    policy_name = 'Reverse'
    row = db((db.additional_pricing.form_type == form_type) &
             (db.additional_pricing.policy_name == policy_name)).select().first()
    if row:
        return dict(rate=row.rate)
    else:
        return dict(rate=None)



@action('default/get_classified_price', method=["GET", "POST"])
def get_classified_price():
    pricing_type = request.query.get('pricing_type')

    if not pricing_type:
        return dict(error="Missing required parameters")


    sql1 = """
    SELECT first_words , addition_words, count_words FROM classified_pricing WHERE pricing_type = '{pricing_type}'
    """

    print(sql1)
    try:
        result = db.executesql(sql1.format(pricing_type=pricing_type), as_dict=True)
        if result:
            unit_price = result[0]['first_words']
            min_words = result[0]['count_words']
            additional_pricing = result[0]['addition_words']
        

            return json.dumps({'unit_price': unit_price,'additional_pricing': additional_pricing,'min_words': min_words})
        else:
            return json.dumps({'error': 'Price not found'})
    
    except Exception as e:
        return json.dumps({'error': str(e)})
    




