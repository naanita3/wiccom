# -*- coding: utf-8 -*-
"""Genera el sitio estático de Wiccom en ../wiccom
Uso:  python3 build.py
"""
import os, json
CHECK = "check"
from base import *
from data import *

def FEATURED():
    """Marcas del carrusel: las de MARQUEE (data.py); si faltan, completa con las que tengan logo."""
    out = [BRAND[k] for k in MARQUEE if k in BRAND]
    out += [b for b in BRANDS if b not in out and brand_logo(b)]
    return out or BRANDS[:14]


OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGES = []   # para sitemap y buscador

def write(path, title, desc, body_fn, active, schemas=(), crumbs=None, search=None, **kw):
    depth = path.count("/")
    Ctx.r = "../" * depth
    Ctx.page = path
    body = body_fn()
    sch = list(schemas)
    if crumbs:
        sch.append(crumb_schema(crumbs))
    html_ = document(path, title, desc, body, active, SOLUTIONS, SERVICES, BRANDS, schemas=sch, **kw)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(html_)
    if not kw.get("noindex"):
        PAGES.append(path)
    if search:
        SEARCH.append(dict(t=search[0], d=search[1], u=path, k=search[2] if len(search) > 2 else ""))

SEARCH = []

# ------------------------------------------------------------------ tarjetas
def sol_card(s, i=0, arrow_only=False):
    img = ph(f"soluciones/{s['slug']}.jpg", f"{s['name']} para empresas", "800x500")
    txt = s["card"] if arrow_only else s["short"]
    more = f'<span class="link-more">Conocer más {ic("arrow")}</span>'
    return f'''<article class="scard" data-aos="fade-up" data-aos-delay="{i*80}">
  <div class="scard__media">{img}<span class="scard__icon">{ic(s["icon"])}</span></div>
  <div class="scard__body"><h3><a class="card-link" href="{u("soluciones/" + s["slug"] + ".html")}">{s["name"]}</a></h3><p>{txt}</p>{more}</div></article>'''

def srv_card(s, i=0):
    img = ph(f"servicios/{s['img']}.jpg", f"Servicio de {s['name'].lower()} Wiccom", "800x500")
    return f'''<article class="scard" data-aos="fade-up" data-aos-delay="{i*70}">
  <div class="scard__media">{img}<span class="scard__icon">{ic(s["icon"])}</span></div>
  <div class="scard__body"><h3><a class="card-link" href="{u("servicios/" + s["slug"] + ".html")}">{s["name"]}</a></h3><p>{s["short"]}</p><span class="link-more">Conocer más {ic("arrow")}</span></div></article>'''

def inc_card(folder, slug, n, icn, t, d, i):
    img = ph(f"{folder}/{slug}-{n}.jpg", t, "800x450")
    return f'''<article class="scard" data-aos="fade-up" data-aos-delay="{i*80}">
  <div class="scard__media">{img}<span class="scard__icon">{ic(icn)}</span></div>
  <div class="scard__body"><h3>{t}</h3><p>{d}</p></div></article>'''

def rcard(a, horizontal=False, i=0, filt=False):
    img = ph(f"recursos/{a['img']}.jpg", a["title"], "800x450")
    attrs = f' data-cat="{a["cat"]}" data-name="{a["title"]} {a["desc"]}"' if filt else ""
    cls = "rcard rcard--h" if horizontal else "rcard"
    aos = "" if filt else f' data-aos="fade-up" data-aos-delay="{i*80}"'
    return f'''<article class="{cls}"{attrs}{aos}>
  <div class="rcard__media">{img}<span class="tag">{a["catn"]}</span></div>
  <div class="rcard__body"><h3><a class="card-link" href="{u("recursos/" + a["slug"] + ".html")}">{a["title"]}</a></h3><p>{a["desc"]}</p>
  <div class="rcard__meta"><span>{ic("cal")}<time datetime="{a["date"]}">{fdate(a["date"])}</time></span><span class="go">{ic("arrow")}</span></div></div></article>'''

def btn_quote(ctx="", label="Solicitar cotización", cls="btn btn--primary"):
    q = f"?interes={ctx.replace(' ', '%20')}" if ctx else ""
    return f'<a class="{cls}" href="{u("cotizacion.html" + q)}">{label} {ic("arrow")}</a>'

def btn_advisor(ctx="", cls="btn btn--ghost"):
    return f'<button class="{cls}" type="button" data-modal="asesor" data-context="{ctx}">Hablar con un asesor</button>'

# ================================================================== INICIO
# ================================================================== SOLUCIONES vs SERVICIOS
def sol_vs_srv(active=None):
    """Explica la diferencia: Soluciones = QUÉ tecnología; Servicios = CÓMO te acompañamos."""
    sl = "".join(f'<li><a href="{u("soluciones/" + o["slug"] + ".html")}">{ic(o["icon"])}{o["name"]}</a></li>' for o in SOLUTIONS)
    sv = "".join(f'<li><a href="{u("servicios/" + o["slug"] + ".html")}">{ic(o["icon"])}{o["name"]}</a></li>' for o in SERVICES)
    def col(kind, tag, title, text, items, href, cta):
        cur = " svs__col--active" if kind == active else ""
        link = "" if kind == active else f'<a class="link-more" href="{u(href)}">{cta} {ic("arrow")}</a>'
        return (f'<div class="svs__col svs__col--{kind}{cur}" data-aos="fade-up"><span class="svs__tag">{tag}</span>'
                f'<h3>{title}</h3><p>{text}</p><ul class="svs__list">{items}</ul>{link}</div>')
    return f'''<section class="section section--tight svs-wrap" aria-labelledby="h-svs"><div class="container">
  {sec_head("Soluciones y servicios: cómo trabajamos contigo", "Dos partes de un mismo proyecto: la tecnología correcta y el acompañamiento para que funcione.", hid="h-svs")}
  <div class="svs">
    {col("sol", "Soluciones · El qué", "La tecnología que tu empresa necesita", "Áreas de tecnología que diseñamos e integramos con marcas líderes: equipos, infraestructura y sistemas.", sl, "soluciones.html", "Ver soluciones")}
    <div class="svs__plus" aria-hidden="true">{ic("plus")}</div>
    {col("srv", "Servicios · El cómo", "Cómo te acompañamos en cada etapa", "Lo que hacemos para que esa tecnología funcione: asesoría, instalación, configuración, soporte y mantenimiento.", sv, "servicios.html", "Ver servicios")}
  </div>
  <p class="svs__result" data-aos="fade-up">{ic("check")}<span><strong>Resultado:</strong> un proyecto llave en mano, desde la propuesta hasta la operación diaria.</span><a class="btn btn--primary btn--sm" href="{u("cotizacion.html")}">Solicitar cotización {ic("arrow")}</a></p>
</div></section>'''

def srv_for_solution(s):
    """Servicios que acompañan a una solución (enlaces a cada servicio)."""
    items = "".join(f'<a class="srvstep" href="{u("servicios/" + o["slug"] + ".html")}" data-aos="fade-up" data-aos-delay="{i*60}"><span class="srvstep__n">{i+1}</span>{ic(o["icon"])}<strong>{o["name"]}</strong></a>' for i, o in enumerate(SERVICES))
    return f'''<section class="section section--tight" aria-labelledby="h-sfs"><div class="container">
  {sec_head("Servicios que acompañan esta solución", f"No solo suministramos los equipos de {s['name'].lower()}: te acompañamos en cada etapa.", ("Conocer los servicios", "servicios.html"), "h-sfs")}
  <div class="srvsteps">{items}</div>
</div></section>'''

# ================================================================== INICIO
def p_home():
    strip = '<section class="strip" aria-label="Por qué Wiccom"><ul class="container strip__list">' + "".join(
        f'<li class="strip__item" data-aos="fade-up" data-aos-delay="{i*80}">{ic(icn)}<span>{t}</span></li>' for i, (icn, t) in enumerate([
            ("gear", "Asesoría<br>especializada"), ("users", "Soluciones a la<br>medida de tu negocio"),
            ("truck", "Envíos a<br>todo México"), ("shield", "Respaldo y garantía<br>con marcas líderes")])) + "</ul></section>"
    sols = carousel([sol_card(s, i, True) for i, s in enumerate(SOLUTIONS)], per=5, label="Nuestras soluciones")
    stats = '<section class="stats" aria-label="Wiccom en números"><ul class="container stats__list">' + "".join(
        f'<li class="stat" data-aos="fade-up" data-aos-delay="{i*90}">{ic(icn)}<div><strong{a}>{n}</strong><span>{t}</span></div></li>'
        for i, (icn, n, a, t) in enumerate([
            ("users", "+500", ' data-count="500" data-prefix="+"', "Proyectos atendidos"),
            ("clock", "+10 años", ' data-count="10" data-prefix="+" data-suffix=" años"', "De experiencia"),
            ("map", "Empresas", "", "de todo México"),
            ("headset", "Soporte", "", "en cada etapa")])) + "</ul></section>"
    feat = [a for a in ARTICLES if a.get("featured")]
    res = carousel([rcard(a, True, i) for i, a in enumerate(feat)], per=3, label="Recursos destacados")
    srv = carousel([srv_card(s, i) for i, s in enumerate(SERVICES)], per=4, autoplay=6000, label="Servicios")
    return f'''
{hero("Tecnología que conecta, protege y mantiene en operación a", "tu empresa",
      "Soluciones integrales en videovigilancia, redes, energía, control de acceso, cómputo y más, con el respaldo de las mejores marcas.",
      "hero/inicio.jpg", "Técnico de Wiccom junto a cámara de seguridad, cableado y UPS",
      eyebrow="Infraestructura · Seguridad · Conectividad · Energía · Cómputo",
      actions=btn_quote() + f'<a class="btn btn--ghost" href="{u("soluciones.html")}">Conocer soluciones</a>',
      script=("Soluciones hoy", "para un mejor mañana"))}
{strip}
<section class="section" aria-labelledby="h-sol"><div class="container">
  {sec_head("Nuestras soluciones", "Qué tecnología integramos: equipos, infraestructura y sistemas para cada necesidad de tu empresa.", ("Ver todas las soluciones", "soluciones.html"), "h-sol")}
  {sols}
</div></section>
<section class="section section--tight section--alt" aria-labelledby="h-srv"><div class="container">
  {sec_head("Servicios que complementan cada solución", "Cómo te acompañamos: no solo suministramos equipos, los instalamos, configuramos y mantenemos.", ("Conocer nuestros servicios", "servicios.html"), "h-srv")}
  {srv}
</div></section>
{sol_vs_srv()}
<section class="section section--tight section--alt" aria-labelledby="h-brands"><div class="container">
  {sec_head("Marcas que impulsan tus proyectos", "Trabajamos con fabricantes líderes a nivel mundial.", ("Ver todas las marcas", "marcas.html"), "h-brands")}
</div>{marquee(FEATURED(), speed=45)}</section>
{stats}
<section class="section" aria-labelledby="h-res"><div class="container">
  {sec_head("Recursos para tu crecimiento", "Guías, consejos y novedades del mundo tecnológico.", ("Ver todos los artículos", "recursos.html"), "h-res")}
  {res}
</div></section>
{ctaband("¿Tienes un proyecto?<br>Hablemos.", "Nuestro equipo te ayuda a encontrar la solución ideal para tu empresa.", ("Contáctanos", "contacto.html"))}'''

