from datetime import datetime
from pathlib import Path
import smtplib
import email.message


class file_utils(object):

    @staticmethod
    def renomear_file(caminho, novo_nome):
        path = Path(caminho)
        ext = path.suffix
        path.rename(Path(path.parent, novo_nome + ext))

    @staticmethod
    def write_to_log(caminho = "C:\Git_PIUE_Gwenergia\Log.txt", p_msg = ""):
        log = open(caminho, "a")
        log.write(p_msg + '\n\n')
        log.close()

    @staticmethod
    def enviar_email(p_msg, p_assunto, email_from = "minhacontatestegw@gmail.com",
                     password = 'SenhaSecreta@23', email_to = "minhacontatestegw@gmail.com"):
        msg = email.message.Message()
        msg['Subject'] = p_assunto
        # necessita retirar a trava de envio por código no email utilizado para enviar
        # Gerenciar minha conta google->Segurança->Acesso a app menos seguro->Ativar
        msg['From'] = "minhacontatestegw@gmail.com"
        msg['To'] = "minhacontatestegw@gmail.com"
        password = 'SenhaSecreta@23'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(p_msg)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        log_msg = str
        try:
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            log_msg = f"[*] Email enviado com sucesso!" + \
                      f"\n> Data de envio: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        except Exception as erro:
            log_msg = f"[*] Ocorrido: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}" + \
                      f"\n> Tipo de erro: {type(erro)}" + \
                      f"\n> Arguemntos:   {erro.args}"
        finally:
            file_utils.write_to_log(p_msg=log_msg)
            s.close()
