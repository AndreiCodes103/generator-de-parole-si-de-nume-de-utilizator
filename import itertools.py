import tkinter as tk
from tkinter import ttk
import secrets
import random
import string

# --- SETURI DE CARACTERE ---
latin_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
symbols = '!@#$%^&*()_=[]{}|;:,.<>?'
classic_chars = latin_letters + digits + symbols + '-+'
complex_chars = (
    classic_chars
    + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    + '的一是不了人我在有他这为之大来以个中上们'
    + 'ابتثجحخدذرزسشصضطظعغفقكلمنهوي'
    + '𓀀𓁿𓂀𓃰𓆣𓇋𓋹𓏏𓐍𓂻'
)

# Variabile pentru a stoca ultimul rezultat generat
last_fake_name = ""
last_username = ""

# --- LOGICA PENTRU GENERATOARE (Parole, Nume, Utilizatori) ---
def generate_complex_password(length):
    return ''.join(secrets.choice(complex_chars) for _ in range(length))

def generate_classic_password(length):
    return ''.join(secrets.choice(classic_chars) for _ in range(length))

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

def generate_random_word(min_len, max_len):
    length = random.randint(min_len, max_len)
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_fake_name():
    global last_fake_name
    while True:
        prenume = generate_random_word(4, 8).capitalize()
        nume = generate_random_word(5, 10).capitalize()
        new_name = f"{prenume} {nume}"
        if new_name != last_fake_name:
            last_fake_name = new_name
            return new_name

def on_generate_name():
    fake_name = generate_fake_name()
    name_result_var.set(fake_name)

def generate_username():
    global last_username
    while True:
        word = generate_random_word(6, 10).lower()
        number = str(random.randint(10, 9999))
        new_username = f"{word}{number}"
        if new_username != last_username:
            last_username = new_username
            return new_username

def on_generate_username():
    username = generate_username()
    username_result_var.set(username)

def copy_to_clipboard(result_var):
    generated_text = result_var.get()
    if generated_text and "✅" not in generated_text and "⚠️" not in generated_text:
        root.clipboard_clear()
        root.clipboard_append(generated_text)
        root.update()
        result_var.set("✅ Copiat în clipboard!")

# --- LOGICA GMAIL TRICKS SIMPLIFICATĂ ---
def generate_dot_trick(email, count):
    username, domain = email.split('@')
    variations = set()
    while len(variations) < count:
        temp = list(username)
        # Generează puncte doar între caracterele username-ului, nu la început sau la sfârșit.
        indices = random.sample(range(1, len(username)), k=random.randint(1, len(username) - 1))
        for i in sorted(indices):
            temp.insert(i, '.')
        variations.add(''.join(temp) + '@' + domain)
    return sorted(list(variations))

def generate_plus_trick(email, count):
    username, domain = email.split('@')
    variations = set()
    while len(variations) < count:
        tag = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        variations.add(f"{username}+{tag}@{domain}")
    return sorted(list(variations))

def generate_combined_trick(email, count):
    username, domain = email.split('@')
    variations = set()
    while len(variations) < count:
        temp = list(username)
        indices = random.sample(range(1, len(username)), k=random.randint(1, len(username) - 1))
        for i in sorted(indices):
            temp.insert(i, '.')
        dotted_username = ''.join(temp)
        tag = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        variations.add(f"{dotted_username}+{tag}@{domain}")
    return sorted(list(variations))

def on_generate_emails():
    email = gmail_entry.get().strip()
    if '@' not in email or not email.endswith('@gmail.com'):
        gmail_result_text.delete(1.0, tk.END)
        gmail_result_text.insert(tk.END, "⚠️ Introdu o adresă Gmail validă.")
        return

    try:
        count = int(email_count_var.get())
        if count <= 0:
            gmail_result_text.delete(1.0, tk.END)
            gmail_result_text.insert(tk.END, "⚠️ Numărul trebuie să fie pozitiv.")
            return
    except ValueError:
        gmail_result_text.delete(1.0, tk.END)
        gmail_result_text.insert(tk.END, "⚠️ Introdu un număr valid.")
        return

    option = trick_type.get()
    results = []
    
    if option == "dot":
        results = generate_dot_trick(email, count)
    elif option == "plus":
        results = generate_plus_trick(email, count)
    elif option == "combined":
        results = generate_combined_trick(email, count)
    
    gmail_result_text.delete(1.0, tk.END)
    gmail_result_text.insert(tk.END, "\n".join(results))

def copy_first_email():
    results = gmail_result_text.get(1.0, tk.END).strip().split('\n')
    if results and results[0] and "⚠️" not in results[0]:
        root.clipboard_clear()
        root.clipboard_append(results[0])
        root.update()

