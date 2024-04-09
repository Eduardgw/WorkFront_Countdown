# -*- coding: utf-8 -*-
# Antes de tudo, sim, esse programa está bagunçado e mal otimizado. Porém não estou planejado melhora-lo significamente.
# Se você, pessoa aleatória ou eu do futuro quiser quiser tentar otimizar, boa sorte. Nem eu mesmo lembro como que isto funciona.
import os
import shutil
import time
import pandas as pd
from datetime import datetime, timedelta
from holidays.countries import brazil
from itertools import cycle
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import sys
from win11toast import toast
import json
from jinja2 import Template
import webbrowser
import threading
import http.server
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import socket
import subprocess
from PyPDF2 import PdfReader
from tabula import read_pdf

# Defina a variável de ambiente PYTHONIOENCODING para utf-8
os.environ['PYTHONIOENCODING'] = 'utf-8'


# Verifica se '--automatic' e/ou '--pdf' está presente nos argumentos da linha de comando.
automatic = False
pdf = False
if '--automatic' in sys.argv:
    automatic = True
if '--pdf' in sys.argv:
    pdf = True


# Encontra os diretórios
appdata_path = os.path.join(os.getenv('LOCALAPPDATA'), "WorkFront Countdown")
save_path = os.path.join(appdata_path, "save") 


# Apenas definindo uma função para desativar o callback idesejado da notificação
def empty_func(args):
    pass

# Verifica se a pasta save já existe
if not os.path.exists(save_path):
    # Cria a pasta se ela não existir
    os.makedirs(save_path)

# Verifica se error_count.txt já existe
if not os.path.exists(os.path.join(save_path, "error_count.txt")):
    # Cria o arquivo .txt se não existir
    with open(os.path.join(save_path, "error_count.txt"), 'w') as file:
        file.write('0')
# Apenas definindo o global_args
global_args = None
def on_click(args):
    global global_args
    global_args = args

# Apenas definindo WrongFileError
class WrongFileError(Exception):
    def __init__(self, message="Wrong file"):
        self.message = message
        super().__init__(self.message)

# Exibe uma mensagem caso 3 erros consecutivos apareçam
with open(os.path.join(save_path, 'error_count.txt'), 'r') as error_count_file:
    # Lê o arquivo e converte para números.
        error_count = error_count_file.read()
        error_count = int(error_count)
print
if error_count >= 3:

    def mostrar_caixa_confirmacao():
        response = messagebox.askyesno("Erros consecutivos detectados", "Diversos erros concecutivos ocorreram em WorkFront Countdown. Caso não tenha conseguido resolver o problema, poderá deletar todos os dados salvos do programa restaurando-o para o padrão. \n\nDeseja deletar os arquivos?",
                                    icon='info', default=messagebox.NO, type='yesno')  # Definir 'Não' como padrão
        
        
        if response:
            def mostrar_caixa_confirmacao():
                response = messagebox.askyesno("Confirmação", "Você tem certeza que deseja excluir todos os dados salvos de WorkFront Countdown? Essa ação não poderá ser desfeita, utilize em último caso.",
                                        icon='warning', default=messagebox.NO)  # Definir 'Não' como padrão
            
            if response:
                def mostrar_caixa_confirmacao():
                    response = messagebox.askyesno("Confirmação", "Você tem certeza que deseja excluir todos os dados salvos de WorkFront Countdown? Essa ação não poderá ser desfeita. \n\n Utilize apenas em último caso.",
                                                icon='warning', default=messagebox.NO)  # Definir 'Não' como padrão
                    
                    if response:
                        try:
                            shutil.rmtree(appdata_path)
                            sys.exit()
                        except Exception as e:
                            sys.exit(1)
                    else:
                        sys.exit()

                # Criar uma window vazia apenas para usar o tkinter
                window = tk.Tk()
                window.withdraw()  # Oculta a window principal
                window.wm_attributes("-topmost", 1)  # Define a window como "sempre no topo"

                # Definir o ícone da janela
                window.iconbitmap('./icon.ico')

                # Chamar a função para mostrar a caixa de confirmação
                mostrar_caixa_confirmacao()

                # Fechar a window (opcional)
                window.destroy()
            else:
                sys.exit()
        else:
            # Já que deletar os arquivos não é uma opção, reseta a sequência de erros
            def error_count_reset():
                error_count = 0
                with open(os.path.join(save_path, 'error_count.txt'), 'w') as error_count_file:
                    error_count_file.write(str(error_count))
            error_count_reset() 
            sys.exit()

    # Criar uma window vazia apenas para usar o tkinter
    window = tk.Tk()
    window.withdraw()  # Oculta a window principal
    window.wm_attributes("-topmost", 1)  # Define a window como "sempre no topo"

    # Definir o ícone da janela
    window.iconbitmap('./icon.ico')

    # Chamar a função para mostrar a caixa de confirmação
    mostrar_caixa_confirmacao()

    # Fechar a window (opcional)
    window.destroy()


