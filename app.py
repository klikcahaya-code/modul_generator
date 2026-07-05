import streamlit as st
import requests
import json

# 1. Mengambil API Key dari Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = None

# Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="AI Generator Modul Ajar", page_icon="📝", layout="centered")

st.title("📝 Generator Modul Ajar Kurikulum Merdeka")
st.write("Buat perangkat ajar instan berbasis AI. Isi form di bawah ini!")

if not api_key:
    st.error("API Key belum dikonfigurasi di server. Silakan atur di Streamlit Secrets.")
else:
    # 2. Form Input untuk Guru
    mapel = st.text_input("Mata Pelajaran (Contoh: Matematika, IPAS, Bahasa Indonesia)")
    
    fase = st.selectbox("Fase / Kelas", [
        "Fase A / Kelas 1-2", 
        "Fase B / Kelas 3-4", 
        "Fase C / Kelas 5-6", 
        "Fase D / Kelas 7-9", 
        "Fase E / Kelas 10", 
        "Fase F / Kelas 11-12"
    ])
    
    materi = st.text_area("Topik atau Materi Pokok (Contoh: Penjumlahan Pecahan, Fotosintesis)")
    waktu = st.text_input("Alokasi Waktu (Contoh: 2 x 35 Menit)")

    # 3. Tombol Eksekusi
    if st.button("Generate Modul Ajar 🔥", type="primary"):
        if not mapel or not materi:
            st.warning("Mohon isi Mata Pelajaran dan Materi Pokok terlebih dahulu!")
        else:
            with st.spinner("Sedang merancang modul ajar standar Kemendikbud... Mohon tunggu..."):
                try:
                    # Alamat API Resmi Google Gemini (Jalur Langsung)
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    
                    # Instruksi Sistem agar hasil akurat
                    instruksi_sistem = (
                        "Anda adalah seorang fasilitator Kurikulum Merdeka yang sangat ahli. "
                        "Tugas Anda adalah menyusun Modul Ajar yang lengkap, sistematis, dan siap pakai. "
                        "Struktur modul harus terdiri dari: "
                        "1. Informasi Umum (Identitas, Kompetensi Awal, Profil Pelajar Pancasila, Sarana Prasarana). "
                        "2. Komponen Inti (Tujuan Pembelajaran, Pemahaman Bermakna, Pertanyaan Pemantik, Kegiatan Pembelajaran Lengkap Pendahuluan-Inti-Penutup). "
                        "3. Lampiran (Lembar Kerja Peserta Didik (LKPD) sederhana, dan Instrumen Asesmen)."
                    )

                    prompt_guru = f"""
                    Buatlah Modul Ajar dengan data berikut:
                    - Mata Pelajaran: {mapel}
                    - {fase}
                    - Materi Pokok: {materi}
                    - Alokasi Waktu: {waktu}
                    
                    Sajikan dalam format tulisan Markdown yang rapi, jelas, dan profesional.
                    """

                    # Menyusun data JSON sesuai standar API Gemini
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt_guru}]
                        }],
                        "systemInstruction": {
                            "parts": [{"text": instruksi_sistem}]
                        },
                        "generationConfig": {
                            "temperature": 0.7
                        }
                    }

                    headers = {"Content-Type": "application/json"}

                    # Menembak API secara langsung
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    res_json = response.json()

                    # Cek jika ada error dari Google
                    if "error" in res_json:
                        st.error(f"Error dari Google API: {res_json['error']['message']}")
                    else:
                        # Mengambil teks hasil generate
                        hasil_teks = res_json['candidates'][0]['content']['parts'][0]['text']
                        
                        # Menampilkan hasil ke layar
                        st.success("Selesai! Silakan salin modul di bawah ini:")
                        st.markdown(hasil_teks)
                        
                        # Fitur unduh sebagai teks
                        st.download_button(
                            label="Unduh Hasil (.txt)",
                            data=hasil_teks,
                            file_name=f"Modul_Ajar_{mapel.replace(' ', '_')}.txt",
                            mime="text/plain"
                        )

                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}")
