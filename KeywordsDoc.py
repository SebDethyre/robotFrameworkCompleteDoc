import os
import re
import sys
import json
import subprocess
import tkinter as tk
from tkinter import StringVar
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict
import html2text
from AnimatedLabel import AnimatedLabel
## => pip install customtkinter pillow html2text ##
## fc-cache -f -v ##

class KeywordsDoc:
    def __init__(self):
        self.current_cases = []
        self.current_program_path = f"{os.path.dirname(os.path.abspath(__file__))}"
        self.colors = {
                "purple" : "#D1A1E9",
                "orange" : "#FFA500",
                "yellow" : "yellow",
                "green" : "#77FF77",
                # "gray" : "#c6c4c3",
                "red" : "red",
                "dark_orange" : "#aa7218",
                "blue" : "#1F6AA5",
                "blue_sky" : "#6cc9e0",
                "blue_button_pressed" : "#164970",
        }
        self.active_window = None 

        self.breadcrumb_label = None
        self.last_selected_keyword_doc = ""
        self.is_return_context = False
        self.first_open = False
        self.toggle_keyword_doc_lang = None
        self.toggle_keyword_doc_lang_icon = None
        self.keyword_doc_lang = ""
        self.label_keyword_doc_source_icon = None
        self.label_keyword_doc_source_text = None
        self.current_keyword_doc_source_file = ""
        self.keywords_doc_source_frame = None
        self.is_selected_on_entry = False
        self.config_file_path = f"{self.current_program_path}/test_config.txt"
        self.is_venv_path_frame_open = False
        self.selection_direction= ""

        self.venv_path = self.find_value_in_file(self.config_file_path, "venv_path:")
        self.venv_path_str = self.venv_path if self.venv_path else "Renseigner le chemin de l'environnement virtuel"
        self.app_path = self.find_value_in_file(self.config_file_path, "app_path:")
        self.app_chosen = self.find_value_in_file(self.config_file_path, "app_chosen:")
        self.dev_chosen = self.find_value_in_file(self.config_file_path, "dev_chosen:")
        self.test_chosen = self.find_value_in_file(self.config_file_path, "test_chosen:")
        self.test_chosen_index = self.find_value_in_file(self.config_file_path, "tc_index:")
        self.test_path = f"{self.app_path}/{self.app_chosen}/{self.dev_chosen}/tests/{self.test_chosen}"
        parsed_cases = self.parse_robot_file(self.test_path)

        if parsed_cases is None:
            print(f"Erreur : Le fichier {self.test_path} n'a pas pu être traité.")
            self.current_cases = []
        elif not parsed_cases:
            print(f"Aucun cas de test trouvé dans le fichier {self.test_path}.")
            self.current_cases = []
        else:
            self.current_cases = list(parsed_cases.keys())
        # self.current_cases = list(self.parse_robot_file(self.test_path).keys())
        if self.test_path:
            self. write_test_cases_to_file(self.parse_robot_file(self.test_path), f"{self.current_program_path}/current_keywords_naked.txt")
        self.app_path_str = self.app_path if self.app_path else "Renseigner le répertoire des applications"
        self.non_json_dirs = [f"{self.venv_path}/site-packages/openmairie/robotframework", str(self.test_path).rsplit("/", 1)[0]]
        jsons_path =f"{self.current_program_path}/jsons/keywords_"
        json_files = [
            "selenium_fr.json", 
            "builtin_fr.json",
            "collections_fr.json",
            "string_fr.json",
            "operatingsystem_fr.json",
            "datetime_fr.json",
        ]
        self.json_dirs = [f"{jsons_path}{filename}" for filename in json_files]

        self.keywords_images_path = f"{self.current_program_path}/images/"
        self.keyword_doc_source_image = {
            "keyword_local" : f"{self.keywords_images_path}keywords.png",
            "keyword_framework" : f"{self.keywords_images_path}keywords-framework-openmairie.png",
            "selenium" : f"{self.keywords_images_path}selenium.png",
            "robotframework" : f"{self.keywords_images_path}robot-framework-logo.png",
            "collections" : f"{self.keywords_images_path}collections.png",
            "string" : f"{self.keywords_images_path}string.png",
            "operatingsystem" : f"{self.keywords_images_path}operatingsystem.png",
            "datetime" : f"{self.keywords_images_path}datetime.png",
        }
        json_files_begin = "keywords_"
        json_files_ext = "_fr.json"
        self.json_files = {
            f"{json_files_begin}builtin{json_files_ext}" : "BuiltIn",
            f"{json_files_begin}collections{json_files_ext}" : "Collections",
            f"{json_files_begin}string{json_files_ext}" : "String",
            f"{json_files_begin}datetime{json_files_ext}" : "DateTime",
            f"{json_files_begin}operatingsystem{json_files_ext}" : "OperatingSystem",
            f"{json_files_begin}selenium{json_files_ext}" : "Selenium",
        }

        # Attributs pour les différentes fenêtres
        self.main_app_geometry = self.get_window_geometry("main_app")
        self.keywords_doc_list_geometry = self.get_window_geometry("keywords_doc_list")

        self.keywords_doc_list_window = None

        self.is_keywords_doc_list_opened = False
        self.is_keywords_doc_list_output = False
        self.current_keywords_doc_list = []
        self.current_keywords_doc_places_list = []
        self.current_keywords_doc_index = 0
   
        self.current_keyword = ""
        self.keywords_doc_file_path = f"{self.current_program_path}/current_keywords_naked.txt"
        self.listbox_keywords = None
        self.listbox_keywords_save = None
        self.listbox_keywords_doc = None


    def update_pathes(self):
        if self.test_path:
            self. write_test_cases_to_file(self.parse_robot_file(self.test_path), f"{self.current_program_path}/current_keywords_naked.txt")
        self.config_file_path = f"{self.current_program_path}/test_config.txt"
        self.keywords_doc_file_path = f"{self.current_program_path}/current_keywords_naked.txt"

        self.venv_path = self.find_value_in_file(self.config_file_path, "venv_path:")
        self.venv_path_str = self.venv_path if self.venv_path else "Renseigner le chemin de l'environnement virtuel"
        self.app_path = self.find_value_in_file(self.config_file_path, "app_path:")
        self.app_chosen = self.find_value_in_file(self.config_file_path, "app_chosen:")
        self.dev_chosen = self.find_value_in_file(self.config_file_path, "dev_chosen:")
        self.app_path_str = self.app_path if self.app_path else "Renseigner le répertoire des applications"
        self.non_json_dirs = [f"{self.venv_path}/site-packages/openmairie/robotframework", str(self.test_path).rsplit("/", 1)[0]]
        jsons_path =f"{self.current_program_path}/jsons/keywords_"
        json_files = [
            "selenium_fr.json", 
            "builtin_fr.json",
            "collections_fr.json",
            "string_fr.json",
            "operatingsystem_fr.json",
            "datetime_fr.json",
        ]
        self.json_dirs = [f"{jsons_path}{filename}" for filename in json_files]
        self.keywords_images_path = f"{self.current_program_path}/images/"
        self.keyword_doc_source_image = {
            "keyword_local" : f"{self.keywords_images_path}keywords.png",
            "keyword_framework" : f"{self.keywords_images_path}keywords-framework-openmairie.png",
            "selenium" : f"{self.keywords_images_path}selenium.png",
            "robotframework" : f"{self.keywords_images_path}robot-framework-logo.png",
            "collections" : f"{self.keywords_images_path}collections.png",
            "string" : f"{self.keywords_images_path}string.png",
            "operatingsystem" : f"{self.keywords_images_path}operatingsystem.png",
            "datetime" : f"{self.keywords_images_path}datetime.png",
        }
        json_files_begin = "keywords_"
        json_files_ext = "_fr.json"
        self.json_files = {
            f"{json_files_begin}builtin{json_files_ext}" : "BuiltIn",
            f"{json_files_begin}collections{json_files_ext}" : "Collections",
            f"{json_files_begin}string{json_files_ext}" : "String",
            f"{json_files_begin}datetime{json_files_ext}" : "DateTime",
            f"{json_files_begin}operatingsystem{json_files_ext}" : "OperatingSystem",
            f"{json_files_begin}selenium{json_files_ext}" : "Selenium",
        }

    def parse_robot_file(self, file_path):
        """
        Analyse un fichier .robot et extrait les sections `*** Test Cases ***`, 
        puis retourne une map contenant les noms des cas de test comme clés 
        et les mots-clés associés comme valeurs.
        """
        # if not os.path.exists(file_path):
        #     print(f"Erreur : Le fichier {file_path} n'existe pas.")
        #     return
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            return

        test_cases = {}
        current_test = None
        current_content = []

        in_test_case_section = False

        for line in lines:
            if re.match(r'^\*\*\* Test Cases \*\*\*', line):
                in_test_case_section = True
                continue

            if in_test_case_section:
                if re.match(r'^[^\s#].*', line):
                    if current_test:
                        test_cases[current_test] = ''.join(current_content).strip()
                    current_test = line.strip()
                    current_content = []
                elif current_test:
                    current_content.append(line)

        if current_test:
            test_cases[current_test] = ''.join(current_content).strip()

        test_cases_map = {}

        if test_cases:
            for name, content in test_cases.items():
                list_content = content.strip().split("\n")

                list_content_only_keywords = []
                for item in list_content:
                    if any(symbol in item for symbol in ["[", "]", "...", "#", "*"]):
                        continue
                    if item.startswith("    "):
                        if "=  " in item:
                            item = item.split("=  ")[-1].strip()
                        keyword = item.strip().split("  ")[0]
                        list_content_only_keywords.append(keyword)

                unique_ordered_keywords = list(OrderedDict.fromkeys(list_content_only_keywords))
                test_cases_map[name] = unique_ordered_keywords
        return test_cases_map

    def write_test_cases_to_file(self, test_cases_map, output_file_path):
        """
        Écrit les cas de test et leurs mots-clés dans un fichier,
        en respectant le format spécifié.

        :param test_cases_map: Dictionnaire avec les noms des cas de test comme clés et leurs mots-clés comme valeurs.
        :param output_file_path: Chemin du fichier dans lequel écrire.
        """
        try:
            if test_cases_map:
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    for test_case, keywords in test_cases_map.items():
                        file.write(f"{test_case}\n")
                        for keyword in keywords:
                            file.write(f"    {keyword}\n")
                        file.write("\n")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier : {e}")



    def save_window_geometry(self, window_prefix, window):
        if window is not None and window.winfo_exists():
            self.configure(self.config_file_path, f"{window_prefix}_width", window.winfo_width())
            self.configure(self.config_file_path, f"{window_prefix}_height", window.winfo_height())
            self.configure(self.config_file_path, f"{window_prefix}_x", window.winfo_x())
            self.configure(self.config_file_path, f"{window_prefix}_y", window.winfo_y())


    def configure(self, filename, search_str, replace_str):
        with open(filename, 'r+', encoding='utf-8') as f:
            content = f.read()
            # print("Original content:\n", content)

            # Expression régulière améliorée pour gérer des espaces autour du ':'
            pattern = f"{re.escape(search_str)}\\s*:?\\s*.+"
            replacement = f"{search_str}:{replace_str}"
            
            # Debugging
            # print("Pattern:", pattern)
            # print("Replacement:", replacement)

            # Recherche et remplacement
            # match = re.search(pattern, content)
            # if match:
            #     print("Match found:", match.group())
            # else:
            #     print("No match found for pattern")

            new_content = re.sub(pattern, replacement, content)
            # print("Modified content:\n", new_content)

            # Réécriture dans le fichier
            f.seek(0)
            f.write(new_content)
            f.truncate()

    def emoji(self, emoji, size=32):
        font = ImageFont.truetype(f"{self.current_program_path}/seguiemj.ttf", size=int(size/1.5))
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((size/2, size/2), emoji,
                embedded_color=True, font=font, anchor="mm")
        img = CTkImage(img, size=(size, size))
        return img
    
    def image(self, image_path, size=32):
        img = Image.open(image_path).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)
        ctk_img = CTkImage(img, size=(size, size))
        return ctk_img
    
    def update_breadcrumb(self, breadcrumb_text):
        if self.breadcrumb_label is not None:
            self.breadcrumb_label.configure(text=breadcrumb_text)

    def find_value_in_file(self, nom_fichier, valeur):
        with open(nom_fichier, 'r') as fichier:
            for ligne in fichier:
                if valeur in ligne:
                    partie_droite = ligne.split(valeur, 1)[1].strip()
                    if partie_droite != "":
                        return partie_droite
                    else:
                        return ""
        return ""
 
    def get_window_geometry(self, window_prefix):
        """
        Récupère la largeur, hauteur et position (x, y) d'une fenêtre à partir du fichier de configuration.
        :param window_prefix: Préfixe utilisé dans les clés du fichier de configuration (ex: 'main_app')
        :return: Un dictionnaire avec 'width', 'height', 'x', 'y'
        """
        width = self.find_value_in_file(self.config_file_path, f"{window_prefix}_width:")
        height = self.find_value_in_file(self.config_file_path, f"{window_prefix}_height:")
        x = self.find_value_in_file(self.config_file_path, f"{window_prefix}_x:")
        y = self.find_value_in_file(self.config_file_path, f"{window_prefix}_y:")
        return {'width': width, 'height': height, 'x': x, 'y': y}    
    
    def launcher(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.launcher_window = ctk.CTk()
        self.launcher_window.geometry(f"{self.main_app_geometry['width']}x{self.main_app_geometry['height']}+{self.main_app_geometry['x']}+{self.main_app_geometry['y']}")
        self.launcher_window.title("Documentation des Keywords")
        self.launcher_window.attributes('-topmost', True)



        venv_path_frame = ctk.CTkFrame(self.launcher_window, height=0)
        venv_path_frame.pack(fill="x", pady=0)
        venv_path_subframe_1 = ctk.CTkFrame(venv_path_frame, fg_color="transparent")
        venv_path_subframe_1.pack(side="top", pady=0)
        venv_path_subframe_2 = ctk.CTkFrame(venv_path_frame, height=0, fg_color="transparent")
        venv_path_subframe_2.pack(fill="x", side="bottom", pady=0)

        venv_path_label = ctk.CTkLabel(venv_path_subframe_1, text=self.venv_path_str, font=("Arial", 15))
        venv_path_label.pack(side="left", padx=5)

        venv_path_entry_var = tk.StringVar()
        venv_path_entry = ctk.CTkEntry(venv_path_subframe_2, textvariable=venv_path_entry_var, fg_color="#3C3C3C", text_color="white", border_width=2)

        def save_venv_path():
            if venv_path_entry.winfo_ismapped():
                if not venv_path_entry_var.get().lower():
                    venv_path_entry.pack_forget()
                else:
                    self.venv_path = venv_path_entry_var.get().lower()
                    venv_path_label.configure(text=self.venv_path)
                    self.configure(self.config_file_path, 'venv_path', self.venv_path)
                    venv_path_entry.pack_forget()
                venv_path_subframe_2.configure(height=0)
            else:
                venv_path_entry.pack(fill="x", padx=5)
                venv_path_subframe_2.configure(height=30)
        
        if not self.venv_path:
            venv_path_entry.pack(fill="x", padx=5)
        else:
            venv_path_button = ctk.CTkButton(venv_path_subframe_1, width=80, text=None, fg_color="transparent", hover_color="#2B2B2B", image=self.image(f"{self.keywords_images_path}iphone-settings-button.png"), command=save_venv_path)
            venv_path_button.pack(side="right", padx=5)

        def on_key_press_entry(event):
            if event.keysym in ["Left", "BackSpace", "Delete"]:
                venv_path_subframe_2.configure(height=0)
            if event.keysym == "Left":
                if venv_path_entry_var.get() == "":
                    venv_path_button.pack(side="right", padx=5)
                    venv_path_entry.pack_forget()
            if event.keysym == "BackSpace":
                if venv_path_entry_var.get() == "":
                    venv_path_button.pack(side="right", padx=5)
                    venv_path_entry.pack_forget()
            if event.keysym == "Delete":
                if venv_path_entry_var.get() == "":
                    venv_path_button.pack(side="right", padx=5)
                    venv_path_entry.pack_forget()
                    
            if event.keysym == "Return":
                save_venv_path()
        
        venv_path_entry.bind("<Left>", on_key_press_entry)
        venv_path_entry.bind("<BackSpace>", on_key_press_entry)
        venv_path_entry.bind("<Delete>", on_key_press_entry)
        venv_path_entry.bind("<Return>", on_key_press_entry)


        app_path_frame = ctk.CTkFrame(self.launcher_window)
        app_path_frame.pack(fill="x", pady=0)
        app_path_subframe_1 = ctk.CTkFrame(app_path_frame, fg_color="#2B2B2B")
        app_path_subframe_1.pack(side="top", pady=0)
        app_path_subframe_2 = ctk.CTkFrame(app_path_frame, height=0, fg_color="#2B2B2B")
        app_path_subframe_2.pack(fill="x", side="bottom", pady=0)
        
        app_path_label = ctk.CTkLabel(app_path_subframe_1, text=self.app_path_str, font=("Arial", 15))
        app_path_label.pack(side="left", padx=5)

        app_path_entry_var = tk.StringVar()
        app_path_entry = ctk.CTkEntry(app_path_subframe_2, textvariable=app_path_entry_var, fg_color="#3C3C3C", text_color="white", border_width=2)

        def save_app_path():
            if app_path_entry.winfo_ismapped():
                if not app_path_entry_var.get().lower():
                    app_path_entry.pack_forget()
                else:
                    self.app_path = app_path_entry_var.get().lower()
                    app_path_label.configure(text=self.app_path)
                    self.configure(self.config_file_path, 'app_path', self.app_path)
                    app_path_entry.pack_forget()
                app_path_subframe_2.configure(height=0)
            else:
                app_path_entry.pack(fill="x", padx=5)
                app_path_subframe_2.configure(height=30)
        
        if not self.app_path:
            app_path_entry.pack(fill="x", padx=5)
        else:
            app_path_button = ctk.CTkButton(app_path_subframe_1, width=80, text=None, fg_color="transparent", hover_color="#2B2B2B", image=self.image(f"{self.keywords_images_path}iphone-settings-button.png"), command=save_app_path)
            app_path_button.pack(side="right", padx=5)

        def on_key_press_entry(event):
            if event.keysym in ["Left", "BackSpace", "Delete"]:
                # app_path_frame.configure(height=0)
                app_path_subframe_2.configure(height=0)
            if event.keysym == "Left":
                if app_path_entry_var.get() == "":
                    app_path_button.pack(side="right", padx=5)
                    app_path_entry.pack_forget()
            if event.keysym == "BackSpace":
                if app_path_entry_var.get() == "":
                    app_path_button.pack(side="right", padx=5)
                    app_path_entry.pack_forget()
            if event.keysym == "Delete":
                if app_path_entry_var.get() == "":
                    app_path_button.pack(side="right", padx=5)
                    app_path_entry.pack_forget()
                    
            if event.keysym == "Return":
                save_app_path()
        
        app_path_entry.bind("<Left>", on_key_press_entry)
        app_path_entry.bind("<BackSpace>", on_key_press_entry)
        app_path_entry.bind("<Delete>", on_key_press_entry)
        app_path_entry.bind("<Return>", on_key_press_entry)

        # def show_settings():
        #     if not self.is_venv_path_frame_open:
        #         self.is_venv_path_frame_open = True
        #         venv_path_frame.configure(height=60)
        #         venv_path_subframe_1.configure(height=30)
        #         venv_path_subframe_2.configure(height=30)
        #     else:
        #         self.is_venv_path_frame_open = False
        #         venv_path_frame.configure(height=0)
        #         venv_path_subframe_1.configure(height=0)
        #         venv_path_subframe_2.configure(height=0)
        # config_button = ctk.CTkButton(self.launcher_window, width=40, corner_radius=30,text=None, fg_color="transparent", hover_color="#2B2B2B", image=self.image(f"{self.keywords_images_path}iphone-settings-button.png", 32), command=show_settings)
        # config_button.pack(side="top", padx=5)
        
        def get_directories(path):
            try:
                return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
            except FileNotFoundError:
                return []
            
        def get_files(path):
            """
            Retourne une liste des fichiers dans le répertoire spécifié.
            
            :param path: Chemin du répertoire à analyser.
            :return: Liste des fichiers dans le répertoire, ou une liste vide si le chemin n'existe pas.
            """
            try:
                return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            except FileNotFoundError:
                return []
            
        def update_menu():
            path = app_path_entry.get()
            directories = get_directories(path)
            if directories:
                app_directory_dropdown.configure(values=directories)
                app_directory_dropdown.set(directories[0])
            else:
                app_directory_dropdown.configure(values=["Aucun répertoire trouvé"])
                app_directory_dropdown.set("Aucun répertoire trouvé")

        def on_app_chosen_selection_change(value):
            self.configure(self.config_file_path, 'app_chosen', value)
            self.app_chosen = value
            dev_dropdown.delete(0, "end")
            test_dropdown.delete(0, "end")
            devs = get_directories(f"{self.app_path}/{value}")
            if devs:
                for dev in devs:
                    dev_dropdown.insert(tk.END, dev)

        # ctk.CTkLabel(self.launcher_window, text="Sélectionnez une application :").pack(pady=10)
        app_directory_dropdown = ctk.CTkComboBox(self.launcher_window, values=[self.app_chosen], width=300, font=("Arial", 15), command=on_app_chosen_selection_change )
        app_directory_dropdown.pack(pady=5)

        directories = get_directories(self.app_path)
        if directories:
            app_directory_dropdown.configure(values=directories) 


        def on_dev_chosen_selection_change(event):
            selected_index = dev_dropdown.curselection()
            # focused_index = dev_dropdown.index("active")
            # # Sélectionne cet élément dans la Listbox
            # if not selected_index:
            #     dev_dropdown.selection_clear(0, "end")  # Nettoie les anciennes sélections
            #     dev_dropdown.selection_set(focused_index) 
            if selected_index:
                value = dev_dropdown.get(selected_index)
                self.configure(self.config_file_path, 'dev_chosen', value)
                self.dev_chosen = value

                test_dir = f"{self.app_path}/{self.app_chosen}/{value}/tests"
                test_files = get_robot_files(test_dir)

                test_dropdown.delete(0, "end")

                if test_files:
                    for item in test_files:
                        test_dropdown.insert(tk.END, item)

        # ctk.CTkLabel(self.launcher_window, text="Sélectionnez un dev :").pack(pady=10)
        
        dev_frame = ctk.CTkFrame(self.launcher_window)
        dev_frame.pack(pady=5,fill=tk.BOTH, expand=True)

        dev_dropdown = tk.Listbox(dev_frame, width=50, height=10, selectmode=tk.SINGLE, bg="#2B2B2B", fg="white", font=("Arial", 12))
        dev_dropdown.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=70)
        # index = self.test_chosen_index[0] if isinstance(self.test_chosen_index, tuple) else self.test_chosen_index
        dev_dropdown.select_set(self.test_chosen_index)

        dev_scrollbar = tk.Scrollbar(dev_frame, orient="vertical")
        dev_scrollbar.pack(side=tk.RIGHT, fill="y")

        dev_dropdown.config(yscrollcommand=dev_scrollbar.set)
        dev_scrollbar.config(command=dev_dropdown.yview)

        devs = get_directories(f"{self.app_path}/{self.app_chosen}")
        if devs:
            for dev in devs:
                dev_dropdown.insert(tk.END, dev)

        # def on_return_press_dev(event):
        #        # Seule la sélection doit être déclenchée lors de la touche Entrée, pas d'activation multiple
        #     selected_index = dev_dropdown.curselection()
        #     if not selected_index:
        #         return
        #     on_dev_chosen_selection_change(event)

        # dev_dropdown.bind("<Return>", on_return_press_dev)
        # dev_dropdown.bind("<Up>", on_return_press_dev)
        # dev_dropdown.bind("<Down>", on_return_press_dev)
        dev_dropdown.bind("<<ListboxSelect>>", on_dev_chosen_selection_change)

        def on_test_chosen_selection_change(event):
            selected_index = test_dropdown.curselection()
            # print(selected_index)
            # Sélectionne cet élément dans la Listbox
            focused_index = test_dropdown.index("active")
            if not selected_index:
                test_dropdown.selection_clear(0, "end")  # Nettoie les anciennes sélections
                test_dropdown.selection_set(focused_index)
                return  # Sélectionne l'élément actuellement en focus
            # if selected_index:
            #     test_dropdown.selection_clear(0, "end")  # Nettoie les anciennes sélections
            #     test_dropdown.selection_set(selected_index)
                # return  # Sélectionne l'élément actuellement en focus
            if self.selection_direction == "up":
                if selected_index[0] > 0: 
                    selected_index = (selected_index[0] - 1,)
            if self.selection_direction == "down":
                if selected_index[0] < test_dropdown.size() - 1:
                    selected_index = (selected_index[0] + 1,)
            #     selected_index = selected_index + 1
            # Déclenche l'événement de sélection pour appliquer les modifications
            # test_dropdown.event_generate("<<ListboxSelect>>")
            if selected_index:
                value = test_dropdown.get(selected_index)
                self.configure(self.config_file_path, 'tc_index', selected_index[0])
                self.configure(self.config_file_path, 'test_chosen', value)
                self.test_chosen = value
                self.test_path = f"{self.app_path}/{self.app_chosen}/{self.dev_chosen}/tests/{value}"
                self.current_cases = list(self.parse_robot_file(self.test_path).keys())
                self.update_pathes()
                if self.keywords_doc_list_window and self.keywords_doc_list_window.winfo_exists(): 
                    update_keywords_doc_content()
                    # self.keywords_doc_list_window.focus_set()

        # def on_test_chosen_selection_change_direct(event):
        #     selected_index = test_dropdown.curselection()
        #     # # print(selected_index)
        #     # # Sélectionne cet élément dans la Listbox
        #     # focused_index = test_dropdown.index("active")
        #     # if not selected_index:
        #     #     test_dropdown.selection_clear(0, "end")  # Nettoie les anciennes sélections
        #     #     test_dropdown.selection_set(focused_index)
        #     #     return  # Sélectionne l'élément actuellement en focus
        #     # # if selected_index:
        #     # #     test_dropdown.selection_clear(0, "end")  # Nettoie les anciennes sélections
        #     # #     test_dropdown.selection_set(selected_index)
        #     #     # return  # Sélectionne l'élément actuellement en focus
        #     # if self.selection_direction == "up":
        #     #     if selected_index[0] > 0: 
        #     #         selected_index = (selected_index[0] - 1,)
        #     # if self.selection_direction == "down":
        #     #     if selected_index[0] < test_dropdown.size() - 1:
        #     #         selected_index = (selected_index[0] + 1,)
        #     #     selected_index = selected_index + 1
        #     # Déclenche l'événement de sélection pour appliquer les modifications
        #     # test_dropdown.event_generate("<<ListboxSelect>>")
        #     if selected_index:
        #         value = test_dropdown.get(selected_index)
        #         self.configure(self.config_file_path, 'tc_index', selected_index[0])
        #         self.configure(self.config_file_path, 'test_chosen', value)
        #         self.test_chosen = value
        #         self.test_path = f"{self.app_path}/{self.app_chosen}/{self.dev_chosen}/tests/{value}"
        #         self.current_cases = list(self.parse_robot_file(self.test_path).keys())
        #         self.update_pathes()
        #         if self.keywords_doc_list_window and self.keywords_doc_list_window.winfo_exists(): 
        #             update_keywords_doc_content()
                    # self.keywords_doc_list_window.focus_set()  
        def on_test_chosen_selection_change_direct(event):
            """
            Sélection directe via un clic.
            """
            # selected_index = test_dropdown.curselection()
            # # self.selection_direction = "neutral"
            # if selected_index:
                
            on_test_chosen_selection_change(event)

        frame = ctk.CTkFrame(self.launcher_window)
        frame.pack(pady=5,fill=tk.BOTH, expand=True)

        test_dropdown = tk.Listbox(frame, width=50, selectmode=tk.SINGLE, bg="#2B2B2B", fg="white", font=("Arial", 12))
        test_dropdown.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=70)

        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill="y")

        test_dropdown.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=test_dropdown.yview)

        def get_robot_files(directory):
            try:
                robot_files = sorted([f for f in os.listdir(directory) if f.endswith('.robot')])
                if not robot_files:
                    print(f"Aucun fichier .robot trouvé dans le répertoire : {directory}")
                return robot_files
            except FileNotFoundError as e:
                print(f"Le répertoire spécifié n'est pas un dev.")
                return []
            except Exception as e:
                print(f"Une erreur inattendue s'est produite : {e}")
                return []

        test_dir = f"{self.app_path}/{self.app_chosen}/{self.dev_chosen}/tests"
        test_files = get_robot_files(test_dir)

        if test_files:
            for item in test_files:
                test_dropdown.insert(tk.END, item)

        # def on_key_press_entry(event):
            # if event.keysym == "Left":
            #     if test_dropdown.get() == "":
            #         self.listbox_keywords = self.listbox_keywords_save
            #         update_keywords_doc_content()
            #         self.listbox_keywords_doc.focus_set()
            # if event.keysym == "BackSpace":
            #     if test_dropdown.get() == "":
            #         self.listbox_keywords = self.listbox_keywords_save
            #         update_keywords_doc_content()
            #         self.listbox_keywords_doc.focus_set()
            # if event.keysym == "Delete":
            #     if test_dropdown.get() == "":
            #         self.listbox_keywords = self.listbox_keywords_save
            #         update_keywords_doc_content()
            #         self.listbox_keywords_doc.focus_set()
                    
            # if event.keysym == "Return":
            #     # update_listbox()
            #     self.listbox_keywords_doc.focus_set()

        def on_return_press_test(event):
            if event.keysym == "Up":
                self.selection_direction = "up"
            elif event.keysym == "Down":
                self.selection_direction = "down"
            else:
                self.selection_direction = "neutral"

               # Seule la sélection doit être déclenchée lors de la touche Entrée, pas d'activation multiple
            selected_index = test_dropdown.curselection()
            if not selected_index:
                return
            on_test_chosen_selection_change(event)
            # return "break"
        

        # Lier l'événement clic simple au déclencheur de double-clic
        test_dropdown.bind("<Button-1>", on_test_chosen_selection_change_direct)
        # test_dropdown.bind("<Return>", on_return_press_test)
        test_dropdown.bind("<Return>", on_test_chosen_selection_change)
        test_dropdown.bind("<Up>", on_return_press_test)
        test_dropdown.bind("<Down>", on_return_press_test)
        test_dropdown.bind("<<ListboxSelect>>", on_test_chosen_selection_change)

        # def on_mouse_click(event):
        #         index = self.listbox_keywords_doc.nearest(event.y)
        #         self.listbox_keywords_doc.selection_clear(0, "end")
        #         self.listbox_keywords_doc.selection_set(index)
        #         self.listbox_keywords_doc.activate(index) 
        #         if event.num == 1:  # Clic g
        #             on_select(event)
        #         elif event.num == 3:  # Clic d
        #             return_keywords_doc()
            
        # test_dropdown.bind("<Button-1>", on_return_press_test)
        # test_dropdown.bind("<Return>", on_test_chosen_selection_change)

