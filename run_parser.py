import re
import urllib.parse
import urllib.request

import lxml.html
import timeout_decorator

export_text = 'customers.txt'


def main():
    for i in range(17, 798):
        url = f"https://agregatoreat.ru/clients/customers/addresses=москва&status=1/page/{i}"
        try:
            print(i)
            get_page(url)
        except Exception as e:
            print(e)


def get_page(url):
    url = urllib.parse.urlsplit(url)
    url = list(url)
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    page = download_page(url)
    extract_num_customer(page)


@timeout_decorator.timeout(35)
def download_page(url):
    req = urllib.request.Request(url=url)
    handler = urllib.request.urlopen(req, timeout=30)
    page = handler.read().decode('utf-8')
    return page


def extract_num_customer(page):
    res = re.findall('\"_type":"organization","_id":\"(\\d+)\"', page)
    for r in res:
        try:
            page_customer_download(r)
        except Exception as e:
            print(e)


def page_customer_download(num):
    url = f"https://agregatoreat.ru/organization/{num}"
    page = download_page(url)
    extract_from_customer(page)


def extract_from_customer(page):
    doc = lxml.html.document_fromstring(page)
    name = doc.xpath('.//div[. = "Полное наименование"]/following-sibling::div')[0].text_content()
    email = doc.xpath('.//div[. = "Адрес электронной почты"]/following-sibling::div/span')[0].text_content().strip(
            ' \t\n')
    phone = ''
    try:
        phone = doc.xpath('.//div[. = "Телефон"]/following-sibling::div/span')[0].text_content().strip(
                ' \t\n')
    except Exception as e:
        print(e)
    with open(export_text, 'a') as f:
        f.write(f"{name}\t{email}\t{phone}\n")


if __name__ == "__main__":
    main()
