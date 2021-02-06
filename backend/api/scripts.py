import bs4
import lxml
from bs4 import BeautifulSoup as bs
from django.utils import dateparse
import datetime

def get_nfe_info(file_name):
    with open(str(file_name), 'r') as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "lxml")
    file.close

    nfe_id = bs_content.find('infnfe')['id']

    emit = bs_content.find('emit')
    emit_cnpj = emit.find('cnpj').text
    emit_nome = emit.find('xnome').text

    dest = bs_content.find('dest')
    dest_cnpj = dest.find('cnpj').text
    dest_nome = dest.find('xnome').text

    ide = bs_content.find('ide')
    exit_date = ide.find('dhsaient').text

    valor_original_total = bs_content.find(
        'cobr').find('fat').find('vorig').text

    venc_dates = [i.find('dvenc').text.split('-') for i in bs_content.find('cobr').find_all('dup')]
    venc_dates = [datetime.datetime(int(i[0]), int(i[1]), int(i[2])).isoformat() for i in venc_dates]

    return {'nfe_id': nfe_id,
            'emit_cnpj': emit_cnpj,
            'emit_name': emit_nome,
            'dest_cnpj': dest_cnpj,
            'dest_name': dest_nome,
            'valor_original_total': valor_original_total,
            'exit_date': dateparse.parse_datetime(exit_date),
            'venc_dates': venc_dates
            }
