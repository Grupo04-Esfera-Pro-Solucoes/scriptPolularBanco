from time import sleep
import mysql.connector
from faker import Faker
import os
import random

conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root", # Alterar para o usuário do seu banco de dados
    password="root", # Alterar para a senha do seu banco de dados
    database="esfera-g2" # Alterar para o nome do seu banco de dados
)

cursor = conn.cursor()

user_id = 1 # Alterar para o id do usuário que os registros serão associados
mult_tentativas = 2 # Valor auxiliar para parar a geração de dados caso ocorra algum erro
value = 1 # Valor auxiliar para gerar chaves estrangeiras, colocar quantidade de linhas já cadastradas no banco mais 1 (por exemplo, se cada tabela tem 100000 linhas, colocar 100001 para executar denovo e não repetir os valores de chave estrangeira)
qtd = 5000 # Alterar para a quantidade de registros a serem gerados para cada execução

def remover_caracteres_cpf_cnpj(cpf_cnpj):
    cpf_cnpj = cpf_cnpj.replace(".", "")
    cpf_cnpj = cpf_cnpj.replace("-", "")
    cpf_cnpj = cpf_cnpj.replace("/", "")
    return cpf_cnpj

def remover_caracteres_telefone(telefone):
    telefone = telefone.replace("(", "")
    telefone = telefone.replace(")", "")
    telefone = telefone.replace("-", "")
    telefone = telefone.replace(" ", "")
    telefone = telefone.replace("+", "")
    return telefone

def gerar_dados_clientes(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (fake.company(), remover_caracteres_cpf_cnpj(random.choice([fake.cpf(), fake.cnpj()])), fake.date_time_this_decade(), fake.name(), fake.job(), user_id)
        dados.add(novo_dado)
        print(f"Gerando dados de clientes: {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def inserir_dados_clientes(cursor, dados):
    sql = "INSERT IGNORE INTO client (company, `cpf-cnpj`, date, name, role, user_id_user) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, dados)
    conn.commit()


def gerar_dados_address(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (fake.city(), fake.country(), fake.building_number(), fake.state(), fake.street_name(), fake.postcode(), tentativas+value)
        dados.add(novo_dado)
        print(f"Gerando dados de endereço: {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def inserir_dados_address(cursor, dados):
    sql = "INSERT IGNORE INTO address (city, country, number, state, street, zip_code, client_id_client) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, dados)
    conn.commit()

def gerar_dados_leads(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (fake.time(), fake.phone_number(), fake.date_time_this_year(), fake.sentence(), fake.time(), tentativas+value, fake.random_int(min=1, max=4))
        dados.add(novo_dado)
        print(f"Gerando dados de leads: {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def inserir_dados_leads(cursor, dados):
    sql = "INSERT IGNORE INTO leads (call_time, contact, date, description, duration, client_id_client, result_id_lead_result) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, dados)
    conn.commit()

def gerar_dados_contact_cel(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (remover_caracteres_telefone(fake.phone_number()), tentativas+value, 1)
        dados.add(novo_dado)
        print(f"Gerando dados de contato (celular): {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def gerar_dados_contact_tel(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (remover_caracteres_telefone(fake.phone_number()), tentativas+value, 2)
        dados.add(novo_dado)
        print(f"Gerando dados de contato (telefone): {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def gerar_dados_contact_whats(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (remover_caracteres_telefone(fake.phone_number()), tentativas+value, 3)
        dados.add(novo_dado)
        print(f"Gerando dados de contato (whats): {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def gerar_dados_contact_email(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (fake.email(), tentativas+value, 4)
        dados.add(novo_dado)
        print(f"Gerando dados de contato (email): {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def inserir_dados_contact(cursor, dados):
    sql = "INSERT IGNORE INTO contact (data, client_id_client, type_contact_id_type_contact) VALUES (%s, %s, %s)"
    cursor.executemany(sql, dados)
    conn.commit()

def gerar_dados_proposal(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (fake.sentence(), '', fake.date_time_this_year(), random.choice(['Acompanhamento', 'Consultoria', 'Treinamento']), fake.random_int(min=100, max=1500), tentativas+value, fake.random_int(min=1, max=4))
        dados.add(novo_dado)
        print(f"Gerando dados de proposta: {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def inserir_dados_proposal(cursor, dados):
    sql = "INSERT IGNORE INTO proposal (description, file, proposal_date, service, value, lead_id_lead, statusproposal_id_statusproposal) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, dados)
    conn.commit()

def gerar_dados_task(quantidade):
    fake = Faker('pt_BR')
    dados = set()
    tentativas = 0
    while len(dados) < quantidade:
        novo_dado = (fake.sentence(), fake.date_time_this_year(), fake.name(), random.choice(['todo-list', 'inprogress-list', 'done-list']), user_id)
        dados.add(novo_dado)
        print(f"Gerando dados de task: {len(dados)}/{quantidade}", end="\r")
        tentativas += 1
        if tentativas > mult_tentativas * quantidade:
            print("Número máximo de tentativas alcançado, parando a geração de dados.")
            break
    return list(dados)

def inserir_dados_task(cursor, dados):
    sql = "INSERT IGNORE INTO task (description, due_date, name, status, user_id_user) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, dados)
    conn.commit()

os.system('cls')
dados_clientes = gerar_dados_clientes(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_clientes(cursor, dados_clientes)
dados_clientes = None
print("Dados de clientes inseridos com sucesso!")
sleep(2)

os.system('cls')
dados_address = gerar_dados_address(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_address(cursor, dados_address)
dados_address = None
print("Dados de endereço inseridos com sucesso!")
sleep(2)

os.system('cls')
dados_leads = gerar_dados_leads(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_leads(cursor, dados_leads)
dados_leads = None
print("Dados de leads inseridos com sucesso!")
sleep(2)

os.system('cls')
dados_contact = gerar_dados_contact_cel(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_contact(cursor, dados_contact)
dados_contact = None
print("Dados de contato inseridos com sucesso!")
sleep(2)

os.system('cls')
dados_contact = gerar_dados_contact_tel(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_contact(cursor, dados_contact)
dados_contact = None
print("Dados de contato inseridos com sucesso!")
sleep(2)

os.system('cls')
dados_contact = gerar_dados_contact_whats(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_contact(cursor, dados_contact)
dados_contact = None
print("Dados de contato inseridos com sucesso!")
sleep(2)

os.system('cls')
dados_contact = gerar_dados_contact_email(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_contact(cursor, dados_contact)
dados_contact = None
print("Dados de contato inseridos com sucesso!")
sleep(2)

os.system('cls')
dados_proposal = gerar_dados_proposal(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_proposal(cursor, dados_proposal)
dados_proposal = None
print("Dados de proposta inseridos com sucesso!")
sleep(2)

os.system('cls')
dados_task = gerar_dados_task(qtd)
os.system('cls')
print("Inserindo dados no banco de dados...")
inserir_dados_task(cursor, dados_task)
dados_task = None
print("Dados de task inseridos com sucesso!")
sleep(2)

os.system('cls')
print("Todos os dados foram inseridos com sucesso!")

cursor.close()
conn.close()