# ================================================================== SOLUCIONES
def p_solutions():
    return f'''
{hero("Soluciones que conectan, protegen y mantienen en operación a", "tu empresa",
      "Integramos tecnología, marcas líderes y experiencia para diseñar soluciones a la medida, desde proyectos empresariales hasta grandes instalaciones.",
      "hero/soluciones.jpg", "Cámara, cableado de red, UPS y equipos de cómputo",
      eyebrow="Infraestructura · Seguridad · Conectividad · Energía · Cómputo",
      actions=btn_quote() + f'<a class="btn btn--ghost" href="{u("contacto.html")}">Contáctanos</a>',
      features=[("shield", "Más seguridad"), ("users", "Mayor productividad"), ("zap", "Operación sin interrupciones"), ("chart", "Crecimiento sostenible")],
      script=("Tecnología para", "un mejor mañana"))}
{intro([("Inicio", "index.html"), ("Soluciones", "soluciones.html")], "Tu aliado en soluciones tecnológicas",
       "Nuestras <strong>soluciones</strong> son las áreas de tecnología que diseñamos e integramos para tu empresa: videovigilancia, redes, energía, control de acceso y cómputo, con el respaldo de las mejores marcas. Cada solución se complementa con nuestros <a class='hl-blue' href='" + u("servicios.html") + "'>servicios</a> de instalación, configuración, soporte y mantenimiento.")}
<section class="section" aria-labelledby="h-nsol"><div class="container">
  {sec_head("Nuestras soluciones", "Tecnología, infraestructura y soporte para cada necesidad de tu empresa.", hid="h-nsol")}
  {carousel([sol_card(s, i) for i, s in enumerate(SOLUTIONS)], per=5, label="Soluciones")}
</div></section>
{sol_vs_srv("sol")}
<section class="section section--tight section--alt"><div class="container">
  <div class="feats-wrap"><div class="feats-wrap__title" data-aos="fade-right"><h2>¿Qué tipo de solución necesitas?</h2><p>Te ayudamos a encontrar la mejor opción para tu empresa.</p></div>
  <div class="feats feats--3">{"".join(f'<div class="feat" data-aos="fade-up" data-aos-delay="{i*90}">{ic(a)}<div><h3>{b}</h3><p>{c}</p></div></div>' for i, (a, b, c) in enumerate([
      ("users", "Asesoría personalizada", "Analizamos tus necesidades y te orientamos en la mejor solución."),
      ("gear", "Tecnología de marcas líderes", "Trabajamos con las mejores marcas del mercado, con calidad y garantía."),
      ("file", "Acompañamiento en tu proyecto", "Te apoyamos desde el diseño hasta la implementación y soporte.")]))}</div></div>
</div></section>
{ctaband("¿Tienes un proyecto?<br>Hablemos.", "Nuestro equipo de expertos te ayudará a encontrar la solución ideal para tu empresa.")}'''

def p_solution(s):
    brands = [BRAND[b] for b in s["brands"]] + [b for b in BRANDS if s["slug"] in b["sols"] and b["slug"] not in s["brands"]]
    brands.sort(key=lambda b: not brand_logo(b))
    apps = carousel([f'<a class="app-tile" href="{u("cotizacion.html?interes=" + s["name"].replace(" ", "%20"))}">{ph("soluciones/" + s["slug"] + f"-app-{i+1}.jpg", a, "600x400")}<span>{a}</span></a>' for i, a in enumerate(s["apps"])], per=5, label="Aplicaciones", cls="carousel--2m")
    others = [o for o in SOLUTIONS if o["slug"] != s["slug"]]
    return f'''
{hero(*s["h1"], s["lead"] + " Tecnología confiable para mantener tus espacios y tu operación funcionando.", f"hero/sol-{s['slug']}.jpg", s["name"],
      eyebrow=s["eyebrow"], actions=btn_quote(s["name"]) + btn_advisor(s["name"]), features=s["feats"], script=s["script"])}
{intro([("Inicio", "index.html"), ("Soluciones", "soluciones.html"), (s["name"], "soluciones/" + s["slug"] + ".html")], s["name"], s["intro"])}
<section class="section" aria-labelledby="h-inc"><div class="container">
  {sec_head("¿Qué incluye esta solución?", "Componentes que integramos según las necesidades de tu proyecto.", hid="h-inc")}
  <div class="grid-4">{"".join(inc_card("soluciones", s["slug"], i+1, *x, i) for i, x in enumerate(s["includes"]))}</div>
</div></section>
<section class="section section--tight section--alt"><div class="container">{feats_row(s["benefits"], "Beneficios para tu empresa", "Más que equipos, resultados para tu operación.")}</div></section>
<section class="section section--tight" aria-labelledby="h-apps"><div class="container">
  <div class="feats-wrap" style="align-items:start"><div class="feats-wrap__title" data-aos="fade-right"><h2 id="h-apps">Aplicaciones</h2><p>Nuestras soluciones de {s["name"].lower()} se adaptan a distintos entornos y sectores.</p></div>{apps}</div>
</div></section>
{srv_for_solution(s)}
<section class="section section--tight section--alt" aria-labelledby="h-mb"><div class="container">
  {sec_head("Trabajamos con las mejores marcas", "Tecnología confiable, alto desempeño y soporte especializado.", ("Ver todas las marcas", "marcas.html"), "h-mb")}
</div>{marquee(brands + brands if len(brands) < 7 else brands, speed=32)}</section>
<section class="section section--tight" aria-labelledby="h-os"><div class="container">
  {sec_head("Otras soluciones", "Integramos varias tecnologías en un mismo proyecto.", ("Ver todas", "soluciones.html"), "h-os")}
  <div class="grid-4">{"".join(f'<a class="pill-link" href="{u("soluciones/" + o["slug"] + ".html")}" data-aos="fade-up" data-aos-delay="{i*60}">{ic(o["icon"])}{o["name"]}</a>' for i, o in enumerate(others))}</div>
</div></section>
{ctaband(s["cta"][0], s["cta"][1], ("Solicitar una propuesta", "cotizacion.html?interes=" + s["name"].replace(" ", "%20")), s["name"])}'''

# ================================================================== SERVICIOS
HOW = [("msg", "Escuchamos", "Conocemos tus necesidades y objetivos."),
       ("file-search", "Analizamos", "Evaluamos la mejor estrategia y solución."),
       ("bulb", "Proponemos", "Te presentamos una propuesta clara y personalizada."),
       ("users", "Acompañamos", "Te respaldamos en la implementación y operación.")]

