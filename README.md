# El Balconcito

Landing estática. Editar `index.html`, que contiene HTML, CSS y JavaScript.
El archivo HTML con el nombre original se conserva como referencia.

## Desarrollo local

Desde esta carpeta:

```powershell
python -m http.server 3000 --bind 127.0.0.1
```

Abrir http://localhost:3000 y recargar el navegador después de guardar cambios.
Las tipografías de Google requieren conexión a Internet.

## Fondo del hero

`assets/oven-embers.gif`: animación de brasas de 48 cuadros, bucle infinito de 3,84 s.
`assets/oven-embers.png`: imagen original de alta resolución y alternativa sin movimiento.
Generación de imagen: herramienta integrada Imagegen, modo predeterminado.
Prompt: primer plano fotográfico dentro de un horno a leña, troncos carbonizados con grietas incandescentes naranjas y rojas, brasas debajo, pequeñas llamas doradas al fondo, luz cálida, sin textos ni logos.
La animación se crea a partir de la imagen: brillo periódico y distorsión por calor; no es una filmación del sitio de referencia.
`tools/build-embers.py` genera el GIF desde el BMP con Python estándar.
