from pathlib import Path
from html import escape
from urllib.parse import urlencode
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://hecho-a-mano-0823.vercel.app'
PHONE = '50489235110'

ICONS = {
    'arrow': '<path d="M4 12h15m-6-6 6 6-6 6"/>',
    'chevron': '<path d="m9 5 7 7-7 7"/>',
    'heart': '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>',
    'spark': '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z"/>',
    'gift': '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v9h14v-9M12 8v13M12 8H7.5A2.5 2.5 0 1 1 10 5.5L12 8Zm0 0h4.5A2.5 2.5 0 1 0 14 5.5L12 8Z"/>',
    'flower': '<path d="M12 12c-10-1-5-12 0-5 5-7 10 4 0 5Zm0 0c-8 6-13-5-4-6M12 12c8 6 13-5 4-6M12 12c-5 8-11 2-8-2M12 12c5 8 11 2 8-2M12 17v5m0-2c-5 0-5-3-5-3 4 0 5 3 5 3Z"/>',
    'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    'zoom': '<circle cx="10" cy="10" r="6"/><path d="m15 15 5 5M7 10h6m-3-3v6"/>',
    'close': '<path d="m6 6 12 12M6 18 18 6"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'whatsapp': '<path d="M20.5 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-4.6A8.5 8.5 0 1 1 20.5 11.5Z"/><path d="M8 7.5c-.5 0-1 .5-1 1.3 0 2.9 3.4 6.2 6.5 6.2.8 0 1.6-.7 1.6-1.3l-2-1-1 1c-1.5-.6-2.7-1.8-3.3-3.2l1-1-1-2Z"/>',
}

def icon(name):
    return f'<svg class="{name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def tr(es, en, tag='span', **attrs):
    attr = ' '.join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k,v in attrs.items())
    return f'<{tag} data-es="{escape(es, quote=True)}" data-en="{escape(en, quote=True)}" {attr}>{escape(es)}</{tag}>'

def wa(message):
    return f'https://wa.me/{PHONE}?' + urlencode({'text': message})

GENERAL_ES = '¡Hola, Hecho a Mano! Me gustaría saber más sobre sus piezas tejidas y hacer un pedido.'
GENERAL_EN = "Hello, Hecho a Mano! I'd like to learn more about your crochet pieces and place an order."

def contact(label_es, label_en, cls='button button-primary', message_es=GENERAL_ES, message_en=GENERAL_EN, **attrs):
    attr = ' '.join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k,v in attrs.items())
    return f'<a class="{cls}" href="{escape(wa(message_es), quote=True)}" data-whatsapp-es="{escape(message_es, quote=True)}" data-whatsapp-en="{escape(message_en, quote=True)}" target="_blank" rel="noopener noreferrer" {attr}>{icon("whatsapp")}{tr(label_es,label_en)}</a>'

def image(name, alt_es, alt_en, cls='', eager=False, sizes='(max-width: 640px) 45vw, 30vw'):
    path = Path(name).stem
    priority = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="{cls}" src="images/web/{path}.webp" srcset="images/web/{path}-small.webp 480w, images/web/{path}.webp 1000w" sizes="{sizes}" alt="{escape(alt_es,quote=True)}" data-alt-es="{escape(alt_es,quote=True)}" data-alt-en="{escape(alt_en,quote=True)}" {priority} decoding="async">'

def button_link(href, es, en, cls='button button-primary'):
    return f'<a class="{cls}" href="{href}">{tr(es,en)}{icon("arrow")}</a>'

