import tkinter as tk
from tkinter import ttk
import random
import string

# --- SETURI DE CARACTERE ---

# Pentru parole (Neschimbat)
latin_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
symbols = '!@#$%^&*()_=[]{}|;:,.<>?'
classic_chars = latin_letters + digits + symbols + '-+' 
complex_chars = classic_chars + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + '的一是不了人我在有他这为之大来以个中上们' + 'ابتثجحخدذرزсشصضطظعغفقكلمنهوي' + '𓀀𓁿𓂀𓃰𓆣𓇋𓋹𓏏𓐍𓂻'

# Variabile pentru a stoca ultimul rezultat generat (Neschimbat)
last_fake_name = ""
last_username = ""

# --- LOGICA PENTRU GENERATOARE ---

# 1. Parole (Neschimbat)
def generate_complex_password(length):
    return ''.join(random.choice(complex_chars) for _ in range(length))

def generate_classic_password(length):
    return ''.join(random.choice(classic_chars) for _ in range(length))

def on_generate_password(password_type):
    try:
        if password_type == 'complex':
            length = int(complex_length_var.get())
            result_var = complex_result_var
            password = generate_complex_password(length)
        else:
            length = int(classic_length_var.get())
            result_var = classic_result_var
            password = generate_classic_password(length)

        if length <= 0:
            result_var.set("⚠️ Lungimea trebuie să fie pozitivă.")
        else:
            result_var.set(password)
    except ValueError:
        result_var.set("⚠️ Introdu un număr valid.")

# MODIFICARE: Funcție ajutătoare pentru a crea un cuvânt din litere aleatorii
def generate_random_word(min_len, max_len):
    """Generează un singur cuvânt din litere aleatorii, cu o lungime aleatorie."""
    length = random.randint(min_len, max_len)
    # Folosim doar litere, conform cerinței "ca la parole"
    letters = string.ascii_letters 
    return ''.join(random.choice(letters) for _ in range(length))

# 2. Nume Fake (Modificat complet)
def generate_fake_name():
    """Generează două cuvinte aleatorii capitalizate, asigurându-se că nu se repetă."""
    global last_fake_name
    
    while True:
        # Generează două cuvinte aleatorii și le capitalizează
        prenume = generate_random_word(4, 8).capitalize()
        nume = generate_random_word(5, 10).capitalize()
        new_name = f"{prenume} {nume}"
        if new_name != last_fake_name:
            last_fake_name = new_name
            return new_name

def on_generate_name():
    fake_name = generate_fake_name()
    name_result_var.set(fake_name)

# 3. Nume de Utilizator (Modificat complet)
def generate_username():
    """Generează un cuvânt aleatoriu (litere mici) + cifre, asigurându-se că nu se repetă."""
    global last_username
    
    while True:
        # Generează un cuvânt aleatoriu și îl face minuscul
        word = generate_random_word(6, 10).lower()
        # Adaugă un număr aleatoriu la final
        number = str(random.randint(10, 9999))
        new_username = f"{word}{number}"
        if new_username != last_username:
            last_username = new_username
            return new_username

def on_generate_username():
    username = generate_username()
    username_result_var.set(username)

# Funcție generică de copiere (Neschimbat)
def copy_to_clipboard(result_var):
    generated_text = result_var.get()
    if generated_text and "✅" not in generated_text and "⚠️" not in generated_text:
        root.clipboard_clear()
        root.clipboard_append(generated_text)
        root.update()
        result_var.set("✅ Copiat în clipboard!")

# --- INTERFAȚA GRAFICĂ (GUI) ---
root = tk.Tk()
root.title("🛠️ Generator Multifuncțional")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

# --- STILIZARE (Neschimbat) ---
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 12), background="#f0f0f0")
style.configure("TButton", font=("Segoe UI", 12))
style.configure("TEntry", font=("Segoe UI", 12))
style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[10, 5])

# --- NOTEBOOK PENTRU TAB-URI (Neschimbat) ---
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab1 = ttk.Frame(notebook, padding="10")
tab2 = ttk.Frame(notebook, padding="10")
tab3 = ttk.Frame(notebook, padding="10")
tab4 = ttk.Frame(notebook, padding="10")

