# sfx.json → sfx.wav — tanıtım filminin müziği ve efektleri. Hazır ses dosyası yok; her şey sentez.
# Müzik: 120 BPM, sahne başına akor değişen pad, sidechain'li kick, hi-hat, sub bas; kapanışta büyük vuruş.
# Efektler: whoosh, pop, tık, zil, tarama, yükselen ton, uyarı; zamanları promo.html'deki window.SFX'ten gelir.
import json, os, numpy as np, wave
from scipy.signal import butter, sosfilt

d = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(d, 'sfx.json'))); EV, BT, DUR = J['events'], J['beats'], J['dur']
SR = 48000; N = int(SR * DUR) + SR * 3
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)
T = lambda n: np.arange(n) / SR
def add(t, x, g=1.0, pan=0.0):
    i = int(t * SR); n = min(len(x), N - i)
    if n <= 0: return
    L[i:i + n] += x[:n] * g * np.sqrt(0.5 * (1 - pan)) * 1.414; R[i:i + n] += x[:n] * g * np.sqrt(0.5 * (1 + pan)) * 1.414
def env(n, a, dec): t = T(n); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / dec)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, f1, f2, o=2): return sosfilt(butter(o, [f1, f2], 'band', fs=SR, output='sos'), x)
def hz(n): return 440 * 2 ** ((n - 69) / 12)

S2, S7 = BT['start'], BT['hit']; beat = 60 / BT['bpm']
SC = [0, S2, 10.6, 16.9, 23.7, 30.6, S7, DUR + 2]
# ── pad akorları (MIDI) ──
CH = [[50, 57, 64, 66], [47, 54, 57, 62], [43, 50, 54, 59], [50, 57, 62, 66], [45, 52, 57, 61], [43, 50, 55, 59, 62], [38, 45, 50, 54, 57, 64]]
BASS = [None, 35, 31, 38, 33, 31, 26]
pad = np.zeros(N); sub = np.zeros(N)
for k, notes in enumerate(CH):
    a, b = SC[k], SC[k + 1]; i0, i1 = int(max(0, a - 0.4) * SR), min(N, int((b + 0.8) * SR)); n = i1 - i0; t = T(n)
    fade = np.minimum(1, t / 0.6) * np.minimum(1, (n - np.arange(n)) / (0.8 * SR))
    x = np.zeros(n)
    for m in notes:
        f = hz(m)
        for det in (-0.0018, 0.0018):
            ph = rng.uniform(0, 6.28)
            x += (np.sin(2 * np.pi * f * (1 + det) * t + ph) + 0.35 * np.sin(4 * np.pi * f * (1 + det) * t + ph) + 0.12 * np.sin(6 * np.pi * f * t + ph))
    x *= (1 + 0.12 * np.sin(2 * np.pi * 0.23 * t)) / len(notes)
    pad[i0:i1] += x * fade * (0.55 if k == 0 else 0.8 if k < 6 else 1.1)
    if BASS[k]:
        fb = hz(BASS[k]); sub[i0:i1] += np.sin(2 * np.pi * fb * t) * fade * (0.9 if k < 6 else 1.2)
pad = lp(pad, 2600)
# ── sidechain zarfı + kick ──
duck = np.ones(N); kick = np.zeros(N)
nk = int(0.45 * SR); tk = T(nk); fk = 42 + 90 * np.exp(-tk / 0.035)
K = np.sin(2 * np.pi * np.cumsum(fk) / SR) * np.exp(-tk / 0.16) + 0.25 * lp(rng.standard_normal(nk), 3000) * np.exp(-tk / 0.008)
bt = S2; bi = 0
while bt < S7 - 0.01:
    i = int(bt * SR); build = bt > 30.6
    if not (26.9 < bt < 27.9):                        # kısa nefes
        kick[i:i + nk] += K[:N - i] * (1.0 if bt > 10.6 else 0.75)
        m = int(0.32 * SR); duck[i:i + m] = np.minimum(duck[i:i + m], 1 - 0.55 * np.exp(-T(m) / 0.12)[:len(duck[i:i + m])])
    bt += beat; bi += 1
# ── hi-hat ve clap ──
hat = np.zeros(N); nh = int(0.05 * SR); H = hp(rng.standard_normal(nh), 7000, 4) * np.exp(-T(nh) / 0.012)
t = 10.6 + beat / 2
while t < S7 - 0.1:
    if not (26.9 < t < 27.9): hat[int(t * SR):int(t * SR) + nh] += H * (0.9 if t > 23.7 else 0.6)
    t += beat
if True:
    nc = int(0.22 * SR); C = bp(rng.standard_normal(nc), 900, 4000) * np.exp(-T(nc) / 0.05)
    t = 23.7 + beat
    while t < S7 - 0.1:
        if not (26.9 < t < 27.9): add(t, C, 0.18)
        t += 2 * beat
