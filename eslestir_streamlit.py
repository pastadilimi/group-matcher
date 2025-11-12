import random
import io
import base64
from pathlib import Path
from collections import Counter, defaultdict
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Rastgele Eşleştirici", page_icon="🎲", layout="centered")

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

# Tür kelimeleri
ROCK_WORDS  = ["Riot","Rebels","Voltage","Amplifier","Echoes","Stones","Road","Route","Garage","Underground","Static","Feedback","Breakers","Storm","Wired"]
METAL_WORDS = ["Forge","Anvil","Raven","Steel","Abyss","Legion","Obsidian","Grim","Hammer","Temple","Crypt","Doom","Leviathan","Berserk","Citadel"]
INDIE_WORDS = ["Parade","Club","Corners","Dreams","Lights","Voyage","Youth","Sundays","Polaroid","Paper","Caravan","Garden","Canvas","Arc","Ghosts"]
SYNTH_WORDS = ["Neon","Waves","Drive","Retro","Arcade","Circuit","Pixel","Static","Stereo","Supernova","VHS","Analog","Pulse","Laser","Midnight"]

PATTERNS = [
    "{N} {G}",
    "The {N} {G}",
    "{N} & the {G}",
    "{N} Overdrive",
    "{N} Echo",
    "{N} Kolektif",
    "{N} ve {G}",
    "{N} Yüksek Gerilim",
    "{N1} {N2}",
    "{N1} of {N2}",
    "The {N1} of {N2}",
]

def words_for_genre(genre: str):
    g = (genre or "rock").lower()
    if g == "metal": return METAL_WORDS
    if g == "indie": return INDIE_WORDS
    if g == "synthwave": return SYNTH_WORDS
    return ROCK_WORDS

# ===================== Header (koda gömülü video) =====================
HEADER_CANDIDATES = ["assets/header.mp4", "assets/banner1.mp4", "assets/banner2.mp4"]

def render_header():
    for fp in HEADER_CANDIDATES:
        p = Path(fp)
        if p.exists():
            data = p.read_bytes()
            b64 = base64.b64encode(data).decode("utf-8")
            st.markdown(
                f"""
                <header style="position:relative;overflow:hidden;border-radius:14px;margin-bottom:16px">
                  <video autoplay loop muted playsinline
                         style="width:100%;height:auto;display:block;border-radius:14px;">
                    <source src="data:video/mp4;base64,{b64}" type="video/mp4">
                  </video>
                </header>
                """,
                unsafe_allow_html=True
            )
            return
    st.markdown(
        """
        <header style="height:140px;border-radius:14px;background:linear-gradient(135deg,#111,#222);margin-bottom:16px"></header>
        """,
        unsafe_allow_html=True
    )

# ===================== Success Video (gruplar oluşturulunca oynat) =====================
SUCCESS_VIDEO_CANDIDATES = [
    "assets/success.mp4",
    "assets/result.mp4",
    "assets/match_success.mp4",
    "assets/Başlıksız.mp4",
    "assets/Basliksiz.mp4"
]

def render_success_video():
    for fp in SUCCESS_VIDEO_CANDIDATES:
        p = Path(fp)
        if p.exists():
            data = p.read_bytes()
            b64 = base64.b64encode(data).decode("utf-8")
            st.markdown(
                f"""
                <div style="position:relative;overflow:hidden;border-radius:12px;margin-top:14px">
                  <video autoplay loop muted playsinline
                         style="width:100%;height:auto;display:block;">
                    <source src="data:video/mp4;base64,{b64}" type="video/mp4">
                  </video>
                </div>
                """,
                unsafe_allow_html=True
            )
            return

# ===================== Yardımcılar =====================
def parse_names(text: str):
    if not text: return []
    text = text.replace(",", "\n")
    return [n.strip() for n in text.splitlines() if n.strip()]

def handle_duplicates(names: list[str], mode: str = "warn"):
    counts = Counter(names)
    dups = [n for n, c in counts.items() if c > 1]
    if mode == "warn":
        if dups:
            st.warning("Aynı isim(ler) tespit edildi: " + ", ".join(dups) +
                       " — Lütfen ikinci ad/soyad gibi ayırt edici bilgi ekleyin.")
        return names
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
    groups = []
    i = 0
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

def band_names_from_tags(n: int, tags: list[str], genre: str):
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

def to_csv_bytes(groups, group_names=None):
    rows = []
    for i, g in enumerate(groups, start=1):
        label = group_names[i-1] if group_names and i-1 < len(group_names) else f"Grup {i}"
        for member in g:
            rows.append({"Grup": label, "Üye": member})
    df = pd.DataFrame(rows)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

