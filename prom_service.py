# -*- coding: utf-8 -*-
import pytz
import dateutil.parser
import urllib

from datetime import datetime


def get_all_prom_dates(initial_tender_data, key):
    tender_period = initial_tender_data.data.auctionPeriod
    start_dt = dateutil.parser.parse(tender_period['startDate'])
    data = {
        'StartDate': start_dt.strftime("%d.%m.%Y %H:%M"),
    }
    return data.get(key, '')


def convert_date_prom(date):
    date_obj = datetime.strptime(date, "%d.%m.%y %H:%M")
    time_zone = pytz.timezone('Europe/Kiev')
    localized_date = time_zone.localize(date_obj)
    return localized_date.strftime("%Y-%m-%d %H:%M:%S.%f%z")


def convert_dgf_date_prom(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d.%m.%Y")


def revert_dgf_date_prom(date_str):
    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    return date_obj.strftime("%Y-%m-%d")


def convert_date_to_prom_tender_startdate(date):
    first_date = date.split(' - ')[0]
    date_obj = datetime.strptime(first_date, "%d.%m.%y %H:%M")
    time_zone = pytz.timezone('Europe/Kiev')
    localized_date = time_zone.localize(date_obj)
    return localized_date.strftime("%Y-%m-%d %H:%M:%S.%f%z")


def convert_date_to_prom_tender_enddate(date):
    second_date = date.split(' - ')[1]
    date_obj = datetime.strptime(second_date, "%d.%m.%y %H:%M")
    time_zone = pytz.timezone('Europe/Kiev')
    localized_date = time_zone.localize(date_obj)
    return localized_date.strftime("%Y-%m-%d %H:%M:%S.%f%z")


def convert_prom_string_to_common_string(string):
    return {
        u"грн": u"UAH",
        u"шт.": u"штуки",
        u"кв.м.": u"метри квадратні",
        u"метры квадратные": u"метри квадратні",
        u"з ПДВ": True,
        u"Класифікатор:": u"CAV",
        u"Період уточнень": u"active.enquiries",
        u"Прийом пропозицій": u"active.tendering",
        u"Аукціон": u"active.auction",
        u"Кваліфікація": u"active.qualification",
        u"Скасована": u"cancelled",
        u"Аукціон не відбувся": u"unsuccessful",
        u"Аукцион не состоялся": u"unsuccessful",
        u"Завершена": u"complete",
        u"Подписанный": u"active",
        u"Впервые": u"Лот виставляється вперше",
        u"Повторно": u"Лот виставляється повторно",
    }.get(string, string)


def convert_cancellations_status(string):
    return {
        u"Скасована": u"active",
    }.get(string, string)


def convert_procurement_method_type(string):
    return {
        u"МАЙНО": u"dgfOtherAssets",
        u"ФІНАНСОВІ АКТИВИ": u"dgfFinancialAssets",
    }.get(string, string)


def convert_prom_code_to_common_string(string):
    return {
        u"кв.м.": u"MTK",
        u"послуга": u"E48",
        u"послуги": u"E48",
        u"шт.": u"H87",
        u"Класифікатор:": u"CAV",
        u"Очікує протокол": u"pending.verification",
        u"очікується протокол": u"pending.verification",
        # u"Очікує кваліфікації": u"pending.waiting",
        u"Очікує рішення": u"pending.waiting",
        u"очікується кінець кваліфікації": u"pending.waiting",
        u"Пропозицію відхилено": u"unsuccessful",
        u"Очікується оплата": u"pending.payment",
        u"Переможець": u"active",
        u"Очікує розгляду": u"cancelled",
    }.get(string, string)


def convert_document_type(string):
    return {
        u"x_nda": u"Договір NDA",
        u"tenderNotice": u"Паспорт торгів",
        u"x_presentation": u"Презентація",
        u"technicalSpecifications": u"Публічний паспорт активу",
    }.get(string, string)


def revert_document_type(string):
    return {
        u"Договір NDA": u"x_nda",
        u"Паспорт торгів": u"tenderNotice",
        u"Презентація": u"x_presentation",
        u"Публічний паспорт активу": u"technicalSpecifications",
        u"Місце та форма прийому заяв на участь в аукціоні та банківські "
        u"реквізити для зарахування гарантійних внесків": u"x_dgfPlatformLegalDetails",
        u"Sample Virtual Data Room": u"virtualDataRoom",
        u"Public Asset Certificate": u"x_dgfAssetFamiliarization",
        u"—": u"None",
    }.get(string, string)


def adapt_procuringEntity(tender_data):
    tender_data['data']['procuringEntity']['name'] = u'ТОВ "ЭТУ КОМПАНИЮ НЕ ТРОГАТЬ"'
    tender_data['data']['procuringEntity']['address']['countryName'] = u"Украина"
    return tender_data


def adapt_qualified(tender_data, username):
    if username == 'Prom_Provider':
        if 'qualified' in tender_data['data']:
            return True
    return False


def download_file(url, file_name, output_dir):
    urllib.urlretrieve(url, ('{}/{}'.format(output_dir, file_name)))


