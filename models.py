"""
This file defines the database models
"""

from .common import db, Field, session,T
from pydal.validators import *
import os
from py4web import request

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()

from .common_cid import date_fixed
APP_FOLDER = os.path.dirname(__file__)

#*******************start Surjo Tables*******************
signature=db.Table(db,'signature',
                Field('field1','string',length=100,default=''), 
                Field('field2','integer',default=0),
                Field('note','string',length=255,default=''),  
                Field('created_on','datetime',default=date_fixed),
                Field('created_by',default=''),
                Field('updated_on','datetime',update=date_fixed),
                Field('updated_by',update=''),
                
                )
#*******************start segment Tables*******************
db.define_table('segment',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('company_id','integer',default=''),
                Field('company_name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end segment Tables*******************

#*******************start company Tables*******************
db.define_table('company',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('language','string',length=50,requires=IS_NOT_EMPTY()),
                Field('address','string',length=50,requires=IS_NOT_EMPTY()),
                Field('phone_no','string',length=50,requires=IS_NOT_EMPTY()),
                Field('website','string',length=50,requires=IS_NOT_EMPTY()),
                Field('email','string',length=50,requires=IS_EMAIL()),
                Field('fax','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end company Tables*******************

#*******************start Category Tables*******************
db.define_table('category',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end Category Tables*******************

#*******************start Supplement Page Tables*******************
db.define_table('supplement_page',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('supplement','string',length=50,requires=IS_NOT_EMPTY()),
                Field('page_id','string',length=20,default='1'),
                Field('page_name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end Supplement Page Tables*******************

#*******************start News Supplement Tables*******************
db.define_table('news_supplement',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('category','string',length=50,requires=IS_NOT_EMPTY()),
                Field('supp_category','string',length=50,requires=IS_NOT_EMPTY()),
                Field('no_of_pages','integer',requires=IS_NOT_EMPTY()),
                Field('column_size','integer',requires=IS_NOT_EMPTY()),
                Field('inch_size','float',requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end News Supplement Tables*******************

#*******************start Assign Day Tables*******************
db.define_table('assign_day',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('news_supplement','string',length=50,requires=IS_NOT_EMPTY()),
                Field('day_wise','string',length=1,default=0),
                Field('date_wise','string',length=50,default=0),
                Field("date_on","date"), 
                Field('sat','integer',length=1,default=0),
                Field('sun','integer',length=1,default=0),
                Field('mon','integer',length=1,default=0),
                Field('tue','integer',length=1,default=0),
                Field('wed','integer',length=1,default=0),
                Field('thu','integer',length=1,default=0),
                Field('fri','integer',length=1,default=0),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end Assign Day Tables*******************

#*******************start Page Type Tables*******************
db.define_table('page_type',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('category','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end Page Type Tables*******************

#*******************start assign page type Tables*******************
db.define_table('assign_page_type',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('category','string',length=50,requires=IS_NOT_EMPTY()),
                Field('news_supplement','string',length=50,requires=IS_NOT_EMPTY()),
                Field('page_type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('assign_page','string',length=50,requires=IS_NOT_EMPTY()),
                Field('color','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end assign page type Tables*******************

#*******************start pricing Tables*******************
db.define_table('pricing',
                Field('cid','string',length=20,default=''),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('category','string',length=50,requires=IS_NOT_EMPTY()),
                Field('news_supplement','string',length=50,requires=IS_NOT_EMPTY()),
                Field('page_name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('page_type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('color_type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('label','string',length=50,requires=IS_NOT_EMPTY()),
                Field('unit_price','float',requires=IS_NOT_EMPTY()),
                Field('max_size','float',requires=IS_NOT_EMPTY()),
                Field('lmd','date',requires=IS_NOT_EMPTY()),
                Field('active_date','date',requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end pricing Tables*******************

#*******************start additional pricing Tables*******************
db.define_table('additional_pricing',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('form_type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('policy_name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('rate','float',requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end additional pricing Tables*******************

#*******************start classified category Tables*******************
db.define_table('classified_category',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('category','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end classified category Tables*******************

#*******************start classified pricing Tables*******************
db.define_table('classified_pricing',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('pricing_type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('count_words','integer'),
                Field('first_words','integer'),
                Field('addition_words','integer'),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end classified pricing Tables*******************

#*******************start adv sector Tables*******************
db.define_table('adv_sector',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('adv_sector','string',length=100,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end adv sector Tables*******************

#*******************start sub adv sector Tables*******************
db.define_table('sub_adv_sector',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('adv_sector','string',length=100,requires=IS_NOT_EMPTY()),
                Field('sub_adv_sector','string',length=100,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end sub adv sector Tables*******************

#*******************start advertiser Tables*******************
db.define_table('advertiser',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('advertiser','string',length=100,requires=IS_NOT_EMPTY()),
                Field('sub_adv_sector','string',length=100,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end advertiser Tables*******************

#*******************start brand Tables*******************
db.define_table('brand',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('advertiser','string',length=100,requires=IS_NOT_EMPTY()),
                Field('sub_adv_sector','string',length=100,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end brand Tables*******************

#*******************start customer Tables*******************
db.define_table('customer',
                Field('cid','string',length=20,default=''),
                Field('accpac_id','string',length=50,requires=IS_NOT_EMPTY()),
                Field('name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('start_date','date'),
                Field('address','string',length=50),
                Field('phone_no','string',length=50),
                Field('website','string',length=50,requires=IS_NOT_EMPTY()),
                Field('email','string',length=50,requires=IS_NOT_EMPTY()),
                Field('fax','string',length=50),
                Field('vat','string'),
                Field('accpac_code','string',length=20),
                Field('accpac_status','string',default=1),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end customer Tables*******************

#*******************start customer type Tables*******************
db.define_table('customer_type',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=200,requires=IS_NOT_EMPTY()),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end customer type Tables*******************

#*******************start beneficiary bank Tables*******************
db.define_table('beneficiary_bank',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('receipt_mode','string',length=50,requires=IS_NOT_EMPTY()),
                Field('bank_id','string',length=50,requires=IS_NOT_EMPTY()),
                Field('bank_name','string',length=200,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end beneficiary bank Tables*******************

#*******************start receipt mode Tables*******************
db.define_table('receipt_mode',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('receipt_mode','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end receipt mode Tables*******************

#*******************start cause cancel Tables*******************
db.define_table('cause_cancel',
                Field('cid','string',length=20,default=''),
                Field('cause','string',length=50,requires=IS_NOT_EMPTY()),
                # Field('aud_user','string',length=50,requires=IS_NOT_EMPTY()),
                # Field('aud_date','date',requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end cause cancel Tables*******************

#*******************start supplement discount Tables*******************
db.define_table('supplement_discount',
                Field('cid','string',length=20,default=''),
                Field('company','string',length=50,requires=IS_NOT_EMPTY()),
                Field('segment','string',length=50,requires=IS_NOT_EMPTY()),
                Field('category','string',length=50,requires=IS_NOT_EMPTY()),
                Field('news_supplement','string',length=80),
                Field('page_type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('discount','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end supplement discount Tables*******************


#*******************start utils_region Tables*******************
db.define_table('utils_region',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end utils_region Tables*******************

#*******************start BOOK PAGE Tables*******************
db.define_table('book_page',
                Field('cid','string',length=20,default=''),
                Field('booking_id','string',length=50),
                Field('booking_date','date',requires=IS_NOT_EMPTY()),
                Field('publish_date','date',requires=IS_NOT_EMPTY()),
                Field('multi_ad_date','date'),
                Field('day_count','string',length=250),
                Field('agency_id','string',length=50),
                Field('agency_name','string',length=200),
                Field('news_supplement','string',length=80),
                Field('page_type','string',length=50),
                Field('page_name','string',length=50),
                Field('customer_id','string',length=200),
                Field('customer_name','string',length=200),
                Field('customer_type','string',length=200),
                Field('brand','string',length=250),
                Field('confused_field','string',length=250),
                Field('advertiser','string',length=250),
                Field('classified_category','string',length=200),
                Field('classified_categorysize','string',length=50),
                Field('reference','string',length=200),
                Field('discount_percentage','float'),
                Field('discount_amount','float'),
                Field('additional_charge','float'),
                Field('options','string',length=100), # Top/ PALO Box/ Bold/ Reversed
                Field('region','string',length=50),
                Field('word','integer',length=50),
                Field('subtotal','float'),
                Field('net_total','float'),
                Field('gross_total','float'), 
                Field('title','string',length=50),
                Field('payment_type','string',length=50),
                Field('credit_limit','float'),
                Field('outstanding','float'),
                Field('availed','float'),
                Field('color_type','string',length=50),
                Field('rate','integer'),
                Field('inch','float',length=50),
                Field('col','float',length=50),
                Field('div_id','integer',length=50),
                Field('div_postop','float',length=50),
                Field('div_posleft','float',length=50),
                Field('exempted_vat','float',length=50),
                Field('adv_sector','string',length=50),
                Field('vat_tax_amount','float',length=50),
                Field('vat','float',length=50,default=0),
                Field('vat_amount','float',length=50),
                Field('vat_tax_percentage','float',length=50),
                Field('receipt_total','float',length=50),
                Field('adjustment_total','float',length=50),
                Field('total_due','float',length=50),
                Field('box','float',length=50,default=0), # Top/ PALO_Box/ Bold/ Reversed
                Field('specific','float',length=50,default=0),
                Field('top','float',length=50,default=0),
                Field('palo_box','float',length=50,default=0),
                Field('bold','float',length=50,default=0),
                Field('reversed','float',length=50,default=0),
                Field('insertion_order','string',length=50),
                Field('ad_matter','string',length=50),
                Field('acc_revenue_ad','string',length=50),
                Field('acc_revenue_specific','string',length=50),
                Field('acc_revenue_box','string',length=50),
                Field('acc_advance','string',length=50),
                Field('acc_receivable','string',length=50),
                Field('acc_vat','string',length=50),
                Field('create_time','date'),
                Field('mult_book_ref','string',length=50),
                Field('job_circular','integer',length=50),
                Field('fixed_rate','integer',length=50),
                Field('fixed_rate_ref','string',length=50),
                Field('dc_type','string',length=50),
                Field('dc_date','date'),
                Field('dc_ref','string',length=50),
                Field('dc_status','integer',length=50),
                Field('dc_reason','string',length=50),
                Field('confirm','integer',default=0),
                Field('hold','integer',default=0),
                Field('booking_cancel_status','integer',default=0), #  cancel Or Not
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end BOOK PAGE Tables*****************************

#*******************start receipt Tables*****************************
db.define_table('receipt',
                Field('cid','string',length=20,default=''),
                Field('receipt_mode','string',length=50,requires=IS_NOT_EMPTY()),
                Field('receipt_type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('cash_bank','string',length=50,requires=IS_NOT_EMPTY()),
                Field('receipt_date','string',length=50,requires=IS_NOT_EMPTY()),
                Field('post_status','string',length=50,requires=IS_NOT_EMPTY()),
                Field('reverse_status','string',length=50,requires=IS_NOT_EMPTY()),
                Field('post_flag','string',length=50,requires=IS_NOT_EMPTY()),
                Field('booking_id','string',length=50),
                Field('cust_type','string',length=50,requires=IS_NOT_EMPTY()),
                Field('receive_amt','string',length=50,requires=IS_NOT_EMPTY()),
                Field('vat','string',length=50,requires=IS_NOT_EMPTY()),
                Field('ait','string',length=50,requires=IS_NOT_EMPTY()),
                Field('others','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end receipt Tables*********************

#*******************start book_cancel Tables*******************
db.define_table('book_cancel',
                Field('cid','string',length=20,default=''),
                Field('booking_id','string',length=50,requires=IS_NOT_EMPTY()),
                Field('booking_date','date'),
                Field('cancel_date','date'),
                Field('cancel_time','time'),
                Field('cause','string',length=50,requires=IS_NOT_EMPTY()),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end book_cancel Tables*******************


#*******************start client  Tables*********************
db.define_table('client',
                Field('cid','string',length=20,default=''),
                Field('name','string',length=100,requires=IS_NOT_EMPTY()),    
                Field('address','text',length=300,requires=IS_NOT_EMPTY()), 
                Field('second_address','text',length=300,requires=IS_NOT_EMPTY()), 
                Field('email','string',length=50,requires=IS_EMAIL()), 
                Field('city','string',length=50,requires=IS_NOT_EMPTY()), 
                Field('contact_person','string',length=100,requires=IS_NOT_EMPTY()), 
                Field('phone_number','string',length=50,requires=IS_NOT_EMPTY()), 
                Field('payment','string',length=20,requires=IS_NOT_EMPTY()), 
                Field('po_number','string',length=20,requires=IS_NOT_EMPTY()), 
                Field('vat','string',requires=IS_NOT_EMPTY()), 
                Field('dis_count','double',requires=IS_NOT_EMPTY()), 
                Field('credit_limit','double',requires=IS_NOT_EMPTY()), 
                Field('current_due','double',requires=IS_NOT_EMPTY()), 
                Field('accpac_code','string',length=20,requires=IS_NOT_EMPTY()), 
                Field('status','integer',length=1,default=1),
                signature,
                migrate=False
                )
#*******************end client  Tables*******************


#*******************start order Tables*******************
db.define_table('customer_orders',
                Field('cid','string',length=20,default=''),
                Field('accpac_id','string',length=50,requires=IS_NOT_EMPTY()),
                Field('customer_name','string',length=200),
                Field('booking_id','string',length=50),
                Field('publish_date','date',requires=IS_NOT_EMPTY()),
                Field('address','string',length=50),
                Field('phone_no','string',length=50),
                Field('email','string',length=50,requires=IS_NOT_EMPTY()),
                Field('accpac_status','string',default=1),
                Field('status','integer',default=1),
                signature,
                migrate=False
                )
#*******************end order Tables*******************