try:
    with open(os.path.join(save_path, 'original_pdf_dir.pkl'), 'rb') as archive:
        selected_archive = pickle.load(archive)
        
        if os.path.exists(selected_archive):
            pass
        else:
            raise FileNotFoundError
        if pdf:
            raise FileNotFoundError
        
except:
    # Define a abertura da janela de seleção do arquivo PDF
    def abrir_janela_selecao_arquivo():
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal
        root.iconbitmap('./icon.ico')
        root.wm_attributes("-topmost", 1)  # Define a window como "sempre no topo
        selected_archive = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=(("Frente de Trabalho", "*.pdf"), ("Todos os arquivos", "*.*"))
        )
        
        if selected_archive:
            # Salva o diretório na memória
            with open(os.path.join(save_path, 'original_pdf_dir.pkl'), 'wb') as archive:
                pickle.dump(selected_archive, archive)
            pass
        else:
            sys.exit()
        return selected_archive
    global_args = None

    if not pdf:
        toast(app_id="WorkFront Countdown" ,
                        title='Arquivo PDF não encontrado',
                        body='Especifique o caminho da tabela para que as informações fornecidas sejam confiáveis.',
                        audio='ms-winsoundevent:Notification.IM',
                        duration = 'long',
                        on_dismissed=empty_func)

    selected_archive = abrir_janela_selecao_arquivo()

# Caminho completo do novo arquivo na pasta de destino
pdf_file = os.path.join(save_path, "Lista da Frente de Trabalho.pdf")

# Copia o arquivo selecionado para a pasta de destino com o novo nome
shutil.copy(selected_archive, pdf_file)

