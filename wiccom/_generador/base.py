# -*- coding: utf-8 -*-
"""Componentes compartidos del sitio Wiccom (header, footer, SEO, modales, íconos)."""
import json, re, html, os

# ------------------------------------------------------------------
# CONFIGURACIÓN GENERAL — cambia aquí y se actualiza en todo el sitio
# ------------------------------------------------------------------
SITE = {
    "name": "Wiccom",
    "tagline": "Conectando Tecnología",
    "domain": "https://www.wiccom.com.mx",
    "store": "https://www.wiccom.mx",
    "phone_display": "+52 1 81 1200 4772",
    "phone_tel": "+5218112004772",
    "whatsapp": "5218112004772",
    "email": "contacto@wiccom.com.mx",
    "email_sales": "ventas@wiccom.com.mx",
    "street": "Av. Ejemplo 1234, Col. Tecnológico",
    "city": "Monterrey",
    "region": "Nuevo León",
    "region_short": "N.L.",
    "zip": "64700",
    "hours": [("Lunes a viernes", "8:30 a 18:30 h"), ("Sábado", "9:00 a 14:00 h")],
    "social": {
        "linkedin": "https://www.linkedin.com/company/wiccom",
        "facebook": "https://www.facebook.com/wiccom",
        "instagram": "https://www.instagram.com/wiccom",
        "youtube": "https://www.youtube.com/@wiccom",
    },
    "og_default": "assets/img/og/wiccom-og.jpg",
    # Cloudflare Turnstile (CAPTCHA). Crea un sitio en dash.cloudflare.com → Turnstile y pega aquí la
    # "Site Key" (pública). La "Secret Key" va SOLO en php/enviar.php del servidor (no la subas a GitHub).
    "turnstile_sitekey": "0x4AAAAAAFKzDE8I1iynBPH3",
}

CUR = ' aria-current="page"'
NOTAB = 'tabindex="-1"'

NAV = [
    ("Inicio", "index.html", "inicio"),
    ("Soluciones", "soluciones.html", "soluciones"),
    ("Servicios", "servicios.html", "servicios"),
    ("Marcas", "marcas.html", "marcas"),
    ("Nosotros", "nosotros.html", "nosotros"),
    ("Recursos", "recursos.html", "recursos"),
    ("Contacto", "contacto.html", "contacto"),
]

