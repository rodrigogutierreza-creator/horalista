# HoraLista

Landing de HoraLista: agendamiento automático de citas por WhatsApp y link de
reservas para PyMEs chilenas (automotoras, pastelerías, barberías, veterinarias).

La página incluye un **agendador funcional** que corre entero en el navegador:
elige rubro, servicio, día y hora, valida los datos y arma el mensaje de
WhatsApp con la cita prellenada. No hay backend todavía.

## Estructura

| Archivo | Qué es |
|---|---|
| `landing.src.html` | **La fuente. El único archivo que se edita a mano.** |
| `build.py` | Compila la fuente y genera las dos salidas. |
| `fonts/` | Archivo y Newsreader (`.woff2`), se incrustan en base64 al compilar. |
| `dist/index.html` | Generado. Es lo que Vercel publica. |
| `horalista-artifact.html` | Generado. Versión sin `<html>/<head>/<body>` para publicar como artifact. |
| `vercel.json` | Configuración de Vercel: publica `dist/`, más cabeceras de seguridad. |

`dist/` se versiona a propósito: la página se compila en este equipo con Python
y el contenedor de Vercel no corre ese paso, así que sube ya compilada.

## Ciclo de trabajo

```bash
# 1. editar landing.src.html
# 2. compilar
python3 build.py
# 3. revisar abriendo dist/index.html en el navegador
# 4. publicar
git add -A && git commit -m "describe el cambio" && git push
```

Vercel publica solo al recibir el push. No hay que hacer nada más.

## Por qué las tipografías van incrustadas

Van en base64 dentro del HTML en vez de enlazadas a Google Fonts. Dos razones:
el CSP de los artifacts bloquea los CDN de fuentes (la página caería a Arial sin
avisar), y así `dist/index.html` es un archivo único sin dependencias externas.
El costo es que pesa ~240 KB, casi todo tipografía.

## Pendientes antes de salir a producción

- [ ] **Número de WhatsApp.** Está el de ejemplo `56912345678` en la constante
      `CONFIG` de `landing.src.html`. Mientras no se cambie, ningún botón de
      WhatsApp llega a nadie.
- [ ] **Precios.** Los montos de la sección Precios son una estructura de
      ejemplo, no un cálculo de costos reales.
- [ ] **Decidir el backend del bot.** Hoy la página arma un link `wa.me`. Para
      que el bot responda solo hace falta la API de WhatsApp Business (Meta
      cobra por conversación y exige verificar el negocio). Esa decisión define
      el costo por cliente y si los precios de arriba se sostienen.

## Diseño

El sistema visual sigue las reglas de [Hallmark](https://github.com/Nutlope/hallmark).
Antes de agregar secciones conviene leer el comentario que encabeza el `<style>`
de `landing.src.html`: ahí está la macroestructura, la paleta en OKLCH y el
emparejamiento tipográfico. En resumen: estructura de hoja de agenda rayada,
papel frío, un solo acento bermellón, cifras tabulares condensadas como
protagonista. Nada de emoji como iconografía, chrome de otras apps redibujado,
ni métricas inventadas.
