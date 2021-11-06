import datetime
import csv
import pandas as pd
from Utils import file_utils as util

listaHTMLs = []
nomes_HTMLs = []
listaUF = (["31", "ACRE", "AC"],
           ["20", "ALAGOAS", "AL"],
           ["30", "AMAZONAS", "AM"],
           ["28", "AMAPÁ", "AP"],
           ["18", "BAHIA", "BA"],
           ["24", "CEARÁ", "CE"],
           ["16", "DISTRITO FEDERAL", "DF"],
           ["9", "ESPÍRITO SANTO", "ES"],
           ["15", "GOIÁS", "GO"],
           ["26", "MARANHÃO", "MA"],
           ["6", "MINAS GERAIS", "MG"],
           ["13", "MATO GROSSO DO SUL", "MS"],
           ["14", "MATO GROSSO", "MT"],
           ["27", "PARÁ", "PA"],
           ["22", "PARAÍBA", "PB"],
           ["21", "PERNAMBUCO", "PE"],
           ["25", "PIAUÍ", "PI"],
           ["12", "PARANÁ", "PR"],
           ["8", "RIO DE JANEIRO", "RJ"],
           ["23", "RIO GRANDE DO NORTE", "RN"],
           ["32", "RONDÔNIA", "RO"],
           ["29", "RORAÍMA", "RR"],
           ["10", "RIO GRANDE DO SUL", "RS"],
           ["11", "SANTA CATARINA", "SC"],
           ["19", "SERGIPE", "SE"],
           ["7", "SÃO PAULO", "SP"],
           ["17", "TOCANTINS", "TO"])


def __set_HTML__(self, html):
    h = type(html).__new__(type(html))
    h = html.copy()
    listaHTMLs += [ h ]


def __set_HTMLs__(self, htmls, forcInsert = False):
    if forcInsert:
        listaHTMLs = htmls
        return True
    else:
        if len(listaHTMLs) > 0:
            return False, "Há elementos na lista => " + str(listaHTMLs)


def __set_nome_HTML__(self, nome):
    listaHTMLs += [ nome ]


def __set_nomes_HTMLs__(self, nomes, forcInsert = False):
    if forcInsert:
        nomes_HTMLs = nomes
        return True
    else:
        if len(nomes_HTMLs) > 0:
            return False, "Há elementos na lista => " + str(nomes_HTMLs)


def __get__html(self, index=-1):
    if index == -1:
        return listaHTMLs
    elif index > len(listaHTMLs):
        return []
    else:
        return listaHTMLs[index]


def set_uf(nome):
    for item in listaUF:
        if nome.split('-')[0] == item[1]:
            return item[2]


def lista_to_str(lista):
    string = ""
    for item in lista:
        string += str(item) + ';'
    return string[:-1]


def formatar_nome_cidade(html):
    lista_cidades = []
    lista_filtrada = []
    for hAS in html:
        lista_cidades += [ str(hAS["UNIDADE"].value_counts()).split("-")[-1].replace(
            "    1\nName: UNIDADE, dtype: int64", "") ]
        i = str(lista_cidades.pop())
        if i != 'Series([], Name: UNIDADE, dtype: int64)':
            lista_filtrada += [ i.replace(' ', '', 1) ]
    return lista_filtrada


def formatar_row(string, char_sep = '  '):
    lista = []
    if(type(string) != list):
        lista = string.split(char_sep)
    listaR = []
    for item in lista:
        if item != '' and item != "NaN":
            if item in ['0.0', '0.00', '0.000', '0.0000'] or \
               item in ['0,0', '0,00', '0,000', '0,0000']:
                listaR += ['0']
            else:
                listaR += [ str(item).replace(" ", '') ]
    if listaR[0] == "NaN":
        listaR.__delitem__(0)
    return listaR


