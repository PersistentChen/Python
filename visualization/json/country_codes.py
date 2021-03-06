from pygal_maps_world.i18n import COUNTRIES

def get_country_code(country_name):
    '''
    根据指定国家返回pygal使用的两个字母的国别码
    '''
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    # 若没找到指定的国家返回None
    return None

# print(get_country_code('Bosnia and Herzegovina'))
# print(get_country_code('Congo, the Democratic Republic of the'))
# print(get_country_code('Venezuela, Bolivarian Republic of'))