# ------------------------------------------------------------------
# ÍCONOS (trazos estilo línea, viewBox 24)
# ------------------------------------------------------------------
ICONS = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "chev-r": '<path d="m9 6 6 6-6 6"/>', "chev-l": '<path d="m15 6-6 6 6 6"/>', "chev-d": '<path d="m6 9 6 6 6-6"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 "cart": '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.6 12.4a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.5L21 8H6"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "wa": '<path d="M12 2.2a9.8 9.8 0 0 0-8.4 14.9L2.2 21.8l4.8-1.3A9.8 9.8 0 1 0 12 2.2z" fill="currentColor" stroke="none"/><path d="M8.6 7.3c.2-.5.5-.5.8-.5h.6c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .6l-.6.8c-.1.2-.2.4 0 .6a7.4 7.4 0 0 0 3.4 3c.2.1.4.1.6-.1l.8-1c.2-.2.4-.2.6-.1l2 .9c.2.1.4.2.4.5 0 .6-.3 1.3-.8 1.7-.6.5-1.5.7-2.5.4-3.3-1-5.2-3.3-6.3-5.2-.7-1.3-.3-2.9.6-3.7z" style="fill:var(--wa-inner,#fff)" stroke="none"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
 "headset": '<path d="M3 14v-2a9 9 0 0 1 18 0v2"/><path d="M21 16a2 2 0 0 1-2 2h-1v-6h3zM3 16a2 2 0 0 0 2 2h1v-6H3z"/><path d="M18 18v1a3 3 0 0 1-3 3h-3"/>',
 "truck": '<path d="M1 5h13v11H1zM14 9h4l4 4v3h-8z"/><circle cx="5.5" cy="18" r="2"/><circle cx="17.5" cy="18" r="2"/>',
 "cctv": '<path d="M16.8 10.6 5 6.3a1 1 0 0 0-1.3.6L2.1 11a1 1 0 0 0 .6 1.3l11.8 4.3a1 1 0 0 0 1.3-.6l1.6-4.1a1 1 0 0 0-.6-1.3z"/><path d="m17 12 4 1.5-1 2.7-4.3-1.6M8 14.5 7 17H3M3 14v6"/>',
 "network": '<rect x="9" y="2" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M12 8v4M5 16v-2h14v2"/>',
 "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
 "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
 "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
 "file-search": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h5"/><path d="M14 2v6h6v3"/><circle cx="16.5" cy="16.5" r="3"/><path d="m21 21-2.3-2.3"/>',
 "bulb": '<path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V17h6v-.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/>',
 "msg": '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.2A8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 "puzzle": '<path d="M4 7h3a2 2 0 1 1 4 0h3v3a2 2 0 1 1 0 4v3h-3a2 2 0 1 0-4 0H4v-3a2 2 0 1 0 0-4z"/>',
 "chart": '<path d="M3 21h18"/><rect x="5" y="12" width="3" height="7"/><rect x="10.5" y="8" width="3" height="11"/><rect x="16" y="4" width="3" height="15"/>',
 "award": '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 8 5-3 5 3-1.5-8"/>',
 "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
 "grad": '<path d="M22 10 12 5 2 10l10 5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
 "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "clip": '<path d="m21.4 11-9.2 9.2a6 6 0 0 1-8.5-8.5l9.2-9.2a4 4 0 0 1 5.7 5.7l-9.2 9.2a2 2 0 0 1-2.8-2.8l8.5-8.5"/>',
 "send": '<path d="M22 2 11 13M22 2l-7 20-4-9-9-4z"/>',
 "linkedin": '<path fill="currentColor" stroke="none" d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1 0-5zM3 9h4v12H3zm7 0h3.8v1.7h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.4c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9V21h-4z"/>',
 "facebook": '<path fill="currentColor" stroke="none" d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/>',
 "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/>',
 "youtube": '<path fill="currentColor" stroke="none" d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12c0 1.3.1 2.6.4 3.8a3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1c.3-1.2.4-2.5.4-3.8s-.1-2.6-.4-3.8zM10 15.2V8.8l5.2 3.2z"/>',
 "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
 "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "handshake": '<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2L15 11l-3.5 2a2 2 0 0 1-2.5-3l3-3h3l4 4"/><path d="M21 5v7M3 5v8l6 6M3 6h5"/>',
 "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
 "map": '<path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/>',
 "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 12 10 5 10-5M2 17l10 5 10-5"/>',
 "cloud": '<path d="M17.5 19H7a5 5 0 1 1 1-9.9A6 6 0 0 1 19.4 11 4 4 0 0 1 17.5 19z"/>',
 "server": '<rect x="3" y="3" width="18" height="7" rx="1.5"/><rect x="3" y="14" width="18" height="7" rx="1.5"/><path d="M7 6.5h.01M7 17.5h.01"/>',
 "sliders": '<path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
 "quote": '<path fill="currentColor" stroke="none" d="M7 7h4v4c0 3-1.5 5.5-4.5 6.5l-.7-1.5C7.4 15.3 8 14 8 12.5H5V9a2 2 0 0 1 2-2zm9 0h4v4c0 3-1.5 5.5-4.5 6.5l-.7-1.5c1.6-.7 2.2-2 2.2-3.5H14V9a2 2 0 0 1 2-2z"/>',
 "link": '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
 "package": '<path d="m21 8-9-5-9 5v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
 "play": '<circle cx="12" cy="12" r="9"/><path d="m10 8 6 4-6 4z"/>',
 "trend": '<path d="m3 17 6-6 4 4 8-8M15 7h6v6"/>',
 "building": '<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
 "store": '<path d="M3 9 4.5 4h15L21 9M3 9v11h18V9M3 9h18M9 20v-6h6v6"/>',
 "refresh": '<path d="M21 12a9 9 0 0 1-15.5 6.3L3 16M3 12a9 9 0 0 1 15.5-6.3L21 8M21 3v5h-5M3 21v-5h5"/>',
 "battery": '<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2M6 10v4M10 10v4"/>',
 "key": '<circle cx="7.5" cy="15.5" r="4.5"/><path d="m10.7 12.3 9.3-9.3M17 6l3 3M15 8l2 2"/>',
 "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>',
 "wifi": '<path d="M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M2 9a15 15 0 0 1 20 0"/><circle cx="12" cy="19.5" r=".8" fill="currentColor"/>',
 "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',
 "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
 "phone-m": '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>',
 "db": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
 "video": '<rect x="2" y="6" width="14" height="12" rx="2"/><path d="m22 8-6 4 6 4z"/>',
 "printer": '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
 "dollar": '<path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
 "home": '<path d="M3 11 12 3l9 8v10h-6v-6H9v6H3z"/>',
 "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
 "walk": '<circle cx="13" cy="4" r="2"/><path d="m9 20 3-6 3 3v4M6 12l3-4 4 1 3 4M12 14l-1-5"/>',
 "sound": '<path d="M11 5 6 9H2v6h4l5 4zM15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/>',
 "hdd": '<rect x="2" y="12" width="20" height="8" rx="2"/><path d="M5.5 5h13L22 12H2zM6 16h.01M10 16h.01"/>',
 "factory": '<path d="M2 21V10l6 4V10l6 4V6l8 5v10z"/><path d="M6 17h2M11 17h2M16 17h2"/>',
 "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
 "rack": '<rect x="5" y="2" width="14" height="20" rx="1"/><path d="M5 7h14M5 12h14M5 17h14M8 4.5h.01M8 9.5h.01M8 14.5h.01M8 19.5h.01"/>',
}

def ic(name, cls="ico", label=None):
    a = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    return f'<svg class="{cls}"{a}><use href="#i-{name}"/></svg>'

def sprite(used):
    syms = "".join(f'<symbol id="i-{n}" viewBox="0 0 24 24">{ICONS[n]}</symbol>' for n in sorted(used) if n in ICONS)
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">{syms}</svg>'

# ------------------------------------------------------------------
# ESTADO DE RENDER (profundidad de carpeta) + registro de imágenes
# ------------------------------------------------------------------
class Ctx:
    r = ""          # prefijo relativo ("" o "../")
    images = {}     # ruta -> (descripción, tamaño sugerido, páginas)
    page = ""

IMG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "img"))
EXTS = (".webp", ".jpg", ".jpeg", ".png", ".svg")