def cria_CSV_mult_tabelas(html_tables,nomes_planilhas):
    # cria o novo aruuivo para inserção dos dados formatados
    data_bu = datetime.datetime.now().strftime('%m_%Y')
    #arquivo = open(f"D:\\Drives compartilhados\\Base de dados GW ENERGIA\\"
    #               f"Script_DL_Ceasas\\{data_bu}-Ceasas.csv", "w", newline="", encoding="ISO-8859-1", errors='strict')
    arquivo = open(f"{data_bu}-Ceasas.csv", "w", newline="", encoding="ISO-8859-1", errors='strict')
    tabela = csv.writer(arquivo, dialect="excel-tab")

    # cria o cabeçalho da tabela
    tabela.writerow(["UNIDADE;CIDADE;UF;Mês/Ano;Qtde Cereais (kg);Valor Cereais (R$);"
                     "Qtde Hortigranjeiros (kg);Valor Hortigranjeiros (R$);Qtde Produtos Diversos (kg);"
                     "Valor Produtos Diversos (R$);Soma (kg);Soma (R$)"])

    nomes_cidades = []
    residuos = []
    rows = []
    unidade = ""
    cidade = ""
    uf = ""
    index = 0
    for tables in html_tables:
        nomes_cidades = [formatar_nome_cidade(tables), 0]
        uf = set_uf(nomes_planilhas[index])
        index += 1
        for table in tables:
            for row in str(table.value_counts(dropna=False)).splitlines():
                ftm_row = formatar_row(row[:-5])
                if ftm_row[0] != "UNIDADE":
                    if ftm_row.__contains__("NaN") or ftm_row[0] == "dtype:" or \
                            ftm_row.__contains__("TOTAL") or ftm_row.__contains__("Sub-Total"):
                        residuos += [ftm_row]
                    elif len(ftm_row) >= 12:
                        unidade = ftm_row[0]
                        cidade = ftm_row[0].split('-')[1]
                        if len(ftm_row[0].split('-')) > 2:
                            cidade = ftm_row[0].split('-')[2]
                        nomes_cidades[1] += 1
                        ftm_row[0], ftm_row[1], ftm_row[2] = unidade, cidade, uf
                        tabela.writerow([lista_to_str(ftm_row[0:12])])
                    else:
                        ftm_row = [unidade, cidade, uf] + ftm_row
                        tabela.writerow([lista_to_str(ftm_row[0:12])])
    arquivo.close()
    return [ "RESIDUOS => " ] + residuos


def cria_CSV(html_table,nomes_planilhas):
    # cria o novo aruuivo para inserção dos dados formatados
    data_bu = datetime.datetime.now().strftime('%m_%Y')
    #arquivo = open(f"D:\\Drives compartilhados\\Base de dados GW ENERGIA\\"
    #               f"Script_DL_Ceasas\\{data_bu}-Ceasas.csv", "w", newline="", encoding="ISO-8859-1", errors='strict')
    arquivo = open(f"{data_bu}-Ceasas.csv", "w", newline="", encoding="ISO-8859-1", errors='strict')
    tabela = csv.writer(arquivo, dialect="excel-tab")

    # cria o cabeçalho da tabela
    tabela.writerow(["UNIDADE;CIDADE;UF;Mês/Ano;Qtde Cereais (kg);Valor Cereais (R$);"
                     "Qtde Hortigranjeiros (kg);Valor Hortigranjeiros (R$);Qtde Produtos Diversos (kg);"
                     "Valor Produtos Diversos (R$);Soma (kg);Soma (R$)"])

    nomes_cidades = []
    residuos = []
    rows = []
    unidade = ""
    cidade = ""
    uf = ""
    nomes_cidades = [formatar_nome_cidade(html_table), 0]
    uf = set_uf(nomes_planilhas)
    for table in html_table:
        for row in str(table.value_counts(dropna=False)).splitlines():
            ftm_row = formatar_row(row[:-5])
            if ftm_row[0] != "UNIDADE":
                if ftm_row.__contains__("NaN") or ftm_row[0] == "dtype:" or \
                   ftm_row.__contains__("TOTAL") or ftm_row.__contains__("Sub-Total"):
                    residuos += [ftm_row]
                elif len(ftm_row) >= 12:
                    unidade = ftm_row[0]
                    cidade = ftm_row[0].split('-')[1]
                    if len(ftm_row[0].split('-')) > 2:
                        cidade = ftm_row[0].split('-')[2]
                    nomes_cidades[1] += 1
                    ftm_row[0], ftm_row[1], ftm_row[2] = unidade, cidade, uf
                    tabela.writerow([lista_to_str(ftm_row[0:12])])
                else:
                    ftm_row = [unidade, cidade, uf] + ftm_row
                    tabela.writerow([lista_to_str(ftm_row[0:12])])
    arquivo.close()
    return [ "RESIDUOS => " ] + residuos


def execurta_format():
    if len(listaHTMLs) == 0:
        return "ERRO", "Não há lista para formatar"
    elif len(listaHTMLs) == 1 and len(nomes_HTMLs) == 1:
        return "SUCESSO", cria_CSV(listaHTMLs[0], nomes_HTMLs[0])
    elif (len(listaHTMLs) == len(nomes_HTMLs)) and len(listaHTMLs) > 1 and len(nomes_HTMLs) > 1:
        return "SUCESSO", cria_CSV(listaHTMLs, nomes_HTMLs)
    else:
        return "ERRO", f"Número de HTMLs({len(listaHTMLs)}) | Número de nome HTML({nomes_HTMLs})"

AC_nome = "ACRE-18_10_2021.xls"
htmlAC = pd.read_html(AC_nome, match='UNIDADE')
SP_nome = 'SÃO PAULO-18_10_2021.xls'
htmlSP = pd.read_html(SP_nome, match='UNIDADE')
#print((cria_CSV(htmlSP, SP_nome))
print(cria_CSV_mult_tabelas([htmlAC, htmlSP], [AC_nome, SP_nome]))

#h = type(htmlSP).__new__(type(htmlSP))
#h = htmlSP.copy()
#print(type(h))
#'''
