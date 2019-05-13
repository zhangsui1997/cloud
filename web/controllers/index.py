# -*- coding: utf-8 -*-
from application import  app,db
from flask import Blueprint
from common.libs.Helper import ops_render
from common.libs.Helper import getFormatDate
from common.models.stat.StatDailySite import StatDailySite
from common.models.pay.PayOrder import PayOrder
from common.models.member.Member import Member
import datetime
route_index = Blueprint( 'index_page',__name__ )

# @route_index.route("/")
# def index():
#     resp_data = {
#         'data':{
#             'finance':{
#                 'today':0,
#                 'month':0
#             },
#             'member': {
#                 'today_new': 0,
#                 'month_new': 0,
#                 'total': 0
#             },
#             'order': {
#                 'today': 0,
#                 'month': 0
#             },
#             'shared': {
#                 'today': 0,
#                 'month': 0
#             },
#         }
#     }
#
#     now = datetime.datetime.now()
#     date_before_30days = now + datetime.timedelta( days = -30 )
#     date_from = getFormatDate( date = date_before_30days,format = "%Y-%m-%d" )
#     date_to = getFormatDate( date = now ,format = "%Y-%m-%d")
#
#     list = StatDailySite.query.filter(  StatDailySite.date >= date_from)\
#         .filter( StatDailySite.date <= date_to ).order_by( StatDailySite.id.asc() )\
#         .all()
#     #resp_data = resp_resp_data['resp_data']
#     if list:
#         for item in list:
#             resp_data['data']['finance']['month'] += item.total_pay_money
#             resp_data['data']['member']['month_new'] += item.total_new_member_count
#             resp_data['data']['member']['total'] = item.total_member_count
#             resp_data['data']['order']['month'] += item.total_order_count
#             resp_data['data']['shared']['month'] += item.total_shared_count
#             if getFormatDate( date = item.date ,format = "%Y-%m-%d") == date_to:
#                 resp_data['data']['finance']['today'] = item.total_pay_money
#                 resp_data['data']['member']['today_new'] = item.total_new_member_count
#                 resp_data['data']['order']['today'] = item.total_order_count
#                 resp_data['data']['shared']['today'] = item.total_shared_count
#     a=new_index()
#     print("===========",str(a))
#     return ops_render( "index/index.html",resp_data )

@route_index.route("/")
def new_index():
    resp_data = {
        'data': {
            'finance': {
                'month': 0
            },
            'member': {
                'month_new': 0
            },
            'order': {
                'month': 0
            },
            'shared': {
                'month': 0
            },
        }
    }
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    now = now + datetime.timedelta(days=1)
    date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    date_to = getFormatDate(date=now, format="%Y-%m-%d")
    f_count,m_count,o_count = 0,0,0

    finance_month = PayOrder.query.filter(PayOrder.express_status==1).filter(PayOrder.pay_time >= date_from) \
        .filter(PayOrder.pay_time <= date_to).all()
    for _ in finance_month:
        f_count += _.total_price
        o_count += 1
    resp_data['data']['finance']['month'] = f_count
    resp_data['data']['order']['month'] = o_count

    member_month = Member.query.filter(Member.created_time >= date_from) \
        .filter(Member.created_time <= date_to).all()
    for _ in member_month:
        m_count += 1

    resp_data['data']['member']['month_new'] = m_count
    return ops_render("index/index.html", resp_data)