def find_img(path, fallback=True):
    """Busca la imagen con cualquier extensión (webp, jpg, png, svg).
    Si no existe y fallback=True, usa la imagen genérica de la carpeta (default.* o 1.*)."""
    stem = os.path.splitext(path)[0]
    for e in EXTS:
        if os.path.isfile(os.path.join(IMG_DIR, stem + e)):
            return stem + e
    if fallback:
        folder = os.path.dirname(path)
        for name in ("default", "1"):
            for e in EXTS:
                cand = (folder + "/" if folder else "") + name + e
                if os.path.isfile(os.path.join(IMG_DIR, cand)):
                    return cand
    return None

def ph(path, alt, size="1200x800", dark=False, eager=False, cls=""):
    """Espacio para imagen. Pon el archivo en assets/img/<ruta> (webp, jpg o png);
    si no existe se muestra un recuadro con la ruta y el tamaño sugerido."""
    w, h = size.split("x")
    real = find_img(path)
    Ctx.images.setdefault(path, [alt, size, set(), real == find_img(path, False) and real is not None])[2].add(Ctx.page)
    src = real or path
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="ph{" ph--dark" if dark else ""} {cls}">'
            f'<img src="{Ctx.r}assets/img/{src}" alt="{html.escape(alt)}" width="{w}" height="{h}" {load} decoding="async"></figure>')

def clean(path):
    """URL pública limpia (sin .html): servicios/instalacion.html -> servicios/instalacion"""
    if path in ("index.html", ""):
        return ""
    return path[:-5] if path.endswith(".html") else path

def u(href):
    """Enlace interno relativo."""
    if href.startswith(("http", "#", "tel:", "mailto:")):
        return href
    return Ctx.r + href

def wa_url(msg="¡Hola! Me gustaría hablar con un asesor de Wiccom."):
    from urllib.parse import quote
    return f"https://wa.me/{SITE['whatsapp']}?text={quote(msg)}"

# Por indicación de Wiccom no se muestran logotipos de fabricantes: las marcas se presentan solo con su nombre en texto.
THIRD_PARTY_LOGOS = False

def brand_logo(b):
    """Ruta del logo de la marca (desactivado mientras THIRD_PARTY_LOGOS sea False)."""
    if not THIRD_PARTY_LOGOS:
        return None
    if b.get("logo"):
        return find_img("marcas/" + b["logo"], False)
    return find_img("marcas/" + b["slug"], False)

def brand_tile(b, tag="a", extra="", sub=""):
    """Marca en texto (nombre y, opcionalmente, las soluciones con que se relaciona)."""
    lg = brand_logo(b)
    if lg:
        inner = f'<img src="{Ctx.r}assets/img/{lg}" alt="{b["name"]}" width="400" height="200" loading="lazy" decoding="async">'
    else:
        inner = f'<span class="brand__name">{b["name"]}</span>' + (f'<span class="brand__sub">{sub}</span>' if sub else "")
    if tag == "a":
        return f'<a class="brand" href="{u("marcas/" + b["slug"] + ".html")}" aria-label="Marca {b["name"]}" {extra}>{inner}</a>'
    return f'<div class="brand" {extra}>{inner}</div>'

def brand_pills(brands, limit=24):
    """Lista estática de marcas en texto, cada una enlazada a su ficha."""
    seen, out = set(), []
    for b in brands:
        if b["slug"] not in seen:
            seen.add(b["slug"]); out.append(b)
    return '<ul class="brand-pills" data-aos="fade-up">' + "".join(
        f'<li><a href="{u("marcas/" + b["slug"] + ".html")}">{b["name"]}</a></li>' for b in out[:limit]) + "</ul>"

# ------------------------------------------------------------------
# BLOQUES DE LAYOUT
# ------------------------------------------------------------------
def logo(light=False):
    """Logo de Wiccom (assets/img/logo-wiccom.png, a color, sin slogan). Es la misma versión en header y footer; el tamaño se ajusta por CSS."""
    src = find_img("logo-wiccom", False) or find_img("logo", False)
    img = f'<img class="logo__img" src="{Ctx.r}assets/img/{src}" alt="Wiccom" width="200" height="56">' if src else ""
    return (f'<a class="logo{" logo--light" if light else ""}" href="{u("index.html")}" aria-label="Wiccom, ir al inicio">{img}'
            f'<span class="logo__fallback"><span class="logo__mark" aria-hidden="true">W</span>'
            f'<span class="logo__text"><span class="logo__name">wiccom</span></span></span></a>')