try:
    # Abre o PDF
    with open(pdf_file, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        
        # Extrai o texto da primeira página
        first_page_text = pdf_reader.pages[0].extract_text()

        # Verifica se as palavras-chave estão presentes
        keywords = ['ESTADO DO PARANÁ', 'MUNICÍPIO DE TUPÃSSI', 'Secretaria de Assistência Social', 'Integrantes']
        if all(keyword in first_page_text for keyword in keywords):
            # Se todas as palavras-chave estiverem presentes, prossiga com a extração das tabelas
            tables = read_pdf(pdf_file, pages='all', encoding='latin-1')

            # Resto do seu código para extrair datas e nomes das tabelas
            dates = []
            names = []
            for table in tables:
                if table.shape[1] >= 6:
                    dates_page = table.iloc[:, 5]
                    names_page = table.iloc[:, 1]
                    dates.extend(dates_page)
                    names.extend(names_page)
        else:
            raise WrongFileError

    #cria um erro caso 'names' não possuir valor
    if not dates and not names:
        raise KeyError


    name_list = []  # Variável para armazenar a lista de nomes
    # Loop para processar apenas name_list
    for name in names:
        if not pd.isna(name):  # Verifica se o valor do nome não é NaN
            name_list.append(name)  # Adiciona os nomes à lista


    # Cria um Data Frame
    data = {
        "Nome": name_list
    }
    # Adicionando as colunas de Janeiro a Dezembro preenchidas com 0
    meses = ["Janeiro 1º Quin.", "Janeiro 2º Quin.", "Fevereiro 1º Quin.", "Fevereiro 2º Quin.", "Março 1º Quin.", "Março 2º Quin.", "Abril 1º Quin.", "Abril 2º Quin.", "Maio 1º Quin.", "Maio 2º Quin.", "Junho 1º Quin.", "Junho 2º Quin.",
            "Julho 1º Quin.", "Julho 2º Quin.", "Agosto 1º Quin.", "Agosto 2º Quin.", "Setembro 1º Quin.", "Setembro 2º Quin.", "Outubro 1º Quin.", "Outubro 2º Quin.", "Novembro 1º Quin.", "Novembro 2º Quin.", "Dezembro 1º Quin.", "Dezembro 2º Quin."]


    for mes in meses:
        data[mes] = [0] * len(name_list)

    # Transformando o dicionário em um DataFrame
    df = pd.DataFrame(data)
    # Salvar o DataFrame em um arquivo JSON

    df.to_json(os.path.join(save_path, 'table_data.json'), orient='records', force_ascii=False)

    if os.path.exists(os.path.join(save_path, 'completed_table_data.json')):

        # Recupera o DF com dados inseridos manualmente
        saved_df = pd.read_json(os.path.join(save_path, 'completed_table_data.json'), orient='records')

        # Processo para comparar e adicionar as linhas no novo DF
        # Definindo o "Nome" como índice para facilitar as comparações
        df.set_index("Nome", inplace=True)
        saved_df.set_index("Nome", inplace=True)

        # Verificando as linhas que existem em df mas não em saved_df e adicionando-as em saved_df
        missing_rows = df[~df.index.isin(saved_df.index)]
        saved_df = pd.concat([saved_df, missing_rows])

        # Verificando as linhas que existem em saved_df mas não em df e removendo-as de saved_df
        extra_rows = saved_df[~saved_df.index.isin(df.index)]
        saved_df = saved_df.drop(extra_rows.index)

        # Resetando o índice para que "Nome" volte a ser uma coluna
        saved_df.reset_index(inplace=True)

        # Organizando o DataFrame em ordem alfabética com base na coluna "Nome"
        saved_df = saved_df.sort_values(by="Nome")

        # Salva o DF novo
        saved_df.to_json(os.path.join(save_path, 'completed_table_data.json'), orient='records', force_ascii=False)


            # Definição da função half_month()
        def half_month():
            current_date = datetime.now().date()
            first_month_date = current_date.replace(day=1)
            last_month_date = current_date.replace(day=1, month=current_date.month % 12 + 1) - timedelta(days=1)
            half_month_date = first_month_date + timedelta(days=(last_month_date.day - 1) // 2)
            
            if current_date <= half_month_date:
                return first_month_date
            else:
                return half_month_date

        month_date = half_month()

        # Soma das horas de cada linha
        saved_df["Total Horas"] = saved_df.iloc[:, 1:].sum(axis=1)

        # Transforma as horas em dias arredondados e remove as casas decimais
        saved_df["Dias Restantes"] = (180 - saved_df["Total Horas"] / 8).round().astype(int)

        # Converter month_date para datetime..
        month_date_datetime = datetime.combine(month_date, datetime.min.time())

        # Adicionar a coluna "Saída Prevista". Ela é calculada a partir do começo ou metade do mês
        saved_df["Saída Prevista"] = month_date_datetime + pd.to_timedelta(saved_df["Dias Restantes"], unit="D")
        
        # Calcular a diferença em dias entre a data atual e a "Saída Prevista"
        current_date = datetime.now()
        

        # Filtrar linhas onde faltam menos de 5 dias para a saída prevista e a data é maior ou igual à atual
        rows_to_print = saved_df[(saved_df["Saída Prevista"] - current_date).dt.days < 7]


        # Lista para armazenar os valores formatados
        final_exit_dates_list = []

        # Iterar sobre as linhas para formatar os valores
        for index, row in rows_to_print.iterrows():
            formatted_date = f"{row['Nome']}   {row['Saída Prevista'].strftime('%d/%m/%Y')}"
            final_exit_dates_list.append(formatted_date)

        # Transformar a lista em uma única string, separando os valores com uma quebra de linha
        final_exit_dates = '\n'.join(final_exit_dates_list)

        print(saved_df)


        saved_df["Saída Prevista"] = saved_df["Saída Prevista"].dt.strftime("%d/%m/%Y")


        # Template HTML atualizado
        template_html = """
        <!DOCTYPE html>
        <html>

        <head>
            <meta charset="UTF-8">
            <link rel="icon" type="image/icon" href="../icon.ico">
            <title>W.F.C - Detalhes</title>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                }

                th,
                td {
                    border: 1px solid rgb(136, 136, 136);
                    padding: 8px;
                    text-align: left;
                }

                th {
                    background-color: rgba(46, 46, 46, 0.322);
                }

                tr:nth-child(even) {
                    background-color: white;
                }

                tr:nth-child(odd) {
                    background-color: rgba(65, 65, 65, 0.322);
                }

                /* Defina o tamanho das colunas */
                .month-cell {
                    width: 12ch;
                }

            </style>
        </head>

        <body>
            <table>
                <thead>
                        <th>Nome</th>
                        <th>Janeiro 1º Quin.</th>
                        <th>Janeiro 2º Quin.</th>
                        <th>Fevereiro 1º Quin.</th>
                        <th>Fevereiro 2º Quin.</th>
                        <th>Março 1º Quin.</th>
                        <th>Março 2º Quin.</th>
                        <th>Abril 1º Quin.</th>
                        <th>Abril 2º Quin.</th>
                        <th>Maio 1º Quin.</th>
                        <th>Maio 2º Quin.</th>
                        <th>Junho 1º Quin.</th>
                        <th>Junho 2º Quin.</th>
                        <th>Julho 1º Quin.</th>
                        <th>Julho 2º Quin.</th>
                        <th>Agosto 1º Quin.</th>
                        <th>Agosto 2º Quin.</th>
                        <th>Setembro 1º Quin.</th>
                        <th>Setembro 2º Quin.</th>
                        <th>Outubro 1º Quin.</th>
                        <th>Outubro 2º Quin.</th>
                        <th>Novembro 1º Quin.</th>
                        <th>Novembro 2º Quin.</th>
                        <th>Dezembro 1º Quin.</th>
                        <th>Dezembro 2º Quin.</th>
                        <th>Total Horas</th>
                        <th>Dias Restantes</th>
                        <th>Saída Prevista</th>
                    </tr>
                </thead>
                <tbody id="table-body">
                    {% for index, row in saved_df.iterrows() %}
                    <tr>
                        <td>{{ row['Nome'] }}</td>
                        <td>{{ row['Janeiro 1º Quin.'] }}</td>
                        <td>{{ row['Janeiro 2º Quin.'] }}</td>
                        <td>{{ row['Fevereiro 1º Quin.'] }}</td>
                        <td>{{ row['Fevereiro 2º Quin.'] }}</td>
                        <td>{{ row['Março 1º Quin.'] }}</td>
                        <td>{{ row['Março 2º Quin.'] }}</td>
                        <td>{{ row['Abril 1º Quin.'] }}</td>
                        <td>{{ row['Abril 2º Quin.'] }}</td>
                        <td>{{ row['Maio 1º Quin.'] }}</td>
                        <td>{{ row['Maio 2º Quin.'] }}</td>
                        <td>{{ row['Junho 1º Quin.'] }}</td>
                        <td>{{ row['Junho 2º Quin.'] }}</td>
                        <td>{{ row['Julho 1º Quin.'] }}</td>
                        <td>{{ row['Julho 2º Quin.'] }}</td>
                        <td>{{ row['Agosto 1º Quin.'] }}</td>
                        <td>{{ row['Agosto 2º Quin.'] }}</td>
                        <td>{{ row['Setembro 1º Quin.'] }}</td>
                        <td>{{ row['Setembro 2º Quin.'] }}</td>
                        <td>{{ row['Outubro 1º Quin.'] }}</td>
                        <td>{{ row['Outubro 2º Quin.'] }}</td>
                        <td>{{ row['Novembro 1º Quin.'] }}</td>
                        <td>{{ row['Novembro 2º Quin.'] }}</td>
                        <td>{{ row['Dezembro 1º Quin.'] }}</td>
                        <td>{{ row['Dezembro 2º Quin.'] }}</td>
                        <td>{{ row['Total Horas'] }}</td>
                        <td>{{ row['Dias Restantes'] }}</td>
                        <td>{{ row['Saída Prevista'] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>

        </html>
        """

        # Renderiza o template com os dados do DataFrame
        template = Template(template_html)
        html_output = template.render(saved_df=saved_df)

        # Salva o resultado em um arquivo HTML
        details_path = os.path.join(save_path, 'Detalhes.html')
        with open (details_path, 'w', encoding="utf-8") as file:
            file.write(html_output)


        # Sem erros até aqui, então poderá finalizar a contagem de erros
        def error_count_reset():
            error_count = 0
            with open(os.path.join(save_path, 'error_count.txt'), 'w') as error_count_file:
                error_count_file.write(str(error_count))
        error_count_reset()

        
        see_details = [
            {'activationType': 'protocol',
                'arguments':  details_path, 'content': 'Ver Detalhes'}
        ]
        if len(final_exit_dates_list) > 0 and automatic:
            toast(
            app_id="WorkFront Countdown",
            title='Os dias úteis dos seguintes trabalhadores estão acabando:',
            body=final_exit_dates,
            audio='ms-winsoundevent:Notification.Looping.Alarm3',
            buttons=['Inserir Dados'] + see_details,
            duration='long',
            on_click=on_click,
            on_dismissed=empty_func
            )
            
        else:
            def verifica_data():
                if automatic:
                    hoje = datetime.today()
                    ultimo_dia_mes = (hoje.replace(day=1, month=hoje.month % 12 + 1, year=hoje.year) - timedelta(days=1)).day
                    metade_mes = ultimo_dia_mes // 2
                    if hoje.day in {1, 2, 3, metade_mes + 1, metade_mes + 2, metade_mes + 3}:

                        toast(
                            app_id="WorkFront Countdown",
                            title="Insira os dados",
                            body="Estamos no período de recolha dos pontos. Clique para adicionar mais dados.",
                            audio='ms-winsoundevent:Notification.Looping.Alarm3',
                            buttons=['Inserir Dados'],
                            duration='long',
                            on_click=on_click,
                            on_dismissed=empty_func
                        )
                else:
                        # Obtém a hora atual
                        current_time = datetime.now().hour

                        # Define o limite para considerar como "tarde"
                        afternoon = 12  # 12 AM

                        if current_time >= afternoon:
                            Greeting = "Boa tarde"
                        else:
                            Greeting = "Bom dia"
                        toast(
                        app_id="WorkFront Countdown",
                        title="Execução Manual",
                        body=Greeting + ", o que você deseja fazer?",
                        audio='ms-winsoundevent:Notification.Looping.Alarm3',
                        buttons=['Inserir Dados', 'Atualizar PDF'] + see_details,
                        duration='long',
                        on_click=on_click,
                        on_dismissed=empty_func
                    )

            # Chame a função verifica_data() para executar a lógica com base no valor de `automatic`.
            verifica_data()

    else:
        toast(
        app_id="WorkFront Countdown",
        title='Nenhum dado inserido',
        body="Não é possível calcular a data de saída pois não há dados. Por favor, insire os dados na tabela.",
        audio='ms-winsoundevent:Notification.IM',
        buttons=['Inserir Dados','Atualizar PDF'],
        duration='long',
        on_click=on_click,
        on_dismissed=empty_func
        )
except KeyError as e:
    error_count += 1
    with open(os.path.join(save_path, 'error_count.txt'), 'w') as error_count_file:
        error_count_file.write(str(error_count))

    toast(
    app_id="WorkFront Countdown",
    title='Erro de Leitura',
    body="Não foi possível realizar a leitura do PDF selecionado. Certifique-se de que o arquivo que contém a lista dos trabalhadores que foi fornecido pela prefeitura esteja selecionado.",
    audio='ms-winsoundevent:Notification.IM',
    buttons=['Atualizar PDF'],
    duration='long',
    on_click=on_click,
    on_dismissed=empty_func
    )
except WrongFileError as e:
    error_count += 1
    with open(os.path.join(save_path, 'error_count.txt'), 'w') as error_count_file:
        error_count_file.write(str(error_count))

    toast(
    app_id="WorkFront Countdown",
    title='Arquivo errado',
    body="Esse arquivo não é o arquivo PDF da frente de trabalho fornecido pela prefeitura. Por favor, selecione o arquivo correto para poder continuar.",
    audio='ms-winsoundevent:Notification.IM',
    buttons=['Atualizar PDF'],
    duration='long',
    on_click=on_click,
    on_dismissed=empty_func
    )

except Exception as e:
    print("Ocorreu um erro:", str(e))
    error_count += 1
    with open(os.path.join(save_path, 'error_count.txt'), 'w') as error_count_file:
        error_count_file.write(str(error_count))
    
    toast(
    app_id="WorkFront Countdown",
    title='Erro Crítico',
    body=f'Durante a execução, ocorreu o erro não tratado: {str(e)}.',
    audio='ms-winsoundevent:Notification.IM',
    buttons=['Atualizar PDF', 'Deletar Dados'],
    duration='long',
    on_click=on_click,
    on_dismissed=empty_func
    )
if global_args is not None and 'arguments' in global_args and 'Atualizar PDF' in global_args['arguments']:
    new_argv = [sys.executable] + sys.argv + ["--pdf"]
    subprocess.call(new_argv)
if global_args is not None and 'arguments' in global_args and 'Deletar Dados' in global_args['arguments']:
    def mostrar_caixa_confirmacao():
        response = messagebox.askyesno("Confirmação", "Você tem certeza que deseja excluir todos os dados salvos de WorkFront Countdown? Essa ação não poderá ser desfeita, utilize em último caso.",
                                    icon='warning', default=messagebox.NO)  # Definir 'Não' como padrão
        
        if response:
            try:
                shutil.rmtree(appdata_path)
            except Exception as e:
                sys.exit()
        else:
            sys.exit()

    # Criar uma window vazia apenas para usar o tkinter
    window = tk.Tk()
    window.withdraw()  # Oculta a window principal
    window.wm_attributes("-topmost", 1)  # Define a window como "sempre no topo"

    # Definir o ícone da janela
    window.iconbitmap('./icon.ico')

    # Chamar a função para mostrar a caixa de confirmação
    mostrar_caixa_confirmacao()

    # Fechar a window (opcional)
    window.destroy()

if global_args is not None and 'arguments' in global_args and 'Inserir Dados' in global_args['arguments']:

    # Define a porta que o servidor vai usar
    PORT = 8012

    def check_port(PORT):
        try:
            # Cria um objeto socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Tenta se conectar à porta especificada
            s.connect(("localhost", PORT))
            
            # Se a conexão for bem-sucedida, a porta está ocupada
            def open_browser():
                webbrowser.open(f"http://localhost:{PORT}")
            open_browser()
            sys.exit()
        except ConnectionRefusedError:
            # Se a conexão for recusada, a porta está disponível
            pass
        finally:
            # Fecha o socket
            s.close()

    check_port(PORT)

    # Define o nome do arquivo HTML que deseja abrir
    HTML_FILE = "table.html"

    # Define o diretório para servir os arquivos

    last_access_time = time.time()

    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header("Content-Type", "text/html; charset=utf-8")
            super().end_headers()

        def do_GET(self):
            global last_access_time
            last_access_time = time.time()  # Atualiza o tempo do último acesso
            if self.path == '/':
                self.path = HTML_FILE
            elif self.path.startswith('/files'):
                self.path = self.path.lstrip('/files')
                self.send_file_response(os.path.join(save_path, self.path))
                return
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        def send_file_response(self, file_path):
            try:
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header("Content-Type", self.guess_type(file_path))
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("Arquivo não encontrado".encode('utf-8'))

        def do_POST(self):
            global last_access_time
            last_access_time = time.time()  # Atualiza o tempo do último acesso
            if self.path == '/save_data':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                table_data = json.loads(post_data)

                # Cria um DataFrame a partir dos dados
                df = pd.DataFrame(table_data)


                def do_backup(save_path="./save", Amount=3):
                    if os.path.exists(save_path):


                        # Renomear os arquivos de backup existentes, se houver
                        for i in range(Amount, 0, -1):
                            last_backup = f"{save_path}.bak{i}"
                            if os.path.exists(last_backup):
                                if i == Amount:
                                    os.remove(last_backup)
                                else:
                                    new_backup = f"{save_path}.bak{i + 1}"
                                    os.rename(last_backup, new_backup)

                        # Renomear o arquivo original para o primeiro backup
                        os.rename(save_path, f"{save_path}.bak1")
                
                file_path = os.path.join(save_path, 'completed_table_data.json')
                if os.path.exists(file_path):
                    do_backup(file_path, 5)
                print(file_path)
                # Salva o DataFrame em um arquivo JSON na pasta com o nome 'completed_table_data.json'
                
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json_file.write(df.to_json(force_ascii=False, orient='records'))

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response = {"message": "Dados salvos com sucesso"}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

    def check_activity():
        global last_access_time
        while True:
            time_since_last_access = time.time() - last_access_time
            if time_since_last_access > 36000:  # Mais de 10 minutos sem acesso
                os._exit(0)  # Encerra o programa (incluindo threads)

            time.sleep(30)  # Verifica a cada 30 segundos

    # Inicia o servidor principal em uma thread
    def start_server():
        handler = MyHttpRequestHandler
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            httpd.serve_forever()

    # Abre o navegador automaticamente com o arquivo HTML e inicia o arquivo de log
    def redirect_output_to_log():
        log_file = os.path.join(appdata_path, "server_log.txt")
        sys.stdout = open(log_file, "w")
        sys.stderr = open(log_file, "w")

    def open_browser():
        webbrowser.open(f"http://localhost:{PORT}")

    # Inicia o servidor e a verificação de atividade, e abre o navegador
    if __name__ == "__main__":
        redirect_output_to_log()

        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()

        activity_thread = threading.Thread(target=check_activity)
        activity_thread.daemon = True
        activity_thread.start()

        open_browser()

        server_thread.join()
