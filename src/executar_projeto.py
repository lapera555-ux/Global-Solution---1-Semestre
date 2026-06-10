from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(cmd):
    print("\n$", " ".join(str(c) for c in cmd))
    return subprocess.call([str(c) for c in cmd], cwd=BASE_DIR)


def instalar_dependencias():
    return run([PYTHON, "-m", "pip", "install", "-r", "requirements.txt"])


def validar():
    return run([PYTHON, "src/validar_entrega.py"])


def treinar_modelo():
    return run([PYTHON, "src/modelo_risco.py"])


def gerar_relatorio():
    return run([PYTHON, "src/gerar_relatorio_html.py"])


def simular_esp32():
    return run([PYTHON, "src/esp32_simulado.py"])


def abrir_dashboard():
    return run([PYTHON, "-m", "streamlit", "run", "src/dashboard.py"])


def main():
    print("AgroENSO Risk IA | Execução completa profissional")
    print("=" * 48)
    etapas = [
        ("Instalação de dependências", instalar_dependencias),
        ("Validação da entrega", validar),
        ("Treinamento do modelo", treinar_modelo),
        ("Geração do relatório HTML", gerar_relatorio),
        ("Simulação ESP32", simular_esp32),
        ("Abertura do dashboard", abrir_dashboard),
    ]
    for nome, fn in etapas:
        print(f"\n>>> {nome}")
        code = fn()
        if code != 0:
            print("\nExecução interrompida por pendência crítica. Avisos simples, como links pendentes, não bloqueiam o projeto.")
            return code
    return 0


if __name__ == "__main__":
    sys.exit(main())
