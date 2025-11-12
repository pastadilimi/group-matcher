# -*- coding: utf-8 -*-
# file: eslestir_tkinter.py

import random
import csv
from collections import Counter, defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from PIL import Image, ImageTk  # yalnızca logo için; istemezsen bu kısmı kaldırabilirsin

APP_TITLE = "Rastgele Eşleştirici (Masaüstü)"

# ===================== KELİME BANKALARI (≥30) =====================
FLOWERS_TR = [
    "Gül","Lale","Sümbül","Manolya","Kardelen","Zambak","Nergis","Menekşe","Kasımpatı","Karanfil",
    "Leylak","Şakayık","Ortanca","Gelincik","Lavanta","Papatya","Sarı Papatya","Yasemin","Hanımeli","Begonya",
    "Orkide","Kamelya","Fesleğen","Sardunya","Açelya","Nilüfer","Zinya","Petunya","Gardenya","Lotus",
    "Mimoza","Hercai Menekşe","Deve Tabanı","Rüzgargülü","Krizantem","Süsen","İris","Gelinçiçeği","Ortancagül","Camgüzeli"
]
COLORS_TR = [
    "Kızıl","Lacivert","Zümrüt","Kehribar","Mor","Turkuaz","Altın","Gümüş","Gece Mavisi","Fuşya",
    "Fildişi","Sedef","Antrasit","Koyu Gri","Şarap","Bakır","Safir","Yakut","Ametist","Topaz",
    "Lavanta","Şampanya","Kiraz","Kömür","Gök Mavisi","Krem","Pastel Pembe","Mint","Kül","Okyanus",
    "Mistik Mor","Ay Taşı","Orkide Tonu","Kuma","Pusu","Orman Yeşili","Bordo","Kestane","Bej","Opal"
]
CITIES_TR = [
    "İstanbul","Ankara","İzmir","Bursa","Eskişehir","Antalya","Mersin","Van","Trabzon","Gaziantep",
    "Konya","Adana","Samsun","Kayseri","Diyarbakır","Şanlıurfa","Mardin","Hatay","Balıkesir","Çanakkale",
    "Tekirdağ","Edirne","Kocaeli","Sakarya","Bolu","Rize","Aydın","Muğla","Artvin","Giresun",
    "Ordu","Malatya","Elazığ","Erzurum","Kars","Isparta","Karabük","Zonguldak","Manisa","Denizli"
]
MYTH_TR = [
    "Anka","Hydra","Pegasus","Feniks","Medusa","Gaia","Eros","Nemesis","Kheiron","Poseidon",
    "Hermes","Athena","Ares","Hera","Zeus","Apollo","Artemis","Hades","Perseus","Odysseus",
    "Valhalla","Odin","Thor","Loki","Freya","Tyr","Heimdall","Fenrir","Sleipnir","Yggdrasil",
    "Kiklop","Minotor","Siren","Nemea","Harpya","Gorgon","Kassandra","Midas","Ariadne","Demeter"
]
SPACE_TR = [
    "Nebula","Orion","Andromeda","Pulsar","Yörünge","Süpernova","Galaksi","Kuyruklu Yıldız","Karanlık Madde","Olay Ufku",
    "Kuazar","Helios","Astro","Asteroit Kuşağı","Işık Yılı","Aurora","Kozmik Toz","Samanyolu","Kepler","Voyager",
    "Apollo","Gemini","Lagrange","Nova","Kara Delik","Yıldız Tozu","Magellan","Hubble","Cassini","Titan",
    "Europa","Io","Phobos","Deimos","Mare Tranquillitatis","Terminatör","Güneş Rüzgarı","Plazma","Işıkyuvar","Spektrum"
]
SEASONS_TR = [
    "İlkbahar","Yaz","Sonbahar","Kış","Bahar","Mevsim","Ekinoks","Gündönümü","Solstis","Ayaz",
    "Serinlik","Poyraz","Lodos","Kırağı","Çise","Çiğ","Tomurcuk","Hasat","Biçim","Yaprak Dökümü",
    "Kar Taneleri","Dalgın Güneş","Yakıcı Öğle","Meltem","Ilık Rüzgar","Gümrah","Sarı Yaprak","Kasım Rüzgarı","Kavurucu","Kış Güneşi",
    "Dolunay","Hilal","Yaz Yağmuru","Gök Gürültüsü","Fırtına","Sükunet","Çöl Sıcağı","Orman Serini","Kıyı Esintisi","Dağ Çiyi"
]
XMAS_TR = [
    "Noel","Yılbaşı","Kardan Adam","Çam","Zencefilli","Kırmızı Çorap","Çan","Işıklar","Kuzey","Aurora",
    "Rudolph","Hediye","Kar Tanesi","Mistletoe","Süsleme","Aralık","Şömine","Tarçın","Sıcak Şarap","Kestane",
    "Buz Pateni","Kardan Melek","Mutlu Yıllar","Kutup","Kış Pazarı","Ziyafet","Geyik","Kardan İz","Zil Sesi","Karlı Geceler",
    "Elf","Noel Baba","Kuzey Işıkları","Kardan Yolu","Yaldız","Nane Şekeri","Gelin Teli","Yılbaşı Kurabiyesi","Yeni Sayfa","Yeni Umut"
]
HALLOWEEN_TR = [
    "Kabak","Balta Gece","Gulyabani","Hayalet","Cadı","Büyü","Zindan","Kara Kedi","Kafatası","Fısıltı",
    "Sis","Mezarlık","Gecenin Ruhu","Lanethane","Gölgeler","Efsun","Mum Işığı","Karanlık Alley","Yarasa","Kara Şato",
    "Kanlı Ay","Kül","Kuzgun","Kurt Adam","Dehliz","Ektoplazma","Korku Tüneli","İskelet","Vampir","Grim",
    "Kasvet","Lantern","Kabak Feneri","Sihirli Kapı","Karanlık Bahçe","Perde","Zifiri","İllet","Kuytu","Sırlı"
]
PASTRY_TR = [
    "Kurabiye","Cookie","Bademli","Fıstıklı","Tart","Eclair","Profiterol","Krokan","Karamel","Kremalı",
    "Sufle","Brownie","Cheesecake","Crème","Glaze","Ganaj","Frambuaz","Limonlu","Meyveli","Tarçınlı",
    "Kakaolu","Çikolatalı","Kremşanti","Pişmaniye","Lokum","Şerbetli","Pasta Kreması","Mereng","Karamelli","Çıtır",
    "Napolyon","Mille-feuille","Pâte à choux","Sablé","Peynirli","Kestaneli","Beyaz Çikolata","Fıstık Ezmeli","Karamelize","Biscotti"
]
CYBORG_TR = [
    "Cyborg","Chromium","Neon Bilek","Analog","Biyonik","Siber","Katot","Hologram","Photon","Mecha",
    "Exo","Nanite","Synth","Neural","Retro-Tech","Grafen","Lityum","Firmware","Kernel","Quantum",
    "Socket","Bus","Matrix","Vector","Pipeline","Protocol","Patch","Core","Overclock","Meta",
    "Servo","Gyro","Optik","Lazer","Diyot","Transistör","Teknofiber","Hiperlink","Bootstrap","Firmware-2"
]