def header(home=False):
    prefix = '' if home else 'index.html'
    return f'''
<a class="skip-link" href="#main">{tr('Saltar al contenido','Skip to content')}</a>
<div class="announcement">{tr('Hecho a mano, elegido con el corazón.','Handmade with care. Chosen with love.')}{tr('Piezas únicas · Pedidos personalizados','Unique pieces · Custom orders')}</div>
<header class="site-header" id="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="Hecho a Mano — Inicio">
      <img src="images/web/logo-small.webp" alt="Logo de Hecho a Mano" width="54" height="54">
      <span><span class="brand-name">Hecho a Mano</span>{tr('PUNTADAS QUE CONECTAN','STITCHES THAT CONNECT',class_='brand-note').replace('class-=', 'class=')}</span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Navegación principal" data-aria-es="Navegación principal" data-aria-en="Main navigation">
      <a href="{prefix}#colecciones">{tr('Colecciones','Collections')}</a>
      <a href="{prefix}#como-pedir">{tr('Cómo pedir','How to order')}</a>
      <a href="{prefix}#historia">{tr('Nuestra historia','Our story')}</a>
    </nav>
    <div class="header-actions">
      <button class="language-button" id="language-button" type="button" aria-label="Switch to English"><span class="chosen" lang="es">ES</span><span lang="en">EN</span></button>
      {contact('Hablemos','Let’s talk','button button-outline button-small')}
      <button class="menu-toggle" id="menu-toggle" type="button" aria-label="Abrir menú" data-aria-es="Abrir o cerrar menú" data-aria-en="Open or close menu" aria-expanded="false" aria-controls="main-nav">{icon('menu')}</button>
    </div>
  </div>
</header>'''

def footer(home=False):
    prefix = '' if home else 'index.html'
    return f'''
<footer class="site-footer">
  <div class="wrap footer-top">
    <div class="footer-brand">
      <a class="brand" href="index.html"><img src="images/web/logo-small.webp" alt="Hecho a Mano" width="54" height="54"><span class="brand-name">Hecho a Mano</span></a>
      {tr('Un emprendimiento pequeño con grandes ideas y mucho amor por el crochet.','A small business with big ideas and a love for crochet.','p')}
    </div>
    <nav class="footer-nav" aria-label="Enlaces del pie de página" data-aria-es="Enlaces del pie de página" data-aria-en="Footer links">
      <a href="{prefix}#colecciones">{tr('Colecciones','Collections')}</a>
      <a href="{prefix}#personaliza">{tr('Tu pedido especial','Your custom order')}</a>
      <a href="{prefix}#preguntas">{tr('Preguntas frecuentes','FAQs')}</a>
    </nav>
    <div class="footer-contact"><a href="{escape(wa(GENERAL_ES))}" target="_blank" rel="noopener noreferrer">{icon('whatsapp')}<span>+504 8923-5110</span></a>{tr('Tu próxima idea empieza con un hola.','Your next idea begins with a hello.','p')}</div>
  </div>
  <div class="wrap footer-bottom"><p>© <span data-year>2026</span> Hecho a Mano. {tr('Todos los derechos reservados.','All rights reserved.')}</p><p>{tr('Hecho a mano… es hecho con amor.','Made by hand… made with love.')} ♡</p></div>
</footer>
{contact('¿Te ayudamos?','Can we help?','floating-contact',aria_label='Escribir a Hecho a Mano por WhatsApp',data_aria_es='Escribir a Hecho a Mano por WhatsApp',data_aria_en='Message Hecho a Mano on WhatsApp')}
'''

