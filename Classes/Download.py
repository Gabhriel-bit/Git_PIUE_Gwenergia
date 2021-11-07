from selenium.webdriver.support.select import Select
from Utils import file_utils as util
from selenium import webdriver
import datetime
import time

'''
|------------------Configurações--------------------|
|Linha | Processo a ser feito                       |
|---------------------------------------------------|
| 31  | Configurar o email de destino dos avisos    |
| 67  | Configurar o local de destido dos arquivos  |
| 70  | Configurar o caminho do chromedriver        |
|---------------------------------------------------|
'''
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


def download(time_pop_up):
    options = webdriver.ChromeOptions()
    caminho = 'C:\Git_PIUE_Gwenergia\Relatórios'
    prefs = { "download.default_directory": caminho}
    #options.add_argument("--headless") #As janelas ficam invisiveis
    options.add_experimental_option("prefs", prefs)
    options.add_argument("user-data-dir=C:\\Path")
    driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chrome.exe', options=options)
    data_bu = datetime.datetime.now().strftime('%d_%m_%Y')
    main_window = driver.window_handles
    driver.close()
    msg = ""

    for uf in listaUF:
        baixar_UFs = True
        try:
            driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chrome.exe', options=options)
            main_window = driver.window_handles

            driver.get('http://www3.ceasa.gov.br/siscomweb/?page=reports.consulta_relatorio_uf_unidade')
            select = Select(driver.find_element(id='ctl0_corpoConsulta_cmbbxUF'))
            select.select_by_visible_text(uf[1])
            select.select_by_value(uf[0])

            driver.find_element('ctl0_corpoConsulta_ctl0').click()
            main_window = driver.window_handles[0]
            time.sleep(time_pop_up)
            driver.switch_to.window(driver.window_handles[1])
            driver.find_element('ctl0_corpo_btnImprimeXLS').click()
            time.sleep(5)

            nome_atual = "Relatorio de Preços" + data_bu
            util.renomear_file(caminho + "\\" + nome_atual + ".xls", uf[1] + "-" + data_bu)


        except Exception as erro:
            msg = f"[*] Ocorrido: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}" + \
                  f"\n> Tipo de erro: {type(erro)}" + \
                  f"\n> Arguemntos:   {erro.args}"
            baixar_UFs = False
            util.enviar_email(f'''
            <p><font color="red">As planilhas do site da SISCOM - Conab <b>não</b> foram atualizadas com sucessso.</font>></p>
            <p>Data de referência da atualização{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
            <p>Tipo de erro: {type(erro)}</p>
            <p>Arguemntos: {erro.args}</p>
            <p>Chrome error: {format(driver.error_handler)}</p>
            ''', "Atualização de dados automático SISCOM - Ceasas")
        finally:
            try:
                driver.switch_to.alert.accept()
            except Exception as error:
                msg += ""
            if driver.window_handles.__len__() > 1:
                driver.close()
            driver.switch_to.window(main_window)
            driver.close()
            time.sleep(2)
    if baixar_UFs:
        util.enviar_email(p_msg=f'''
        <p>As planilhas do site da SISCOM - Conab foram atualizadas com sucessso.</p>
        <p>Data de referência da atualização{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
        <p>Foram salva em {prefs}, e já estão diponíveis para consulta.</p>
        ''', p_assunto="Atualização de dados automático SISCOM - Ceasas")
    return msg


def executar():
    sleep_pop_up = 5
    redownload = 0
    try_times = 0
    try:
        while True:
            time.sleep(redownload)
            # um mês :
            redownload = 2#592000
            msg = download(sleep_pop_up)
            if (msg != "") and (try_times < 3):
                util.write_to_log(p_msg=msg)
                sleep_pop_up += 1
                redownload = 0
                try_times += 1
            elif try_times == 3:
                dataest = datetime.datetime.now()
                dataest.day = dataest.day.__add__(1)
                enviar_email("<p>Houve uma falha ao acessar o site</p>\n"
                             "<p>A data de atualização foi adiada em 1 dia</p>\n"
                             "<p>Data para a próxima tentativa "
                             f"{dataest.strftime('%d/%m/%Y %H:%M')}</p>",
                             p_assunto="Atualização automática SISCOM-Ceasas ADIADA")
                redownload = 86400
            else:
                try_times = 0
    except Exception as erro:
        util.write_to_log(f"[*] Ocorrido: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}" +
                     f"\n> Tipo de erro: {type(erro)}\n> Arguemntos:   {erro.args}")


while True:
    executar()