def header(active):
    links = "".join(
        f'<li><a class="nav__link" href="{u(h)}"{CUR if k == active else ""}>{t}</a></li>'
        for t, h, k in NAV)
    mlinks = "".join(
        f'<li><a href="{u(h)}"{CUR if k == active else ""}>{t}{ic("chev-r")}</a></li>'
        for t, h, k in NAV)
    hours = " · ".join(f"{d}: {h}" for d, h in SITE["hours"])
    return f'''
<a class="skip-link" href="#main">Saltar al contenido</a>
<header class="site-header">
  <div class="container header__inner">
    {logo()}
    <nav class="nav" aria-label="Navegación principal"><ul class="nav__list">{links}</ul></nav>
    <div class="header__actions">
      <button class="icon-btn search-trigger" type="button" data-open-search aria-label="Buscar en el sitio (Ctrl + K)">{ic("search")}</button>
      <div class="store">
        <a class="store__btn" href="{SITE["store"]}" target="_blank" rel="noopener" aria-describedby="store-tip">{ic("cart")} Tienda</a>
        <span class="store__tip" id="store-tip" role="tooltip">Conoce nuestro catálogo de productos en wiccom.mx</span>
      </div>
      <button class="icon-btn burger" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="mnav">{ic("menu")}</button>
    </div>
  </div>
</header>
<div class="mnav" id="mnav" aria-hidden="true">
  <div class="mnav__overlay" data-close-nav></div>
  <div class="mnav__panel" role="dialog" aria-modal="true" aria-label="Menú" tabindex="-1">
    <div class="mnav__head">{logo()}<button class="icon-btn" type="button" data-close-nav aria-label="Cerrar menú">{ic("x")}</button></div>
    <nav aria-label="Navegación móvil"><ul class="mnav__list">{mlinks}</ul></nav>
    <div class="mnav__cta">
      <button class="btn btn--outline" type="button" data-open-search>{ic("search")} Buscar en el sitio</button>
      <a class="btn btn--primary" href="{SITE["store"]}" target="_blank" rel="noopener">{ic("cart")} Visitar tienda</a>
      <a class="btn btn--dark" href="{u("cotizacion.html")}">Solicitar cotización {ic("arrow")}</a>
    </div>
    <div class="mnav__contact">
      <a href="tel:{SITE["phone_tel"]}">{ic("phone")} {SITE["phone_display"]}</a>
      <a href="mailto:{SITE["email"]}">{ic("mail")} {SITE["email"]}</a>
      <span>{ic("clock")} {hours}</span>
    </div>
  </div>
</div>
<div class="search" id="search" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Buscar">
  <div class="search__box">
    <div class="search__field">{ic("search")}<label class="sr-only" for="search-input">Buscar</label><input id="search-input" type="search" placeholder="Buscar soluciones, servicios, marcas o artículos…" autocomplete="off"><button class="icon-btn" type="button" data-close-search aria-label="Cerrar búsqueda">{ic("x")}</button></div>
    <div class="search__results" id="search-results" aria-live="polite"></div>
  </div>
</div>'''

def footer(solutions, services):
    sols = "".join(f'<li><a href="{u("soluciones/" + s["slug"] + ".html")}">{s["name"]}</a></li>' for s in solutions)
    servs = "".join(f'<li><a href="{u("servicios/" + s["slug"] + ".html")}">{s["name"]}</a></li>' for s in services)
    soc = SITE["social"]
    social = "".join(f'<a href="{soc[k]}" target="_blank" rel="noopener" aria-label="Wiccom en {n}">{ic(k)}</a>'
                     for k, n in [("linkedin", "LinkedIn"), ("facebook", "Facebook"), ("instagram", "Instagram"), ("youtube", "YouTube")])
    return f'''
<footer class="site-footer">
  <div class="container footer__grid">
    <div class="footer__brand">{logo(True)}<p>Soluciones en TI, telecomunicaciones, seguridad electrónica e infraestructura para empresas en todo México.</p><div class="social">{social}</div></div>
    <div class="footer__col"><h3>Soluciones</h3><ul>{sols}</ul></div>
    <div class="footer__col"><h3>Servicios</h3><ul>{servs}</ul></div>
    <div class="footer__col"><h3>Nosotros</h3><ul>
      <li><a href="{u("nosotros.html")}">Empresa</a></li>
      <li><a href="{u("nosotros.html#areas")}">Nuestro equipo</a></li>
      <li><a href="{u("marcas.html")}">Marcas</a></li>
      <li><a href="{u("recursos.html")}">Recursos</a></li>
      <li><a href="{u("contacto.html")}">Contacto</a></li>
      <li><a href="{SITE["store"]}" target="_blank" rel="noopener">Tienda en línea</a></li></ul></div>
    <div class="footer__col"><h3>Contacto</h3><ul class="footer__contact">
      <li>{ic("pin")}<span>{SITE["city"]}, {SITE["region_short"]}</span></li>
      <li>{ic("phone")}<a href="tel:{SITE["phone_tel"]}">{SITE["phone_display"]}</a></li>
      <li>{ic("mail")}<a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
      <li>{ic("clock")}<span>{SITE["hours"][0][0]}<br>{SITE["hours"][0][1]}</span></li></ul></div>
  </div>
  <div class="container footer__bottom">
    <nav class="footer__legal" aria-label="Legal"><a href="{u("terminos.html")}">Términos y condiciones</a><a href="{u("aviso-de-privacidad.html")}">Aviso de privacidad</a><a href="{u("preguntas-frecuentes.html")}">Preguntas frecuentes</a></nav>
    <p style="margin:0">© <span data-year>2026</span> Wiccom. Todos los derechos reservados.</p>
  </div>
</footer>'''