def shell(title, description, body, filename, home=False, products=None):
    dialog = ''
    if products:
        dialog = f'''
<dialog class="product-dialog" id="product-dialog" aria-labelledby="dialog-title">
  <button class="dialog-close" id="dialog-close" type="button" aria-label="Cerrar" data-aria-es="Cerrar" data-aria-en="Close">{icon('close')}</button>
  <div class="dialog-inner">
    <div class="dialog-media"><img id="dialog-image" alt="" width="500" height="400"><div class="dialog-controls" id="dialog-controls"><button type="button" id="dialog-prev" aria-label="Foto anterior" data-aria-es="Foto anterior" data-aria-en="Previous photo">{icon('arrow')}</button><span id="dialog-count" aria-live="polite"></span><button type="button" id="dialog-next" aria-label="Foto siguiente" data-aria-es="Foto siguiente" data-aria-en="Next photo">{icon('arrow')}</button></div></div>
    <div class="dialog-copy"><p class="eyebrow">{tr('Una pieza con historia','A piece with a story')}</p><h2 id="dialog-title"></h2><p class="dialog-price" id="dialog-price"></p><p id="dialog-description"></p><a id="dialog-order" class="button button-primary" target="_blank" rel="noopener noreferrer">{icon('whatsapp')}{tr('Pedir por WhatsApp','Order on WhatsApp')}</a>{tr('Conversemos sobre colores, detalles y disponibilidad.','Let’s talk about colors, details, and availability.','p')}</div>
  </div>
</dialog>
<script type="application/json" id="catalog-data">{json.dumps(products, ensure_ascii=False).replace('<', r'\u003c')}</script>'''
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#fcf9f5">
  <title>{escape(title)} · Hecho a Mano</title>
  <meta name="description" content="{escape(description,quote=True)}">
  <link rel="canonical" href="{SITE}/{'' if home else filename}">
  <meta property="og:title" content="{escape(title,quote=True)} · Hecho a Mano">
  <meta property="og:description" content="{escape(description,quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_HN">
  <meta property="og:url" content="{SITE}/{'' if home else filename}">
  <meta property="og:image" content="{SITE}/images/web/tulipan-modelo.webp">
  <link rel="icon" href="images/web/logo-small.webp" type="image/webp">
  <link rel="preload" href="fonts/dm-sans-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/dm-serif-display-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="styles.css">
  <script src="app.js" defer></script>