# --- INTERFAȚA GRAFICĂ (GUI) ---
root = tk.Tk()
root.title("🛠️ Generator Multifuncțional")
root.geometry("600x650")
root.configure(bg="#f0f0f0")

# --- STILIZARE ---
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 12), background="#f0f0f0")
style.configure("TButton", font=("Segoe UI", 12))
style.configure("TEntry", font=("Segoe UI", 12))
style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=[10, 5])

# --- NOTEBOOK PENTRU TAB-URI ---
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab1 = ttk.Frame(notebook, padding="10")
tab2 = ttk.Frame(notebook, padding="10")
tab3 = ttk.Frame(notebook, padding="10")
tab4 = ttk.Frame(notebook, padding="10")
tab5 = ttk.Frame(notebook, padding="10")

notebook.add(tab1, text="🔑 Parolă Clasică")
notebook.add(tab2, text="🌌 Parolă Avansată")
notebook.add(tab3, text="👤 Nume Aleatoriu")
notebook.add(tab4, text="🧑‍💻 Utilizator Aleatoriu")
notebook.add(tab5, text="📧 Gmail Trick Generator")

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

# --- CONȚINUT TAB 3: GENERATOR DE NUME ALEATORIU ---
ttk.Label(tab3, text="Generator de Nume Aleatorii", style="Title.TLabel").pack(pady=(10, 10))
ttk.Label(tab3, text="Generează un nume din două 'cuvinte' aleatorii.", wraplength=400, justify="center").pack(pady=10)
ttk.Button(tab3, text="Generează nume", command=on_generate_name).pack(pady=20)
name_result_var = tk.StringVar()
ttk.Label(tab3, textvariable=name_result_var, font=("Segoe UI", 18), foreground="#333", padding=5).pack(pady=10)
ttk.Button(tab3, text="Copiază numele", command=lambda: copy_to_clipboard(name_result_var)).pack()

# --- CONȚINUT TAB 4: GENERATOR DE NUME DE UTILIZATOR ---
ttk.Label(tab4, text="Generator de Nume de Utilizator", style="Title.TLabel").pack(pady=(10, 10))
ttk.Label(tab4, text="Generează un utilizator aleatoriu ('cuvânt' + cifre).", wraplength=400, justify="center").pack(pady=10)
ttk.Button(tab4, text="Generează utilizator", command=on_generate_username).pack(pady=20)
username_result_var = tk.StringVar()
ttk.Label(tab4, textvariable=username_result_var, font=("Courier New", 18), foreground="#333", padding=5).pack(pady=10)
ttk.Button(tab4, text="Copiază utilizatorul", command=lambda: copy_to_clipboard(username_result_var)).pack()

# --- CONȚINUT TAB 5: GMAIL TRICK ---
ttk.Label(tab5, text="Gmail Trick Generator", style="Title.TLabel").pack(pady=(10, 10))
ttk.Label(tab5, text="Introdu adresa ta Gmail (@gmail.com):").pack()
gmail_entry = tk.Entry(tab5, width=40)
gmail_entry.pack(pady=5)

ttk.Label(tab5, text="Numărul de variante:", font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))
email_count_var = tk.StringVar(value="10")
ttk.Entry(tab5, textvariable=email_count_var, width=5).pack(pady=5)

trick_type = tk.StringVar(value="dot")
ttk.Label(tab5, text="Alege tipul de trick:", font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))

ttk.Radiobutton(tab5, text="Dot Trick", variable=trick_type, value="dot").pack()
ttk.Radiobutton(tab5, text="Plus Trick", variable=trick_type, value="plus").pack()
ttk.Radiobutton(tab5, text="Combined Trick (Dot + Plus)", variable=trick_type, value="combined").pack()

ttk.Button(tab5, text="Generează variante", command=on_generate_emails).pack(pady=10)

# Am înlocuit Label-ul cu un Text widget pentru a permite copierea selectivă
gmail_result_text = tk.Text(tab5, height=10, width=50, font=("Courier New", 10), foreground="#333", relief="solid", borderwidth=1)
gmail_result_text.pack(pady=5)

# Am adăugat un nou buton pentru a copia doar primul email
button_frame = ttk.Frame(tab5)
button_frame.pack()
ttk.Button(button_frame, text="Copiază primul email", command=copy_first_email).pack(side="left", padx=5)
ttk.Button(button_frame, text="Copiază toate email-urile", command=lambda: root.clipboard_clear() or root.clipboard_append(gmail_result_text.get(1.0, tk.END))).pack(side="left", padx=5)

root.mainloop()