def modals(solutions, services, brands):
    opts = options_html(solutions, services)
    brand_opts = "".join(f'<option value="{b["name"]}">{b["name"]}</option>' for b in brands)
    return f'''
<dialog class="modal" id="modal-asesor" aria-labelledby="asesor-title">
  <div class="modal__view" data-name="menu">
    <div class="modal__head"><div><h2 id="asesor-title">Hablar con un asesor</h2><p>Elige el medio que prefieras. Estamos listos para ayudarte.</p></div><button class="modal__close" type="button" data-close-modal aria-label="Cerrar">{ic("x")}</button></div>
    <div class="modal__body opt-list">
      <a class="opt-btn" data-wa-link href="{wa_url()}" target="_blank" rel="noopener"><span class="channel__ico channel__ico--wa">{ic("wa")}</span><span><strong>WhatsApp</strong><span>Chatea con un asesor por WhatsApp.</span></span>{ic("chev-r", "ico go")}</a>
      <button class="opt-btn" type="button" data-view="call"><span class="channel__ico">{ic("phone")}</span><span><strong>Llamada telefónica</strong><span>Habla directamente con nuestro equipo.</span></span>{ic("chev-r", "ico go")}</button>
      <button class="opt-btn" type="button" data-view="form"><span class="channel__ico">{ic("mail")}</span><span><strong>Formulario rápido</strong><span>Déjanos tus datos y te contactamos.</span></span>{ic("chev-r", "ico go")}</button>
    </div>
  </div>
  <div class="modal__view" data-name="call" hidden>
    <div class="modal__head"><div></div><button class="modal__close" type="button" data-close-modal aria-label="Cerrar">{ic("x")}</button></div>
    <div class="modal__body call-box">
      {ic("phone", "ico ico-lg")}<h2>¿Deseas llamarnos?</h2>
      <a class="num" href="tel:{SITE["phone_tel"]}">{SITE["phone_display"]}</a>
      <p class="muted">{SITE["hours"][0][0]} · {SITE["hours"][0][1]}</p>
      <div class="btns"><button class="btn btn--outline" type="button" data-view="menu">Cancelar</button><a class="btn btn--primary" href="tel:{SITE["phone_tel"]}">{ic("phone")} Llamar</a></div>
    </div>
  </div>
  <div class="modal__view modal__form" data-name="form" hidden>
    <div class="modal__head"><div><button class="back-link" type="button" data-view="menu">{ic("chev-l")} Otras opciones</button><h2>Te contactamos</h2><p>Déjanos tus datos y un asesor se comunicará contigo.</p></div><button class="modal__close" type="button" data-close-modal aria-label="Cerrar">{ic("x")}</button></div>
    <div class="modal__body">
      <form action="{u("php/enviar.php")}" method="post" data-validate novalidate>
        <input type="hidden" name="tipo" value="Asesor (formulario rápido)"><input type="hidden" name="contexto" value=""><input type="hidden" name="_ts" value="">
        <div class="hp" aria-hidden="true"><label>No llenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <div class="form-grid">
          {field("nombre", "Nombre completo", required=True, ph="Ej. Juan Pérez", ac="name", idp="qa")}
          {field("empresa", "Empresa", required=True, ph="Ej. Empresa S.A. de C.V.", ac="organization", idp="qa")}
          {field("telefono", "Teléfono", "tel", True, "Ej. 81 0000 0000", "tel", idp="qa")}
          {field("correo", "Correo electrónico", "email", True, "nombre@empresa.com", "email", idp="qa")}
          {field("mensaje", "Mensaje", "textarea", False, "¿En qué te podemos ayudar?", idp="qa", full=True, opt=True)}
          <div class="field field--full">{privacy("qa")}</div>
          {captcha("qa")}
        </div>
        <div class="form-actions" style="margin-top:16px"><button class="btn btn--primary" type="submit">Enviar solicitud {ic("send")}</button></div>
      </form>
      {success()}
    </div>
  </div>
</dialog>

<dialog class="modal modal--lg" id="modal-cotizacion" aria-labelledby="cot-title">
  <div class="modal__view modal__form" data-name="form">
    <div class="modal__head"><div><h2 id="cot-title">Solicitar cotización</h2><p>Cuéntanos qué necesitas. Nuestro equipo te ayudará a identificar la solución adecuada.</p></div><button class="modal__close" type="button" data-close-modal aria-label="Cerrar">{ic("x")}</button></div>
    <div class="modal__body">
      <form action="{u("php/enviar.php")}" method="post" data-validate novalidate>
        <input type="hidden" name="tipo" value="Cotización de marca o producto"><input type="hidden" name="contexto" value=""><input type="hidden" name="_ts" value="">
        <div class="hp" aria-hidden="true"><label>No llenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
        <div class="form-grid">
          {field("nombre", "Nombre completo", required=True, ph="Ej. Juan Pérez", ac="name", idp="mc")}
          {field("empresa", "Empresa", required=True, ph="Ej. Empresa S.A. de C.V.", ac="organization", idp="mc")}
          {field("correo", "Correo electrónico", "email", True, "nombre@empresa.com", "email", idp="mc")}
          {field("telefono", "Teléfono", "tel", True, "Ej. 81 0000 0000", "tel", idp="mc")}
          <div class="field"><label for="mc-marca">Marca de interés <span class="req">*</span></label><input class="input" id="mc-marca" name="marca" list="dl-marcas" required placeholder="Ej. Hikvision" data-prefill><datalist id="dl-marcas">{brand_opts}</datalist><span class="field__error" aria-live="polite"></span></div>
          {field("modelo", "Modelo o producto", ph="Ej. DS-2CD2347G2-LU", idp="mc", opt=True)}
          {field("mensaje", "Detalles de tu requerimiento", "textarea", True, "Cantidades, ubicación, fechas, etc.", idp="mc", full=True)}
          <div class="field field--full">{privacy("mc")}</div>
          {captcha("mc")}
        </div>
        <div class="form-actions" style="margin-top:16px"><button class="btn btn--primary" type="submit">Enviar solicitud {ic("send")}</button><span class="secure">{ic("lock")} Tus datos están protegidos.</span></div>
      </form>
      {success()}
    </div>
  </div>
</dialog>'''

