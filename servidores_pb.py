# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from time import sleep
import csv
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

servidores = []
url_base = "http://sagres.tce.pb.gov.br/"


cidades_pb = {}
with open('cidades_pb.csv', 'r') as cidades_csv:
    for linha in csv.reader(cidades_csv):
        cidades_pb[linha[0]] = linha[1]

with open('ugestoras_pb.csv', 'r') as ugestoras_csv:
    for entidade in csv.reader(ugestoras_csv):
        entidade_cod = entidade[0]
        entidade_desc = entidade[1]

        # O sagres fecha a conexao apos alguns requests. Nesse caso,
        # esperamos algum tempo, e reiniciamos daquela unidade gestora
        tentativas = 0
        sucesso = False
        while not sucesso and tentativas < 5:
            tentativas += 1
            try:
                session = requests.Session()
                session.headers.update({'User-Agent': '#horaextrajp crawler'})

                #Ano 'hardcodado' p/ 2013
                for ano in ['2013']:
                    session.get(url_base)
                    # Equivale a selecionar municipio, ano e entidade
                    # no combobox
                    session.post(
                        '%s/%s' % (url_base, 'index.php?acao=add'),
                        data={
                            "ano": ano, "entidade": entidade_cod,
                            #o cod da cidade é os ultimos 3 digitos do cod da entidade
                            "ugestora": entidade_cod[3:],
                            "bt_consultar": "Consultar"
                        }
                    )
                    #Mes 'hardcodado' p/ maio (ultimo publicado ate entao)
                    for mes in [5]:
                        url = "%s/pessoal02.php?cd_ugestora=%s&dt_mes=%.2d&dt_ano=%s" % (
                            (url_base, entidade_cod, mes, ano)
                        )
                        result = session.get(url)
                        pessoal2_dom = BeautifulSoup(result.content)

                        # Encontra os links de detalhamento do cargos
                        for tipo in (
                            pessoal2_dom.select(".trConteudoCor1") +
                            pessoal2_dom.select(".trConteudoCor2")
                        ):
                            #Pega o label do tipo de cargo e o link de detalhamento
                            tipo_label = tipo.select(
                                'td:nth-of-type(2) font'
                            )[0].string.strip()
                            tipo_link = tipo.select('a')[0].attrs['href']

                            #Clica no link do detalhamento do cargo
                            result = session.get('%s/%s' % (url_base, tipo_link))
                            pessoal3_dom = BeautifulSoup(result.content)

                            #Itera sobre o cargos
                            for cargo in (
                                pessoal3_dom.select(".trConteudoCor1") +
                                pessoal3_dom.select(".trConteudoCor2")
                            ):
                                #Pega o label do cargo e seu link de detalhamento
                                cargo_label = cargo.select(
                                    'td:nth-of-type(3) font'
                                )[0].string.strip().title()
                                cargo_link = cargo.select('a')[0].attrs['href']

                                #Clica no detalhamento do cargo
                                result = session.get('%s/%s' % (url_base, cargo_link))
                                pessoal4_dom = BeautifulSoup(result.content)

                                #Extrai o nome das pessoas
                                for pessoa in (
                                    pessoal4_dom.select(".trConteudoCor1") +
                                    pessoal4_dom.select(".trConteudoCor2")
                                ):

                                    #Grava o nome, cargo, tipo do cargo, unidade
                                    #gestora, municipio
                                    nome = pessoa.select(
                                        'td:nth-of-type(2) font'
                                    )[0].string.strip().title()

                                    print u'%s,%s,%s,"%s",%s' % (
                                        cidades_pb[entidade_cod[3:]],
                                        entidade_desc,
                                        tipo_label,
                                        cargo_label,
                                        nome,
                                    )
            # Quando o sagres fechar a conexao, aguarda 2min e depois
            # volta para o inicio da mesma unidade gestora
            except Exception:
                sleep(120)
                continue
            sucesso=True
        if not sucesso:
            exit()