</head>
<body data-page="{'home' if home else filename.split('.')[0]}">
{header(home)}
{body}
{footer(home)}
{dialog}
</body>
</html>
'''
    (ROOT / filename).write_text(html)

COLLECTIONS = [
    {'slug':'tulipanes','es':'Tulipanes','en':'Tulips','image':'tulip1.jpg','tag_es':'Flores que se quedan contigo.','tag_en':'Flowers to keep forever.','price':120,'photo':True},
    {'slug':'llaveros','es':'Llaveros','en':'Keychains','image':'llavero1.png','tag_es':'Pequeños detalles, mucha ternura.','tag_en':'Little details, lots of charm.','price':150},
    {'slug':'munecas','es':'Muñecas','en':'Dolls','image':'rapunzel1.png','tag_es':'Personajes llenos de magia.','tag_en':'Characters with a little magic.','price':350},
    {'slug':'cupcakes','es':'Cupcakes','en':'Cupcakes','image':'cupcake1.png','tag_es':'Un antojo de lo más especial.','tag_en':'A little treat, a lot of joy.','price':150},
]

collection_cards = ''
for c in COLLECTIONS:
    collection_cards += f'''<a class="collection-card reveal" href="{c['slug']}.html"><div class="collection-image {'photo' if c.get('photo') else ''}">{image(c['image'],c['es']+' tejidos a mano',c['en']+' crocheted by hand',sizes='(max-width: 640px) 45vw, (max-width: 900px) 45vw, 24vw')}<span class="collection-arrow">{icon('arrow')}</span></div><div class="collection-info">{tr(c['es'],c['en'],'h3')}{tr(c['tag_es'],c['tag_en'],'p')}{tr(f"Desde L. {c['price']}",f"From L. {c['price']}",class_='from-price').replace('class-=', 'class=')}</div></a>'''

custom_es = '¡Hola, Hecho a Mano! Me gustaría cotizar una pieza personalizada.'
custom_en = "Hello, Hecho a Mano! I'd like a quote for a custom crochet piece."
home_body = f'''
<main id="main">
  <section class="hero wrap" aria-labelledby="hero-title">
    <div class="hero-copy">
      <p class="eyebrow"><span class="little-flower" aria-hidden="true">✳</span>{tr('Crochet con corazón · Honduras','Crochet with heart · Honduras')}</p>
      <h1 id="hero-title">{tr('Un poquito de hilo.','A little yarn.')}{tr('Mucho amor.','A lot of love.','em')}</h1>
      {tr('Tejemos detalles que abrazan: flores que no se marchitan, personajes que enamoran y regalos tan únicos como tú.','We crochet little things that feel like a hug: flowers that never fade, lovable characters, and gifts as unique as you.','p',class_='hero-description').replace('class-=', 'class=')}
      <div class="hero-buttons">{button_link('#colecciones','Explorar colecciones','Explore collections')}{contact('Tengo una idea','I have an idea','text-link',custom_es,custom_en)}</div>
      <p class="hero-note">{icon('heart')}{tr('Hecho con calma. Pensado para alguien especial.','Made with care. Meant for someone special.')}</p>
    </div>
    <div class="hero-art">
      <div class="hero-photo">{image('tulip1.jpg','Tres tulipanes tejidos en tonos rosa, rojo y crema','Three crocheted tulips in pink, red, and cream',eager=True,sizes='(max-width: 640px) 85vw, 42vw')}</div>
      <div class="hero-stamp"><b>100%</b>{tr('hecho a mano','handmade')}</div>
      <span class="hero-spark" aria-hidden="true">✳</span>
      <div class="hero-label">{icon('gift')}<div>{tr('Para regalar. O regalarte.','To give. Or to keep.','strong')}{tr('Un detalle que dura.','A little joy that lasts.','small')}</div></div>
    </div>
  </section>
  <div class="values-strip"><div class="wrap values-inner">
    <div class="value-item">{icon('heart')}{tr('Tejido a mano con amor','Crocheted by hand with love')}</div><span class="value-separator" aria-hidden="true"></span>
    <div class="value-item">{icon('spark')}{tr('Tan único como tú','As unique as you')}</div><span class="value-separator" aria-hidden="true"></span>
    <div class="value-item">{icon('gift')}{tr('Detalles para regalar','Thoughtful little gifts')}</div><span class="value-separator" aria-hidden="true"></span>
    <div class="value-item">{icon('whatsapp')}{tr('Pedidos por WhatsApp','Order on WhatsApp')}</div>
  </div></div>
  <section class="wrap section" id="colecciones" aria-labelledby="collections-title">
    <div class="section-heading reveal"><div><p class="eyebrow">{tr('Encuentra tu próximo favorito','Find your next favorite')}</p><h2 id="collections-title">{tr('Un mundo de','A world of')} <em>{tr('pequeños detalles.','little wonders.')}</em></h2></div>{tr('Cada pieza tiene su encanto. ¿Cuál cuenta tu historia?','Every piece has its own charm. Which one tells your story?','p')}</div>
    <div class="collection-grid">{collection_cards}</div>
  </section>
  <section class="custom-section wrap" id="personaliza" aria-labelledby="custom-title">
    <div class="custom-copy"><p class="eyebrow">{tr('Imagina. Nosotros lo tejemos.','Imagine it. We’ll crochet it.')}</p><h2 id="custom-title">{tr('Tu idea, nuestra','Your idea, our')} <em>{tr('próxima puntada.','next stitch.')}</em></h2>{tr('¿Un personaje favorito, tu mascota o un regalo con tus colores? Nos encanta convertir tus ideas en algo que puedas abrazar.','A favorite character, your pet, or a gift in your colors? We love turning your ideas into something you can hold.','p')}</div>
    <div class="custom-form">
      <label for="custom-type">{tr('¿Qué te gustaría crear?','What would you like to create?')}</label>
      <select id="custom-type"><option value="especial" data-es="Una idea especial" data-en="Something special">Una idea especial</option><option value="tulipanes" data-es="Tulipanes" data-en="Tulips">Tulipanes</option><option value="llaveros" data-es="Llaveros" data-en="Keychains">Llaveros</option><option value="munecas" data-es="Muñecas o personajes" data-en="Dolls or characters">Muñecas o personajes</option><option value="cupcakes" data-es="Cupcakes" data-en="Cupcakes">Cupcakes</option></select>
      <label for="custom-idea">{tr('Cuéntanos un poquito','Tell us a little more')}</label>
      <textarea id="custom-idea" maxlength="600" placeholder="Colores, ocasión o esa idea que tienes en mente…" data-placeholder-es="Colores, ocasión o esa idea que tienes en mente…" data-placeholder-en="Colors, the occasion, or that idea you have in mind…" rows="2"></textarea>
      {contact('Conversemos por WhatsApp','Let’s chat on WhatsApp','button button-primary',custom_es,custom_en,id='custom-order')}
      {tr('Se abrirá WhatsApp con tu idea lista para compartir.','WhatsApp will open with your idea ready to share.','p',class_='form-note').replace('class-=', 'class=')}
    </div>
  </section>
  <section class="wrap section" id="como-pedir" aria-labelledby="steps-title">
    <div class="section-heading reveal"><div><p class="eyebrow">{tr('De nuestra manos a las tuyas','From our hands to yours')}</p><h2 id="steps-title">{tr('Algo bonito empieza','Something lovely starts')} <em>{tr('con un hola.','with a hello.')}</em></h2></div>{tr('Pedir tu pieza es sencillo. Te acompañamos en cada detalle.','Ordering your piece is easy. We’ll help with every little detail.','p')}</div>
    <div class="steps-grid">
      <article class="step reveal"><span class="step-number">01</span>{tr('Elige lo que te enamora','Find something you love','h3')}{tr('Explora las colecciones o comparte una idea que quieras hacer realidad.','Browse our collections or share an idea you’d love to bring to life.','p')}{button_link('#colecciones','Ver colecciones','Browse collections','text-link')}</article>
      <article class="step reveal"><span class="step-number">02</span>{tr('Hablemos de los detalles','Let’s talk about the details','h3')}{tr('Escríbenos por WhatsApp para consultar colores, personalización y disponibilidad.','Message us on WhatsApp to discuss colors, personalization, and availability.','p')}{contact('Escríbenos','Send us a hello','text-link')}</article>
      <article class="step reveal"><span class="step-number">03</span>{tr('Lo hacemos especial para ti','We make it special for you','h3')}{tr('Confirmamos contigo el precio, el tiempo de elaboración y la forma de entrega antes de empezar.','We’ll confirm the price, creation time, and delivery arrangements with you before we begin.','p')}</article>
    </div>
  </section>
  <section class="story-section section" id="historia" aria-labelledby="story-title"><div class="wrap story-grid">
    <div class="story-art reveal"><img src="images/web/logo.webp" alt="Hecho a Mano — Hecho a mano es hecho con amor" width="300" height="300" loading="lazy">{tr('Con cariño, Hecho a Mano','With love, Hecho a Mano',class_='story-signature').replace('class-=', 'class=')}</div>
    <div class="story-copy reveal"><p class="eyebrow">{tr('Un poquito sobre nosotros','A little about us')}</p><h2 id="story-title">{tr('Un emprendimiento pequeño.','A small business.')} <em>{tr('Un corazón enorme.','A whole lot of heart.')}</em></h2>{tr('Damos vida a la creatividad con el arte de tejer. Cada puntada lleva tiempo, dedicación y la ilusión de crear algo que signifique mucho para alguien.','We bring creativity to life through crochet. Every stitch carries time, care, and the hope of creating something that means a lot to someone.','p')}{tr('Desde amigurumis hasta tus propias ideas o mascotas, nos encanta crear piezas únicas por encargo. También compartimos este arte en nuestras clases de crochet.','From amigurumi to your own ideas or pets, we love creating unique pieces to order. We also share this craft through our crochet classes.','p')}{contact('Quiero saber de las clases','Tell me about the classes','text-link','¡Hola, Hecho a Mano! Me gustaría recibir información sobre sus clases de crochet.','Hello, Hecho a Mano! I’d like more information about your crochet classes.')}</div>
  </div></section>
  <section class="wrap section faq-grid" id="preguntas" aria-labelledby="faq-title"><div class="reveal"><p class="eyebrow">{tr('Antes de decir hola','Before you say hello')}</p><h2 id="faq-title">{tr('Por si te lo','Just in case you’re')} <em>{tr('preguntabas.','wondering.')}</em></h2>{tr('Y si tienes otra duda, estamos a un mensaje de distancia.','And if you have another question, we’re just a message away.','p')}</div><div class="faq-list">
    <details><summary>{tr('¿Puedo personalizar mi pedido?','Can I personalize my order?')}</summary>{tr('¡Sí! Cuéntanos tu idea, colores favoritos o personaje por WhatsApp. Revisaremos los detalles contigo y te compartiremos una cotización.','Yes! Share your idea, favorite colors, or character on WhatsApp. We’ll go over the details with you and prepare a quote.','p')}</details>
    <details><summary>{tr('¿Cómo puedo hacer un pedido?','How do I place an order?')}</summary>{tr('Entra a una colección y elige “Pedir por WhatsApp” en la pieza que te guste. Se abrirá un chat con el producto en el mensaje. Tú lo revisas y lo envías.','Open a collection and choose “Order on WhatsApp” on the piece you like. A chat will open with the product in the message. You can review and send it.','p')}</details>
    <details><summary>{tr('¿Cuánto tarda y cómo recibo mi pieza?','How long does it take, and how will I receive it?')}</summary>{tr('El tiempo de elaboración depende de la pieza y de la personalización. Escríbenos para confirmar disponibilidad, tiempo y opciones de entrega antes de realizar tu pedido.','Creation time depends on the piece and personalization. Message us to confirm availability, timing, and delivery options before placing your order.','p')}</details>
    <details><summary>{tr('¿También dan clases de crochet?','Do you also offer crochet classes?')}</summary>{tr('Sí, ofrecemos clases para aprender y desarrollar tu creatividad. Consulta por WhatsApp los horarios, requisitos y disponibilidad.','Yes, we offer classes to help you learn and explore your creativity. Ask us on WhatsApp about schedules, requirements, and availability.','p')}</details>
  </div></section>
