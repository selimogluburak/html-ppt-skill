# Verimlilik ve Kârlılık — motion graphics tanıtımı

`Verimlilik_ve_Karlilik_Yeni_Tasarim_1.html` ekranlarının 31 saniyelik tanıtım filmi. Tarz:
[yasinozmeen/animasyon-stil-katalogu](https://github.com/yasinozmeen/animasyon-stil-katalogu) → **19 · Veri görselleştirme**
(`stiller/veri`): editoryal veri gazeteciliği, haber sitesi grafiği.

Tarzdan alınanlar: gren dokulu kâğıt zemin, Source Serif 4 başlık + Libre Franklin metin, maskeden yükselen başlık satırları,
vurgulanan sözcüğün altını çizen çizgi, kendini çizen grafikler, uçta sayan etiket, lejant yerine doğrudan etiketler,
parantezli not + büyük sayı, "Temsili veri" kaynak satırı, sahneler arası sayfa kaydırma (scrollytelling), sinüs sentezli tık sesleri.
Renkler ürünün kimliğinden: lacivert `#1F3A5F`, altın `#FDB913`, olumlu yeşil / olumsuz kırmızı.

| Süre | Bölüm | Grafik |
|---|---|---|
| 0–3 sn | Giriş | Başlık + dört bölümlük içindekiler cetveli |
| 3–9 sn | 01 · Genel Görünüm | Günlük portföy net kârı çizgisi (8,39 → 8,9 mn TL, %6,1), sinyal birim kareleri |
| 9–16 sn | 02 · Müşteri Özeti | 2024→2025 dambıl grafiği (beş kalem, %16–19), sağlık skoru ve cüzdan payı halkaları |
| 16–22 sn | 03 · Kârlılık | Şelale grafiği (2,11 M → 2,09 M) ve genel toplam denklemi |
| 22–28 sn | 04 · Taahhüt İzleme | Gerçekleşme çubukları, %100 hedef çizgisi, katkı sütunu (113.702,05 TL) |
| 28–31 sn | Kapanış | Ürün işareti |

Tüm rakamlar kaynak HTML'deki örnek verilerdir. Genel Görünüm'deki günlük çizgi, ekranın kendisindeki gibi temsilidir
(yalnız başlangıç, bitiş ve değişim değerleri gerçek ekrandan).

## Dosyalar
- `verimlilik-tanitim.mp4` — 1920×1080, 30 fps, H.264 + AAC ses
- `anim.html` — tarayıcıda açınca oynar (boşluk: duraklat, ←/→: 1 sn atla). `?render` ile açılınca `window.draw({t})` kare döndürür.
- `render.mjs`, `sfx.py`, `build.sh` — yeniden üretim: Node + global `playwright`, Python 3 + `numpy`, `ffmpeg`.
  `./build.sh` (ffmpeg PATH'te değilse `FFMPEG=/yol/ffmpeg ./build.sh`).

Yazı tipleri Google Fonts'tan (SIL Open Font License), `fonts/` içinde.