def p_services():
    return f'''
{hero("Servicios que impulsan", "tus proyectos",
      "En Wiccom complementamos cada solución con servicios de asesoría, instalación, configuración, soporte y acompañamiento para empresas y proyectos.",
      "hero/servicios.jpg", "Técnico de Wiccom instalando una cámara domo",
      eyebrow="Asesoría · Instalación · Configuración · Soporte · Mantenimiento",
      actions=btn_quote() + btn_advisor(), features=[("headset", "Atención especializada"), ("gear", "Implementación confiable"), ("users", "Acompañamiento técnico"), ("sliders", "Soluciones a la medida")],
      script=("Tu proyecto", "en manos expertas"))}
{intro([("Inicio", "index.html"), ("Servicios", "servicios.html")], "Servicios pensados para cada etapa del proyecto",
       "Nuestros <strong>servicios</strong> son el trabajo profesional con el que te acompañamos en todo el ciclo de vida del proyecto: asesorar, instalar, configurar, dar soporte, mantener y capacitar. Aplican sobre cualquiera de nuestras <a class='hl-blue' href='" + u("soluciones.html") + "'>soluciones</a>, incluso si ya cuentas con los equipos.")}
<section class="section" aria-labelledby="h-ns"><div class="container">
  {sec_head("Nuestros servicios", "Soluciones expertas para que tu empresa nunca se detenga.", hid="h-ns")}
  {carousel([srv_card(s, i) for i, s in enumerate(SERVICES)], per=6, label="Servicios")}
</div></section>
{sol_vs_srv("srv")}
<section class="section section--tight section--tint"><div class="container">{steps(HOW, "¿Cómo trabajamos?", "Un proceso simple y efectivo para lograr grandes resultados.")}</div></section>
<section class="section section--tight"><div class="container">{feats_row([
    ("gear", "Experiencia técnica", "Un equipo de especialistas con amplio conocimiento."),
    ("award", "Marcas líderes", "Trabajamos con las mejores marcas del mercado."),
    ("truck", "Cobertura para proyectos", "Atención en todo México."),
    ("users", "Atención cercana", "Relación de largo plazo con nuestros clientes.")])}</div></section>
{ctaband("¿Necesitas apoyo<br>para tu proyecto?", "Nuestro equipo te ayuda a identificar el servicio adecuado para tu empresa.")}'''

def p_service(s):
    others = [o for o in SERVICES if o["slug"] != s["slug"]]
    return f'''
{hero(*s["h1"], s["lead"], f"hero/srv-{s['slug']}.jpg", s["name"], eyebrow=s["eyebrow"],
      actions=btn_quote(s["name"]) + btn_advisor(s["name"]), features=s["feats"], script=("Soluciones de hoy", "para un mejor mañana"))}
{intro([("Inicio", "index.html"), ("Servicios", "servicios.html"), (s["name"], "servicios/" + s["slug"] + ".html")], s["name"], s["intro"], s["sub"])}
<section class="section" aria-labelledby="h-inc"><div class="container">
  {sec_head("¿Qué incluye este servicio?", "Un servicio completo para cuidar tu proyecto con seguridad y confianza.", hid="h-inc")}
  <div class="grid-4">{"".join(inc_card("servicios", s["slug"], i+1, *x, i) for i, x in enumerate(s["includes"]))}</div>
</div></section>
<section class="section section--tight section--tint"><div class="container">{steps(HOW, "¿Cómo trabajamos?", "Un proceso claro y colaborativo, enfocado en tu resultado.")}</div></section>
<section class="section section--tight"><div class="container">{feats_row(s["benefits"], "Beneficios para tu empresa", "Más que un servicio, un aliado para tu crecimiento.")}</div></section>
<section class="section section--tight section--alt"><div class="container">
  <div class="feats-wrap"><div class="feats-wrap__title" data-aos="fade-right"><h2>¿En qué soluciones te apoyamos?</h2><p>Experiencia en múltiples áreas de tecnología.</p></div>
  <div class="grid-4" style="grid-template-columns:repeat(auto-fit,minmax(170px,1fr))">{"".join(f'<a class="pill-link" href="{u("soluciones/" + o["slug"] + ".html")}" data-aos="fade-up" data-aos-delay="{i*60}">{ic(o["icon"])}{o["name"]}</a>' for i, o in enumerate(SOLUTIONS))}</div></div>
</div></section>
<section class="section section--tight" aria-labelledby="h-os"><div class="container">
  {sec_head("Otros servicios", "Complementa tu proyecto de principio a fin.", ("Ver todos", "servicios.html"), "h-os")}
  {carousel([srv_card(o, i) for i, o in enumerate(others)], per=4, label="Otros servicios")}
</div></section>
{ctaband("¿Necesitas orientación<br>para tu proyecto?", "Hablemos sobre tus necesidades y encontremos en conjunto la mejor solución tecnológica.", ("Solicitar asesoría", "cotizacion.html?interes=" + s["name"].replace(" ", "%20")), s["name"])}'''

# ================================================================== MARCAS
def p_brands():
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">Todas</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{k}" aria-pressed="false">{n}</button>' for k, n in CATS)
    sel = '<option value="all">Todas las categorías</option>' + "".join(f'<option value="{k}">{n}</option>' for k, n in CATS)
    tiles = "".join(brand_tile(b, extra=f'data-cat="{b["cats"]}" data-name="{b["name"]}"') for b in BRANDS)
    feats = "".join(f'<div class="icard" data-aos="fade-up" data-aos-delay="{i*80}" style="background:transparent;border:0">{ic(a)}<h3>{b}</h3></div>' for i, (a, b) in enumerate([
        ("shield", "Productos originales y con garantía"), ("gear", "Soluciones para cada necesidad"), ("headset", "Respaldo y soporte técnico"), ("truck", "Disponibilidad a nivel nacional")]))
    return f'''
<section class="mhero"><div class="container mhero__grid">
  <div data-aos="fade-up">{breadcrumb([("Inicio", "index.html"), ("Marcas", "marcas.html")])}
    <h1 style="margin-top:12px">Tecnología de marcas líderes</h1>
    <p class="muted" style="font-size:1.08rem;max-width:520px">Trabajamos con fabricantes reconocidos en seguridad electrónica, redes, telecomunicaciones, infraestructura, energía y cómputo, seleccionando la tecnología adecuada para cada proyecto.</p>
    <div class="hero__actions"><a class="btn btn--primary" href="#directorio">Explorar marcas {ic("arrow")}</a><a class="btn btn--outline" href="{SITE["store"]}" target="_blank" rel="noopener">{ic("cart")} Visitar tienda</a></div></div>
  <div class="mhero__img" data-aos="zoom-in">{ph("marcas/hero-alianzas.jpg", "Apretón de manos frente a edificios corporativos", "1200x900", dark=True, eager=True)}<p>Alianzas que impulsan<br>tus proyectos</p></div>
</div>
<div class="container"><h2 class="sr-only">Por qué comprar con Wiccom</h2><div class="grid-4" style="padding-bottom:28px">{feats}</div></div></section>
<section class="section" id="directorio" aria-labelledby="h-dir"><div class="container" data-filter-group data-page-size="20">
  {sec_head("Directorio de marcas", "Filtra por categoría o busca por nombre.", hid="h-dir")}
  <div class="toolbar"><div class="searchbox">{ic("search")}<label class="sr-only" for="brand-q">Buscar una marca</label><input class="input" id="brand-q" type="search" placeholder="Buscar una marca…" data-filter-search></div>
    <label class="sr-only" for="brand-cat">Categoría</label><select class="input" id="brand-cat" style="max-width:260px" data-filter-select>{sel}</select></div>
  <div class="chips" style="margin-bottom:24px" role="group" aria-label="Filtrar por categoría">{chips}</div>
  <div class="brand-grid" data-filter-items>{tiles}</div>
  <p class="empty-state">No encontramos esa marca en el directorio. <button class="hl-blue" type="button" data-modal="cotizacion" style="font-weight:600">Pídenos que la cotizemos</button>.</p>
  <div class="load-more"><button class="btn btn--outline" type="button" data-load-more>Cargar más marcas {ic("plus")}</button></div>
</div></section>
<section class="section section--tight" style="padding-top:0"><div class="container" style="display:grid;gap:18px">
  <div class="store-invite" data-aos="fade-up">{ic("cart", "ico ico-lg")}<div><h2>¿Buscas otra marca?</h2><p>En nuestra tienda encontrarás un catálogo más amplio de fabricantes y productos.</p></div><a class="btn btn--dark" href="{SITE["store"]}" target="_blank" rel="noopener">Visitar tienda {ic("arrow")}</a></div>
  <div class="store-invite store-invite--plain" data-aos="fade-up">{ic("headset", "ico ico-lg")}<div><h2>¿No encuentras la marca o modelo que buscas?</h2><p>Trabajamos con una amplia red de fabricantes y distribuidores. Podemos ayudarte a localizarlo y cotizarlo.</p></div><button class="btn btn--outline" type="button" data-modal="cotizacion">Solicitar marca o producto</button></div>
</div></section>
{ctaband("¿Tienes un proyecto?<br>Hablemos.", "Te recomendamos la marca y el modelo adecuados para tu necesidad.")}'''

def brand_lines(b):
    if b.get("lines"):
        return b["lines"]
    out, seen = [], set()
    for c in b["cats"].split():
        for icn, t in LINES_BY_CAT.get(c, []):
            if t not in seen:
                seen.add(t); out.append((icn, t))
    return out[:6]

def brand_apps(b):
    if b.get("apps"):
        return b["apps"]
    out = []
    for c in b["cats"].split():
        for t in APPS_BY_CAT.get(c, []):
            if t not in out:
                out.append(t)
    return out[:6]