</main>
'''
home_body = home_body.replace('De nuestra manos', 'De nuestras manos')
shell('Crochet con corazón', 'Piezas únicas tejidas a mano en Honduras. Descubre tulipanes, llaveros, muñecas y cupcakes de crochet. Personaliza tu pedido por WhatsApp.', home_body, 'index.html', True)

def product(id, name_es, name_en, images, price=None, **extra):
    return dict(id=id,name={'es':name_es,'en':name_en},images=[f'images/web/{Path(x).stem}.webp' for x in images],price=price,**extra)

catalogs = {
 'llaveros':{
   'title':('Llaveros','Keychains'),'intro':('Un toque de ternura para llevar a todas partes. Detalles tejidos a mano que alegran tus llaves, tu mochila o el día de alguien especial.','A little charm to take everywhere. Handmade details to brighten your keys, your bag, or someone special’s day.'),
   'products':[
    product('gatito-corazon','Gatito y corazón','Kitten & heart',['llavero1.png'],220),
    product('conejito','Conejito con flor','Bunny with a flower',['llavero2.png'],150),
    product('sombreritos-pastel','Sombreritos pastel','Pastel little hats',['llavero3.png'],150),
    product('sombreritos-flor','Sombreritos con flor','Flower little hats',['llavero4.png'],150),
    product('bolsitos','Bolsitos de flores','Little flower bags',['llavero5.png'],150),
    product('sombreritos-color','Sombreritos de colores','Colorful little hats',['llavero6.png'],150),
    product('sombreritos-sol','Sombreritos de sol','Sunny little hats',['llavero7.png'],150),
   ]},
 'cupcakes':{
   'title':('Cupcakes','Cupcakes'),'intro':('Un poquito de dulzura que dura para siempre. Cupcakes tejidos para regalar, decorar o llevar contigo una sonrisa.','A little sweetness that lasts forever. Crocheted cupcakes to give, decorate with, or carry a smile along.'),
   'products':[
    product('cupcake-flor','Cupcake con flor','Flower cupcake',['cupcake1.png'],150),
    product('cupcake-azul','Cupcake azul','Blue cupcake',['cupcake4.png'],150),
    product('set-cuatro','Set de 4 cupcakes','Set of 4 cupcakes',['cupcake3.png'],500,set_size=4),
    product('set-dos','Set de 2 cupcakes','Set of 2 cupcakes',['cupcake5.png'],250,set_size=2),
    product('cupcakes-inspiracion','Un mundo de cupcakes','A world of cupcakes',['cupcake2.png'],reference=True),
   ]},
 'munecas':{
   'title':('Muñecas','Dolls'),'intro':('Personajes que cobran vida, puntada a puntada. Pequeñas compañeras llenas de imaginación, detalles y un toque de magia.','Characters brought to life, stitch by stitch. Little companions full of imagination, detail, and a touch of magic.'),
   'products':[
    product('rapunzel','Rapunzel','Rapunzel',['rapunzel1.png','rapunzel2.png','rapunzel3.png'],1300),
    product('jasmine','Princesa Jasmine','Princess Jasmine',['jasmine1.png','jasmine2.png'],1300),
    product('bella-bestia','Bella y Bestia','Beauty and the Beast',['bella1.png','bella2.png','bella3.png','bella4.png'],2400),
    product('gatita','Gatita','Kitten',['gatita1.png'],1300),
    product('closet','Muñequita con clóset','Doll with a closet',['closet1.png','closet2.png'],1500),
    product('campanita','Campanita','Tinker Bell',['tinkerbell1.png'],1300),
    product('bailarina','Bailarina','Ballerina',['bailarina1.png'],350),
    product('tomato','Mr. Tomato','Mr. Tomato',['tomato1.png'],350),
   ]},
 'tulipanes':{
   'title':('Tulipanes','Tulips'),'intro':('Flores que nunca se marchitan y siempre dicen algo bonito. Regala un ramo tejido con amor, o llena tu espacio de pequeños colores felices.','Flowers that never fade and always say something lovely. Give a bouquet crocheted with love, or fill your space with little happy colors.'),
   'products':[
    product('pack-tres','Pack de 3 tulipanes','Pack of 3 tulips',['tulip1.jpg'],375,photo=True,tag={'es':'Popular','en':'Popular'},set_size=3),
    product('ramo-cuatro','Ramo de 4 tulipanes','Bouquet of 4 tulips',['ramo-4-tulipanes.jpg'],500,photo=True,set_size=4),
    product('tulipan-individual','Tulipán individual','Individual tulip',['tulip2.jpg'],140,photo=True,unit=True),
    product('hello-kitty','Tulipán Hello Kitty','Hello Kitty tulip',['tulipan-hello-kitty.jpg'],150,photo=True,tag={'es':'Especial','en':'Special'}),
    product('llavero-tulipan','Llavero de tulipán','Tulip keychain',['llavero-tulipan-1.jpg','llavero-tulipan-2.jpg'],120,unit=True),
    product('tulipanes-inspiracion','Un jardín de posibilidades','A garden of possibilities',['tulipan-modelo.jpg'],reference=True,photo=True),
   ]},
}

for slug, catalog in catalogs.items():
    es,en = catalog['title'];desc_es,desc_en=catalog['intro'];cards='';products=catalog['products']
    for position,p in enumerate(products):
        name_es,name_en=p['name']['es'],p['name']['en'];price=p['price'];price_text=f'L. {price:,}' if price is not None else ''
        p['url']=f'{SITE}/{slug}.html#{p["id"]}'
        if price is not None:
            message_es=f'¡Hola, Hecho a Mano! Me interesa: {name_es} ({price_text}{" c/u" if p.get("unit") else ""}). ¿Podrían confirmarme disponibilidad y detalles? {p["url"]}'
            message_en=f'Hello, Hecho a Mano! I’m interested in: {name_en} ({price_text}{" each" if p.get("unit") else ""}). Could you confirm availability and details? {p["url"]}'
        else:
            message_es=f'¡Hola, Hecho a Mano! Me gustaría cotizar una pieza inspirada en: {name_es}. {p["url"]}'
            message_en=f'Hello, Hecho a Mano! I’d like a quote for a piece inspired by: {name_en}. {p["url"]}'
        p['message']={'es':message_es,'en':message_en}
        if p.get('reference'):
            meta_es,meta_en='Modelo de referencia · Consulta tu idea','Reference model · Ask us about your idea'
        elif p.get('set_size'):
            meta_es,meta_en=f'Set de {p["set_size"]} piezas · Tejido a mano',f'Set of {p["set_size"]} · Handmade'
        else:
            meta_es,meta_en='Hecho a mano · Consulta colores','Handmade · Ask about colors'
        p['description']={'es':meta_es,'en':meta_en}
        tag = p.get('tag') or ({'es':'Inspiración','en':'Inspiration'} if p.get('reference') else None)
        tag_html = tr(tag['es'],tag['en'],class_='product-tag').replace('class-=', 'class=') if tag else ''
        img_name=Path(p['images'][0]).name.replace('.webp','.png')
        picture = image(img_name,name_es+' tejido a mano',name_en+' crocheted by hand',eager=position<3,sizes='(max-width: 640px) 44vw, 30vw')
        unit=tr(' c/u',' each',class_='product-unit').replace('class-=', 'class=') if p.get('unit') else ''
        price_html=f'<p class="product-price">{price_text}{unit}</p>' if price is not None else ''
        cards+=f'''
      <article class="product-card" id="{p['id']}" data-price="{price if price is not None else 'Infinity'}" data-original-order="{position}">
        <button class="product-image-button {'photo' if p.get('photo') else ''}" type="button" data-product="{p['id']}" aria-label="Ver detalles de {escape(name_es,quote=True)}" data-aria-es="Ver detalles de {escape(name_es,quote=True)}" data-aria-en="View details of {escape(name_en,quote=True)}">{picture}{tag_html}<span class="view-pill">{icon('zoom')}{tr('Ver detalles','View details')}</span></button>
        <div class="product-info"><div class="product-title-row">{tr(name_es,name_en,'h2')}{price_html}</div>{tr(meta_es,meta_en,'p',class_='product-meta').replace('class-=', 'class=')}{contact('Consultar por WhatsApp' if p.get('reference') else 'Pedir por WhatsApp','Ask on WhatsApp' if p.get('reference') else 'Order on WhatsApp','text-link',message_es,message_en)}</div>
      </article>'''
    tabs = ''.join(f'<a href="{c["slug"]}.html" {"aria-current=page" if c["slug"]==slug else ""}>{tr(c["es"],c["en"])}</a>' for c in COLLECTIONS)
    count=len([p for p in products if not p.get('reference')]);ref=len(products)-count
    count_es=f'{count} diseños'+(' + inspiración' if ref else '')+' · Precios en lempiras'
    count_en=f'{count} designs'+(' + inspiration' if ref else '')+' · Prices in HNL'
    body=f'''
