import requests
from bs4 import BeautifulSoup
import requests
import json

cookies = {
    '_ga': 'GA1.1.376623384.1739685686',
    'lbck': '53a0c769f685378747de76da90c9bf2f',
    'citrix_ns_id': 'AAI7LH-xZzsean0CAAAAADubbGeFOQORckOwOxdMjfkyoD1i7GHp39YLvyWsiNZ3Ow==4YaxZw==4nZx3q4rALF3TVj3CCZjlpCUrXo=',
    'citrix_ns_id_.india.gov.in_%2F_wat': 'AAAAAAVgO8p5_G0pjjMMd3x4g7VOPo5s7Oc7_7BtRay6fJCLGwZKzmGwHceY2Z9HUu1o4xlolUbSDEJBJRkmGAaxSYHn&AAAAAAVO2bcKXQPZsgPVZSXiFzZAOROQhxJoyy7To-HvVAjlWmn9XMN5S_arrw-G3YADJLUDQ9w8HEX1Fsyyaf2e9UPp&',
    '_ga_0BZ8R3LVHG': 'GS1.1.1739685685.1.1.1739686750.0.0.0',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_ga=GA1.1.376623384.1739685686; lbck=53a0c769f685378747de76da90c9bf2f; citrix_ns_id=AAI7LH-xZzsean0CAAAAADubbGeFOQORckOwOxdMjfkyoD1i7GHp39YLvyWsiNZ3Ow==4YaxZw==4nZx3q4rALF3TVj3CCZjlpCUrXo=; citrix_ns_id_.india.gov.in_%2F_wat=AAAAAAVgO8p5_G0pjjMMd3x4g7VOPo5s7Oc7_7BtRay6fJCLGwZKzmGwHceY2Z9HUu1o4xlolUbSDEJBJRkmGAaxSYHn&AAAAAAVO2bcKXQPZsgPVZSXiFzZAOROQhxJoyy7To-HvVAjlWmn9XMN5S_arrw-G3YADJLUDQ9w8HEX1Fsyyaf2e9UPp&; _ga_0BZ8R3LVHG=GS1.1.1739685685.1.1.1739686750.0.0.0',
    'origin': 'https://www.india.gov.in',
    'priority': 'u=1, i',
    'referer': 'https://www.india.gov.in/my-government/schemes-0',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'page': '0',
    'view_name': 'metadata_for_schemes',
    'view_display_id': 'block',
    'view_args': '166854',
    'view_path': 'taxonomy/term/166854',
    'view_base_path': 'my-government/schemes',
    'view_dom_id': '8c69c28486e1c6a7a7e1ee69036f5588',
    'pager_element': '0',
    'ajax_html_ids[]': [
        'nvpn_position_meta',
        'header',
        'block-block-4',
        'text_resize_decrease',
        'text_resize_reset',
        'text_resize_increase',
        'switch-lang',
        'logo',
        'menu-bar',
        'block-panels-mini-main-menu',
        'mini-panel-main_menu',
        'nav',
        'block-block-16',
        'searchForm',
        'search_key',
        'edit-submit1',
        'auto_suggesion',
        'advsearchbtn',
        'light',
        'views-exposed-form-advance-metadata-search-page-1',
        'edit-title-wrapper',
        'edit-title',
        'edit-term-node-tid-depth-wrapper',
        'edit-term-node-tid-depth',
        'edit-sort-by',
        'edit-sort-order',
        'edit-submit-advance-metadata-search',
        'block-views-most-search-block',
        'main',
        'content-column',
        'main-content',
        'content',
        'block-system-main',
        'leftside-bar',
        'views-exposed-form-metadata-for-schemes-block',
        'edit-title-wrapper',
        'edit-title',
        'edit-submit-metadata-for-schemes',
        'block-suggest-metadata-suggest-metadata',
        'info-suggestion-wrapper',
        'information-suggestion-wrapper',
        'suggest_us',
        'metadata-suggestion-form-ajax',
        'edit-metadata-suggestion',
        'metadata_suggestion_form',
        'footer',
        'footertop',
        'menutext',
        'block-block-6',
        'fotter-bottom',
        'block-block-7',
        'block-block-9',
    ],
    'ajax_page_state[theme]': 'npi_adaptive',
    'ajax_page_state[theme_token]': 'iIGcsIGL5rtHpCzcAlJ6O7T64xEkZKu2uj8j2E5Kekg',
    'ajax_page_state[css][modules/system/system.base.css]': '1',
    'ajax_page_state[css][modules/system/system.menus.css]': '1',
    'ajax_page_state[css][modules/system/system.messages.css]': '1',
    'ajax_page_state[css][sites/all/modules/contributed/calendar/css/calendar_multiday.css]': '1',
    'ajax_page_state[css][sites/all/modules/contributed/date/date_api/date.css]': '1',
    'ajax_page_state[css][sites/all/modules/contributed/date/date_popup/themes/datepicker.1.7.css]': '1',
    'ajax_page_state[css][sites/all/modules/contributed/date/date_repeat_field/date_repeat_field.css]': '1',
    'ajax_page_state[css][modules/field/theme/field.css]': '1',
    'ajax_page_state[css][sites/all/modules/contributed/logintoboggan/logintoboggan.css]': '1',
    'ajax_page_state[css][modules/node/node.css]': '1',
    'ajax_page_state[css][modules/search/search.css]': '1',
    'ajax_page_state[css][modules/user/user.css]': '1',
    'ajax_page_state[css][sites/all/modules/contributed/views/css/views.css]': '1',
    'ajax_page_state[css][sites/all/modules/contributed/ctools/css/ctools.css]': '1',
    'ajax_page_state[css][sites/all/modules/contributed/panels/css/panels.css]': '1',
    'ajax_page_state[css][sites/all/themes/adaptivetheme/at_core/css/at.layout.css]': '1',
    'ajax_page_state[css][sites/all/themes/adaptivetheme/npi_adaptive/css/font-awesome.min.css]': '1',
    'ajax_page_state[css][sites/all/themes/adaptivetheme/npi_adaptive/css/global.custom.responsive.css]': '1',
    'ajax_page_state[css][sites/all/themes/adaptivetheme/npi_adaptive/css/global.base.css]': '1',
    'ajax_page_state[css][sites/all/themes/adaptivetheme/npi_adaptive/css/global.styles.css]': '1',
    'ajax_page_state[css][sites/all/themes/adaptivetheme/npi_adaptive/css/print.css]': '1',
    'ajax_page_state[css][public://adaptivetheme/npi_adaptive_files/npi_adaptive.default.layout.css]': '1',
    'ajax_page_state[js][sites/all/modules/contributed/jquery_update/replace/jquery/3.1/jquery.min.js]': '1',
    'ajax_page_state[js][misc/jquery-extend-3.4.0.js]': '1',
    'ajax_page_state[js][misc/jquery-html-prefilter-3.5.0-backport.js]': '1',
    'ajax_page_state[js][misc/jquery.once.js]': '1',
    'ajax_page_state[js][misc/drupal.js]': '1',
    'ajax_page_state[js][sites/all/modules/contributed/jquery_update/replace/ui/external/jquery.cookie.js]': '1',
    'ajax_page_state[js][sites/all/modules/contributed/jquery_update/replace/jquery.form/4/jquery.form.min.js]': '1',
    'ajax_page_state[js][misc/form-single-submit.js]': '1',
    'ajax_page_state[js][misc/ajax.js]': '1',
    'ajax_page_state[js][sites/all/modules/contributed/jquery_update/js/jquery_update.js]': '1',
    'ajax_page_state[js][sites/all/modules/contributed/admin_menu/admin_devel/admin_devel.js]': '1',
    'ajax_page_state[js][sites/all/modules/customs/hb_documents/hb_documents.js]': '1',
    'ajax_page_state[js][sites/all/modules/customs/hb_schemes/hb_schemes.js]': '1',
    'ajax_page_state[js][sites/all/modules/customs/webform_email_reply/script.js]': '1',
    'ajax_page_state[js][sites/all/modules/contributed/views/js/base.js]': '1',
    'ajax_page_state[js][misc/progress.js]': '1',
    'ajax_page_state[js][sites/all/modules/contributed/views/js/ajax_view.js]': '1',
    'ajax_page_state[js][sites/all/themes/adaptivetheme/npi_adaptive/scripts/jquery.min.js]': '1',
    'ajax_page_state[js][sites/all/themes/adaptivetheme/npi_adaptive/scripts/custom.js]': '1',
    'ajax_page_state[jquery_version]': '3.1',
}

href_list = []
for i in range(213):
    data['page'] = str(i)

    response = requests.post('https://www.india.gov.in/views/ajax', cookies=cookies, headers=headers, data=data)


    res = response.json()
    # print(res[2]['data'])


    soup = BeautifulSoup(res[2]['data'], 'html.parser')


    # Find all 'a' tags and extract their href attributes
    links = soup.find_all('a')

    for link in links:
        href = link.get('href')
        if href and "my-government" not in href:  # Only add if href exists and doesn't contain "my-government"
            href_list.append(href)
    json.dump(href_list, open("links.json", "w"))

    print("No of links: ", len(href_list))


print("Base Case: https://www.india.gov.in/")