def p_brand(b):
    sols = [SOL[s] for s in b["sols"]]
    cards = [f'''<article class="scard" data-aos="fade-up" data-aos-delay="{i*80}"><div class="scard__media">{ph("soluciones/" + s["slug"] + ".jpg", s["name"], "800x500")}<span class="scard__icon">{ic(s["icon"])}</span></div>
      <div class="scard__body"><h3><a class="card-link" href="{u("soluciones/" + s["slug"] + ".html")}">{s["name"]}</a></h3><p>{s["short"]}</p><span class="link-more">Ver solución {ic("arrow")}</span></div></article>''' for i, s in enumerate(sols)]
    others = [x for x in BRANDS if x["slug"] != b["slug"] and set(x["cats"].split()) & set(b["cats"].split())][:10] or BRANDS[:10]
    cats = " · ".join(n for k, n in CATS if k in b["cats"].split())
    lines = "".join(f'<div class="bline" data-aos="fade-up" data-aos-delay="{i*70}">{ic(icn)}<h3>{t}</h3></div>' for i, (icn, t) in enumerate(brand_lines(b)))
    apps = "".join(f'<li data-aos="fade-up" data-aos-delay="{i*60}">{ic("check")}<span>{t}</span></li>' for i, t in enumerate(brand_apps(b)))
    q = "cotizacion.html?interes=" + b["name"].replace(" ", "%20")
    return f'''
<section class="mhero mhero--brand"><div class="container mhero__grid">
  <div data-aos="fade-up">{breadcrumb([("Inicio", "index.html"), ("Marcas", "marcas.html"), (b["name"], "marcas/" + b["slug"] + ".html")])}
    <div class="mhero__logo">{brand_tile(b, tag="div")}</div>
    <p class="mhero__cats">{cats}</p>
    <h1 class="mhero__h1"><span class="sr-only">{b["name"]}: </span>{b["lead"]}</h1>
    <p class="muted">{b["desc"]}</p>
    <div class="hero__actions"><a class="btn btn--primary" href="{u(q)}">Solicitar cotización {ic("arrow")}</a><a class="btn btn--outline" href="{SITE["store"]}" target="_blank" rel="noopener">Ver productos en tienda {ic("link")}</a></div></div>
  <div class="mhero__img" data-aos="zoom-in">{ph(f"marcas/{b['slug']}-hero.jpg", f"Productos {b['name']}", "1200x900", dark=True, eager=True)}<p>Tecnología que<br>respalda tu proyecto</p></div>
</div></section>
<section class="section" aria-labelledby="h-bs"><div class="container">
  {sec_head(f"Soluciones relacionadas", f"Integramos productos {b['name']} en estas soluciones.", hid="h-bs")}
  <div class="grid-{min(max(len(cards), 2), 4)}">{"".join(cards)}</div>
</div></section>
<section class="section section--alt" aria-labelledby="h-bl"><div class="container brand-info">
  <div>{sec_head("Líneas de producto", f"Principales líneas de {b['name']} que suministramos e integramos.", hid="h-bl")}
    <div class="bline-grid">{lines}</div></div>
  <div>{sec_head("Aplicaciones", "Dónde se utilizan comúnmente.", hid="h-ba")}
    <ul class="checklist checklist--cards">{apps}</ul></div>
</div></section>
<section class="section section--tight"><div class="container">
  <div class="store-invite store-invite--plain" data-aos="fade-up">{ic("msg", "ico ico-lg")}<div><h2>¿Te interesa implementar {b["name"]} en tu proyecto?</h2><p>Te asesoramos para elegir el modelo adecuado y lo cotizamos con instalación, configuración y soporte.</p></div><div class="store-invite__actions"><a class="btn btn--primary" href="{u(q)}">Solicitar cotización {ic("arrow")}</a>{btn_advisor(b["name"], "btn btn--outline")}</div></div>
</div></section>
<section class="section section--tight section--alt" aria-labelledby="h-ob"><div class="container">{sec_head("Otras marcas relacionadas", "", ("Ver todas las marcas", "marcas.html"), "h-ob")}</div>{marquee(others + others if len(others) < 6 else others, speed=34)}</section>
{ctaband("¿Tienes un proyecto?<br>Hablemos.", f"Te ayudamos a elegir el modelo {b['name']} adecuado para tu necesidad.", ("Solicitar cotización", q), b["name"])}'''

# ================================================================== NOSOTROS
def p_about():
    vals = [("handshake", "Compromiso", "Cumplimos lo que acordamos."), ("shield", "Confianza", "Relaciones transparentes y de largo plazo."),
            ("users", "Integridad", "Actuamos con honestidad."), ("bulb", "Innovación", "Tecnología con propósito."),
            ("user", "Enfoque en el cliente", "Entendemos sus necesidades."), ("star", "Calidad", "En productos, servicios y atención.")]
    areas = [("ingenieria", "gear", "Ingeniería y proyectos", "Diseño e integración de soluciones a la medida."),
             ("atencion", "users", "Atención al cliente", "Asesoría personalizada en cada etapa."),
             ("soporte", "wrench", "Soporte técnico", "Tu operación siempre en buenas manos."),
             ("logistica", "box", "Logística y distribución", "Productos disponibles y entregas confiables.")]
    area_cards = [f'''<article class="scard" data-aos="fade-up" data-aos-delay="{i*80}"><div class="scard__media">{ph(f"nosotros/area-{k}.jpg", t, "800x450")}<span class="scard__icon">{ic(a)}</span></div><div class="scard__body"><h3>{t}</h3><p>{d}</p></div></article>''' for i, (k, a, t, d) in enumerate(areas)]
    diff = [("gear", "Soluciones integrales", "Productos, servicios y soporte en un solo lugar."), ("users", "Atención personalizada", "Te acompañamos en cada etapa."),
            ("chart", "Experiencia comprobada", "Proyectos en diversos sectores."), ("shield", "Alianzas estratégicas", "Trabajamos con fabricantes líderes a nivel global.")]
    return f'''
{hero("Conectando personas con un", "mejor futuro",
      "En Wiccom acercamos la tecnología a las personas, empresas e instituciones, con soluciones confiables, innovadoras y un acompañamiento cercano en cada proyecto.",
      "hero/nosotros.jpg", "Fachada del edificio corporativo de Wiccom", eyebrow="Nosotros",
      actions=f'<a class="btn btn--white" href="{u("soluciones.html")}">Conoce nuestras soluciones {ic("arrow")}</a><a class="btn btn--ghost" href="{u("contacto.html")}">Contáctanos</a>',
      features=[("gear", "Soluciones"), ("users", "Personas"), ("shield", "Confianza"), ("trend", "Crecimiento")], script=("Tecnología que", "impulsa resultados"))}
<section class="section" aria-labelledby="h-who"><div class="container about">
  <div data-aos="fade-right"><h2 id="h-who">¿Quiénes somos?</h2>
    <p>Somos una empresa mexicana especializada en soluciones de Tecnologías de la Información, Telecomunicaciones, Seguridad Electrónica e Infraestructura Tecnológica.</p>
    <p>Acompañamos a nuestros clientes en cada etapa de sus proyectos: desde el diseño y la consultoría, hasta la implementación y el soporte, con un enfoque en calidad, eficiencia y atención personalizada.</p>
    <a class="btn btn--outline" href="#mvv">Conoce más sobre Wiccom {ic("arrow")}</a></div>
  <div class="about__img" data-aos="zoom-in">{ph("nosotros/oficina-recepcion.jpg", "Recepción de las oficinas de Wiccom", "900x600")}</div>
  <figure class="quote-card" data-aos="fade-left" style="margin:0">{ic("quote")}<blockquote>Creemos en el poder de la tecnología para generar oportunidades y construir un futuro más conectado.</blockquote><cite>Equipo Wiccom</cite></figure>
</div></section>
<section class="section section--alt" id="mvv" aria-labelledby="h-mvv"><div class="container">
  {sec_head("Misión, visión y valores", "Nuestros principios guían todo lo que hacemos.", hid="h-mvv")}
  <div class="mvv">
    <div class="mvv__card" data-aos="fade-up"><div class="mvv__title">{ic("target")}<h3>Misión</h3></div><p>Brindar soluciones tecnológicas confiables y de alto valor que impulsen el crecimiento de nuestros clientes.</p></div>
    <div class="mvv__card" data-aos="fade-up" data-aos-delay="100"><div class="mvv__title">{ic("eye")}<h3>Visión</h3></div><p>Ser el aliado tecnológico líder en México, reconocido por nuestra innovación, servicio y compromiso.</p></div>
    <div class="mvv__card mvv__card--values" data-aos="fade-up" data-aos-delay="200"><div class="mvv__title">{ic("users")}<h3>Valores</h3></div>
      <div class="values">{"".join(f'<div class="value">{ic(a)}<h4>{t}</h4><p>{d}</p></div>' for a, t, d in vals)}</div></div>
  </div>
</div></section>
<section class="diff" aria-labelledby="h-diff"><div class="diff__img">{ph("nosotros/tecnico-site.jpg", "Técnico de Wiccom en un site de servidores", "1200x600", dark=True)}</div>
  <div class="container diff__inner"><div data-aos="fade-up"><h2 id="h-diff">Lo que nos diferencia</h2><p style="color:#cfdcf2">Más que productos, ofrecemos soluciones y un verdadero acompañamiento.</p></div>
  <ul class="diff__list">{"".join(f'<li data-aos="fade-up" data-aos-delay="{i*90}">{ic(a)}<div><strong>{t}</strong><span>{d}</span></div></li>' for i, (a, t, d) in enumerate(diff))}</ul></div></section>
<section class="section" aria-labelledby="h-how"><div class="container work">
  <div><h2 id="h-how" data-aos="fade-up">Cómo trabajamos</h2><p class="muted" data-aos="fade-up">Un proceso simple y efectivo para llevar tu proyecto del plan a la realidad.</p>
    {steps([("", "Te escuchamos", "Entendemos tus necesidades."), ("", "Te asesoramos", "Diseñamos la mejor solución."), ("", "Implementamos", "Integramos tecnología de forma eficiente."), ("", "Te acompañamos", "Soporte y seguimiento continuo.")], numbered=True)}</div>
  <div class="work__img" data-aos="zoom-in">{ph("nosotros/reunion-proyecto.jpg", "Asesor de Wiccom revisando un proyecto con un cliente", "900x450")}<p>De la idea<br>a la solución</p></div>
</div></section>
<section class="section section--alt" id="areas" aria-labelledby="h-areas"><div class="container">
  {sec_head("Áreas que respaldan cada proyecto", "Un equipo especializado para ofrecerte la mejor experiencia.", hid="h-areas")}
  {carousel(area_cards, per=4, label="Áreas de Wiccom")}
</div></section>
<section class="section section--tight" aria-labelledby="h-mq"><div class="container">
  {sec_head("Marcas que nos respaldan", "Trabajamos con fabricantes líderes a nivel global.", ("Ver todas las marcas", "marcas.html"), "h-mq")}
</div>{marquee(FEATURED(), speed=40, board=True)}</section>
{ctabig("Hagamos tu próximo proyecto realidad", "Cuéntanos qué necesitas. Nuestro equipo te asesorará para encontrar la mejor solución en tecnología.",
        f'<a class="btn btn--white" href="{u("contacto.html")}">Contáctanos {ic("arrow")}</a><a class="btn btn--ghost" href="{SITE["store"]}" target="_blank" rel="noopener">Visitar tienda</a>',
        tiles=[("file", "Solicita una cotización", "cotizacion.html"), ("msg", "Habla con un asesor", "contacto.html"), ("cart", "Explora nuestra tienda", SITE["store"])])}'''

