import psycopg2
from psycopg2 import Error

# Configurações do banco de dados
DB_HOST = "localhost"
DB_NAME = "sistema_alunos"
DB_USER = "postgres"
DB_PASS = "124589"
DB_PORT = "5432"


# Cores para o terminal 
COR_SUCESSO = "\033[92m"  # Verde
COR_ERRO = "\033[91m"  # Vermelho
COR_INFO = "\033[94m"  # Azul
COR_RESET = "\033[0m"  # Reseta a cor


def conectar():
  try:
    conexao = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
    )
    return conexao
  except Error as e:
    print(f"{COR_ERRO}❌ Erro ao conectar ao banco de dados: {e}{COR_RESET}")
    return None


def criar_tabela():
  conexao = conectar()
  if conexao:
    try:
      cursor = conexao.cursor()
      cursor.execute("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    idade INTEGER NOT NULL,
                    nota NUMERIC(4,2) NOT NULL
                );
            """)
      conexao.commit()
      cursor.close()
      conexao.close()
    except Error as e:
      print(f"{COR_ERRO}❌ Erro ao criar a tabela: {e}{COR_RESET}")


def adicionar():
  print("\n" + "=" * 40)
  print("          CADASTRAR NOVO ALUNO")
  print("=" * 40)
  nome = input("👤 Nome do aluno: ").strip()

  try:
    idade = int(input("🎂 Idade do aluno: "))
    nota = float(input("📝 Nota do aluno (0 a 10): "))
  except ValueError:
    print(
        f"{COR_ERRO}❌ Erro: Idade e nota devem ser numeros validos.{COR_RESET}"
    )
    return

  while nota < 0 or nota > 10:
    print(f"{COR_ERRO}⚠️ Nota invalida! Insira um valor entre 0 e 10.{COR_RESET}")
    try:
      nota = float(input("📝 Nota do aluno (0 a 10): "))
    except ValueError:
      nota = -1

  conexao = conectar()
  if conexao:
    try:
      cursor = conexao.cursor()
      cursor.execute(
          "INSERT INTO alunos (nome, idade, nota) VALUES (%s, %s, %s)",
          (nome, idade, nota),
      )
      conexao.commit()
      print(f"{COR_SUCESSO}✅ Aluno cadastrado com sucesso!{COR_RESET}")
      cursor.close()
      conexao.close()
    except Error as e:
      print(f"{COR_ERRO}❌ Erro ao cadastrar aluno: {e}{COR_RESET}")


def listar():
  print("\n" + "=" * 65)
  print(f"{'ID':<5} | {'NOME DO ALUNO':<30} | {'IDADE':<6} | {'NOTA':<6}")
  print("=" * 65)

  conexao = conectar()
  if conexao:
    try:
      cursor = conexao.cursor()
      cursor.execute("SELECT id, nome, idade, nota FROM alunos ORDER BY id;")
      registros = cursor.fetchall()

      if not registros:
        print(f"{COR_INFO}ℹ️ Nao existem alunos cadastrados.{COR_RESET}")
      else:
        for aluno in registros:
          id_aluno, nome, idade, nota = aluno
          print(
              f"{id_aluno:<5} | {nome:<30} | {str(idade):<6} |"
              f" {str(nota):<6}"
          )

      print("=" * 65)
      cursor.close()
      conexao.close()
    except Error as e:
      print(f"{COR_ERRO}❌ Erro ao listar alunos: {e}{COR_RESET}")


def buscar():
  print("\n" + "=" * 40)
  print("           BUSCAR ALUNO")
  print("=" * 40)
  nome = input("🔍 Digite o nome (ou parte do nome): ").strip()

  conexao = conectar()
  if conexao:
    try:
      cursor = conexao.cursor()
      cursor.execute(
          "SELECT id, nome, idade, nota FROM alunos WHERE nome ILIKE %s;",
          (f"%{nome}%",),
      )
      registros = cursor.fetchall()

      if not registros:
        print(f"{COR_ERRO}❌ Nenhum aluno encontrado com esse nome.{COR_RESET}")
      else:
        print("\n" + "=" * 65)
        print(f"{'ID':<5} | {'NOME DO ALUNO':<30} | {'IDADE':<6} | {'NOTA':<6}")
        print("=" * 65)
        for aluno in registros:
          print(
              f"{aluno[0]:<5} | {aluno[1]:<30} | {str(aluno[2]):<6} |"
              f" {str(aluno[3]):<6}"
          )
        print("=" * 65)

      cursor.close()
      conexao.close()
    except Error as e:
      print(f"{COR_ERRO}❌ Erro ao buscar aluno: {e}{COR_RESET}")


def remover():
  print("\n" + "=" * 40)
  print("           REMOVER ALUNO")
  print("=" * 40)
  nome = input("🗑️ Digite o nome exato do aluno para remover: ").strip()

  conexao = conectar()
  if conexao:
    try:
      cursor = conexao.cursor()
      cursor.execute(
          "SELECT id, nome FROM alunos WHERE nome ILIKE %s;", (nome,)
      )
      registros = cursor.fetchall()

      if not registros:
        print(f"{COR_ERRO}❌ Aluno nao encontrado para remocao.{COR_RESET}")
      else:
        cursor.execute("DELETE FROM alunos WHERE nome ILIKE %s;", (nome,))
        conexao.commit()
        print(f"{COR_SUCESSO}✅ Aluno removido com sucesso!{COR_RESET}")

      cursor.close()
      conexao.close()
    except Error as e:
      print(f"{COR_ERRO}❌ Erro ao remover aluno: {e}{COR_RESET}")


def media():
  print("\n" + "=" * 40)
  print("         ESTATISTICAS DA TURMA")
  print("=" * 40)
  conexao = conectar()
  if conexao:
    try:
      cursor = conexao.cursor()
      cursor.execute("SELECT AVG(nota), COUNT(*) FROM alunos;")
      resultado = cursor.fetchone()

      media_notas = resultado[0]
      total_alunos = resultado[1]

      if total_alunos == 0 or media_notas is None:
        print(
            f"{COR_INFO}ℹ️ Nao ha alunos cadastrados para calcular a"
            f" media.{COR_RESET}"
        )
      else:
        print(f"📊 Total de alunos cadastrados: {total_alunos}")
        print(f"📈 Media geral da turma: {float(media_notas):.2f}")
      print("=" * 40)

      cursor.close()
      conexao.close()
    except Error as e:
      print(f"{COR_ERRO}❌ Erro ao calcular media: {e}{COR_RESET}")


def main():
  criar_tabela()
  while True:
    print(f"\n{COR_INFO}======================================================{COR_RESET}")
    print("                 SISTEMA DE GESTAO DE ALUNOS")
    print(f"{COR_INFO}======================================================{COR_RESET}")
    print(" [1] ➕ Adicionar novo aluno")
    print(" [2] 📋 Listar todos os alunos")
    print(" [3] 🔍 Buscar aluno por nome")
    print(" [4] 🗑️ Remover aluno")
    print(" [5] 📊 Ver media da turma")
    print(" [6] 🚪 Sair do sistema")
    print(f"{COR_INFO}======================================================{COR_RESET}")

    op = input("👉 Escolha uma opcao: ").strip()

    if op == "1":
      adicionar()
    elif op == "2":
      listar()
    elif op == "3":
      buscar()
    elif op == "4":
      remover()
    elif op == "5":
      media()
    elif op == "7":
      print(f"\n{COR_SUCESSO}👋 Saindo do sistema. Ate logo!{COR_RESET}")
      break
    else:
      print(
          f"{COR_ERRO}❌ Opcao invalida! Escolha uma opcao do menu.{COR_RESET}"
      )


if __name__ == "__main__":
  main()
