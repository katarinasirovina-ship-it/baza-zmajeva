import streamlit as st

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    dict(st.secrets["gcp_service_account"]),
    scopes=SCOPES
)

client = gspread.authorize(credentials)

SHEET_ID = "1P00-mNFtA5mJOmQU-vIElZa91U4_O8P53-EcZxo-gfk"

spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.sheet1

st.set_page_config(
    page_title="Baza zmajeva",
    page_icon="🐉"
)

st.title("🐉 BAZA ZMAJEVA")

st.write("Dobrodošli u bazu zmajeva iz svijeta Westerosa!")

st.subheader("O aplikaciji")

st.write(
    "Ova aplikacija omogućuje pregled, pretraživanje, "
    "filtriranje, dodavanje, brisanje i sortiranje zmajeva."
)

# Učitavanje podataka iz Google Sheetsa
podaci = worksheet.get_all_records()
df = pd.DataFrame(podaci)

st.subheader("🐲 Popis zmajeva")
st.dataframe(df, use_container_width=True)

st.subheader("🔎 Filtriranje zmajeva")

pretraga = st.text_input("Pretraži zmaja po imenu:")

odabrani_spol = st.selectbox(
    "Odaberi spol zmaja:",
    ["Svi", "Muški", "Ženski"]
)

if odabrani_spol == "Svi":
    filtrirani_podaci = df
else:
    filtrirani_podaci = df[df["SPOL"] == odabrani_spol]

if pretraga:
    filtrirani_podaci = filtrirani_podaci[
        filtrirani_podaci["IME"].str.contains(pretraga, case=False, na=False)
    ]

st.dataframe(filtrirani_podaci, use_container_width=True)

st.subheader("➕ Dodaj novog zmaja")

with st.form("forma_zmaj"):
    ime = st.text_input("Ime zmaja")
    spol = st.selectbox("Spol", ["Muški", "Ženski"])
    boja = st.text_input("Boja")
    jahac = st.text_input("Jahač")
    godina = st.text_input("Godina rođenja")
    snaga = st.slider("Snaga", 1, 10)

    dodaj = st.form_submit_button("Dodaj zmaja")

if dodaj:
    novi_id = len(df) + 1

    worksheet.append_row([
        novi_id,
        ime,
        spol,
        boja,
        jahac,
        snaga,
        godina
    ])

    st.success("Zmaj je uspješno dodan! 🐉")

    st.subheader("🗑️ Obriši zmaja")

zmaj_za_brisanje = st.selectbox(
    "Odaberi zmaja kojeg želiš obrisati:",
    df["IME"].tolist()
)

if st.button("Obriši zmaja"):
    red = df[df["IME"] == zmaj_za_brisanje].index[0] + 2
    worksheet.delete_rows(red)

    st.success(f"Zmaj {zmaj_za_brisanje} je uspješno obrisan! 🗑️")


st.subheader("📊 Sortiranje zmajeva")

nacin_sortiranja = st.selectbox(
    "Odaberi način sortiranja:",
    [
        "Od najjačeg prema najslabijem",
        "Od najslabijeg prema najjačem"
    ]
)

if nacin_sortiranja == "Od najjačeg prema najslabijem":
    sortirani_podaci = df.sort_values(by="SNAGA 1-10", ascending=False)
else:
    sortirani_podaci = df.sort_values(by="SNAGA 1-10", ascending=True)

st.dataframe(sortirani_podaci, use_container_width=True)

st.subheader("🏆 Najjači i najslabiji zmaj")

najveca_snaga = df["SNAGA 1-10"].max()
najmanja_snaga = df["SNAGA 1-10"].min()

najjaci = df[df["SNAGA 1-10"] == najveca_snaga]
najslabiji = df[df["SNAGA 1-10"] == najmanja_snaga]

st.write(
    f"🏆 Najjači zmajevi (snaga {najveca_snaga}): "
    + ", ".join(najjaci["IME"].tolist())
)

st.write(
    f"🔻 Najslabiji zmajevi (snaga {najmanja_snaga}): "
    + ", ".join(najslabiji["IME"].tolist())
)