# ================================================================== RECURSOS
def p_resources():
    feat = [a for a in ARTICLES if a.get("featured")]
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">Todas</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{k}" aria-pressed="false">{n}</button>' for k, n, _, _ in ART_CATS)
    cats = "".join(f'<a class="icard" href="#articulos" data-set-filter="{k}" data-aos="fade-up" data-aos-delay="{i*60}">{ic(a)}<h3>{n}</h3><p>{d}</p></a>' for i, (k, n, a, d) in enumerate(ART_CATS))
    allcards = "".join(rcard(a, filt=True) for a in ARTICLES)
    return f'''
{hero("Recursos para impulsar", "tus decisiones tecnológicas",
      "En Wiccom compartimos guías, tutoriales, comparativas, consejos técnicos y novedades para ayudar a empresas y proyectos a elegir mejor, con información confiable y actualizada.",
      "hero/recursos.jpg", "Cámara, cableado de red y UPS", eyebrow="Recursos",
      actions=f'<a class="btn btn--primary" href="{u("soluciones.html")}">Conocer soluciones {ic("arrow")}</a><a class="btn btn--ghost" href="{u("contacto.html")}">Contáctanos</a>',
      script=("Tecnología, conocimiento,", "mejores decisiones"))}
<section class="section" aria-labelledby="h-fe"><div class="container">
  {sec_head("Recursos destacados", "Contenido seleccionado por nuestro equipo para ayudarte a tomar mejores decisiones.", ("Ver todos los recursos", "#articulos"), "h-fe")}
  {carousel([rcard(a, i=i) for i, a in enumerate(feat)], per=3, autoplay=6500, label="Recursos destacados")}
</div></section>
<section class="section section--tight section--alt" aria-labelledby="h-cat"><div class="container">
  {sec_head("Explora por categoría", "Encuentra fácilmente el contenido que más te interesa.", hid="h-cat")}
  <div class="grid-6">{cats}</div>
</div></section>
<section class="section" id="articulos" aria-labelledby="h-art"><div class="container" data-filter-group data-page-size="6">
  {sec_head("Artículos recientes", "Contenido nuevo y actualizado para mantenerte siempre informado.", hid="h-art")}
  <div class="toolbar"><div class="searchbox">{ic("search")}<label class="sr-only" for="art-q">Buscar artículos</label><input class="input" id="art-q" type="search" placeholder="Buscar recursos, temas o palabras clave…" data-filter-search></div>
    <div class="chips chips--blue" role="group" aria-label="Filtrar por categoría">{chips}</div></div>
  <div class="grid-3" data-filter-items>{allcards}</div>
  <p class="empty-state">No hay artículos con ese criterio. Prueba otra palabra o <a class="hl-blue" href="{u("contacto.html")}">pregúntale a un asesor</a>.</p>
  <div class="load-more"><button class="btn btn--outline" type="button" data-load-more>Cargar más artículos {ic("plus")}</button></div>
</div></section>
<section class="section section--tight" style="padding-top:0"><div class="container duo">
  <div class="duo__card" data-aos="fade-up">{ic("users", "ico ico-lg")}<div style="flex:1"><h2>¿Buscas orientación para tu proyecto?</h2><p>Nuestro equipo de especialistas puede ayudarte a encontrar la mejor solución para tus necesidades.</p>
    <div class="duo__actions">{btn_quote()}{btn_advisor(cls="btn btn--outline")}</div></div></div>
  <div class="duo__card" data-aos="fade-up" data-aos-delay="120">{ic("mail", "ico ico-lg")}<div style="flex:1"><h2>Recibe novedades y consejos</h2><p>Suscríbete y mantente al día con las últimas guías, artículos y noticias del sector.</p>
    <form class="inline-form" data-newsletter novalidate><label class="sr-only" for="nl-res">Tu correo electrónico</label><input id="nl-res" type="email" placeholder="Tu correo electrónico" required autocomplete="email"><button type="submit" aria-label="Suscribirme">{ic("arrow")}</button></form></div></div>
</div></section>
{ctabig("Hablemos de tu próximo proyecto", "Cuéntanos qué necesitas. Nuestro equipo está listo para asesorarte y encontrar la mejor solución en tecnología.",
        f'<a class="btn btn--white" href="{u("contacto.html")}">Contáctanos {ic("arrow")}</a><a class="btn btn--ghost" href="{SITE["store"]}" target="_blank" rel="noopener">Visitar tienda {ic("cart")}</a>',
        script=("Tecnología hoy.", "Oportunidades mañana."))}'''

def article_body_full():
    loc = [("Interior", ["Diseño discreto", "Ideal para oficinas, comercios y hogares", "Opciones fijas o con movimiento (PT)"]),
           ("Exterior", ["Resistencia a intemperie (IP66 o superior)", "Visión nocturna", "Materiales más robustos"])]
    res = [("2 MP (Full HD)", "Uso básico: pasillos y áreas pequeñas."), ("4 MP (2K)", "Mayor detalle para identificar rostros."), ("8 MP (4K)", "Ideal para espacios amplios y mayor precisión.")]
    types = [("Cámara tipo bala", "Ideal para exteriores y largas distancias."), ("Cámara domo", "Diseño discreto y uso en interiores."),
             ("Cámara PTZ", "Movimiento horizontal, vertical y zoom."), ("Cámara Wi-Fi", "Fácil instalación y monitoreo desde el celular.")]
    extra = [("moon", "Visión nocturna", "Imágenes claras en condiciones de poca luz."), ("walk", "Detección de movimiento", "Alertas en tiempo real."),
             ("sound", "Audio bidireccional", "Comunicación en tiempo real."), ("hdd", "Almacenamiento", "NVR, DVR, nube o tarjeta SD.")]
    s = "como-elegir-la-camara-de-seguridad-ideal"
    return f'''
<h2 id="introduccion">Introducción</h2>
<p>Elegir una cámara de seguridad no se trata solo de ver el precio o la resolución. Es importante considerar el entorno, el tipo de instalación, las funciones que realmente necesitas y la compatibilidad con tu sistema. En esta guía te explicamos los puntos clave para tomar la mejor decisión.</p>
<h2 id="lugar">1. Define el lugar de instalación</h2>
<p class="lead">El entorno donde se instalará la cámara es fundamental para elegir el modelo adecuado.</p>
<div class="opt-grid opt-grid--2">{"".join(f'<div class="opt"><div class="opt__img">{ph(f"recursos/{s}-{t.lower()}.jpg", f"Cámara de seguridad en {t.lower()}", "800x450")}</div><div class="opt__body"><h3>{t}</h3><ul class="checklist">{"".join(f"<li>{ic(CHECK)}{x}</li>" for x in xs)}</ul></div></div>' for t, xs in loc)}</div>
<h2 id="resolucion">2. Considera la resolución</h2>
<p class="lead">La resolución determina la calidad de la imagen y el nivel de detalle que podrás ver.</p>
<div class="opt-grid opt-grid--3">{"".join(f'<div class="opt"><div class="opt__img">{ph(f"recursos/{s}-res-{i+1}.jpg", f"Ejemplo de imagen en {t}", "600x340")}</div><div class="opt__body"><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(res))}</div>
<h2 id="tipo">3. Elige el tipo de cámara</h2>
<p class="lead">Existen diferentes tipos de cámaras según tus necesidades.</p>
<div class="opt-grid opt-grid--4">{"".join(f'<div class="opt"><div class="opt__img">{ph(f"recursos/{s}-tipo-{i+1}.jpg", t, "500x400")}</div><div class="opt__body"><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(types))}</div>
<h2 id="caracteristicas">4. Otras características importantes</h2>
<div class="opt-grid opt-grid--4">{"".join(f'<div class="opt opt--center">{ic(a)}<h3 style="font-size:.95rem;margin:0 0 4px">{t}</h3><p style="margin:0;font-size:.84rem;color:var(--muted)">{d}</p></div>' for a, t, d in extra)}</div>
<div class="conclusion" id="conclusion"><div><h2>Conclusión</h2><p>La cámara de seguridad ideal es la que se adapta a tus necesidades específicas. Evalúa el entorno, la resolución, el tipo de cámara y las funciones adicionales para obtener un sistema confiable y eficiente.</p></div>
  {btn_quote("Videovigilancia", "Solicita una cotización")}</div>'''

