# main.py

import sys

def main():
    """Ponto de entrada do programa"""
    print("🚀 Iniciando Sistema de Gerenciamento Esportivo...")
    print("📱 Carregando interface gráfica...")
    
    try:
        from app_tkinter import main as tkinter_main
        tkinter_main()
    except ImportError as e:
        print(f"❌ Erro ao carregar interface: {e}")
        print("Verifique se o Tkinter está instalado no seu sistema.")
        sys.exit(1)

if __name__ == "__main__":
    main()