# Verimlilik ve Kârlılık — ürün tanıtım filmi

40 saniyelik, müzikli ürün tanıtımı (1920×1080, 30 fps, H.264 + AAC, −14 LUFS). Sunum değil, ürün lansmanı dili:
gerçek ekran görüntüleri 3D uzayda, sürekli kamera hareketi, ekrandan kopup öne çıkan parçalar, imleçle etkileşim.

| Süre | Bölüm | Ne oluyor |
|---|---|---|
| 0–4 sn | Açılış | "Bugün nereye bakmalıyım?" |
| 4–11 sn | Portföy özeti | Genel Görünüm ekranı 3D'de süzülür, kamera hero kartına dalar, beş sinyal kutucuğu ekrandan yükselir |
| 11–17 sn | Akıllı öneriler | Müşteri kartı taranır, sinyal şeridi karttan ayrılır: sinyal ⟶ önerilen ürün ("Öneri hazır") |
| 17–24 sn | Görev takibi | Günlük Bülten görev paneline dönüşür; imleç görevi atar, bir görevi tamamlar, ilerleme dolar |
| 24–31 sn | Taahhüt durumu | Genel gerçekleşme halkası %66'ya dolar, beş taahhüdün çubukları, riskli satır nabız atar, katkı sayar |
| 31–35 sn | Dört ekran | Genel · Müşteri · Kârlılık · Taahhüt ekranları 3D karuselde |
| 35–40 sn | Kapanış | Ürün işareti, "Portföyü izlemeyin, yönetin." |

Rakamlar ve ekran görüntüleri `Verimlilik_ve_Karlilik_Yeni_Tasarim_1.html` dosyasından (örnek veri).
**Görev takibi paneli** kaynak HTML'de ayrı bir modül olarak yok; ürünün tasarım diliyle (renkler, yazı tipleri, durum rozetleri)
Günlük Bülten'deki iki öneriden türetilmiş bir canlandırmadır. Gerçek ekran geldiğinde `capture.mjs` ile değiştirilebilir.

## Dosyalar
- `verimlilik-tanitim.mp4`: film
- `promo.html`: tarayıcıda açınca oynar (boşluk: duraklat, ←/→: 2 sn atla); `?render` ile `window.seek(t)` kareyi kurar
- `ui/`: kaynak ekrandan 2x yakalanmış parçalar (`capture.mjs`)
- `render.mjs`: kareleri Chromium'da çizer; `sfx.py`: müzik ve efekt sentezi (120 BPM, hazır ses yok)
- `build.sh [kaynak.html]`: hepsini baştan üretir. Kaynak verilirse ekranlar yeniden yakalanır, tasarım değişince film kendini günceller.
  Gerekenler: Node + global `playwright`, Python 3 + `numpy` + `scipy`, `ffmpeg` (ya da `FFMPEG=/yol/ffmpeg`).

Yazı tipleri ürünle aynı: Fraunces, IBM Plex Sans, IBM Plex Mono (Google Fonts, SIL OFL), `fonts/` içinde.