def p_article(a):
    rel = [x for x in ARTICLES if x["slug"] != a["slug"]]
    rel = sorted(rel, key=lambda x: x["cat"] != a["cat"])[:6]
    if a.get("full"):
        body = article_body_full()
        toc = [("introduccion", "Introducción"), ("lugar", "Lugar de instalación"), ("resolucion", "Resolución"), ("tipo", "Tipo de cámara"), ("caracteristicas", "Características"), ("conclusion", "Conclusión")]
    else:
        body = f'''<h2 id="introduccion">Introducción</h2><p>{a["desc"]}</p>
<!-- ============================================================
     CONTENIDO DEL ARTÍCULO: reemplaza este bloque con el texto final.
     Usa <h2 id="..."> para cada sección (se agregan solas al índice
     si también las listas en la variable toc de build.py).
     ============================================================ -->
<p>Mientras publicamos la versión completa de este artículo, nuestro equipo puede resolver tus dudas sobre este tema de forma directa y sin compromiso.</p>
<div class="conclusion" id="conclusion"><div><h2>¿Tienes dudas sobre este tema?</h2><p>Un asesor de Wiccom te ayuda a elegir la opción adecuada para tu proyecto.</p></div>{btn_advisor(a["title"], "btn btn--primary")}</div>'''
        toc = [("introduccion", "Introducción"), ("conclusion", "Siguiente paso")]
    toc_html = "".join(f'<a href="#{i}">{t}</a>' for i, t in toc)
    return f'''
<section class="ahero" aria-labelledby="hero-title"><div class="ahero__img">{ph(f"recursos/{a['img']}.jpg", a["title"], "1600x900", dark=True, eager=True)}</div>
  <div class="container"><div class="ahero__inner">{breadcrumb([("Recursos", "recursos.html"), (dict((k, n) for k, n, _, _ in ART_CATS)[a["cat"]], "recursos.html?categoria=" + a["cat"] + "#articulos"), (a["title"].strip("¿?"), "recursos/" + a["slug"] + ".html")]).replace('class="breadcrumb"', 'class="breadcrumb" style="--muted:#b8c7e3"')}
    <span class="cat" style="margin-top:22px">{a["catn"]}</span><h1 id="hero-title" data-aos="fade-up">{a["title"]}</h1><p data-aos="fade-up" data-aos-delay="100">{a["desc"]}</p></div></div></section>
<div class="container">
  <div class="ameta"><span><span class="avatar" aria-hidden="true">W</span> Equipo Wiccom</span><span>{ic("cal")}<time datetime="{a["date"]}">{fdate(a["date"], True)}</time></span><span>{ic("clock")} Lectura: {a["read"]} min</span>
    <div class="share"><span>Compartir:</span><a data-share="linkedin" href="#" target="_blank" rel="noopener" aria-label="Compartir en LinkedIn">{ic("linkedin")}</a><a data-share="facebook" href="#" target="_blank" rel="noopener" aria-label="Compartir en Facebook">{ic("facebook")}</a><a data-share="whatsapp" href="#" target="_blank" rel="noopener" aria-label="Compartir por WhatsApp">{ic("wa")}</a><button type="button" data-copy-link aria-label="Copiar enlace">{ic("link")}</button></div></div>
  <div class="article">
    <article class="prose">{body}</article>
    <aside class="article__aside" aria-label="Contenido relacionado">
      <nav class="help-card toc" aria-label="Índice del artículo"><h3 style="margin-top:0">En este artículo</h3>{toc_html}</nav>
      <div class="help-card">{ic("mail")}<h3>¿Necesitas ayuda para tu proyecto?</h3><p>Nuestro equipo te asesora sin compromiso.</p><a class="btn btn--primary btn--block btn--sm" href="{u("contacto.html")}">Contáctanos {ic("arrow")}</a></div>
    </aside>
  </div>
</div>
<section class="section section--alt" aria-labelledby="h-rel"><div class="container">
  {sec_head("Artículos relacionados", "", ("Ver todos", "recursos.html#articulos"), "h-rel")}
  {carousel([rcard(x, i=i) for i, x in enumerate(rel)], per=3, label="Artículos relacionados")}
</div></section>
{ctaband("¿Tienes un proyecto<br>en mente?", "Nuestro equipo te asesora para encontrar la mejor solución en tecnología.")}'''

# ================================================================== COTIZACIÓN
def quote_form(idp="cz", title="Completa el formulario", sub="Nos pondremos en contacto contigo para brindarte una propuesta personalizada.", tipo="Solicitud de cotización"):
    return f'''<div class="form-card" id="formulario" data-aos="fade-up"><h2>{title}</h2><p>{sub}</p>
  <form action="{u("php/enviar.php")}" method="post" enctype="multipart/form-data" data-validate novalidate>
    <input type="hidden" name="tipo" value="{tipo}"><input type="hidden" name="_ts" value="">
    <div class="hp" aria-hidden="true"><label>No llenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="form-grid">
      {field("nombre", "Nombre", required=True, ph="Ej. Juan Pérez", ac="name", idp=idp)}
      {field("empresa", "Empresa", required=True, ph="Ej. Nombre de tu empresa", ac="organization", idp=idp)}
      {field("correo", "Correo electrónico", "email", True, "nombre@empresa.com", "email", idp=idp)}
      {field("telefono", "Teléfono", "tel", True, "Ej. 81 1234 5678", "tel", idp=idp)}
      {field("interes", "Solución, producto o servicio requerido", "select", True, idp=idp, options=options_html(SOLUTIONS, SERVICES), from_url=True)}
      {field("ciudad", "Ciudad / Estado", ph="Ej. Monterrey, N.L.", ac="address-level2", idp=idp, opt=True)}
      {field("mensaje", "Descripción de tu proyecto o necesidad", "textarea", True, "Cuéntanos más detalles: número de equipos, ubicaciones, fechas, etc.", idp=idp)}
      {dropzone(idp)}
      <div class="field field--full">{privacy(idp)}</div>
      {captcha(idp)}
    </div>
    <div class="form-actions" style="margin-top:18px"><button class="btn btn--primary" type="submit">Enviar solicitud {ic("send")}</button><span class="secure">{ic("lock")} Tus datos están protegidos. Solo los usamos para atender tu solicitud.</span></div>
  </form>{success()}</div>'''

def channels_card():
    h = SITE["hours"]
    return f'''<div class="aside-card" data-aos="fade-left"><h2>¿Prefieres atención directa?</h2><p>Estamos listos para asesorarte por el canal de tu preferencia.</p>
  <div class="channels">
    <a class="channel" href="{wa_url()}" target="_blank" rel="noopener"><span class="channel__ico channel__ico--wa">{ic("wa")}</span><span><strong>WhatsApp</strong><span>{SITE["phone_display"]} · Escríbenos ahora</span></span>{ic("chev-r", "ico go")}</a>
    <a class="channel" href="tel:{SITE["phone_tel"]}"><span class="channel__ico">{ic("phone")}</span><span><strong>Teléfono</strong><span>{SITE["phone_display"]}</span></span>{ic("chev-r", "ico go")}</a>
    <a class="channel" href="mailto:{SITE["email"]}"><span class="channel__ico">{ic("mail")}</span><span><strong>Correo electrónico</strong><span>{SITE["email"]}</span></span>{ic("chev-r", "ico go")}</a>
    <div class="channel"><span class="channel__ico">{ic("clock")}</span><span><strong>Horario de atención</strong><span>{h[0][0]}: {h[0][1]}<br>{h[1][0]}: {h[1][1]}</span></span></div>
  </div>
  <div class="note" style="margin-top:12px">{ic("msg")}<span><strong>Tiempo estimado de respuesta: 24 h hábiles.</strong><br>Un especialista se pondrá en contacto contigo.</span></div></div>'''

def p_quote():
    mini = "".join(f'<a href="{u("soluciones/" + s["slug"] + ".html")}">{ic(s["icon"])}{s["name"]}</a>' for s in SOLUTIONS)
    return f'''
{hero("Solicita una", "cotización", "Cuéntanos qué necesitas y te ayudaremos a encontrar la solución adecuada para tu empresa o proyecto.",
      "hero/cotizacion.jpg", "Cámara domo de videovigilancia", eyebrow="Asesoría · Planeación · Tecnología",
      badges=[("shield", "Asesoría especializada en cada proyecto"), ("clock", "Soluciones a la medida"), ("users", "Respuesta rápida y acompañamiento")],
      features=[("shield", "Tecnología para un futuro más seguro"), ("users", "Expertos en soluciones integrales"), ("user", "Te acompañamos en todo el proceso"), ("gear", "Tu aliado tecnológico de confianza")],
      script=("Proyectos más seguros,", "empresas más fuertes"))}
<div class="intro"><div class="container" style="padding:14px 0">{breadcrumb([("Inicio", "index.html"), ("Contacto", "contacto.html"), ("Solicita una cotización", "cotizacion.html")])}</div></div>
<section class="section"><div class="container quote-grid">
  {quote_form()}
  <div class="aside-stack">
    {channels_card()}
    <div class="aside-card" data-aos="fade-left" data-aos-delay="100"><h2>¿Qué puedes cotizar?</h2><p>Nuestras soluciones se adaptan a las necesidades de tu empresa.</p>
      <div class="mini-sol">{mini}<a href="{SITE["store"]}" target="_blank" rel="noopener">{ic("plus")}Y más en la tienda</a></div>
      <div class="note">{ic("msg")}<span><strong>¿No estás seguro de qué solución necesitas?</strong><br>Cuéntanos tu proyecto y te asesoramos sin compromiso.</span></div></div>
  </div>
</div></section>
{ctaband("¿Listo para un entorno<br>más seguro?", "Si ya cuentas con planos o lista de materiales, adjúntalos para agilizar la revisión.", ("Hablar con un asesor", "contacto.html"))}'''

