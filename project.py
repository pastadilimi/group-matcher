# file: eslestir_tkinter.py
import tkinter as tk
from tkinter import messagebox
import random

def parse_names(raw_text: str):
    # satır satır veya virgül ile ayırmayı destekler
    text = raw_text.replace(",", "\n")
    names = [n.strip() for n in text.splitlines() if n.strip()]
    # isimleri tekilleştirmek istemiyorsanız bu satırı kaldırın:
    return list(dict.fromkeys(names))  # sıra koruyarak tekrarları atar

def make_groups(names, allow_trio=True):
    # boş veya tek kişi durumları dahil tüm kenar durumlarına dayanıklı
    shuffled = names[:]
    random.shuffle(shuffled)
    groups = []

    i = 0
    while i < len(shuffled):
        # normalde ikişer al
        if i + 1 < len(shuffled):
            groups.append([shuffled[i], shuffled[i+1]])
            i += 2
        else:
            # son kişi kaldı
            if allow_trio and groups:
                groups[-1].append(shuffled[i])  # son grubu üçler
            else:
                groups.append([shuffled[i]])     # tek grup olarak bırak
            i += 1
    return groups

def on_group():
    names = parse_names(txt_names.get("1.0", tk.END))
    if not names:
        messagebox.showwarning("Uyarı", "Lütfen en az bir isim girin.")
        return
    allow_trio = var_trio.get() == 1
    groups = make_groups(names, allow_trio=allow_trio)
    show_groups(groups)

def show_groups(groups):
    txt_out.config(state="normal")
    txt_out.delete("1.0", tk.END)
    for idx, g in enumerate(groups, start=1):
        line = f"Grup {idx}: " + " - ".join(g) + "\n"
        txt_out.insert(tk.END, line)
    txt_out.config(state="disabled")

def on_shuffle_again():
    on_group()

# --- UI ---
root = tk.Tk()
root.title("Rastgele Eşleştirme (2'li gruplar, gerekirse 3'lü)")

frm = tk.Frame(root, padx=12, pady=12)
frm.pack(fill="both", expand=True)

lbl = tk.Label(frm, text="İsimleri yazın (satır satır veya virgülle):")
lbl.pack(anchor="w")

txt_names = tk.Text(frm, height=10, width=50)
txt_names.pack(fill="x")
txt_names.insert(tk.END, "Özgün\nDeniz\nAyşe\nMehmet\nEce\nBurak\nZeynep\nAli\nSelin\nKerem\nCan\nElif")

var_trio = tk.IntVar(value=1)
chk = tk.Checkbutton(frm, text="Tek kişi kalırsa 3’lü grup yap", variable=var_trio)
chk.pack(anchor="w", pady=(6, 6))

btns = tk.Frame(frm)
btns.pack(fill="x")
btn_group = tk.Button(btns, text="Grupla", command=on_group)
btn_group.pack(side="left")
btn_again = tk.Button(btns, text="Tekrarla", command=on_shuffle_again)
btn_again.pack(side="left", padx=8)

lbl_out = tk.Label(frm, text="Sonuçlar:")
lbl_out.pack(anchor="w", pady=(10, 0))

txt_out = tk.Text(frm, height=10, width=50, state="disabled")
txt_out.pack(fill="both", expand=True)

root.mainloop()