def options_html(solutions, services, selected=None):
    sol = "".join(f'<option value="{s["name"]}">{s["name"]}</option>' for s in solutions)
    srv = "".join(f'<option value="{s["name"]}">{s["name"]}</option>' for s in services)
    return (f'<option value="">Selecciona una opción</option><optgroup label="Soluciones">{sol}</optgroup>'
            f'<optgroup label="Servicios">{srv}</optgroup><optgroup label="Otros"><option>Marca o producto específico</option><option>Otro</option></optgroup>')

def field(name, label, kind="text", required=False, ph="", ac="", idp="f", full=False, opt=False, options=None, maxlength=1000, from_url=False):
    fid = f"{idp}-{name}"
    req = ' <span class="req">*</span>' if required else ""
    optl = " <small>(opcional)</small>" if opt else ""
    r = " required" if required else ""
    acs = f' autocomplete="{ac}"' if ac else ""
    cls = "field field--full" if full or kind == "textarea" else "field"
    if kind == "textarea":
        ctl = (f'<textarea class="input" id="{fid}" name="{name}" placeholder="{ph}" maxlength="{maxlength}"{r}></textarea>'
               f'<span class="field__foot"><span class="field__error" aria-live="polite"></span><span data-count-for="{name}">0/{maxlength}</span></span>')
        return f'<div class="{cls}"><label for="{fid}">{label}{req}{optl}</label>{ctl}</div>'
    if kind == "select":
        fu = " data-from-url" if from_url else ""
        ctl = f'<select class="input" id="{fid}" name="{name}"{r}{fu}>{options}</select>'
    else:
        im = ' inputmode="tel"' if kind == "tel" else ""
        ctl = f'<input class="input" id="{fid}" type="{kind}" name="{name}" placeholder="{ph}"{acs}{im}{r}>'
    return f'<div class="{cls}"><label for="{fid}">{label}{req}{optl}</label>{ctl}<span class="field__error" aria-live="polite"></span></div>'

def dropzone(idp):
    return f'''<div class="field field--full"><span class="label" id="{idp}-dz-l">Adjuntar archivo <small>(opcional)</small></span>
      <div class="dropzone">{ic("clip")}<p>Arrastra y suelta tus archivos aquí o <u>haz clic para seleccionar</u></p><small>Planos, listas de materiales, especificaciones · PDF, DOC, XLS, JPG, PNG · máx. 10 MB por archivo</small>
      <input type="file" multiple accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.dwg" aria-labelledby="{idp}-dz-l"></div><ul class="files"></ul></div>'''

def privacy(idp):
    return (f'<label class="check"><input type="checkbox" name="privacidad" value="acepto" required> <span>Acepto el <a href="{u("aviso-de-privacidad.html")}" target="_blank">Aviso de Privacidad</a> de Wiccom y autorizo el tratamiento de mis datos para atender mi solicitud. <span class="req" style="color:var(--blue)">*</span></span></label>'
            f'<span class="field__error" aria-live="polite"></span>')

def captcha(idp):
    """Verificación anti-robots (Cloudflare Turnstile), antes del botón de envío."""
    return (f'<div class="field field--full captcha"><span class="sr-only" id="{idp}-cap-l">Verificación de seguridad</span>'
            f'<div class="cf-turnstile" data-sitekey="{SITE["turnstile_sitekey"]}" data-language="es" data-theme="light" data-size="flexible" aria-labelledby="{idp}-cap-l"></div>'
            f'<span class="field__error" aria-live="polite"></span></div>')

def success(msg="Recibimos tu solicitud. Un asesor se pondrá en contacto contigo para dar seguimiento."):
    return f'''<div class="form-success" role="status">{ic("check")}<h3>¡Gracias por escribirnos!</h3><p class="muted">{msg}</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn btn--wa btn--sm" href="{wa_url()}" target="_blank" rel="noopener">{ic("wa")} Seguir por WhatsApp</a><button class="btn btn--outline btn--sm" type="button" data-reset-form>Enviar otra solicitud</button></div></div>'''

