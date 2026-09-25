# Sitio web Wiccom (wiccom.com.mx)

Sitio estático en **HTML + CSS + JS** (sin frameworks) con AOS, carruseles, marquee de marcas,
modales, buscador global (Ctrl + K), formularios con adjuntos y SEO técnico.

## Estructura
```
index.html, soluciones.html, servicios.html, marcas.html, nosotros.html,
recursos.html, contacto.html, cotizacion.html, aviso-de-privacidad.html, terminos.html, 404.html
soluciones/*.html   servicios/*.html   marcas/*.html   recursos/*.html   (páginas de detalle)
assets/css/styles.css      estilos (variables de color al inicio)
assets/js/main.js          interacciones (menú, carruseles, modales, formularios, filtros…)
assets/js/search-index.js  índice del buscador (se genera solo)
assets/img/                AQUÍ van las imágenes → ver IMAGENES.md
php/enviar.php             envío de formularios por correo (configura destinatarios arriba)
.htaccess, sitemap.xml, robots.txt, site.webmanifest
_generador/                scripts Python que generan todo el HTML
```

## Imágenes
Cada hueco muestra la ruta y el tamaño sugerido. Solo guarda el archivo con ese nombre en esa ruta y aparece solo.
La lista completa está en **IMAGENES.md**. Logos de marcas: `assets/img/marcas/<slug>.svg` (o cambia la extensión en `data.py`).
Logo de Wiccom: `assets/img/logo-wiccom.svg` y `logo-wiccom-blanco.svg`.

## Editar textos / datos y regenerar
Teléfonos, correos, dirección, WhatsApp, redes → `SITE` en `_generador/base.py`.
Soluciones, servicios, marcas, artículos, FAQ → `_generador/data.py`.
Después ejecuta (Python 3.12+):
```
cd _generador && python3 build.py
```
(Regenera todo el HTML en la carpeta superior; no toca CSS, JS, imágenes ni PHP.)

## Formularios
En local (abriendo el .html directo) el envío se simula. En el hosting con PHP se envían a `php/enviar.php`,
que valida, filtra bots (honeypot + tiempo mínimo), acepta hasta 5 adjuntos de 10 MB y manda correo.
Si el hosting bloquea `mail()`, cámbialo por PHPMailer con SMTP.

## Pendiente de confirmar
Los datos de contacto y la dirección son de ejemplo (81 1234 5678, Av. Ejemplo 1234…).
Solo el artículo "Cómo elegir la cámara de seguridad ideal" tiene contenido completo; los demás traen introducción
y un comentario `<!-- CONTENIDO -->` para completar.