# ================================================================== CONTACTO
def p_contact():
    h = SITE["hours"]
    faqs = "".join(f'<details data-aos="fade-up" data-aos-delay="{(i%3)*80}"><summary>{ic(a)}<span>{q}</span></summary><p>{r}</p></details>' for i, (a, q, r) in enumerate(FAQ))
    maps_q = f"{SITE['street']}, {SITE['city']}, {SITE['region']}".replace(" ", "+")
    return f'''
{hero("Estamos para", "ayudarte", "Cuéntanos qué necesitas y nuestro equipo te asesorará para encontrar la mejor solución en tecnología.",
      "hero/contacto.jpg", "Laptop con logotipo Wiccom y audífonos de atención a clientes", eyebrow="Contacto", compact=True,
      badges=[("msg", "Respuesta rápida"), ("users", "Atención personalizada"), ("shield", "Acompañamiento en tu proyecto")],
      script=("Tu proyecto comienza", "con una conversación"))}
<section class="section"><div class="container grid-2" style="align-items:start">
  <div class="form-card" data-aos="fade-up"><h2>Envíanos un mensaje</h2><p>Completa el formulario y uno de nuestros asesores se pondrá en contacto a la brevedad.</p>
    <form action="{u("php/enviar.php")}" method="post" data-validate novalidate>
      <input type="hidden" name="tipo" value="Mensaje de contacto"><input type="hidden" name="_ts" value="">
      <div class="hp" aria-hidden="true"><label>No llenar<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <div class="form-grid">
        {field("nombre", "Nombre completo", required=True, ph="Tu nombre", ac="name", idp="ct")}
        {field("empresa", "Empresa", ph="Nombre de tu empresa", ac="organization", idp="ct", opt=True)}
        {field("correo", "Correo electrónico", "email", True, "nombre@empresa.com", "email", idp="ct")}
        {field("telefono", "Teléfono", "tel", True, "Ej. 81 1234 5678", "tel", idp="ct")}
        {field("interes", "¿En qué podemos ayudarte?", "select", True, idp="ct", options=options_html(SOLUTIONS, SERVICES), full=True, from_url=True)}
        {field("mensaje", "Mensaje", "textarea", True, "Cuéntanos los detalles de tu proyecto…", idp="ct")}
        <div class="field field--full">{privacy("ct")}</div>
      {captcha("ct")}
      </div>
      <div class="form-actions" style="margin-top:18px"><button class="btn btn--primary btn--block" type="submit">Enviar mensaje {ic("arrow")}</button></div>
    </form>{success()}</div>
  <div><h2 data-aos="fade-up" style="color:var(--blue)">Otras formas de contactarnos</h2><p class="muted" data-aos="fade-up">Elige el medio que prefieras, estamos listos para atenderte.</p>
    <div class="contact-cards">
      <div class="ccard" data-aos="fade-up"><span class="ccard__ico ccard__ico--wa">{ic("wa")}</span><h3>WhatsApp</h3><p>Chatea con un asesor de forma inmediata.</p><a class="btn btn--wa btn--sm" href="{wa_url()}" target="_blank" rel="noopener">Abrir WhatsApp {ic("arrow")}</a></div>
      <div class="ccard" data-aos="fade-up" data-aos-delay="80"><span class="ccard__ico">{ic("phone")}</span><h3>Teléfono</h3><p>Llámanos para atención directa.</p><strong>{SITE["phone_display"]}</strong><a class="btn btn--outline btn--sm" href="tel:{SITE["phone_tel"]}">Llamar ahora {ic("arrow")}</a></div>
      <div class="ccard" data-aos="fade-up" data-aos-delay="160"><span class="ccard__ico">{ic("mail")}</span><h3>Correo electrónico</h3><p>Envíanos tu solicitud o dudas.</p><strong style="font-size:.95rem">{SITE["email_sales"]}<br>{SITE["email"]}</strong><a class="btn btn--outline btn--sm" href="mailto:{SITE["email_sales"]}">Enviar correo {ic("arrow")}</a></div>
      <div class="ccard" data-aos="fade-up" data-aos-delay="240"><span class="ccard__ico">{ic("clock")}</span><h3>Horario de atención</h3><p>{h[0][0]}<br><strong>{h[0][1]}</strong></p><p>{h[1][0]}<br><strong>{h[1][1]}</strong></p></div>
    </div></div>
</div></section>
<section class="section section--alt" aria-labelledby="h-visit"><div class="container visit">
  <div class="visit__info" data-aos="fade-right"><div><h2 id="h-visit">Visítanos</h2><p class="muted">Te recibimos en nuestras oficinas en {SITE["city"]}, {SITE["region_short"]}</p></div>
    <div class="visit__item">{ic("pin")}<div><h3>Dirección</h3><p>{SITE["street"]}<br>{SITE["city"]}, {SITE["region_short"]} C.P. {SITE["zip"]}</p></div></div>
    <div class="visit__item">{ic("globe")}<div><h3>Cobertura</h3><p>Atendemos proyectos en todo México.</p></div></div>
    <a class="btn btn--outline" style="justify-self:start" href="https://www.google.com/maps/dir/?api=1&destination={maps_q}" target="_blank" rel="noopener">{ic("pin")} Cómo llegar {ic("arrow")}</a></div>
  <div class="map" data-aos="zoom-in"><iframe title="Ubicación de Wiccom en Google Maps" src="https://www.google.com/maps?q={maps_q}&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
<section class="section" id="faq" aria-labelledby="h-faq"><div class="container">
  {sec_head("Preguntas frecuentes", "Respuestas rápidas a las dudas más comunes.", hid="h-faq")}
  <div class="faq">{faqs}</div>
</div></section>
{ctabig("Conectemos tu próximo proyecto", "Ya sea un proyecto de infraestructura, seguridad, redes o cómputo, nuestro equipo está listo para ayudarte.",
        f'<a class="btn btn--white" href="{u("cotizacion.html")}">Solicita una cotización {ic("arrow")}</a><a class="btn btn--ghost" href="{wa_url()}" target="_blank" rel="noopener">Chatea en WhatsApp {ic("arrow")}</a>',
        script=("Tecnología que acerca", "grandes ideas"))}'''

# ================================================================== LEGALES / 404
def p_legal(kind):
    if kind == "privacidad":
        t, body = "Aviso de privacidad", f'''
<p class="muted"><em>Texto de referencia. Debe ser revisado y validado por el área legal de Wiccom antes de publicarse.</em></p>
<h2>Responsable del tratamiento</h2><p>Wiccom, con domicilio en {SITE["street"]}, {SITE["city"]}, {SITE["region"]}, es responsable del tratamiento de tus datos personales conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares.</p>
<h2>Datos que recabamos</h2><p>Nombre, empresa, correo electrónico, teléfono, ciudad y la información que compartas sobre tu proyecto, incluidos los archivos que adjuntes.</p>
<h2>Finalidades</h2><p>Atender tus solicitudes de cotización, asesoría y soporte; darte seguimiento comercial y, si lo autorizas, enviarte información sobre productos, servicios y novedades.</p>
<h2>Derechos ARCO</h2><p>Puedes acceder, rectificar, cancelar u oponerte al uso de tus datos escribiendo a <a class="hl-blue" href="mailto:{SITE["email"]}">{SITE["email"]}</a>.</p>
<h2>Cambios al aviso</h2><p>Cualquier modificación se publicará en esta página.</p>'''
    else:
        t, body = "Términos y condiciones", f'''
<p class="muted"><em>Texto de referencia. Debe ser revisado y validado por el área legal de Wiccom antes de publicarse.</em></p>
<h2>Uso del sitio</h2><p>La información publicada en wiccom.com.mx es informativa. Las especificaciones de productos pertenecen a sus fabricantes y pueden cambiar sin previo aviso.</p>
<h2>Cotizaciones</h2><p>Las cotizaciones tienen la vigencia indicada en cada documento y están sujetas a disponibilidad de inventario.</p>
<h2>Marcas registradas</h2><p>Las marcas y logotipos mostrados pertenecen a sus respectivos titulares y se usan únicamente para identificar los productos que comercializamos.</p>
<h2>Tienda en línea</h2><p>Las compras realizadas en {SITE["store"].replace("https://", "")} se rigen por los términos publicados en esa plataforma.</p>'''
    return f'''<section class="section"><div class="container legal">{breadcrumb([("Inicio", "index.html"), (t, "#")])}<h1 style="margin-top:14px;font-size:clamp(1.8rem,3vw,2.4rem)">{t}</h1>{body}</div></section>'''

def p_404():
    return f'''<section class="notfound"><div class="container"><p class="notfound__code" data-aos="zoom-in">404</p>
<h1 style="font-size:clamp(1.6rem,3vw,2.2rem)">Esta página no existe o cambió de lugar</h1>
<p class="muted">Revisa la dirección o continúa desde alguna de estas secciones.</p>
<div class="hero__actions" style="justify-content:center"><a class="btn btn--primary" href="{u("index.html")}">Ir al inicio {ic("arrow")}</a><a class="btn btn--outline" href="{u("soluciones.html")}">Ver soluciones</a><a class="btn btn--outline" href="{u("contacto.html")}">Contacto</a></div></div></section>'''

