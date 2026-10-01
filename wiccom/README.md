# Sitio web Wiccom (wiccom.com.mx)

Sitio estático en **HTML + CSS + JS** (sin frameworks) con AOS, carruseles, marquee de marcas,
modales, buscador global (Ctrl + K), formularios con adjuntos y CAPTCHA, y SEO técnico.

## Estructura
```
index.html, soluciones.html, servicios.html, marcas.html, nosotros.html,
recursos.html, contacto.html, cotizacion.html, aviso-de-privacidad.html, terminos.html, 404.html
soluciones/*.html   servicios/*.html   marcas/*.html   recursos/*.html   (páginas de detalle)
assets/css/styles.css      estilos (variables de color al inicio)
assets/js/main.js          interacciones (menú, carruseles, modales, formularios, filtros…)
assets/js/search-index.js  índice del buscador (se genera solo)
assets/img/                AQUÍ van las imágenes → ver IMAGENES.md
php/enviar.php             envío de formularios por correo + verificación del CAPTCHA
.htaccess                  configuración para hosting Apache (cPanel)
vercel.json                configuración para Vercel (URLs limpias, caché)
sitemap.xml, robots.txt, site.webmanifest
_generador/                scripts Python que generan todo el HTML
```

## Editar textos / datos y regenerar
- Teléfonos, correos, dirección, WhatsApp, redes, clave del CAPTCHA → `SITE` en `_generador/base.py`.
- Soluciones, servicios, marcas, artículos, FAQ → `_generador/data.py`.

Después ejecuta (Python 3.11 o superior):
```
cd _generador
python build.py
```
Regenera todo el HTML; no toca CSS, JS, imágenes ni PHP. **No edites los .html a mano**: se sobrescriben al regenerar.

## Imágenes
Cada hueco muestra la ruta y el tamaño sugerido. Guarda el archivo con ese nombre y vuelve a regenerar.
- Sirve **.webp, .jpg o .png** con el mismo nombre; el generador detecta la extensión sola (prefiere .webp).
- Si una carpeta tiene `default.webp` (o `1.png`), se usa como imagen temporal para las fotos que falten.
- La lista completa, con lo que ya está listo, está en **IMAGENES.md**.
- Logo de Wiccom: `assets/img/logo-wiccom.png` (color) y `logo-wiccom-blanco.png` (footer).

## Marcas
- Cada marca es un `dict` en `BRANDS` (`data.py`) y tiene su propia página con la misma plantilla:
  logo, descripción, soluciones relacionadas, líneas de producto, aplicaciones y botón de cotización.
- Logo: `assets/img/marcas/<slug>.png` (o .svg/.webp). Si no hay logo, se muestra el nombre.
- Líneas de producto y aplicaciones salen de la categoría (`LINES_BY_CAT`, `APPS_BY_CAT`).
  Para personalizar una marca agrega `lines=[("icono", "Texto"), ...]` y `apps=["...", ...]` en su dict.
- Las marcas del carrusel y su orden se eligen en `MARQUEE` (`data.py`).

## Formularios y CAPTCHA
Todos los formularios (Contacto, Cotización y los modales) piden aceptar el Aviso de Privacidad y pasar
**Cloudflare Turnstile** antes de enviar. `php/enviar.php` vuelve a verificar el CAPTCHA en el servidor,
filtra bots (honeypot + tiempo mínimo), acepta hasta 5 adjuntos de 10 MB y manda el correo.

Antes de publicar:
1. Entra a dash.cloudflare.com → **Turnstile** → *Add site*, con el dominio `wiccom.com.mx`.
2. Copia la **Site Key** en `SITE["turnstile_sitekey"]` (`_generador/base.py`) y regenera.
3. Copia la **Secret Key** en `TURNSTILE_SECRET` (`php/enviar.php`).
4. Configura `DESTINO` y `REMITENTE` en `php/enviar.php`.

Las claves que vienen son las de **prueba** de Cloudflare (siempre aprueban).

En tu computadora (`file://`, `localhost`) y en la vista previa de Vercel el envío se **simula**: Vercel no
ejecuta PHP. El envío real funciona en un hosting con PHP. Si el hosting bloquea `mail()`, usa PHPMailer con SMTP.

## Publicar
- **Hosting con cPanel / Apache:** sube el contenido de esta carpeta a `public_html` (incluye `.htaccess`).
  El `.htaccess` fuerza `https://www.wiccom.com.mx`, quita el `.html` de las URLs y usa `404.html`.
- **Vercel:** *Root Directory* = `wiccom`. `vercel.json` activa URLs limpias.

## Pendiente de confirmar
Los datos de contacto y la dirección son de ejemplo (81 1234 5678, Av. Ejemplo 1234…).
Solo el artículo "Cómo elegir la cámara de seguridad ideal" tiene contenido completo; los demás traen introducción
y un comentario `<!-- CONTENIDO -->` para completar.
