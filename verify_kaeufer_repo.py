#!/usr/bin/env python3
"""Anhang-F-Proof fürs Buch: QR-Referenz + URL im Vault-F (finalisiert 14.10.)"""
import subprocess, re
# 1) Vault-F trägt die URL + QR (L-mode)
f = open('/home/pi/ki-os/vault/10-Projekte/KI-Buch-Senioren/F-Werkzeug-Quelle.md', encoding='utf-8').read()
assert 'das-ki-buch-senioren-vorlagen' in f, 'URL fehlt im Vault-F'
assert 'build-media/qr-buch.png' in f, 'QR-Referenz fehlt'
assert 'Platzhalter' not in f, 'Platzhalter-Rest im Vault-F'
# 2) QR-Roh-Fassung im Vault-F ist L-Mode Grayscale
from PIL import Image
im = Image.open('/home/pi/ki-os/vault/10-Projekte/KI-Buch-Senioren/illustrationen/qr-buch.png')
assert im.mode == 'L', f'QR-Mode: {im.mode}'
print('Vault-F: URL ✓ QR ✓ kein Platzhalter ✓, QR-Mode L ✓')

# 3) Käufer-Repo-F gleiche Bedingung + live via API
kauf = subprocess.run(['gh', 'api', 'repos/robotfreak/das-ki-buch-senioren-vorlagen/contents/anhaenge/Anhang-F-Werkzeug-Quelle.md', '-H', 'Accept: application/vnd.github.raw'], capture_output=True, text=True).stdout
assert 'das-ki-buch-senioren-vorlagen' in kauf, 'URL fehlt im Repo-F'
assert 'illustrationen/qr-buch.png' in kauf, 'QR-Referenz fehlt im Repo-F'
print('Repo-F live: URL ✓ QR-Referenz ✓')
print('ALLE BEWEISE OK')
# 4) Live-Proof Erweiterung: QR-Raw im Repo = L-Mode + dekodierbar
import subprocess as sp
sp.run(['gh', 'api', 'repos/robotfreak/das-ki-buch-senioren-vorlagen/contents/anhaenge/illustrationen/qr-buch.png', '-H', 'Accept: application/vnd.github.raw', '-q', '.content'], capture_output=True, text=True)
# Basis64-Fassung holen und dekodieren:
import base64
out = sp.run(['gh', 'api', 'repos/robotfreak/das-ki-buch-senioren-vorlagen/contents/anhaenge/illustrationen/qr-buch.png', '-H', 'Accept: application/vnd.github.raw'], capture_output=True)
open('/tmp/qr-live.png', 'wb').write(out.stdout)
im2 = Image.open('/tmp/qr-live.png')
print('Live-QR-Mode:', im2.mode, im2.size)
dec = sp.run(['zbarimg', '--quiet', '/tmp/qr-live.png'], capture_output=True, text=True).stdout.strip()
print('Live-QR dekodiert:', dec)
assert 'das-ki-buch-senioren-vorlagen' in dec
print('LIVE-QR-PROOF OK')
