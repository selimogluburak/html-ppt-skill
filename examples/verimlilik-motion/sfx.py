# sfx.json → sfx.wav — veri tarzı: marimba benzeri yumuşak tıklar (veri noktası), not için "tok", kapanışta iki notalı akor.
# Hazır ses dosyası yok; her şey sinüs sentezi. Hışırtı/whoosh yok.
import json, numpy as np, wave, os, sys
SR = 48000; DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 31.0
d = os.path.dirname(os.path.abspath(__file__)); ev = json.load(open(os.path.join(d, 'sfx.json')))
out = np.zeros(int(SR * DUR) + SR)
def env(n, a=0.002, dec=0.05): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / dec)
def sine(n, f): return np.sin(2 * np.pi * f * np.arange(n) / SR)
def add(t, x, g): i = int(t * SR); out[i:i + len(x)] += x[:len(out) - i] * g
for e in ev:
    k, t, v = e['k'], e['t'], e.get('v') or 0
    if k == 'dot':    # çizgi yükseldikçe perde yükselir
        f = 523.25 * 2 ** (v / 12); n = int(0.35 * SR); add(t, (sine(n, f) + 0.25 * sine(n, 4 * f)) * env(n, 0.002, 0.06), 0.07)
    elif k == 'pip':  # birim kare / sayı
        f = 987.77 * 2 ** ((v % 5) / 24); n = int(0.15 * SR); add(t, (sine(n, f) + 0.15 * sine(n, 3 * f)) * env(n, 0.001, 0.035), 0.05)
    elif k == 'tick': n = int(0.2 * SR); f = 660 * 2 ** ((v % 6) / 24); add(t, (sine(n, f) + 0.2 * sine(n, 4 * f)) * env(n, 0.002, 0.05), 0.07)
    elif k == 'tock': n = int(0.5 * SR); add(t, (sine(n, 392) + 0.3 * sine(n, 1176)) * env(n, 0.003, 0.12), 0.12)
    elif k in ('soft', 'soft2'):
        for j, f in enumerate([523.25, 659.25, 783.99] if k == 'soft' else [587.33, 880.0]):
            n = int(1.2 * SR); add(t + j * 0.09, sine(n, f) * env(n, 0.004, 0.35), 0.06)
out *= 2.6
out = out[:int(SR * DUR)]; fade = int(0.4 * SR); out[-fade:] *= np.linspace(1, 0, fade)
pk = np.abs(out).max(); out = out * (0.7 / pk) if pk > 0.7 else out
pcm = (np.clip(np.stack([out, out], 1), -1, 1) * 32767).astype('<i2')
w = wave.open(os.path.join(d, 'sfx.wav'), 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('sfx.wav', len(ev), 'olay')