# 30.6–35.3 arası 16'lık hat ile yükseliş
t = 30.6 + beat / 4
while t < S7 - 0.1:
    hat[int(t * SR):int(t * SR) + nh] += H * 0.35 * (0.5 + (t - 30.6) / 5); t += beat / 2
mus_L = (pad * duck * 0.33 + sub * duck * 0.32 + kick * 0.75 + hat * 0.12)
mus_R = mus_L.copy()
L += mus_L; R += mus_R

# ── efektler ──
PENTA = [76, 79, 81, 83, 86, 88]
for e in EV:
    k, t, v = e['k'], e['t'], e.get('v', 0)
    if k == 'whoosh':
        n = int(0.9 * SR); x = rng.standard_normal(n); tt = T(n); pos = 0.55
        e_ = np.where(tt < pos, (tt / pos) ** 2, np.exp(-(tt - pos) / 0.12))
        y = np.zeros(n)
        for j in range(8):  # parça parça kayan bant geçiren
            a, b = j * n // 8, (j + 1) * n // 8; fc = 400 + 2600 * np.sin(np.pi * (j + 0.5) / 8)
            y[a:b] = bp(x, fc * 0.6, min(fc * 1.6, 20000))[a:b]
        add(t - pos, y * e_, 0.22 if v == 1 else 0.12, pan=-0.3 if v == 2 else 0.2)
    elif k == 'pop':
        n = int(0.12 * SR); tt = T(n); f = 300 + 700 * np.exp(-tt / 0.02)
        add(t, np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.03), 0.28, pan=-0.6 + v * 0.3)
    elif k == 'click':
        n = int(0.04 * SR); add(t, hp(rng.standard_normal(n), 2500) * env(n, 0.0005, 0.006) + np.sin(2 * np.pi * 2200 * T(n)) * env(n, 0.0005, 0.01) * 0.4, 0.35)
    elif k == 'ding':
        f = hz(PENTA[v % len(PENTA)]); n = int(1.6 * SR); tt = T(n)
        x = np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.5) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt / 0.18) + 0.2 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt / 0.07)
        add(t, x * np.minimum(1, tt / 0.002), 0.16, pan=0.3)
    elif k == 'scan':
        n = int(1.3 * SR); tt = T(n); f = 500 * 2 ** (tt / 1.3 * 2)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / 1.3) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * tt))
        add(t, x, 0.05)
    elif k in ('rise', 'swell'):
        n = int(1.8 * SR); tt = T(n); f = (220 if k == 'rise' else 330) * 2 ** (tt / 1.8 * 1.5)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (tt / 1.8) ** 1.5 * np.exp(-np.maximum(0, tt - 1.6) / 0.05)
        add(t, x, 0.05)
    elif k == 'tick':
        n = int(0.08 * SR); add(t, np.sin(2 * np.pi * (1200 + 120 * v) * T(n)) * env(n, 0.0005, 0.015), 0.14, pan=-0.2 + 0.1 * v)
    elif k == 'alert':
        n = int(0.25 * SR); tt = T(n); add(t, (np.sin(2 * np.pi * 523 * tt) + 0.5 * np.sin(2 * np.pi * 622 * tt)) * env(n, 0.004, 0.07), 0.1)
    elif k == 'shimmer':
        for j, m in enumerate([74, 78, 81, 85, 88]):
            n = int(2.2 * SR); tt = T(n); add(t + j * 0.16, np.sin(2 * np.pi * hz(m) * tt) * env(n, 0.01, 0.7), 0.05, pan=-0.5 + j * 0.25)
    elif k == 'rise2':
        n = int(1.4 * SR); tt = T(n); x = hp(rng.standard_normal(n), 1500) * (tt / 1.4) ** 3
        f = 200 * 2 ** (tt / 1.4 * 2.5); x += 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * (tt / 1.4) ** 2
        add(t - 1.15, x, 0.12)
    elif k == 'hit':
        n = int(3.5 * SR); tt = T(n); fk2 = 38 + 110 * np.exp(-tt / 0.05)
        x = np.sin(2 * np.pi * np.cumsum(fk2) / SR) * np.exp(-tt / 0.5) * 1.2
        x += lp(rng.standard_normal(n), 9000) * np.exp(-tt / 0.9) * 0.25
        for m in [50, 57, 62, 66, 69, 76]:
            x += 0.18 * np.sin(2 * np.pi * hz(m) * tt) * np.exp(-tt / 1.8)
        add(t, x, 0.55)

out = np.stack([L, R], 1)[:int(SR * DUR)]
fi = int(0.5 * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(1.0 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
out = np.tanh(out * 1.1) * 0.9
out *= 0.63 / max(1e-9, np.abs(out).max())   # ≈ −14 LUFS
pcm = (out * 32767).astype('<i2')
w = wave.open(os.path.join(d, 'sfx.wav'), 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('sfx.wav', len(EV), 'efekt,', DUR, 'sn')
