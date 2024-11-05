import os
import json
import customtkinter as ctk
from tkinter import filedialog, simpledialog, messagebox, Menu
import webbrowser  # Para abrir os arquivos

# Inicialize o CustomTkinter com tema escuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Arquivos")
        self.root.geometry("910x600")

        # Inicializa a estrutura de dados para armazenar as seções e arquivos
        self.sections = {}

        # Carrega os dados salvos, se existirem
        self.load_data()

        # Cria os widgets de interface
        self.create_widgets()

    def create_widgets(self):
        # Criando a barra de menus com tkinter.Menu
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menu de temas
        theme_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Temas", menu=theme_menu)

        theme_menu.add_command(label="Tema Claro", command=lambda: self.set_theme("light"))
        theme_menu.add_command(label="Tema Escuro", command=lambda: self.set_theme("dark"))

        # Botão para adicionar uma nova seção
        add_section_button = ctk.CTkButton(self.root, text="+ Nova Seção", command=self.add_section)
        add_section_button.pack(pady=10)

        # Frame para exibir as seções e arquivos
        self.sections_frame = ctk.CTkFrame(self.root)
        self.sections_frame.pack(fill=ctk.BOTH, expand=True)

        self.refresh_sections()

    def set_theme(self, theme_name):
        # Função para alterar o tema
        ctk.set_appearance_mode(theme_name)
        if theme_name == "dark":
            ctk.set_default_color_theme("blue")
        elif theme_name == "light":
            ctk.set_default_color_theme("green")

    def add_section(self):
        # Solicita o nome da nova seção
        section_name = simpledialog.askstring("Nova Seção", "Digite o nome da nova seção:")
        if section_name:
            self.sections[section_name] = []
            self.refresh_sections()

    def add_file_to_section(self, section_name):
        # Abre um diálogo para selecionar múltiplos arquivos
        file_paths = filedialog.askopenfilenames()  # Agora permite selecionar múltiplos arquivos
        for file_path in file_paths:
            if file_path and file_path not in self.sections[section_name]:
                self.sections[section_name].append(file_path)
        self.refresh_sections()

    def open_file(self, file_path):
        # Abre o arquivo no aplicativo padrão
        try:
            webbrowser.open(file_path)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")

    def open_all_files_in_section(self, section_name):
        # Abre todos os arquivos da seção especificada
        for file_path in self.sections[section_name]:
            self.open_file(file_path)

    def remove_file(self, section_name, file_path):
        # Remove um arquivo da seção sem apagar a seção em si
        if file_path in self.sections[section_name]:
            self.sections[section_name].remove(file_path)
        self.refresh_sections()

    def remove_section(self, section_name):
        # Remove a seção e todos os arquivos associados
        if section_name in self.sections:
            del self.sections[section_name]
        self.refresh_sections()

    def rename_section(self, old_name):
        # Solicita um novo nome para a seção
        new_name = simpledialog.askstring("Renomear Seção", "Digite o novo nome da seção:", initialvalue=old_name)
        if new_name and new_name != old_name:
            self.sections[new_name] = self.sections.pop(old_name)
            self.refresh_sections()

    def refresh_sections(self):
        # Atualiza a exibição das seções e arquivos
        for widget in self.sections_frame.winfo_children():
            widget.destroy()

        row = 0  # Define a linha inicial para grid layout

        # Configuração para ajustar a largura das colunas
        self.sections_frame.columnconfigure(0, weight=3)
        self.sections_frame.columnconfigure(1, weight=1)
        self.sections_frame.columnconfigure(2, weight=1)
        self.sections_frame.columnconfigure(3, weight=1)
        self.sections_frame.columnconfigure(4, weight=1)

        for section_name, files in self.sections.items():
            # Adiciona uma linha separadora antes de cada seção (apenas um label com largura)
            separator = ctk.CTkLabel(self.sections_frame, text="", width=400, height=2, fg_color="gray")
            separator.grid(row=row, column=0, columnspan=5, pady=(10, 5))  # linha separadora
            row += 1

            # Mostra o nome da seção com botão para renomear
            section_label = ctk.CTkLabel(self.sections_frame, text=section_name, font=("Arial", 12, "bold"))
            section_label.grid(row=row, column=0, sticky="w", pady=5)

            rename_button = ctk.CTkButton(self.sections_frame, text="Renomear", command=lambda name=section_name: self.rename_section(name))
            rename_button.grid(row=row, column=1, padx=5)

            add_file_button = ctk.CTkButton(self.sections_frame, text="Adicionar Arquivo", command=lambda name=section_name: self.add_file_to_section(name))
            add_file_button.grid(row=row, column=2, padx=5)

            delete_section_button = ctk.CTkButton(self.sections_frame, text="Excluir Seção", command=lambda name=section_name: self.remove_section(name))
            delete_section_button.grid(row=row, column=3, padx=5)

            open_all_button = ctk.CTkButton(
                self.sections_frame, 
                text=f"Abrir todos {section_name}", 
                command=lambda name=section_name: self.open_all_files_in_section(name)
            )
            open_all_button.grid(row=row, column=4, padx=5)

            row += 1  # Move para a próxima linha para os arquivos

            # Lista arquivos na seção
            for file_path in files:
                file_label = ctk.CTkLabel(self.sections_frame, text=file_path, wraplength=400)
                file_label.grid(row=row, column=0, sticky="w", padx=10, pady=2)

                open_button = ctk.CTkButton(self.sections_frame, text="Abrir", command=lambda fp=file_path: self.open_file(fp))
                open_button.grid(row=row, column=1, padx=5)

                remove_button = ctk.CTkButton(self.sections_frame, text="Remover", command=lambda sec=section_name, fp=file_path: self.remove_file(sec, fp))
                remove_button.grid(row=row, column=2, padx=5)

                row += 1  # Próxima linha para o próximo arquivo

        self.save_data()

    def save_data(self):
        # Salva os dados em um arquivo JSON
        with open("file_organizer_data.json", "w") as file:
            json.dump(self.sections, file)

    def load_data(self):
        # Carrega os dados do arquivo JSON
        if os.path.exists("file_organizer_data.json"):
            with open("file_organizer_data.json", "r") as file:
                self.sections = json.load(file)

if __name__ == "__main__":
    root = ctk.CTk()
    app = FileOrganizerApp(root)
    root.mainloop()