# ================================================================== BUILD
def build():
    Ctx.images.clear(); PAGES.clear(); SEARCH.clear()
    write("index.html", "Wiccom | Videovigilancia, redes, energía y cómputo en Monterrey",
          "Tecnología que conecta, protege y mantiene en operación a tu empresa. Videovigilancia, redes, energía, control de acceso y cómputo con marcas líderes. Envíos a todo México.",
          p_home, "inicio", schemas=[{"@context": "https://schema.org", "@type": "WebSite", "name": "Wiccom", "url": SITE["domain"] + "/"}],
          search=("Inicio", "Tecnología que conecta, protege y mantiene en operación a tu empresa."), keywords="Wiccom, videovigilancia Monterrey, redes, cableado estructurado, UPS, control de acceso, cómputo empresarial")
    write("soluciones.html", "Soluciones tecnológicas para empresas", "Videovigilancia, redes y cableado, energía y respaldo, control de acceso y cómputo. Diseñamos soluciones a la medida con marcas líderes.",
          p_solutions, "soluciones", crumbs=[("Inicio", "index.html"), ("Soluciones", "soluciones.html")],
          search=("Soluciones", "Todas las soluciones tecnológicas de Wiccom."))
    for s in SOLUTIONS:
        write(f"soluciones/{s['slug']}.html", f"{s['name']} para empresas", f"{s['lead']} Solicita tu cotización con Wiccom.",
              lambda s=s: p_solution(s), "soluciones", crumbs=[("Inicio", "index.html"), ("Soluciones", "soluciones.html"), (s["name"], f"soluciones/{s['slug']}.html")],
              schemas=[{"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": s["lead"], "provider": {"@id": SITE["domain"] + "/#org"}, "areaServed": "MX"}],
              og_img=f"assets/img/hero/sol-{s['slug']}.jpg", keywords=s["kw"], search=(s["name"], s["short"], s["kw"]))
    write("servicios.html", "Servicios de instalación, soporte y mantenimiento", "Asesoría, instalación, configuración, soporte técnico, mantenimiento y capacitación para cada etapa de tu proyecto tecnológico.",
          p_services, "servicios", crumbs=[("Inicio", "index.html"), ("Servicios", "servicios.html")], search=("Servicios", "Asesoría, instalación, configuración, soporte, mantenimiento y capacitación."))
    for s in SERVICES:
        write(f"servicios/{s['slug']}.html", s["name"], f"{s['lead'][:150]}",
              lambda s=s: p_service(s), "servicios", crumbs=[("Inicio", "index.html"), ("Servicios", "servicios.html"), (s["name"], f"servicios/{s['slug']}.html")],
              schemas=[{"@context": "https://schema.org", "@type": "Service", "name": s["name"], "description": s["lead"], "provider": {"@id": SITE["domain"] + "/#org"}, "areaServed": "MX"}],
              keywords=s["kw"], search=(s["name"], s["short"], s["kw"]))
    write("marcas.html", "Marcas con las que trabajamos", "Hikvision, Dahua, Ubiquiti, Fortinet, Dell, APC, Panduit y más. Productos originales, con garantía y soporte técnico.",
          p_brands, "marcas", crumbs=[("Inicio", "index.html"), ("Marcas", "marcas.html")], search=("Marcas", "Directorio de fabricantes con los que trabajamos."))
    for b in BRANDS:
        write(f"marcas/{b['slug']}.html", f"{b['name']} en Monterrey | Distribuidor e integrador", f"{b['lead']} {b['desc'][:90]}… Cotiza {b['name']} con Wiccom.",
              lambda b=b: p_brand(b), "marcas", crumbs=[("Inicio", "index.html"), ("Marcas", "marcas.html"), (b["name"], f"marcas/{b['slug']}.html")],
              search=(b["name"], b["lead"], b["cats"]))
    write("nosotros.html", "Nosotros | Conoce a Wiccom", "Empresa mexicana especializada en TI, telecomunicaciones, seguridad electrónica e infraestructura tecnológica. Conoce nuestra misión, visión y forma de trabajar.",
          p_about, "nosotros", crumbs=[("Inicio", "index.html"), ("Nosotros", "nosotros.html")], search=("Nosotros", "Misión, visión, valores y equipo de Wiccom."))
    write("recursos.html", "Recursos: guías, comparativas y consejos técnicos", "Guías, tutoriales, comparativas y consejos técnicos sobre videovigilancia, redes, energía y cómputo para tomar mejores decisiones.",
          p_resources, "recursos", crumbs=[("Inicio", "index.html"), ("Recursos", "recursos.html")], search=("Recursos", "Guías, tutoriales y comparativas."))
    for a in ARTICLES:
        write(f"recursos/{a['slug']}.html", a["title"], a["desc"], lambda a=a: p_article(a), "recursos", article=True, og_type="article",
              og_img=f"assets/img/recursos/{a['img']}.jpg",
              crumbs=[("Inicio", "index.html"), ("Recursos", "recursos.html"), (a["title"], f"recursos/{a['slug']}.html")],
              schemas=[{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": a["date"], "dateModified": a["date"],
                        "image": SITE["domain"] + "/assets/img/" + (find_img(f"recursos/{a['img']}") or f"recursos/{a['img']}.jpg"), "author": {"@type": "Organization", "name": "Wiccom"}, "publisher": {"@id": SITE["domain"] + "/#org"},
                        "mainEntityOfPage": SITE["domain"] + f"/recursos/{a['slug']}", "inLanguage": "es-MX"}],
              search=(a["title"], a["desc"], a["catn"]))
    write("cotizacion.html", "Solicita una cotización", "Cuéntanos tu proyecto y recibe una propuesta personalizada en menos de 24 horas hábiles. Adjunta planos o listas de materiales.",
          p_quote, "contacto", crumbs=[("Inicio", "index.html"), ("Contacto", "contacto.html"), ("Solicita una cotización", "cotizacion.html")], search=("Solicitar cotización", "Formulario de cotización con carga de archivos.", "precio presupuesto"))
    write("contacto.html", "Contacto", f"Contáctanos por WhatsApp, teléfono o correo. Oficinas en {SITE['city']}, {SITE['region_short']} y cobertura en todo México.",
          p_contact, "contacto", crumbs=[("Inicio", "index.html"), ("Contacto", "contacto.html")],
          schemas=[{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for _, q, r in FAQ]}],
          search=("Contacto", "Teléfono, WhatsApp, correo, dirección y preguntas frecuentes.", "ubicación horario"))
    write("aviso-de-privacidad.html", "Aviso de privacidad", "Conoce cómo Wiccom recaba, usa y protege tus datos personales, y cómo ejercer tus derechos ARCO conforme a la ley mexicana.", lambda: p_legal("privacidad"), "", search=("Aviso de privacidad", "Tratamiento de datos personales."))
    write("terminos.html", "Términos y condiciones", "Términos y condiciones de uso del sitio web de Wiccom: contenido, cotizaciones, propiedad intelectual y enlaces a la tienda en línea.", lambda: p_legal("terminos"), "", search=("Términos y condiciones", "Condiciones de uso del sitio."))
    write("404.html", "Página no encontrada", "La página que buscas no existe o cambió de dirección. Explora nuestras soluciones, servicios y marcas desde aquí.", p_404, "", noindex=True)

    # --- archivos auxiliares
    js = "window.SEARCH_INDEX=" + json.dumps(SEARCH, ensure_ascii=False) + ";"
    open(os.path.join(OUT, "assets/js/search-index.js"), "w", encoding="utf-8").write(js)
    urls = "".join(f"<url><loc>{SITE['domain']}/{clean(p)}</loc><changefreq>{'weekly' if p.startswith('recursos') else 'monthly'}</changefreq><priority>{'1.0' if p == 'index.html' else '0.8' if p.count('/') == 0 else '0.6'}</priority></url>\n" for p in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /php/\n\nSitemap: {SITE['domain']}/sitemap.xml\n")
    return Ctx.images

if __name__ == "__main__":
    imgs = build()
    done = sum(1 for v in imgs.values() if v[3])
    lines = ["# Imágenes que necesita el sitio\n",
             f"**{done} de {len(imgs)} listas.** Guarda cada archivo en la ruta indicada (relativa a la carpeta del sitio) y vuelve a correr `python build.py`.\n",
             "- Puedes usar **.webp, .jpg o .png** con el mismo nombre: el generador detecta la extensión sola (si hay varias, usa primero .webp).",
             "- Mientras falte una foto se muestra un recuadro con la ruta. Si en la carpeta existe `default.webp` (o `1.png`), se usa como imagen temporal.",
             "- Peso recomendado: < 250 KB para fotos y < 400 KB para héroes. Convierte a WebP en squoosh.app.\n",
             "| Estado | Ruta | Qué debe mostrar | Tamaño sugerido |", "|---|---|---|---|"]
    for p, (alt, size, pages, ok) in sorted(imgs.items(), key=lambda kv: (kv[1][3], kv[0])):
        lines.append(f"| {'✅' if ok else '⏳'} | `assets/img/{p}` | {alt} | {size} |")
    open(os.path.join(OUT, "IMAGENES.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(len(PAGES), "páginas ·", len(imgs), "imágenes")