# ===================== UI =====================
render_header()

with st.sidebar:
    # --- LOGO: Eşleştirici başlığının üstüne küçük ikon ---
    # (pixerl.png yazımına da tolerans verdik)
    logo_candidates = ["assets/pixel.png", "assets/pixerl.png"]
    for lp in logo_candidates:
        if Path(lp).exists():
            st.image(lp, width=80)
            break

    st.markdown("## Eşleştirici")
    st.caption("İsimleri alta satır satır ya da virgülle gir.")

    names_text = st.text_area(
    "İsimler", 
    value="", 
    height=220, 
    placeholder="Her satıra bir isim yazın (virgül de olur)…"
)

    st.markdown("### 👥 Aynı İsimler")
    dup_mode = st.radio(
        "Aynı isim girilirse",
        ["Uyarı ver", "Ayrı kişi say (numaralandır)"],
        index=0
    )
    dup_mode_value = "warn" if dup_mode == "Uyarı ver" else "number"

    allow_trio = st.checkbox("Tek kişi kalırsa 3'lü grup yap", value=True)

    st.markdown("### 🏷️ Tema Etiketleri (çoklu seçim)")
    THEME_OPTIONS = list(THEME_BANKS.keys())
    selected_tags = st.multiselect("Etiketler", THEME_OPTIONS, default=["çiçek"])

    st.markdown("### 🎧 Müzik Türü")
    GENRES = ["rock", "metal", "indie", "synthwave"]
    genre_pick = st.selectbox("Tür", GENRES, index=0)

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_match = st.button("🎯 Grupla")
    with col_btn2:
        btn_rename = st.button("♻️ Grup Adlarını Değiştir")

st.title("Rastgele Grup Eşleştirici")
st.caption("Tek eşleştirme üretir. Gruplar sabit kalır; **grup adlarını 3 kez** yenileyebilirsin.")

# Session
if "groups" not in st.session_state:
    st.session_state.groups = None
if "rename_remaining" not in st.session_state:
    st.session_state.rename_remaining = 3
if "group_names" not in st.session_state:
    st.session_state.group_names = None
if "play_success_video" not in st.session_state:
    st.session_state.play_success_video = False

# isimler + duplicate politikası
names = parse_names(names_text)
names = handle_duplicates(names, mode=dup_mode_value)

# Grupla
if btn_match:
    if len(names) < 2:
        st.warning("Lütfen en az iki isim girin.")
    else:
        st.session_state.groups = make_groups(names, allow_trio=allow_trio)
        st.session_state.group_names = band_names_from_tags(len(st.session_state.groups), selected_tags, genre_pick)
        st.session_state.rename_remaining = 3
        st.session_state.play_success_video = True
        st.success("✅ Gruplar oluşturuldu. Grup adları atandı (3 değişiklik hakkın var).")

# Grup adlarını değiştir
if btn_rename:
    if st.session_state.groups is None:
        st.info("Önce 'Grupla'ya bas.")
    else:
        if st.session_state.rename_remaining > 0:
            st.session_state.group_names = band_names_from_tags(len(st.session_state.groups), selected_tags, genre_pick)
            st.session_state.rename_remaining -= 1
            st.session_state.play_success_video = True  # yeniden adlandırmada da oynatmak istersen dursun
            st.success(f"🔁 Grup adları yenilendi. Kalan hak: {st.session_state.rename_remaining}")
        else:
            st.error("⛔ Grup adlarını değiştirme hakkın bitti (maks. 3).")

# Sonuçlar + CSV + Başarı videosu
if st.session_state.groups is not None:
    st.subheader("Sonuçlar")
    gnames = st.session_state.group_names or [f"Grup {i+1}" for i in range(len(st.session_state.groups))]
    for i, g in enumerate(st.session_state.groups, start=1):
        label = gnames[i-1] if i-1 < len(gnames) else f"Grup {i}"
        st.markdown(f"**{label}:** " + " — ".join(g))

    csv_bytes = to_csv_bytes(st.session_state.groups, gnames)
    st.download_button(
        "⬇️ CSV indir",
        data=csv_bytes,
        file_name="eslesmeler.csv",
        mime="text/csv",
        use_container_width=True
    )

    # başarı videosunu sayfanın en altında oynat
    if st.session_state.play_success_video:
        render_success_video()
else:
    st.info("İsimleri gir, temaları seç ve **Grupla**'ya bas.")