# ------------------------------------------------------------------
# SECCIONES REUTILIZABLES
# ------------------------------------------------------------------
def hero(h1a, h1b, lead, img, img_alt, eyebrow="", actions="", features=None, script=None, badges=None, compact=False, h1_tag="h1", banner=False):
    feats = ""
    if features:
        feats = '<ul class="hero__features" data-aos="fade-left" data-aos-delay="300">' + "".join(f"<li>{ic(i)}<span>{t}</span></li>" for i, t in features) + "</ul>"
    sc = f'<p class="hero__script" aria-hidden="true" data-aos="zoom-in" data-aos-delay="450">{script[0]}<em>{script[1]}</em></p>' if script else ""
    bd = ""
    if badges:
        bd = '<ul class="hero__badges">' + "".join(f"<li>{ic(i)}<span>{t}</span></li>" for i, t in badges) + "</ul>"
    eb = f'<p class="hero__eyebrow">{eyebrow}</p>' if eyebrow else ""
    cls = "hero" + ("" if features else " hero--plain") + (" hero--compact" if compact else "") + (" hero--banner" if banner else "")
    return f'''
<section class="{cls}" aria-labelledby="hero-title">
  <div class="hero__media">{ph(img, img_alt, "2000x667" if banner else "1600x900", dark=True, eager=True)}</div>
  <span class="hero__slash" aria-hidden="true"></span>
  <div class="container hero__inner">
    <div class="hero__content">
      <div data-aos="fade-up">{eb}<{h1_tag} id="hero-title">{h1a} <span class="hl">{h1b}</span></{h1_tag}></div>
      <p class="hero__lead" data-aos="fade-up" data-aos-delay="120">{lead}</p>
      {f'<div class="hero__actions" data-aos="fade-up" data-aos-delay="220">{actions}</div>' if actions else ""}
      {f'<div data-aos="fade-up" data-aos-delay="260">{bd}</div>' if bd else ""}
    </div>
  </div>
  {feats}{sc}
</section>'''

def breadcrumb(items):
    lis = []
    for i, (name, href) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li><span aria-current="page">{name}</span></li>')
        else:
            lis.append(f'<li><a href="{u(href)}">{name}</a></li>')
    return f'<nav class="breadcrumb" aria-label="Ruta de navegación"><ol>{"".join(lis)}</ol></nav>'

def intro(crumbs, title, text, sub=""):
    s = f'<p class="intro__sub">{sub}</p>' if sub else ""
    return f'''
<section class="intro"><div class="container intro__grid">
  <div>{breadcrumb(crumbs)}<h2>{title}</h2>{s}</div>
  <p class="intro__text">{text}</p>
</div></section>'''

def sec_head(title, sub="", link=None, hid=None):
    lk = f'<a class="link-more" href="{u(link[1])}">{link[0]} {ic("arrow")}</a>' if link else ""
    i = f' id="{hid}"' if hid else ""
    return f'<div class="sec-head" data-aos="fade-up"><div><h2{i}>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>{lk}</div>'

def carousel(slides, per=4, autoplay=0, label="Carrusel", cls=""):
    ap = f' data-autoplay="{autoplay}"' if autoplay else ""
    items = "".join(f'<div class="carousel__slide" role="group" aria-roledescription="diapositiva">{s}</div>' for s in slides)
    return f'''<div class="carousel {cls}" data-carousel{ap} style="--per-d:{per}" role="region" aria-roledescription="carrusel" aria-label="{label}">
  <div class="carousel__track" tabindex="0">{items}</div>
  <div class="carousel__ctrl"><div class="carousel__dots"></div><div class="carousel__arrows"><button class="carousel__btn" type="button" data-prev aria-label="Anterior">{ic("chev-l")}</button><button class="carousel__btn" type="button" data-next aria-label="Siguiente">{ic("chev-r")}</button></div></div>
</div>'''

def marquee(brands, speed=40, board=False, reverse=False, label="Marcas con las que trabajamos", plain=False):
    brands = list(brands)
    while brands and len(brands) < 10:
        brands = brands + brands[:10 - len(brands)]
    a = "".join(f"<li>{brand_tile(b)}</li>" for b in brands)
    b2 = "".join(f'<li aria-hidden="true">{brand_tile(b, extra=NOTAB)}</li>' for b in brands)
    cls = "marquee" + (" marquee--board" if board else "") + (" marquee--reverse" if reverse else "") + (" marquee--plain" if plain else "")
    speed = max(speed, round(len(brands) * 3.6))
    return f'<div class="{cls}" style="--speed:{speed}s" aria-label="{label}"><ul class="marquee__track">{a}{b2}</ul></div>'

def feats_row(items, title=None, sub=""):
    row = '<div class="feats">' + "".join(
        f'<div class="feat" data-aos="fade-up" data-aos-delay="{i*80}">{ic(icn)}<div><h3>{t}</h3><p>{d}</p></div></div>'
        for i, (icn, t, d) in enumerate(items)) + "</div>"
    if title:
        return f'<div class="feats-wrap"><div class="feats-wrap__title" data-aos="fade-right"><h2>{title}</h2><p>{sub}</p></div>{row}</div>'
    return row

def steps(items, title=None, sub="", numbered=False):
    out = []
    for i, (icn, t, d) in enumerate(items):
        badge = f'<span class="step__num">{i+1}</span>' if numbered else f'<span class="step__ico">{ic(icn)}</span>'
        label = t if numbered else f"{i+1}. {t}"
        out.append(f'<li class="step" data-aos="fade-up" data-aos-delay="{i*100}">{badge}<div><h3>{label}</h3><p>{d}</p></div></li>')
    ol = f'<ol class="steps{" steps--v2" if numbered else ""}">{"".join(out)}</ol>'
    if title:
        return f'<div class="feats-wrap"><div class="feats-wrap__title" data-aos="fade-right"><h2>{title}</h2><p>{sub}</p></div>{ol}</div>'
    return ol