<main id="main" class="wrap">
  <nav class="breadcrumb" aria-label="Ubicación" data-aria-es="Ubicación" data-aria-en="Breadcrumb"><a href="index.html">{tr('Inicio','Home')}</a>{icon('chevron')}<a href="index.html#colecciones">{tr('Colecciones','Collections')}</a>{icon('chevron')}{tr(es,en)}</nav>
  <header class="catalog-heading"><p class="eyebrow">{tr('Pequeños detalles, grandes sonrisas','Little details, big smiles')}</p><h1>{tr(es,en)}</h1>{tr(desc_es,desc_en,'p')}</header>
  <nav class="collection-tabs" aria-label="Colecciones" data-aria-es="Colecciones" data-aria-en="Collections">{tabs}</nav>
  <div class="catalog-toolbar">{tr(count_es,count_en,'p')}<label class="sort-label" for="catalog-sort">{tr('Ordenar:','Sort:')}<select id="catalog-sort"><option value="featured" data-es="Selección del taller" data-en="Workshop selection">Selección del taller</option><option value="price-asc" data-es="Precio: menor a mayor" data-en="Price: low to high">Precio: menor a mayor</option><option value="price-desc" data-es="Precio: mayor a menor" data-en="Price: high to low">Precio: mayor a menor</option></select></label></div>
  <div class="product-grid" id="product-grid">{cards}</div>
  <section class="catalog-note"><div><h2>{tr('¿Lo imaginas diferente?','Imagining something different?')}</h2>{tr('Tus colores, tu idea, tu detalle especial. Conversemos y lo hacemos tuyo.','Your colors, your idea, your special little detail. Let’s make it yours.','p')}</div>{contact('Personalizar mi pedido','Personalize my order','button button-green',custom_es,custom_en)}</section>
</main>'''
    shell(es,desc_es,body,slug+'.html',products=products)

print('Generated home and all four collections with',sum(len(c['products']) for c in catalogs.values()),'product cards.')
