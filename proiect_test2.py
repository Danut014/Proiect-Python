import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Cursuri de schimb pentru fiecare monedă
currency_rates = {
    "RON": 1,
    "EUR": 4.9,
    "USD": 4.7,
    "GBP": 6.0
}

currency_symbol = "RON"
currency_rate = currency_rates[currency_symbol]


def adauga_articol():
    articol = entry_articol.get()
    try:
        pret = float(entry_pret.get())
        # Salvează prețul în moneda curentă
        lista.append((articol, pret, currency_symbol))
        update_lista()
        messagebox.showinfo("Succes", f"Articol '{articol}' adăugat!")
        entry_articol.delete(0, tk.END)
        entry_pret.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Eroare", "Prețul trebuie să fie un număr valid!")


def sterge_articol():
    try:
        selectie = listbox.curselection()
        if not selectie:
            messagebox.showwarning("Eroare", "Te rog selectează un produs din listă pentru a-l șterge.")
            return
        # Obținem indexul selectat
        index = selectie[0]
        produs = lista.pop(index)  # Ștergem articolul din listă
        update_lista()
        messagebox.showinfo("Succes", f"Produsul '{produs[0]}' a fost șters din listă!")
    except IndexError:
        messagebox.showwarning("Eroare", "Te rog selectează un produs valid pentru a-l șterge.")


def update_lista():
    listbox.delete(0, tk.END)
    total = sum(pret / currency_rate for _, pret, _ in lista)
    for articol, pret, moneda in lista:
        pret_convertit = pret / currency_rates[moneda]
        listbox.insert(tk.END, f"{articol} - {pret_convertit:.2f} {currency_symbol}")

    # Actualizăm totalul în timp real
    total_label.config(text=f"Total: {total:.2f} {currency_symbol}")


def verifica_buget():
    try:
        buget = float(entry_buget.get())
        total = sum(pret / currency_rate for _, pret, _ in lista)
        if total <= buget:
            messagebox.showinfo("Buget", "Buget suficient! Poți cumpăra tot.")
        else:
            diferenta = total - buget
            messagebox.showwarning("Buget insuficient", f"Îți lipsesc {diferenta:.2f} {currency_symbol}.")
    except ValueError:
        messagebox.showerror("Eroare", "Bugetul trebuie să fie un număr valid!")


# Funcție pentru schimbarea monedei
def schimba_moneda(event=None):
    global currency_rate, currency_symbol
    currency_symbol = moneda_combobox.get()
    currency_rate = currency_rates[currency_symbol]
    update_lista()


# Configurare fereastră principală
root = tk.Tk()
root.title("Lista de Cumpărături")
root.configure(bg="#f0f8ff")
root.geometry("400x600")

# Elemente GUI
frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(pady=10)

font_label = ("Arial", 12, "bold")
font_entry = ("Arial", 12)
font_button = ("Arial", 10, "bold")
font_text = ("Arial", 10)

label_articol = tk.Label(frame, text="Articol:", font=font_label, bg="#f0f8ff")
label_articol.grid(row=0, column=0, padx=5, pady=5)
entry_articol = tk.Entry(frame, font=font_entry)
entry_articol.grid(row=0, column=1, padx=5, pady=5)

label_pret = tk.Label(frame, text="Preț:", font=font_label, bg="#f0f8ff")
label_pret.grid(row=1, column=0, padx=5, pady=5)
entry_pret = tk.Entry(frame, font=font_entry)
entry_pret.grid(row=1, column=1, padx=5, pady=5)

button_adauga = tk.Button(frame, text="Adaugă", font=font_button, bg="#87ceeb", fg="white", command=adauga_articol)
button_adauga.grid(row=2, columnspan=2, pady=10)

label_buget = tk.Label(frame, text="Buget:", font=font_label, bg="#f0f8ff")
label_buget.grid(row=3, column=0, padx=5, pady=5)
entry_buget = tk.Entry(frame, font=font_entry)
entry_buget.grid(row=3, column=1, padx=5, pady=5)

button_verifica = tk.Button(frame, text="Verifică bugetul", font=font_button, bg="#4682b4", fg="white",
                            command=verifica_buget)
button_verifica.grid(row=4, columnspan=2, pady=10)

# Combobox pentru alegerea monedei
moneda_combobox = ttk.Combobox(frame, values=["RON", "EUR", "USD", "GBP"], state="readonly", font=font_button)
moneda_combobox.set("RON")
moneda_combobox.grid(row=5, columnspan=2, pady=10)
moneda_combobox.bind("<<ComboboxSelected>>", schimba_moneda)

# Listbox pentru produse
listbox = tk.Listbox(root, height=10, width=40, font=font_text, bg="#e6f7ff", fg="black")
listbox.pack(pady=10)

# Etichetă pentru total
total_label = tk.Label(root, text="Total: 0 RON", font=("Arial", 12, "bold"), bg="#f0f8ff")
total_label.pack(pady=10)

# Buton pentru a șterge un articol selectat
button_sterge = tk.Button(root, text="Șterge produs", font=font_button, bg="#ff6347", fg="white",
                          command=sterge_articol)
button_sterge.pack(pady=10)

button_iesire = tk.Button(root, text="Ieși", font=font_button, bg="#ff4500", fg="white", command=root.quit)
button_iesire.pack(pady=10)

# Inițializare listă
lista = []

# Lansare aplicație
root.mainloop()