def ctaband(title, text, btn=("Solicitar cotización", "cotizacion.html"), ctx="", extra=None):
    if extra is None:
        extra = f'<button class="btn btn--ghost" type="button" data-modal="asesor" data-context="{ctx}">Hablar con un asesor</button>'
    return f'''
<section class="ctaband" aria-label="Contacto rápido"><div class="container ctaband__grid">
  <h2 data-aos="fade-right">{title}</h2>
  <p data-aos="fade-up">{text}</p>
  <div class="ctaband__btns" data-aos="zoom-in"><a class="btn btn--primary" href="{u(btn[1])}">{btn[0]} {ic("arrow")}</a>{extra}</div>
  <div class="ctaband__quick" data-aos="fade-left">
    <a class="quick" href="tel:{SITE["phone_tel"]}">{ic("phone")}Llámanos</a>
    <a class="quick" href="mailto:{SITE["email"]}">{ic("mail")}Escríbenos</a>
    <a class="quick" href="{wa_url(f"¡Hola! Me interesa {ctx} y me gustaría hablar con un asesor." if ctx else "¡Hola! Me gustaría hablar con un asesor de Wiccom.")}" target="_blank" rel="noopener" style="--wa-inner:var(--navy)">{ic("wa")}WhatsApp</a>
  </div>
</div></section>'''

def ctabig(title, text, actions, script=("Tecnología", "que acerca"), tiles=None, img="banners/monterrey-ciudad.jpg"):
    right = ""
    if tiles:
        right = '<div class="ctabig__tiles" data-aos="fade-left">' + "".join(f'<a href="{u(h)}">{ic(i)}{t}</a>' for i, t, h in tiles) + "</div>"
    elif script:
        right = f'<p class="ctabig__script" aria-hidden="true" data-aos="zoom-in">{script[0]}<br>{script[1]}</p>'
    return f'''
<section class="ctabig" aria-labelledby="ctabig-title">
  {f'<div class="ctabig__bg">{ph(img, "Vista panorámica de Monterrey con la Sierra Madre al fondo", "1920x600", dark=True)}</div>' if img else ""}
  <div class="container ctabig__grid">
    <div data-aos="fade-up"><h2 id="ctabig-title">{title}</h2><p>{text}</p><div class="ctabig__actions">{actions}</div></div>
    {right}
  </div>
</section>'''

# ------------------------------------------------------------------
# DOCUMENTO COMPLETO
# ------------------------------------------------------------------
def org_schema():
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE["domain"] + "/#org",
        "name": "Wiccom", "slogan": SITE["tagline"], "url": SITE["domain"] + "/",
        "logo": SITE["domain"] + "/assets/img/" + (find_img("logo-wiccom", False) or "logo.png"), "image": SITE["domain"] + "/" + SITE["og_default"],
        "telephone": SITE["phone_tel"], "email": SITE["email"], "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressLocality": SITE["city"], "addressRegion": SITE["region"], "addressCountry": "MX"},
        "areaServed": {"@type": "Country", "name": "México"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:30", "closes": "18:30"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:00"}],
        "sameAs": list(SITE["social"].values()),
    }

def crumb_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["domain"] + "/" + clean(h)}
        for i, (n, h) in enumerate(items)]}

def document(path, title, desc, body, active, solutions, services, brands, schemas=(), og_img=None, og_type="website", extra_head="", keywords="", noindex=False, article=False):
    depth = path.count("/")
    if len(desc) > 160:  # Google muestra ~155-160 caracteres
        desc = desc[:157].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    canonical = SITE["domain"] + "/" + clean(path)
    og = SITE["domain"] + "/" + (og_img or SITE["og_default"])
    full_title = title if "Wiccom" in title else f"{title} | Wiccom"
    ld = [org_schema()] + list(schemas)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in ld)
    r = "../" * depth
    page = f'''<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full_title}</title>
<meta name="description" content="{desc}">
{f'<meta name="keywords" content="{keywords}">' if keywords else ""}
<meta name="robots" content="{"noindex, follow" if noindex else "index, follow, max-image-preview:large"}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0B2552">
<meta name="author" content="Wiccom">
<meta name="geo.region" content="MX-NLE"><meta name="geo.placename" content="{SITE["city"]}">
<meta property="og:locale" content="es_MX"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Wiccom">
<meta property="og:title" content="{full_title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{full_title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{og}">
<link rel="icon" href="{r}assets/img/favicon.png" type="image/png" sizes="64x64"><link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{r}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css">
<link rel="stylesheet" href="{r}assets/css/styles.css">
{extra_head}{ld_html}
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer(solutions, services)}
{modals(solutions, services, brands)}
<a class="fab-wa" href="{wa_url()}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{ic("wa")}</a>
<button class="to-top" type="button" aria-label="Volver arriba">{ic("up")}</button>
<div class="toast" id="toast" role="status" aria-live="polite"><span class="toast__ok">{ic("check")}</span><span class="toast__err">{ic("x")}</span><span class="toast__msg"></span></div>
{'<div class="progress" aria-hidden="true"></div>' if article else ""}
<script>window.WICCOM={{root:"{r}",whatsapp:"{SITE["whatsapp"]}"}};</script>
<script src="{r}assets/js/search-index.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js" defer></script>
<script src="{r}assets/js/main.js" defer></script>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
</body>
</html>'''
    used = set(re.findall(r'#i-([a-z0-9-]+)"', page))
    used |= {"clip", "x", "check"}
    page = page.replace("<body>\n", "<body>\n" + sprite(used) + "\n", 1)
    return page