THEME_BANKS = {
    "çiçek": FLOWERS_TR,
    "renk": COLORS_TR,
    "şehir": CITIES_TR,
    "mitoloji": MYTH_TR,
    "uzay": SPACE_TR,
    "mevsimler": SEASONS_TR,
    "yılbaşı": XMAS_TR,
    "halloween": HALLOWEEN_TR,
    "pastane": PASTRY_TR,
    "cyborg": CYBORG_TR,
}

ROCK_WORDS  = ["Riot","Rebels","Voltage","Amplifier","Echoes","Stones","Road","Route","Garage","Underground","Static","Feedback","Breakers","Storm","Wired"]
METAL_WORDS = ["Forge","Anvil","Raven","Steel","Abyss","Legion","Obsidian","Grim","Hammer","Temple","Crypt","Doom","Leviathan","Berserk","Citadel"]
INDIE_WORDS = ["Parade","Club","Corners","Dreams","Lights","Voyage","Youth","Sundays","Polaroid","Paper","Caravan","Garden","Canvas","Arc","Ghosts"]
SYNTH_WORDS = ["Neon","Waves","Drive","Retro","Arcade","Circuit","Pixel","Static","Stereo","Supernova","VHS","Analog","Pulse","Laser","Midnight"]

PATTERNS = [
    "{N} {G}", "The {N} {G}", "{N} & the {G}", "{N} Overdrive", "{N} Echo",
    "{N} Kolektif", "{N} ve {G}", "{N} Yüksek Gerilim", "{N1} {N2}",
    "{N1} of {N2}", "The {N1} of {N2}"
]

def words_for_genre(genre: str):
    g = (genre or "rock").lower()
    if g == "metal": return METAL_WORDS
    if g == "indie": return INDIE_WORDS
    if g == "synthwave": return SYNTH_WORDS
    return ROCK_WORDS

# ===================== ÇEKİRDEK İŞLEVLER =====================
def parse_names(raw: str):
    if not raw: return []
    raw = raw.replace(",", "\n")
    return [n.strip() for n in raw.splitlines() if n.strip()]