# Bind les événements de navigation au clavier (flèches haut/bas) pour forcer la mise à jour
        # test_dropdown.bind("<Up>", on_test_chosen_selection_change)
        # test_dropdown.bind("<Down>", on_test_chosen_selection_change)

        def on_window_configure(event):
            self.save_window_geometry("main_app", self.launcher_window)

        self.launcher_window.bind("<Configure>", on_window_configure)
    
        def extract_blocks_from_directories(string_to_find, dirs, json_dirs):
            """
            Cherche une string seule sur une ligne dans les fichiers de deux répertoires,
            puis renvoie tout le texte en dessous jusqu'à une autre string similaire.
            Cherche également dans un fichier JSON si la chaîne correspond à une clé name.

            Args:
                string_to_find (str): La chaîne de caractères à rechercher.
                dirs (list[str]): Liste des chemins des répertoires à scanner.
                json_dirs (list[str]): Liste des chemins des fichiers JSON.

            Returns:
                dict: Une clé par fichier ou JSON avec le texte trouvé en tant que valeur.
            """
            result = {}

            def is_binary(file_path):
                """Vérifie si un fichier est binaire."""
                try:
                    with open(file_path, 'rb') as file:
                        chunk = file.read(1024)
                        if b'\0' in chunk:
                            return True
                except Exception as e:
                    print(f"Erreur lors de la vérification binaire : {e}")
                    return True
                return False
            
            def is_pdf(file_path):
                """Vérifie si un fichier est un PDF."""
                try:
                    if not os.path.isfile(file_path):
                        print(f"Le fichier {file_path} n'existe pas.")
                        return False  # Si le fichier n'existe pas, il n'est pas un PDF

                    with open(file_path, 'rb') as file:
                        # Lire les 4 premiers octets pour détecter la signature PDF
                        header = file.read(4)
                        if header == b'%PDF':
                            return True
                except Exception as e:
                    print(f"Erreur lors de la vérification du PDF : {e}")
                    return False
                return False
            
            def process_file(file_path):
                """Traite un fichier texte pour extraire des blocs."""
                blocks = []
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        inside_block = False
                        current_block = []

                        for line in file:
                            if re.match(f"^{re.escape(string_to_find)}$", line):
                                if inside_block:
                                    blocks.append("".join(current_block).replace("\n\n", "\n"))
                                    current_block = []
                                inside_block = True
                            elif inside_block and re.match("^\\S+", line):
                                blocks.append("".join(current_block).replace("\n\n", "\n"))
                                current_block = []
                                inside_block = False
                            elif inside_block:
                                current_block.append(line)
                            blocks = [line.replace("\n\n", "\n") for line in blocks]
                        if current_block:
                            blocks.append("".join(current_block).replace("\n\n", "\n"))
                except Exception as e:
                    print(f"Erreur lors du traitement de {file_path}: {e}")
                return blocks

            def grep_files(string_to_find, directory):
                """Utilise grep pour trouver les fichiers contenant une chaîne spécifique."""
                try:
                    grep_result = subprocess.run(
                        ["grep", "-ril", string_to_find, directory],
                        text=True,
                        capture_output=True
                    )
                    if grep_result.returncode == 0:
                        return grep_result.stdout.strip().split("\n")
                    return []
                except Exception as e:
                    print(f"Erreur lors de l'exécution de grep : {e}")
                    return []

            def process_json(json_path):
                """Traite un fichier JSON pour formater les blocs associés."""
                try:
                    converter = html2text.HTML2Text()
                    converter.ignore_links = False
                    converter.ignore_images = True
                    converter.ignore_emphasis = False

                    with open(json_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    json_blocks = {}
                    for entry in data:
                        if isinstance(entry, dict) and entry.get("name", "").lower() == string_to_find.lower():
                            args = "\n".join([f"  - {arg['repr']}" for arg in entry.get("args", [])])

                            doc = entry.get("doc", "")
                            doc_html_converted = converter.handle(doc).splitlines() if doc else []                          
                            doc_html_converted = [line.replace("|", "") for line in doc_html_converted]
                            doc_html_converted_formatted = "\n".join(doc_html_converted)
                            doc_fr = str(entry.get("doc_fr", "")).replace("|", "")

                            if self.keyword_doc_lang.get() == "en":
                                block = f"{entry['name']}\n\n{args}\n\n{doc_html_converted_formatted}"
                            elif self.keyword_doc_lang.get() == "fr":
                                block = f"{entry['name']}\n\n{args}\n\n{doc_fr}"
                            else:
                                block = f"{entry['name']}\n\n{args}\n\n{doc_html_converted_formatted}"

                            json_blocks[f"{json_path}::{entry['name']}"] = block

                    return json_blocks
                except Exception as e:
                    print(f"Erreur lors du traitement du fichier JSON {json_path}: {e}")
                    return {}

            # Recherche dans les répertoires avec grep
            for directory in dirs:
                if os.path.exists(directory):
                    matched_files = grep_files(string_to_find, directory)
                    for file_path in matched_files:
                        if not is_binary(file_path) and not is_pdf(file_path):
                            file_blocks = process_file(file_path)
                            if file_blocks:
                                result[file_path] = file_blocks

            # Traitement des fichiers JSON
            for json_dir in json_dirs:
                if os.path.exists(json_dir):
                    json_results = process_json(json_dir)
                    result.update(json_results)

            return result

        def extract_entries_from_directories(string_to_find, dirs, json_dirs):
            """
            Recherche une chaîne dans des fichiers texte et JSON dans des répertoires donnés.

            Args:
                string_to_find (str): La chaîne à rechercher.
                dirs (list): Liste des répertoires à explorer pour les fichiers texte.
                json_dirs (list): Liste des répertoires contenant des fichiers JSON.

            Returns:
                list: Liste unique des lignes ou blocs contenant la chaîne recherchée, triée par ordre alphabétique.
            """
            result = set()

            def is_binary(file_path):
                """Vérifie si un fichier est binaire."""
                try:
                    with open(file_path, 'rb') as file:
                        chunk = file.read(1024)
                        return b'\0' in chunk
                except Exception as e:
                    print(f"Erreur lors de la vérification binaire : {e}")
                    return True
                
            def is_pdf(file_path):
                """Vérifie si un fichier est un PDF."""
                try:
                    if not os.path.isfile(file_path):
                        print(f"Le fichier {file_path} n'existe pas.")
                        return False

                    with open(file_path, 'rb') as file:
                        # Lire les 4 premiers octets pour détecter la signature PDF
                        header = file.read(4)
                        if header == b'%PDF':
                            return True
                except Exception as e:
                    print(f"Erreur lors de la vérification du PDF : {e}")
                    return False
                return False
            
            def process_file(file_path):
                """Recherche les lignes contenant la chaîne dans un fichier texte."""
                matches = set()
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            line = line.split("  ")[0]
                            if string_to_find.lower() in line.lower() and '#' not in line:
                                matches.add(line.strip())
                    return matches
                except Exception as e:
                    print(f"Erreur lors du traitement de {file_path}: {e}")
                    return set()

            def grep_files(string_to_find, directory):
                """Utilise grep pour trouver les fichiers contenant la chaîne."""
                try:
                    grep_result = subprocess.run(
                        ["grep", "-ril", string_to_find, directory],
                        text=True,
                        capture_output=True
                    )
                    files = grep_result.stdout.strip().split("\n") if grep_result.returncode == 0 else []
                    return [file for file in files if file.endswith(".robot")]
                except Exception as e:
                    print(f"Erreur lors de l'exécution de grep : {e}")
                    return []

            def process_json(json_path):
                """Recherche les blocs contenant la chaîne dans un fichier JSON."""
                matches = set()
                try:
                    with open(json_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    for entry in data:
                        if isinstance(entry, dict) and string_to_find.lower() in entry.get("name", "").lower():
                            matches.add(entry.get("name", ""))
                    return matches
                except Exception as e:
                    print(f"Erreur lors du traitement du fichier JSON {json_path}: {e}")
                    return set()

            for directory in dirs:
                if os.path.exists(directory):
                    matched_files = grep_files(string_to_find, directory)
                    for file_path in matched_files:
                        if not is_binary(file_path) and not is_pdf(file_path):
                            result.update(process_file(file_path))

            for json_dir in json_dirs:
                if os.path.exists(json_dir):
                    if os.path.isfile(json_dir) and json_dir.endswith('.json'):
                        # Si c'est un fichier JSON, le traiter directement
                        result.update(process_json(json_dir))
                    elif os.path.isdir(json_dir):
                        # Si c'est un répertoire, traiter tous les fichiers JSON à l'intérieur
                        for json_file in os.listdir(json_dir):
                            json_path = os.path.join(json_dir, json_file)
                            if os.path.isfile(json_path) and json_path.endswith('.json'):
                                result.update(process_json(json_path))
            return sorted(result)

        def return_keywords_doc():
            self.last_selected_keyword_doc = ""
            self.current_keywords_doc_index -= 1
            if self.current_keywords_doc_index <= 0: self.current_keywords_doc_index =0
            if self.current_keywords_doc_index == 0:
                self.current_keyword_doc_source_file = ""
                self.is_keywords_doc_list_opened = False
                self.save_window_geometry("keywords_doc_list", self.keywords_doc_list_window)
                self.is_keywords_doc_list_output = False
                if self.current_keywords_doc_list: self.current_keywords_doc_list.pop()
                open_keywords_doc(update=True)
                if self.current_keywords_doc_places_list: current_word_place = self.current_keywords_doc_places_list[0]
                else: current_word_place = 0
                self.listbox_keywords_doc.selection_clear(0, "end")
                self.listbox_keywords_doc.selection_set(current_word_place)
                self.listbox_keywords_doc.activate(current_word_place)
                self.listbox_keywords_doc.see(current_word_place)
                if self.current_keywords_doc_places_list: self.current_keywords_doc_places_list.pop()
                keywords = ""
                for keyword in self.current_keywords_doc_list:
                    keywords += f" ⮕ {keyword}"
                test_name = str(self.test_path).split("/")[-1][:-6].replace("_", " ")
                breadcrumb_text = ""
                breadcrumb_text_str = f"{test_name}{keywords}"
                if len(breadcrumb_text_str) > 100:
                    keywords_doc_list_last_elements = " ⮕ ".join(self.current_keywords_doc_list[-3:])
                    breadcrumb_text = f"... {keywords_doc_list_last_elements}"
                else: 
                    breadcrumb_text = breadcrumb_text_str
                self.update_breadcrumb(breadcrumb_text)
                self.label_keyword_doc_source_icon.configure(image=self.emoji("", 42))
                if self.label_keyword_doc_source_text: self.label_keyword_doc_source_text.configure(text="")
                self.keywords_doc_source_frame.configure(width=0)
                return
            current_word = self.current_keywords_doc_list[self.current_keywords_doc_index -1]

            self.current_keywords_doc_list.pop()
            keywords = ""
            for keyword in self.current_keywords_doc_list:
                keywords += f" ⮕ {keyword}"
            test_name = str(self.test_path).split("/")[-1][:-6].replace("_", " ")
            breadcrumb_text = ""
            breadcrumb_text_str = f"{test_name}{keywords}"

            if len(breadcrumb_text_str) > 100:
                keywords_doc_list_last_elements = " ⮕ ".join(self.current_keywords_doc_list[-3:])
                breadcrumb_text = f"... {keywords_doc_list_last_elements}"
            else: 
                breadcrumb_text = breadcrumb_text_str
            self.update_breadcrumb(breadcrumb_text)

            blocks = extract_blocks_from_directories(current_word, self.non_json_dirs, self.json_dirs)
            output_file_path = f"{self.current_program_path}/blocks_output.txt"

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for source_file, value in blocks.items():
                    if "::" in source_file:
                        json_source, json_key = source_file.split("::", 1)
                        self.current_keyword_doc_source_file = json_source
                        source = self.current_keyword_doc_source_file.split("/")[-1]
                        output_file.write(f"{value}\n")
                        json_source_short = str(json_source).split("/")[-1]
                        self.label_keyword_doc_source_text.configure(text=self.json_files[json_source_short])
                        self.label_keyword_doc_source_text.pack(side="right", padx=15)
                        recalculated_width = len(self.json_files[json_source_short]) * 9 + 110
                        self.keywords_doc_source_frame.configure(width=recalculated_width)
                        source_file_str = json_source
                    elif isinstance(value, list):
                        for block in value:
                            self.current_keyword_doc_source_file = source_file
                            source_file_short = str(source_file).split("/")[-1]
                            source_file_short = source_file_short.split(".")[0]
                            output_file.write(f"{current_word}\n\n")
                            output_file.write(f"{block}\n")
                            self.label_keyword_doc_source_text.configure(text=source_file_short)
                            self.label_keyword_doc_source_text.pack(side="right", padx=15)
                            recalculated_width = len(source_file_short)  * 9 + 100
                            self.keywords_doc_source_frame.configure(width=recalculated_width)
                            source_file_str = source_file
                    else:
                        output_file.write(f"{value}\n")

                    if source_file_str:
                        image_label_keyword_doc = "" 
                        if "openmairie/robotframework" in source_file_str:
                            image_label_keyword_doc = "keyword_framework" 
                        elif "tests" in source_file_str:
                            image_label_keyword_doc = "keyword_local" 
                        elif "selenium" in source_file_str:
                            image_label_keyword_doc = "selenium"
                        elif "collections" in source_file_str:
                            image_label_keyword_doc = "collections"
                        elif "operatingsystem" in source_file_str:
                            image_label_keyword_doc = "operatingsystem"
                        elif "datetime" in source_file_str:
                            image_label_keyword_doc = "datetime"
                        elif "string" in source_file_str:
                            image_label_keyword_doc = "string"
                        elif "json" in source_file_str:
                            image_label_keyword_doc = "robotframework"
                        else:
                            image_label_keyword_doc = ""

                        if image_label_keyword_doc != "":
                            self.label_keyword_doc_source_icon.configure(image=self.image(self.keyword_doc_source_image.get(image_label_keyword_doc), 42))
                        else: 
                            self.label_keyword_doc_source_icon.configure(image=self.emoji("", 42))
                            if self.label_keyword_doc_source_text: self.label_keyword_doc_source_text.configure(text="")
                            self.keywords_doc_source_frame.configure(width=0)
                        self.label_keyword_doc_source_icon.pack(side="left", padx=15)
            self.is_keywords_doc_list_opened = False
            self.save_window_geometry("keywords_doc_list", self.keywords_doc_list_window)
            self.is_keywords_doc_list_output = True
            open_keywords_doc(update=True)
            
            if self.current_keywords_doc_places_list: current_word_place = self.current_keywords_doc_places_list[self.current_keywords_doc_index]
            else: current_word_place = 0
            self.listbox_keywords_doc.selection_clear(0, "end")
            self.listbox_keywords_doc.selection_set(current_word_place)
            self.listbox_keywords_doc.activate(current_word_place)
            self.listbox_keywords_doc.see(current_word_place) 
            self.current_keywords_doc_places_list.pop()
        
        # def apply_coloring_to_listbox(listbox, lines, patterns, keyword_pattern):
        #     """
        #     appique des couleurs spécifiques aux éléments de la Listbox en fonction des patterns.
        #     """
        #     listbox.delete(0, "end")
        #     for line in lines:
        #         line_content = line.strip()
        #         listbox.insert("end", line_content)
        #         if keyword_pattern and re.match(keyword_pattern, line_content):
        #             index = listbox.size() - 1
        #             listbox.itemconfig(index, {'bg': "#2B2B2B", 'fg': self.colors["purple"]})
        #         for pattern, color in patterns:
        #             print(pattern, line_content)
        #             if re.search(pattern, line_content):
        #                 print("match")
        #                 index = listbox.size() - 1
        #                 listbox.itemconfig(index, {'bg': "#2B2B2B", 'fg': color})
        #                 break
                    
        # def apply_coloring_to_listbox(listbox, lines, patterns, keyword_pattern, patterns_only_word = None):
        #     """
        #     Applique des couleurs spécifiques aux éléments de la Listbox en fonction des patterns.
        #     Certains patterns ne colorent que le mot correspondant.
        #     """
        #     listbox.delete(0, "end")
        #     for line in lines:
        #         line_content = line.strip()
        #         listbox.insert("end", line_content)
        #         index = listbox.size() - 1

        #         # Applique la couleur pour le keyword_pattern
        #         if keyword_pattern and re.match(keyword_pattern, line_content):
        #             listbox.itemconfig(index, {'bg': "#2B2B2B", 'fg': self.colors["purple"]})

        #         # Applique les couleurs pour les patterns généraux
        #         for pattern, color in patterns:
        #             if re.search(pattern, line_content):
        #                 listbox.itemconfig(index, {'bg': "#2B2B2B", 'fg': color})
        #                 break

        #         # Applique les couleurs uniquement pour certains mots
        #         if patterns_only_word:
        #             modified_line =""
        #             if patterns_only_word:
        #                 for pattern, color in patterns_only_word:
        #                     matches = re.finditer(pattern, line)
        #                     for match in matches:
        #                         word = match.group(0)
        #                         # Entoure le mot par des caractères visuellement distinctifs
        #                         highlighted_word = f"({word})"
        #                         modified_line = modified_line.replace(word, highlighted_word)
        #                 listbox.insert(tk.END, modified_line)
        #                 listbox.itemconfig(listbox.size() - 1, {'bg': "#1E1E1E", 'fg': "white"})
        
        def apply_coloring_to_listbox(listbox, lines, patterns, keyword_pattern, patterns_only_word=None, patterns_only_word_image_map=None):
            """
            Applique des couleurs spécifiques aux éléments de la Listbox en fonction des patterns.
            Certains patterns ne colorent que le mot correspondant.
            """
            listbox.delete(0, "end")
            for line in lines:
                line_content = line.strip()
                modified_line = line_content  # Ligne modifiable pour ajouter les highlights
                should_highlight_line = False  # Indicateur pour éviter d'insérer deux fois

                # Applique la couleur pour le keyword_pattern
                if keyword_pattern and re.match(keyword_pattern, line_content):
                    listbox.insert("end", line_content)
                    index = listbox.size() - 1
                    listbox.itemconfig(index, {'bg': "#2B2B2B", 'fg': self.colors["purple"]})
                    should_highlight_line = True

                # Applique les couleurs pour les patterns généraux
                if not should_highlight_line:
                    for pattern, color in patterns:
                        if re.search(pattern, line_content):
                            listbox.insert("end", line_content)
                            index = listbox.size() - 1
                            listbox.itemconfig(index, {'bg': "#2B2B2B", 'fg': color})
                            should_highlight_line = True
                            break

                # Applique les couleurs uniquement pour certains mots
                if patterns_only_word and not should_highlight_line:
                    for pattern, color, emoticon in patterns_only_word:
                        matches = re.finditer(pattern, line_content)
                        for match in matches:
                            word = match.group(0)
                            highlighted_word = f"*{word}*"  # Simule le surlignage
                            # modified_line = modified_line.replace(word, highlighted_word)
                            modified_line = f"{modified_line}  {emoticon}"
                    # Ajoute la ligne modifiée si elle a été altérée
                    if modified_line != line_content:
                        listbox.insert("end", modified_line)
                        index = listbox.size() - 1
                        # listbox.itemconfig(index, {'bg': "#1E1E1E", 'fg': "white"})
                    else:
                        # Si aucun mot n'a été surligné, insère la ligne originale
                        listbox.insert("end", line_content)


        
        def update_keywords_doc_content():
            
            if self.current_keywords_doc_index <= 0: self.current_keywords_doc_index =0
            if self.current_keywords_doc_index == 0:
                self.current_keyword_doc_source_file = ""
                self.is_keywords_doc_list_opened = False
                self.save_window_geometry("keywords_doc_list", self.keywords_doc_list_window)
                self.is_keywords_doc_list_output = False
                if self.current_keywords_doc_list: self.current_keywords_doc_list.pop()
                open_keywords_doc(update=True)
                if self.current_keywords_doc_places_list: current_word_place = self.current_keywords_doc_places_list[0]
                else: current_word_place = 0
                if self.listbox_keywords_doc:
                    self.listbox_keywords_doc.selection_clear(0, "end")
                    self.listbox_keywords_doc.selection_set(current_word_place)
                    self.listbox_keywords_doc.activate(current_word_place)
                    self.listbox_keywords_doc.see(current_word_place)
                if self.current_keywords_doc_places_list: self.current_keywords_doc_places_list.pop()
                keywords = ""
                for keyword in self.current_keywords_doc_list:
                    keywords += f" ⮕ {keyword}"
                test_name = str(self.test_path).split("/")[-1][:-6].replace("_", " ")
                breadcrumb_text = ""
                breadcrumb_text_str = f"{test_name}{keywords}"
                if len(breadcrumb_text_str) > 100:
                    keywords_doc_list_last_elements = " ⮕ ".join(self.current_keywords_doc_list[-3:])
                    breadcrumb_text = f"... {keywords_doc_list_last_elements}"
                else: 
                    breadcrumb_text = breadcrumb_text_str
                self.update_breadcrumb(breadcrumb_text)
                return
            if self.current_keywords_doc_index > 0:
                current_word = self.current_keywords_doc_list[self.current_keywords_doc_index - 1]
                keywords = ""
                for keyword in self.current_keywords_doc_list:
                    keywords += f" ⮕ {keyword}"
                test_name = str(self.test_path).split("/")[-1][:-6].replace("_", " ")
                breadcrumb_text = ""
                breadcrumb_text_str = f"{test_name}{keywords}"
                if len(breadcrumb_text_str) > 100:
                    keywords_doc_list_last_elements = " ⮕ ".join(self.current_keywords_doc_list[-3:])
                    breadcrumb_text = f"... {keywords_doc_list_last_elements}"
                else: 
                    breadcrumb_text = breadcrumb_text_str
                self.update_breadcrumb(breadcrumb_text)

                blocks = extract_blocks_from_directories(current_word, self.non_json_dirs, self.json_dirs)
                output_file_path = f"{self.current_program_path}/blocks_output.txt"

                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for source_file, value in blocks.items():
                        if "::" in source_file:
                            json_source, json_key = source_file.split("::", 1)
                            self.current_keyword_doc_source_file = json_source
                            source = self.current_keyword_doc_source_file.split("/")[-1]
                            output_file.write(f"{value}\n")
                            json_source_short = str(json_source).split("/")[-1]
                            self.label_keyword_doc_source_text.configure(text=self.json_files[json_source_short])
                            self.label_keyword_doc_source_text.pack(side="right", padx=15)
                            recalculated_width = len(self.json_files[json_source_short]) * 9 + 110
                            self.keywords_doc_source_frame.configure(width=recalculated_width)
                            source_file_str = json_source
                        elif isinstance(value, list):
                            for block in value:
                                self.current_keyword_doc_source_file = source_file
                                source_file_short = str(source_file).split("/")[-1]
                                source_file_short = source_file_short.split(".")[0]
                                output_file.write(f"{current_word}\n\n")
                                output_file.write(f"{block}\n")
                                self.label_keyword_doc_source_text.configure(text=source_file_short)
                                self.label_keyword_doc_source_text.pack(side="right", padx=15)
                                recalculated_width = len(source_file_short) * 9 + 100
                                self.keywords_doc_source_frame.configure(width=recalculated_width)
                                source_file_str = source_file
                        else:
                            output_file.write(f"{value}\n")

                        if source_file_str:
                            image_label_keyword_doc = "" 
                            if "openmairie/robotframework" in source_file_str:
                                image_label_keyword_doc = "keyword_framework" 
                            elif "tests" in source_file_str:
                                image_label_keyword_doc = "keyword_local" 
                            elif "selenium" in source_file_str:
                                image_label_keyword_doc = "selenium"
                            elif "collections" in source_file_str:
                                image_label_keyword_doc = "collections"
                            elif "operatingsystem" in source_file_str:
                                image_label_keyword_doc = "operatingsystem"
                            elif "datetime" in source_file_str:
                                image_label_keyword_doc = "datetime"
                            elif "string" in source_file_str:
                                image_label_keyword_doc = "string"
                            elif "json" in source_file_str:
                                image_label_keyword_doc = "robotframework"
                            else:
                                image_label_keyword_doc = ""

                            if image_label_keyword_doc != "":
                                self.label_keyword_doc_source_icon.configure(image=self.image(self.keyword_doc_source_image.get(image_label_keyword_doc), 42))
                            else: 
                                self.label_keyword_doc_source_icon.configure(image=self.emoji("", 42))
                                if self.label_keyword_doc_source_text: self.label_keyword_doc_source_text.configure(text="")
                                self.keywords_doc_source_frame.configure(width=0)
                            self.label_keyword_doc_source_icon.pack(side="left", padx=15)
                self.is_keywords_doc_list_opened = False
                self.save_window_geometry("keywords_doc_list", self.keywords_doc_list_window)
                self.is_keywords_doc_list_output = True
                open_keywords_doc(update=True)

        def open_keywords_doc(update=False):
            if self.is_keywords_doc_list_opened is True: 
                self.is_keywords_doc_list_opened = False
                self.first_open = False
                self.save_window_geometry("keywords_doc_list", self.keywords_doc_list_window)
                self.configure(self.config_file_path, 'keyword_doc_lang', self.keyword_doc_lang.get())
                update = False
                # self.keywords_doc_list_window.withdraw()
                self.keywords_doc_list_window.destroy()
                return
            if self.first_open is True:
                update = True
            if self.first_open is False:
                self.first_open = True

            words_to_color = self.current_cases
            color_for_titles = self.colors["purple"]
            color_for_commentaries = self.colors["green"]
            color_for_doc_tag = self.colors["orange"]
            color_for_should = self.colors["yellow"]
            color_for_example = self.colors["blue"]

            test_cases_pattern = r"^(" + "|".join(map(re.escape, words_to_color)) + r")$"
            commentaries_pattern = r"^# "
            documentation_tag_pattern = r"^\s*\["
            documentation_tag_dots_pattern = r"^\s*\.\.\.(?!.*[=_])"
            documentation_json_dots_pattern = r"^- "

            add_pattern = r"\b(Ajouter|Ajout|Add)\b"
            listing_pattern = r"\b(Listing|listing)\b"
            should_pattern = r"\b(Should|Doit|doit)\b"
            click_pattern = r"\b(Click|click)\b"
            wait_pattern = r"\b(Wait|Sleep)\b"
            write_pattern = r"\b(Saisir|Input Text)\b"
            examples_pattern = r"^(Example|Exemple)"
            # exemples_pattern = r"^Exemple"
            # variables_pattern = r"\${.*?}"
            # variables_pattern = r".\w.*?}"
            
            add_pattern_emoticon = "➕"
            listing_pattern_emoticon = "𝄚"
            should_pattern_emoticon = "👁"
            click_pattern_emoticon = "👆"
            wait_pattern_emoticon = "⏳"
            write_pattern_emoticon = "🖋"

            patterns = [
                (commentaries_pattern, color_for_commentaries),
                (documentation_tag_pattern, color_for_doc_tag),
                (documentation_tag_dots_pattern, color_for_doc_tag),
                (documentation_json_dots_pattern, color_for_doc_tag),
                (examples_pattern, color_for_example),
                (test_cases_pattern, color_for_titles),
                # (variables_pattern, color_for_variable)
            ]
            patterns_only_word = [
                # (add_pattern, color_for_should, add_pattern_emoticon),
                # (listing_pattern, color_for_should, listing_pattern_emoticon),
                (should_pattern, color_for_should, should_pattern_emoticon),
                # (click_pattern, color_for_should, click_pattern_emoticon),
                # (wait_pattern, color_for_should, wait_pattern_emoticon),
                # (write_pattern, color_for_should, write_pattern_emoticon),
                # (exemples_pattern, color_for_example),
                # (variables_pattern, color_for_variable)
            ]

            if self.current_keywords_doc_list and self.current_keywords_doc_index > 0:
                keyword_list = self.current_keywords_doc_list[self.current_keywords_doc_index - 1]
                if keyword_list:
                    keyword_pattern = r"^(" + re.escape(keyword_list) + r")$"
                else:
                    keyword_pattern = None
            else:
                keyword_pattern = None

            if update:
                if self.is_keywords_doc_list_output:
                    current_file = f"{self.current_program_path}/blocks_output.txt"
                else:
                    current_file = self.keywords_doc_file_path
                with open(current_file, 'r') as file:
                    new_lines = file.readlines()
                    if self.listbox_keywords_doc:
                        try:
                            apply_coloring_to_listbox(
                                self.listbox_keywords_doc,
                                new_lines,
                                patterns,
                                keyword_pattern,
                                patterns_only_word
                            )

                            current_word_place = 0
                            self.listbox_keywords_doc.selection_clear(0, "end")
                            self.listbox_keywords_doc.selection_set(current_word_place)
                            self.listbox_keywords_doc.activate(current_word_place)
                            self.listbox_keywords_doc.see(current_word_place)
                            self.is_keywords_doc_list_opened = True

                        except tk.TclError:
                            self.listbox_keywords_doc = None
                return 
          
            self.is_keywords_doc_list_opened = True
            if self.keywords_doc_list_window and self.keywords_doc_list_window.winfo_exists():
                self.keywords_doc_list_window.deiconify()
                self.is_keywords_doc_list_opened = True
            else:
                self.keywords_doc_list_window = ctk.CTkToplevel(self.launcher_window)
                self.keywords_doc_list_geometry = self.get_window_geometry("keywords_doc_list")
                reajust_y = int(self.keywords_doc_list_geometry['y']) - 37
                self.keywords_doc_list_window.geometry(f"{self.keywords_doc_list_geometry['width']}x{self.keywords_doc_list_geometry['height']}+{self.keywords_doc_list_geometry['x']}+{reajust_y}")
                self.keywords_doc_list_window.title("Keywords Doc")
                self.keywords_doc_list_window.attributes("-topmost", True)
                
                def on_close():
                    self.is_keywords_doc_list_opened = False
                    self.first_open = False
                    self.configure(self.config_file_path, 'keyword_doc_lang', self.keyword_doc_lang.get())
                    self.save_window_geometry("keywords_doc_list", self.keywords_doc_list_window)
                    # self.keywords_doc_list_window.withdraw()
                    self.keywords_doc_list_window.destroy()

                self.keywords_doc_list_window.protocol("WM_DELETE_WINDOW", on_close)
                
                def on_window_configure(event):
                    self.save_window_geometry("keywords_doc_list", self.keywords_doc_list_window)
                self.keywords_doc_list_window.bind("<Configure>", on_window_configure)

                keywords = ""
                for keyword in self.current_keywords_doc_list:
                    keywords += f" ⮕ {keyword}"
                test_name = str(self.test_path).split("/")[-1][:-6].replace("_", " ")
                breadcrumb_text = ""
                breadcrumb_text_str = f"{test_name}{keywords}"
                if len(breadcrumb_text_str) > 100:
                    keywords_doc_list_last_elements = " ⮕ ".join(self.current_keywords_doc_list[-3:])
                    breadcrumb_text = f"... {keywords_doc_list_last_elements}"
                else: 
                    breadcrumb_text = breadcrumb_text_str
                self.breadcrumb_label = ctk.CTkLabel(self.keywords_doc_list_window, text=breadcrumb_text, font=("Arial", 16))
                self.breadcrumb_label.pack(pady=10)

                if self.is_keywords_doc_list_output == True:
                    current_file = f"{self.current_program_path}/blocks_output.txt"
                else:
                    current_file = self.keywords_doc_file_path
                with open(current_file, 'r') as file:
                    lines = file.readlines()
                frame = ctk.CTkFrame(self.keywords_doc_list_window)
                frame.pack(fill="both", expand=True, pady=10, padx=10)
                
                self.listbox_keywords_doc = tk.Listbox(frame, height=10, bg="#2B2B2B", fg="white", selectbackground=self.colors["blue"], selectforeground="white")
                self.listbox_keywords_doc.pack(fill="both", expand=True, pady=10, padx=10)

                padding = "    "

                keyword_doc_entry_var = tk.StringVar()
                keyword_doc_entry = ctk.CTkEntry(frame, textvariable=keyword_doc_entry_var, fg_color="#3C3C3C", text_color="white", border_width=2)
                keyword_doc_entry.pack(fill="x", pady=10, padx=10)

                def update_listbox(*args):
                    self.listbox_keywords_save = self.listbox_keywords
                    self.is_selected_on_entry = True
                    query = keyword_doc_entry_var.get()

                    entries = extract_entries_from_directories(query, self.non_json_dirs, self.json_dirs)
                    var = str(self.test_path).rsplit("/", 1)[0]
                    self.listbox_keywords_doc.delete(0, "end")

                    for variable in entries:
                        if query.lower() in variable.lower():
                            self.listbox_keywords_doc.insert("end", variable)

                keyword_doc_entry_var.trace_add("write", update_listbox)
                def on_key_press_entry(event):
                    if event.keysym == "Left":
                        if keyword_doc_entry_var.get() == "":
                            self.listbox_keywords = self.listbox_keywords_save
                            update_keywords_doc_content()
                            self.listbox_keywords_doc.focus_set()
                    if event.keysym == "BackSpace":
                        if keyword_doc_entry_var.get() == "":
                            self.listbox_keywords = self.listbox_keywords_save
                            update_keywords_doc_content()
                            self.listbox_keywords_doc.focus_set()
                    if event.keysym == "Delete":
                        if keyword_doc_entry_var.get() == "":
                            self.listbox_keywords = self.listbox_keywords_save
                            update_keywords_doc_content()
                            self.listbox_keywords_doc.focus_set()
                            
                    if event.keysym == "Return":
                        update_listbox()
                        self.listbox_keywords_doc.focus_set()

                    if event.keysym == "Up":
                        update_listbox()
                        self.listbox_keywords_doc.focus_set()
                    
                    if event.keysym == "Down":
                        update_listbox()
                        self.listbox_keywords_doc.focus_set()

                def on_mouse_click(event):
                    if event.num == 1:
                        update_listbox()
            
                keyword_doc_entry.bind("<Left>", on_key_press_entry)
                keyword_doc_entry.bind("<BackSpace>", on_key_press_entry)
                keyword_doc_entry.bind("<Delete>", on_key_press_entry)
                keyword_doc_entry.bind("<Return>", on_key_press_entry)
                keyword_doc_entry.bind("<Up>", on_key_press_entry)
                keyword_doc_entry.bind("<Down>", on_key_press_entry)
                update_listbox()
                for line in lines:
                    apply_coloring_to_listbox(
                        self.listbox_keywords_doc,
                        lines,
                        patterns,
                        keyword_pattern,
                        patterns_only_word
                    )

                return_kw_button = ctk.CTkButton(frame, text=None, width=30, corner_radius=30, fg_color="transparent", hover_color="#454444", image=self.image(f"{self.keywords_images_path}iphone7-black-return-button.png", 52), command=return_keywords_doc)
                return_kw_button.pack(pady=10)

                self.keyword_doc_lang = StringVar(value=self.find_value_in_file(self.config_file_path, "keyword_doc_lang:"))
                toggle_keyword_doc_text = "English" if self.keyword_doc_lang.get() == "en" else "Français"
                toggle_keyword_doc_icon_path = f"{self.keywords_images_path}england_flag.png" if self.keyword_doc_lang.get() == "en" else f"{self.keywords_images_path}france_flag.png"
                
                def toggle_keyword_doc_lang():
                    update_keywords_doc_content()
                    if self.keyword_doc_lang.get() == "en":
                        self.toggle_keyword_doc_lang.configure(text="English")
                        self.toggle_keyword_doc_lang_icon.configure(image=self.image(f"{self.keywords_images_path}england_flag.png", 20))
                        self.configure(self.config_file_path, "keyword_doc_lang", "en")
                        update_keywords_doc_content()
                    if self.keyword_doc_lang.get() == "fr":
                        self.toggle_keyword_doc_lang.configure(text="Français")
                        self.toggle_keyword_doc_lang_icon.configure(image=self.image(f"{self.keywords_images_path}france_flag.png", 20))
                        self.configure(self.config_file_path, "keyword_doc_lang", "fr")
                        update_keywords_doc_content()

                toggle_keyword_doc_lang_frame = ctk.CTkFrame(
                    frame, 
                    fg_color="transparent", 
                )
                toggle_keyword_doc_lang_frame.pack(side="left", padx=5)

                self.toggle_keyword_doc_lang = ctk.CTkSwitch(toggle_keyword_doc_lang_frame, text=toggle_keyword_doc_text, variable=self.keyword_doc_lang, onvalue="fr", offvalue="en", command=toggle_keyword_doc_lang)
                self.toggle_keyword_doc_lang.pack(side="left")

                self.toggle_keyword_doc_lang_icon = ctk.CTkLabel(toggle_keyword_doc_lang_frame, text=None, fg_color="transparent", image=self.image(toggle_keyword_doc_icon_path, 20))
                self.toggle_keyword_doc_lang_icon.pack(side="left")

                self.keywords_doc_source_frame = ctk.CTkFrame(
                    frame, 
                    fg_color="transparent", 
                    height=120,
                    width=0,
                    border_width=3,
                    border_color=self.colors["blue"],
                    corner_radius=15,
                )
                self.keywords_doc_source_frame.pack(side="right", padx=5)
                self.keywords_doc_source_frame.pack_propagate(False)
                self.label_keyword_doc_source_icon = ctk.CTkLabel(self.keywords_doc_source_frame, text=None, fg_color="transparent", image=self.emoji("", 42))
                def link_keywords_doc():
                    if "selenium" in self.current_keyword_doc_source_file:
                        subprocess.Popen(["firefox", f"https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html"])
                        return
                    if ".json" in self.current_keyword_doc_source_file:
                        source = self.current_keyword_doc_source_file.split("/")[-1]
                        subprocess.Popen(["firefox", f"https://robotframework.org/robotframework/latest/libraries/{self.json_files[source]}"])
                    else:
                        subprocess.Popen(["code", self.current_keyword_doc_source_file])

                underline_font = ctk.CTkFont(family="Arial", size=14, underline=True)
                self.label_keyword_doc_source_text = ctk.CTkButton(
                    self.keywords_doc_source_frame,
                    width=50,
                    text=self.current_keyword_doc_source_file,      
                    fg_color="transparent",
                    text_color="white",
                    font=underline_font,
                    hover_color="lightblue",
                    command=link_keywords_doc
                )

                def on_select(event):
                    selection = self.listbox_keywords_doc.curselection()
                    if not selection:
                        self.current_keyword_doc_source_file = ""
                        return
                    try:
                        selected_item = str(self.listbox_keywords_doc.get(selection[0]))
                        if selected_item == "":
                            self.current_keyword_doc_source_file = ""
                            return
                        if self.last_selected_keyword_doc == selected_item:
                            return
                        if selected_item.startswith("${"):
                            selected_item = selected_item.split("  ")[1]
                            selected_item = selected_item.strip()
                        if "=  " in selected_item:
                            selected_item = selected_item.split("=  ")[1]
                            selected_item = selected_item.strip()
                        selected_item_short = selected_item.split("  ")[0]
                        selected_item_short = selected_item_short.strip()
                        
                        if selected_item_short not in self.current_keywords_doc_list and self.last_selected_keyword_doc != selected_item and not self.is_return_context:
                            self.current_keywords_doc_list.append(selected_item_short)
                            self.current_keywords_doc_places_list.append(selection[0])
                        elif self.is_return_context is True:
                            self.current_keywords_doc_list.append(selected_item_short)
                            self.current_keywords_doc_places_list.append(selection[0])
                        else:
                            return

                        self.last_selected_keyword_doc = selected_item

                        keywords = ""
                        for keyword in self.current_keywords_doc_list:
                            keywords += f" ⮕ {keyword}"
                        test_name = str(self.test_path).split("/")[-1][:-6].replace("_", " ")
                        breadcrumb_text = ""
                        breadcrumb_text_str = f"{test_name}{keywords}"
                        if len(breadcrumb_text_str) > 100:
                            keywords_doc_list_last_elements = " ⮕ ".join(self.current_keywords_doc_list[-3:])
                            breadcrumb_text = f"... {keywords_doc_list_last_elements}"
                        else: 
                            breadcrumb_text = breadcrumb_text_str
                        self.update_breadcrumb(breadcrumb_text)

                        blocks = extract_blocks_from_directories(selected_item_short, self.non_json_dirs, self.json_dirs)
                        if not blocks:
                            self.current_keyword_doc_source_file = ""
                            self.current_keywords_doc_list.pop()
                            self.current_keywords_doc_places_list.pop()
                            return

                        output_file_path = f"{self.current_program_path}/blocks_output.txt"
                        source_file_str = ""
                        with open(output_file_path, 'w', encoding='utf-8') as output_file:
                            for source_file, value in blocks.items():
                                if "::" in source_file:
                                    json_source, json_key = source_file.split("::", 1)
                                    self.current_keyword_doc_source_file = json_source
                                    source = self.current_keyword_doc_source_file.split("/")[-1]
                                    output_file.write(f"{value}\n")
                                    json_source_short = str(json_source).split("/")[-1]
                                    self.label_keyword_doc_source_text.configure(text=self.json_files[json_source_short])
                                    self.label_keyword_doc_source_text.pack(side="right", padx=15)
                                    recalculated_width = len(self.json_files[json_source_short]) * 9 + 110
                                    self.keywords_doc_source_frame.configure(width=recalculated_width)
                                    source_file_str = json_source
                                elif isinstance(value, list):
                                    for block in value:
                                        self.current_keyword_doc_source_file = source_file
                                        source_file_short = str(source_file).split("/")[-1]
                                        source_file_short = source_file_short.split(".")[0]
                                        output_file.write(f"{selected_item_short}\n\n")
                                        output_file.write(f"{block}\n")
                                        self.label_keyword_doc_source_text.configure(text=source_file_short)
                                        self.label_keyword_doc_source_text.pack(side="right", padx=15)
                                        recalculated_width = len(source_file_short) * 9 + 100
                                        self.keywords_doc_source_frame.configure(width=recalculated_width)
                                        source_file_str = source_file
                                else:
                                    output_file.write(f"{value}\n")

                                if source_file_str:
                                    image_label_keyword_doc = "" 
                                    if "openmairie/robotframework" in source_file_str:
                                        image_label_keyword_doc = "keyword_framework" 
                                    elif "tests" in source_file_str:
                                        image_label_keyword_doc = "keyword_local" 
                                    elif "selenium" in source_file_str:
                                        image_label_keyword_doc = "selenium"
                                    elif "collections" in source_file_str:
                                        image_label_keyword_doc = "collections"
                                    elif "operatingsystem" in source_file_str:
                                        image_label_keyword_doc = "operatingsystem"
                                    elif "datetime" in source_file_str:
                                        image_label_keyword_doc = "datetime"
                                    elif "string" in source_file_str:
                                        image_label_keyword_doc = "string"
                                    elif "json" in source_file_str:
                                        image_label_keyword_doc = "robotframework"
                                    else:
                                        image_label_keyword_doc = ""

                                    if image_label_keyword_doc != "":
                                        self.label_keyword_doc_source_icon.configure(image=self.image(self.keyword_doc_source_image.get(image_label_keyword_doc), 42))
                                    else: 
                                        self.label_keyword_doc_source_icon.configure(image=self.emoji("", 42))
                                        if self.label_keyword_doc_source_text: self.label_keyword_doc_source_text.configure(text="")
                                        self.keywords_doc_source_frame.configure(width=0)
                                    self.label_keyword_doc_source_icon.pack(side="left", padx=15)
                        
                        self.is_keywords_doc_list_opened = False
                        self.is_keywords_doc_list_output = True
                        self.save_window_geometry("keywords_doc_list", self.keywords_doc_list_window)
                        self.current_keywords_doc_index += 1
                        open_keywords_doc()

                    except IndexError as e:
                        print(f"Erreur de sélection : {e}")
                    except Exception as e:
                        print(f"Erreur inattendue : {e}")

                def on_key_press(event):
                    if event.widget is not self.listbox_keywords_doc:
                        return  # Ignorer l'événement si ce n'est pas pour la fenêtre listbox_keywords_doc

                    selected_index = self.listbox_keywords_doc.curselection()
                    focused_index = self.listbox_keywords_doc.index("active")

                    if event.keysym == "Right":
                        self.is_return_context = True
                        if not selected_index:
                            self.listbox_keywords_doc.selection_set(focused_index)
                        on_select(event)
                        # return "break"

                    elif event.keysym == "Return":
                        self.is_return_context = True
                        if not selected_index:
                            self.listbox_keywords_doc.selection_set(focused_index)
                        on_select(event)

                    elif event.keysym == "Left":
                        self.is_return_context = True
                        return_keywords_doc()

                    elif event.keysym == "Up":
                        if not selected_index or selected_index[0] == 0:
                            return  # Pas de sélection ou déjà en haut
                        self.listbox_keywords_doc.selection_clear(0, "end")
                        self.listbox_keywords_doc.selection_set(selected_index[0] - 1)
                        self.listbox_keywords_doc.activate(selected_index[0] - 1)

                    elif event.keysym == "Down":
                        if not selected_index or selected_index[0] == self.listbox_keywords_doc.size() - 1:
                            return  # Pas de sélection ou déjà en bas
                        self.listbox_keywords_doc.selection_clear(0, "end")
                        self.listbox_keywords_doc.selection_set(selected_index[0] + 1)
                        self.listbox_keywords_doc.activate(selected_index[0] + 1)

                    elif event.keysym == "space":
                        keyword_doc_entry.focus_set()
                        return "break"


                def on_window_focus_in(event):
                    self.active_window = event.widget
                    if event.widget is self.keywords_doc_list_window:
                        self.listbox_keywords_doc.focus_set()


                def on_window_focus_out(event):
                    if event.widget is self.keywords_doc_list_window:
                        self.active_window = None


                # Liaison des événements
                self.listbox_keywords_doc.bind("<Left>", on_key_press)
                self.listbox_keywords_doc.bind("<Right>", on_key_press)
                self.listbox_keywords_doc.bind("<Return>", on_key_press)
                self.listbox_keywords_doc.bind("<Up>", on_key_press)
                self.listbox_keywords_doc.bind("<Down>", on_key_press)
                self.listbox_keywords_doc.bind("<Key>", on_key_press)
                self.keywords_doc_list_window.bind("<FocusIn>", on_window_focus_in)
                self.keywords_doc_list_window.bind("<FocusOut>", on_window_focus_out)


                def on_mouse_click(event):
                    index = self.listbox_keywords_doc.nearest(event.y)
                    self.listbox_keywords_doc.selection_clear(0, "end")
                    self.listbox_keywords_doc.selection_set(index)
                    self.listbox_keywords_doc.activate(index) 
                    if event.num == 1:  # Clic g
                        on_select(event)
                    elif event.num == 3:  # Clic d
                        return_keywords_doc()
                
                self.listbox_keywords_doc.bind("<Button-1>", on_mouse_click)  # Clic g
                self.listbox_keywords_doc.bind("<Button-3>", on_mouse_click)
            
        open_kw_button = ctk.CTkButton(self.launcher_window, width=40, corner_radius=30,text=None, fg_color="transparent", hover_color="#2B2B2B", image=self.image(f"{self.keywords_images_path}iphone7-black-button.png", 52), command=open_keywords_doc)
        open_kw_button.pack(pady=10)
        
        self.launcher_window.mainloop()

if __name__ == "__main__":
    kw_doc = KeywordsDoc()
    kw_doc.launcher()
