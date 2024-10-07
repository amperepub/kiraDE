import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import configparser

# Configurazione dei percorsi
FILESYSTEM_PATH = "C:/ampere/filesystem/"
PACKAGES_DIR = os.path.join(FILESYSTEM_PATH, "system", "packages", "apps", "astolfodl")
WALLPAPERS_DIR = os.path.join(FILESYSTEM_PATH, "Wallpapers")
CONFIG_FILE = os.path.join(FILESYSTEM_PATH, "kirade.conf")

# Assicurati che le cartelle esistano
os.makedirs(PACKAGES_DIR, exist_ok=True)
os.makedirs(WALLPAPERS_DIR, exist_ok=True)

# Gestione della configurazione
config = configparser.ConfigParser()

if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)
else:
    config['Settings'] = {'background': ''}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def save_config():
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

# Funzione per eseguire un pacchetto
def run_package(package_name):
    package_path = os.path.join(PACKAGES_DIR, package_name + ".py")
    if not os.path.exists(package_path):
        messagebox.showerror("Errore", f"Il pacchetto '{package_name}' non esiste.")
        return
    try:
        # Apri una nuova finestra terminale ed esegui il pacchetto
        subprocess.Popen(["python", package_path], shell=True)
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile eseguire il pacchetto: {e}")

# Funzione per aprire il terminale
def open_terminal():
    try:
        subprocess.Popen(["cmd.exe"], shell=True)
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile aprire il terminale: {e}")

# Funzione per aprire le impostazioni
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Impostazioni")
    settings_window.geometry("400x300")

    def change_background():
        # Apri una finestra di dialogo per selezionare un'immagine PNG
        file_path = filedialog.askopenfilename(
            initialdir=WALLPAPERS_DIR,
            title="Seleziona una wallpaper",
            filetypes=(("PNG files", "*.png"), ("All files", "*.*"))
        )
        if file_path:
            # Copia l'immagine nella cartella Wallpapers
            try:
                filename = os.path.basename(file_path)
                destination = os.path.join(WALLPAPERS_DIR, filename)
                if not os.path.exists(destination):
                    shutil.copy(file_path, destination)
                # Aggiorna la configurazione
                config['Settings']['background'] = filename
                save_config()
                # Aggiorna lo sfondo della finestra principale
                set_background()
                messagebox.showinfo("Successo", "Sfondo cambiato con successo.")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile cambiare lo sfondo: {e}")

    change_bg_button = tk.Button(settings_window, text="Cambia Sfondo", command=change_background)
    change_bg_button.pack(pady=20)

    # Lista delle wallpapers disponibili
    wallpapers_label = tk.Label(settings_window, text="Wallpapers Disponibili:")
    wallpapers_label.pack()

    wallpapers_listbox = tk.Listbox(settings_window)
    wallpapers_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    wallpapers = [f for f in os.listdir(WALLPAPERS_DIR) if f.lower().endswith('.png')]
    for wallpaper in wallpapers:
        wallpapers_listbox.insert(tk.END, wallpaper)

    def select_wallpaper(event):
        selected = wallpapers_listbox.curselection()
        if selected:
            selected_wallpaper = wallpapers_listbox.get(selected[0])
            config['Settings']['background'] = selected_wallpaper
            save_config()
            set_background()
            messagebox.showinfo("Successo", "Sfondo cambiato con successo.")

    wallpapers_listbox.bind('<<ListboxSelect>>', select_wallpaper)

# Funzione per impostare lo sfondo
def set_background():
    bg_filename = config['Settings'].get('background', '')
    if bg_filename:
        bg_path = os.path.join(WALLPAPERS_DIR, bg_filename)
        if os.path.exists(bg_path):
            try:
                image = Image.open(bg_path)
                image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
                bg_image = ImageTk.PhotoImage(image)
                background_label.config(image=bg_image)
                background_label.image = bg_image
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile caricare lo sfondo: {e}")

# Funzione per caricare i pacchetti
def load_packages():
    packages = [f[:-3] for f in os.listdir(PACKAGES_DIR) if f.endswith('.py')]
    for pkg in packages:
        create_package_icon(pkg)

# Funzione per creare l'icona di un pacchetto
def create_package_icon(package_name):
    icon_button = tk.Button(root, text=package_name, command=lambda: run_package(package_name))
    icon_button.place(x=50 + (len(icon_buttons) % 5) * 100, y=50 + (len(icon_buttons) // 5) * 100)
    icon_buttons.append(icon_button)

# Funzione per creare l'icona del terminale
def create_terminal_icon():
    terminal_button = tk.Button(root, text="Terminale", command=open_terminal)
    terminal_button.place(x=50 + (len(icon_buttons) % 5) * 100, y=50 + (len(icon_buttons) // 5) * 100)
    icon_buttons.append(terminal_button)

# Funzione per creare l'icona delle impostazioni
def create_settings_icon():
    settings_button = tk.Button(root, text="Impostazioni", command=open_settings)
    settings_button.place(x=50 + (len(icon_buttons) % 5) * 100, y=50 + (len(icon_buttons) // 5) * 100)
    icon_buttons.append(settings_button)

# Lista per tenere traccia delle icone
icon_buttons = []

# Creazione della finestra principale
root = tk.Tk()
root.title("Ampere Desktop Environment")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.attributes("-fullscreen", True)

# Etichetta di sfondo
background_label = tk.Label(root)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Imposta lo sfondo iniziale
set_background()

# Carica e crea le icone dei pacchetti
load_packages()

# Crea icone per terminale e impostazioni
create_terminal_icon()
create_settings_icon()

# Esegui la finestra principale
root.mainloop()
