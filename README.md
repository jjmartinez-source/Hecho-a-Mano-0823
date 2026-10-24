# Hecho a Mano

A responsive, bilingual crochet storefront with a home page and four collections.
It is a static site: Vercel serves the HTML, CSS, JavaScript, images, and fonts
directly, without an install or build step.

## Preview locally

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000`.

## Edit the content

- `tools/build_site.py` contains the Spanish/English copy, product names, original
  lempira prices, gallery photos, and WhatsApp message templates.
- `styles.css` contains the palette, responsive layouts, and motion preferences.
- `app.js` handles the language preference, mobile menu, photo dialog, sorting,
  and custom-order message.

After editing the Python content source, regenerate the five HTML pages:

```sh
python3 tools/build_site.py
```

This generator only requires Python's standard library. Commit both the source
and the generated HTML. Prices remain in Honduran lempiras in both languages.
Reference photos do not have an invented price.

## WhatsApp

The contact number is `50489235110` (Honduras, +504 8923-5110). Order buttons use
`https://wa.me/50489235110?text=...` with an encoded, prefilled message. Visitors
review and send their own messages in WhatsApp.

To change the number, update `PHONE` in `tools/build_site.py` and
`WHATSAPP_NUMBER` in `app.js`, then regenerate the HTML.

## Images and fonts

The original product photos and logo are preserved in `images/`. The site serves
browser-compatible, resized WebP copies from `images/web/`, including 480px
responsive versions. This also fixes original photos containing HEIC data under
PNG filenames. The doll gallery uses the existing `bella2.png` photo instead of
the missing `bella2new.png` path.

To rebuild the responsive copies after replacing a source photo:

```sh
python3 -m pip install Pillow pillow-heif
python3 tools/optimize_images.py
```

DM Sans and DM Serif Display are served locally. Their SIL Open Font License
files are included in `fonts/`.
