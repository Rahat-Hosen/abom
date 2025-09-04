# check compatibility
import py4web

assert py4web.check_compatible("0.1.20190709.1")

# by importing db you expose it to the _dashboard/dbadmin
from .models import db

# by importing controllers you expose the actions defined in it
from .controllers import login,default,dashboard,segment,company,category,news_supplement,assign_day,page_type,assign_page_type,supplement_page,pricing,additional_pricing,classified_category,classified_pricing,adv_sector,sub_adv_sector,advertiser,brand,receipt_mode,beneficiary_bank,book_page,classified,supplement_discount,cause_cancel,customer_type,customer,utils_region,receipt,test_conn,client

# optional parameters
__version__ = "0.0.0"
__author__ = "you <you@example.com>"
__license__ = "anything you want"
