import sqlite3
import os
from datetime import datetime

# 🔧 Cria o banco e a tabela, se não existirem
def criar_tabela():
    with sqlite3.connect("diario.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anotacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                texto TEXT NOT NULL
            );
        """)
        conn.commit()

# 📝 Escreve no diário (arquivo + banco)
def escrever_no_diario():
    texto = input("Digite sua anotação: ")
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    entrada_formatada = f"[{data_hora}] {texto}\n"

    # Salva no banco de dados
    with sqlite3.connect("diario.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO anotacoes (data_hora, texto) VALUES (?, ?)", (data_hora, texto))
        conn.commit()

    # Salva no arquivo texto
    with open("diario.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(entrada_formatada)

    print("✅ Anotação salva no banco de dados e no arquivo .txt!\n")

# 📖 Lê todas as anotações do banco
def ler_diario():
    if not os.path.exists("diario.db"):
        print("📭 O diário está vazio.\n")
        return

    with sqlite3.connect("diario.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data_hora, texto FROM anotacoes ORDER BY id")
        entradas = cursor.fetchall()

        if not entradas:
            print("📭 O diário está vazio.\n")
        else:
            print("\n📖 Entradas do Diário:")
            for data_hora, texto in entradas:
                print(f"[{data_hora}] {texto}")
            print()

# 📋 Menu principal
def menu():
    criar_tabela()
    while True:
        print("=== Diário Eletrônico ===")
        print("1. Escrever no diário")
        print("2. Ler diário")
        print("3. Sair")
        escolha = input("Escolha uma opção (1/2/3): ")

        if escolha == "1":
            escrever_no_diario()
        elif escolha == "2":
            ler_diario()
        elif escolha == "3":
            print("👋 Saindo do programa. Até logo!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    menu()