def handle_duplicates(names, mode="warn"):
    counts = Counter(names)
    dups = [n for n, c in counts.items() if c > 1]
    if mode == "warn":
        if dups:
            messagebox.showwarning(
                "Aynı İsimler",
                "Aynı isim(ler) tespit edildi: " + ", ".join(dups) +
                "\nLütfen ikinci ad/soyad gibi ayırt edici bilgi ekleyin."
            )
        return names
    # number
    seen = defaultdict(int)
    out = []
    for n in names:
        if counts[n] > 1:
            seen[n] += 1
            out.append(f"{n} ({seen[n]})")
        else:
            out.append(n)
    return out

def make_groups(names, allow_trio=True):
    rng = random.Random()
    names = names[:]
    if len(names) < 2:
        return [[n] for n in names]
    rng.shuffle(names)
    groups, i = [], 0
    while i < len(names):
        if i + 1 < len(names):
            groups.append([names[i], names[i+1]])
            i += 2
        else:
            if allow_trio and groups:
                groups[-1].append(names[i])
            else:
                groups.append([names[i]])
            i += 1
    return groups

def band_names_from_tags(n: int, tags, genre: str):
    chosen_banks = [THEME_BANKS[t] for t in tags if t in THEME_BANKS]
    if not chosen_banks:
        chosen_banks = [THEME_BANKS["çiçek"]]
    genre_words = words_for_genre(genre)
    rng = random.Random()
    out, used = [], set()

    def pick_noun():
        bank = rng.choice(chosen_banks)
        return rng.choice(bank)

    while len(out) < n:
        patt = rng.choice(PATTERNS)
        if "{N1}" in patt and "{N2}" in patt:
            n1, n2 = pick_noun(), pick_noun()
            tries = 0
            while n2 == n1 and tries < 5:
                n2 = pick_noun(); tries += 1
            g  = rng.choice(genre_words)
            name = patt.replace("{N1}", n1).replace("{N2}", n2).replace("{G}", g)
        else:
            noun = pick_noun()
            g    = rng.choice(genre_words)
            name = patt.replace("{N}", noun).replace("{G}", g)
        if name not in used:
            used.add(name)
            out.append(name)
    return out

