import sqlite3
import json
import re

def validar_e_tratar_dados(dados):
    """Valida e normaliza os dados do lead."""
    erros = []
    
    nome = dados.get("nome", "").strip()
    if not nome:
        erros.append("O campo 'nome' é obrigatório e não pode ser vazio.")
        
    telefone_raw = dados.get("telefone", "").strip()
    if not telefone_raw:
        erros.append("O campo 'telefone' é obrigatório e não pode ser vazio.")
    else:
        # remover caracteres especiais, mantendo apenas números
        telefone = re.sub(r'\D', '', telefone_raw)
    
    # Validação e Tratamento de E-mail
    email_raw = dados.get("email", "").strip()
    if not email_raw:
        erros.append("O campo 'email' é obrigatório e não pode ser vazio.")
    else:
        email = email_raw.lower().strip()
        
    especialidade = dados.get("especialidade", "").strip()
    if not especialidade:
        erros.append("O campo 'especialidade' é obrigatório e não pode ser vazio.")
        
    desafio = dados.get("principal_desafio", "").strip()
    if not desafio:
        erros.append("O campo 'principal_desafio' é obrigatório e não pode ser vazio.")
        
    if erros:
        for erro in erros:
            print(f"Erro: {erro}")
        return None
    
    return {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "especialidade": especialidade,
        "principal_desafio": desafio
    }

def salvar_no_banco(lead):
    """Salva os dados do lead no SQLite."""
    try:
        conn = sqlite3.connect("leads.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL,
                especialidade TEXT NOT NULL,
                principal_desafio TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            INSERT INTO leads (nome, telefone, email, especialidade, principal_desafio)
            VALUES (?, ?, ?, ?, ?)
        """, (lead['nome'], lead['telefone'], lead['email'], lead['especialidade'], lead['principal_desafio']))
        
        conn.commit()
        conn.close()
        print("Lead salvo com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")
        return False

def simular_clickup(lead):
    """Simula a criação de uma tarefa no ClickUp."""
    payload = {
        "name": f"Novo Lead - {lead['nome']}",
        "description": f"""
Nome: {lead['nome']}
Telefone: {lead['telefone']}
Email: {lead['email']}
Especialidade: {lead['especialidade']}
Desafio: {lead['principal_desafio']}
""",
        "assignee": "Comercial"
    }
    
    print("\n=== TAREFA CLICKUP ===")
    print(json.dumps(payload, indent=4, ensure_ascii=False))

def processar_lead(json_entrada):
    """Fluxo principal de processamento do lead."""
    try:
        dados = json.loads(json_entrada)
        lead_tratado = validar_e_tratar_dados(dados)
        
        if lead_tratado:
            if salvar_no_banco(lead_tratado):
                simular_clickup(lead_tratado)
    except json.JSONDecodeError:
        print("Erro: JSON de entrada inválido.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    json_exemplo = '''
    {
      "nome": "Maria Silva",
      "telefone": "(54) 99999-8888",
      "email": " MARIA@EMAIL.COM",
      "especialidade": "Dermatologia",
      "principal_desafio": "Captar mais pacientes"
    }
    '''
    
    processar_lead(json_exemplo)