notebook.add(tab1, text="🔑 Parolă Clasică")
notebook.add(tab2, text="🌌 Parolă Avansată")
notebook.add(tab3, text="👤 Nume Aleatoriu") # Text tab schimbat
notebook.add(tab4, text="🧑‍💻 Utilizator Aleatoriu") # Text tab schimbat


# --- CONȚINUT TAB 1 și 2 (Parole - Neschimbat) ---
# ... (codul pentru tab-urile 1 și 2 rămâne identic)
# --- CONȚINUT TAB 1: GENERATOR PAROLĂ CLASICĂ ---
ttk.Label(tab1, text="Generator de Parole Clasice", style="Title.TLabel").pack(pady=(10, 10))
ttk.Label(tab1, text="Litere, Cifre, Simboluri, Plus, Minus", wraplength=400, justify="center").pack()
ttk.Label(tab1, text="📏 Lungimea parolei:").pack(pady=(20,0))
classic_length_var = tk.StringVar(value="16")
ttk.Entry(tab1, textvariable=classic_length_var, width=10, justify="center").pack(pady=5)
ttk.Button(tab1, text="Generează parola", command=lambda: on_generate_password('classic')).pack(pady=10)
classic_result_var = tk.StringVar()
ttk.Label(tab1, textvariable=classic_result_var, wraplength=550, font=("Courier New", 14), foreground="#333", padding=5).pack(pady=5)
ttk.Button(tab1, text="Copiază parola", command=lambda: copy_to_clipboard(classic_result_var)).pack()

# --- CONȚINUT TAB 2: GENERATOR PAROLĂ AVANSATĂ ---
ttk.Label(tab2, text="Generator de Parole Avansate", style="Title.TLabel").pack(pady=(10, 10))
ttk.Label(tab2, text="Include caractere din multiple alfabete", wraplength=400, justify="center").pack()
ttk.Label(tab2, text="📏 Lungimea parolei:").pack(pady=(20,0))
complex_length_var = tk.StringVar(value="20")
ttk.Entry(tab2, textvariable=complex_length_var, width=10, justify="center").pack(pady=5)
ttk.Button(tab2, text="Generează parola", command=lambda: on_generate_password('complex')).pack(pady=10)
complex_result_var = tk.StringVar()
ttk.Label(tab2, textvariable=complex_result_var, wraplength=550, font=("Courier New", 14), foreground="#333", padding=5).pack(pady=5)
ttk.Button(tab2, text="Copiază parola", command=lambda: copy_to_clipboard(complex_result_var)).pack()


# --- CONȚINUT TAB 3: GENERATOR DE NUME ALEATORIU (Modificat) ---
ttk.Label(tab3, text="Generator de Nume Aleatorii", style="Title.TLabel").pack(pady=(10, 10))
# MODIFICARE: Textul descriptiv a fost actualizat
ttk.Label(tab3, text="Generează un nume din două 'cuvinte' aleatorii.", wraplength=400, justify="center").pack(pady=10)
ttk.Button(tab3, text="Generează nume", command=on_generate_name).pack(pady=20)
name_result_var = tk.StringVar()
ttk.Label(tab3, textvariable=name_result_var, font=("Segoe UI", 18), foreground="#333", padding=5).pack(pady=10)
ttk.Button(tab3, text="Copiază numele", command=lambda: copy_to_clipboard(name_result_var)).pack()

# --- CONȚINUT TAB 4: GENERATOR DE NUME DE UTILIZATOR (Modificat) ---
ttk.Label(tab4, text="Generator de Nume de Utilizator", style="Title.TLabel").pack(pady=(10, 10))
# MODIFICARE: Textul descriptiv a fost actualizat
ttk.Label(tab4, text="Generează un utilizator aleatoriu ('cuvânt' + cifre).", wraplength=400, justify="center").pack(pady=10)
ttk.Button(tab4, text="Generează utilizator", command=on_generate_username).pack(pady=20)
username_result_var = tk.StringVar()
ttk.Label(tab4, textvariable=username_result_var, font=("Courier New", 18), foreground="#333", padding=5).pack(pady=10)
ttk.Button(tab4, text="Copiază utilizatorul", command=lambda: copy_to_clipboard(username_result_var)).pack()


root.mainloop()