# ===================== TKINTER UYGULAMASI =====================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x650")
        self.minsize(900, 600)

        # ttk tema
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.group_names = []
        self.groups = []
        self.rename_remaining = 3

        self._build_ui()

    def _build_ui(self):
        # Üst bar: logo + başlık
        top = ttk.Frame(self, padding=(12, 10))
        top.pack(side=tk.TOP, fill=tk.X)

        # logo (opsiyonel)
        self.logo_label = ttk.Label(top)
        self.logo_label.pack(side=tk.LEFT, padx=(0, 10))
        self._load_logo()

        ttk.Label(top, text="Rastgele Grup Eşleştirici", font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)

        # Ana bölünme
        main = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

        # Sol panel (ayarlar)
        left = ttk.Frame(main, padding=10)
        main.add(left, weight=1)

        ttk.Label(left, text="İsimler (satır satır veya virgülle):").pack(anchor="w")
        self.txt_names = tk.Text(left, height=14, wrap="word")
        self.txt_names.pack(fill=tk.BOTH, expand=True, pady=4)
        self.txt_names.insert("1.0",
            "Özgün\nDeniz\nAyşe\nMehmet\nEce\nBurak\nZeynep\nAli\nSelin\nKerem\nCan\nElif"
        )

        dup_frame = ttk.LabelFrame(left, text="Aynı İsimler", padding=8)
        dup_frame.pack(fill=tk.X, pady=6)
        self.dup_mode = tk.StringVar(value="warn")
        ttk.Radiobutton(dup_frame, text="Uyarı ver", value="warn", variable=self.dup_mode).pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(dup_frame, text="Ayrı kişi say (numaralandır)", value="number", variable=self.dup_mode).pack(side=tk.LEFT, padx=4)

        self.allow_trio = tk.BooleanVar(value=True)
        ttk.Checkbutton(left, text="Tek kişi kalırsa 3'lü grup yap", variable=self.allow_trio).pack(anchor="w", pady=(2,8))

        # Temalar
        theme_frame = ttk.LabelFrame(left, text="Tema Etiketleri (Ctrl ile çoklu seç)", padding=8)
        theme_frame.pack(fill=tk.BOTH, expand=False, pady=6)
        self.lst_themes = tk.Listbox(theme_frame, selectmode=tk.MULTIPLE, height=8, exportselection=False)
        for k in THEME_BANKS.keys():
            self.lst_themes.insert(tk.END, k)
        self.lst_themes.pack(fill=tk.X)
        # varsayılan seçili
        self.lst_themes.selection_set(0)

        # Tür
        genre_frame = ttk.Frame(left)
        genre_frame.pack(fill=tk.X, pady=6)
        ttk.Label(genre_frame, text="Müzik türü:").pack(side=tk.LEFT)
        self.genre = tk.StringVar(value="rock")
        ttk.Combobox(genre_frame, textvariable=self.genre, values=["rock","metal","indie","synthwave"], width=12, state="readonly").pack(side=tk.LEFT, padx=6)

        # Butonlar
        btns = ttk.Frame(left)
        btns.pack(fill=tk.X, pady=8)
        ttk.Button(btns, text="🎯 Grupla", command=self.on_match).pack(side=tk.LEFT)
        ttk.Button(btns, text="♻️ Grup Adlarını Değiştir", command=self.on_rename).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="⬇️ CSV Kaydet", command=self.on_save_csv).pack(side=tk.LEFT, padx=6)

        self.lbl_rename = ttk.Label(left, text="Kalan grup adı değiştirme hakkı: 3")
        self.lbl_rename.pack(anchor="w", pady=(2,0))

        # Sağ panel (sonuçlar)
        right = ttk.Frame(main, padding=10)
        main.add(right, weight=2)

        ttk.Label(right, text="Sonuçlar", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.result = tk.Text(right, height=18, wrap="word")
        self.result.pack(fill=tk.BOTH, expand=True, pady=(4,0))

        ttk.Label(right, text="İpucu: Çoklu tema için Ctrl (Mac'te Cmd) ile birden fazlasını seç.").pack(anchor="w", pady=(6,0))

    def _load_logo(self):
        # assets/pixel.png veya assets/pixerl.png
        for name in ("assets/pixel.png", "assets/pixerl.png"):
            p = Path(name)
            if p.exists():
                try:
                    img = Image.open(p).resize((96, 96), Image.NEAREST)
                    self.logo_img = ImageTk.PhotoImage(img)
                    self.logo_label.configure(image=self.logo_img)
                except Exception:
                    pass
                break

    def read_names(self):
        txt = self.txt_names.get("1.0", tk.END)
        names = parse_names(txt)
        names = handle_duplicates(names, mode=self.dup_mode.get())
        return names

    def selected_tags(self):
        idxs = self.lst_themes.curselection()
        return [self.lst_themes.get(i) for i in idxs]

    def on_match(self):
        names = self.read_names()
        if len(names) < 2:
            messagebox.showwarning("Uyarı", "Lütfen en az iki isim girin.")
            return
        self.groups = make_groups(names, allow_trio=self.allow_trio.get())
        self.group_names = band_names_from_tags(len(self.groups), self.selected_tags(), self.genre.get())
        self.rename_remaining = 3
        self.refresh_output()
        self.lbl_rename.configure(text=f"Kalan grup adı değiştirme hakkı: {self.rename_remaining}")

    def on_rename(self):
        if not self.groups:
            messagebox.showinfo("Bilgi", "Önce ‘Grupla’ butonuna basın.")
            return
        if self.rename_remaining <= 0:
            messagebox.showerror("Bitti", "Grup adlarını değiştirme hakkınız bitti (maks. 3).")
            return
        self.group_names = band_names_from_tags(len(self.groups), self.selected_tags(), self.genre.get())
        self.rename_remaining -= 1
        self.refresh_output()
        self.lbl_rename.configure(text=f"Kalan grup adı değiştirme hakkı: {self.rename_remaining}")

    def refresh_output(self):
        self.result.delete("1.0", tk.END)
        if not self.groups:
            return
        gnames = self.group_names or [f"Grup {i+1}" for i in range(len(self.groups))]
        for i, g in enumerate(self.groups, start=1):
            label = gnames[i-1] if i-1 < len(gnames) else f"Grup {i}"
            self.result.insert(tk.END, f"{label}: " + " — ".join(g) + "\n")

    def on_save_csv(self):
        if not self.groups:
            messagebox.showinfo("Bilgi", "Kaydetmek için önce grupları oluşturun.")
            return
        gnames = self.group_names or [f"Grup {i+1}" for i in range(len(self.groups))]
        path = filedialog.asksaveasfilename(
            title="CSV olarak kaydet",
            defaultextension=".csv",
            filetypes=[("CSV Files","*.csv")]
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Grup","Üye"])
            for i, g in enumerate(self.groups, start=1):
                label = gnames[i-1] if i-1 < len(gnames) else f"Grup {i}"
                for member in g:
                    writer.writerow([label, member])
        messagebox.showinfo("Kaydedildi", f"CSV kaydedildi:\n{path}")

if __name__ == "__main__":
    try:
        App().mainloop()
    except Exception as e:
        messagebox.showerror("Hata", str(e))
