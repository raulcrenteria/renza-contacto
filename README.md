# Renza — sitio de contacto

Sitio estático de 3 páginas para `renzaservices.com`. Cada `.html` es
autocontenido (CSS y JS inline) a propósito — así se ve bien en cualquier
vista previa o al abrirlo directo desde el disco, sin depender de que
carguen archivos externos.

- `index.html` — portada con los dos accesos (Distribución / Servicios)
- `servicios.html` — asesoría fiscal y contable
- `distribucion.html` — compra/venta al mayoreo

## Antes de publicar

Busca `CONFIG` dentro de `servicios.html` y `distribucion.html` (cada uno
tiene su propio bloque `CONFIG` al final del archivo, dentro de `<script>`)
y reemplaza en ambos:

- `whatsapp`: tu número en formato `52XXXXXXXXXX` (sin espacios ni "+").
- `email`: el correo real que quieras publicar.

`index.html` no necesita CONFIG — solo tiene los dos botones de entrada.

## Formulario de contacto

El formulario de `servicios.html` y `distribucion.html` usa un proveedor
externo mediante fetch/AJAX — no recarga la página y muestra un mensaje de
éxito o error inline.

Cada página manda un campo oculto `_subject` distinto ("— Servicios" /
"— Distribución") para que puedas distinguir de dónde vino cada lead sin
entrar al dashboard.

## Sobre los íconos

Los dos símbolos (balanza en Distribución, documento sellado en Servicios)
son SVG dibujados a mano dentro del propio HTML — no son imágenes externas,
así que no dependen de ningún archivo ni conexión, y no hay tema de
derechos de autor. Comparten el mismo marco circular, grosor de línea y
paleta para leerse como un mismo set.

## Publicar con GitHub Pages

1. El repo debe ser **público** — GitHub Pages en cuentas Free no publica
   desde repos privados; para privado se necesita GitHub Pro.
2. Settings → Pages → Source: rama `main`, carpeta `/ (root)`.
3. El archivo `CNAME` ya deja configurado `renzaservices.com`; no lo borres.
4. En el DNS de GoDaddy para `renzaservices.com`, agrega:
   - 4 registros `A` en `@` apuntando a:
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Un registro `CNAME` en `www` apuntando a `raulcrenteria.github.io`
5. Espera la propagación DNS y activa "Enforce HTTPS" en Settings → Pages.
