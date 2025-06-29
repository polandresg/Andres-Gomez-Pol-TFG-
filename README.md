TFG – Sistema de Monitorización Submarina

Este proyecto tiene como objetivo desarrollar un sistema no invasivo para monitorizar la biodiversidad marina. Captura vídeo en tiempo real desde dos cámaras ojo de pez de 180º (formando una vista de 360º) a través de RTSP y después transforma las imágenes a formato equirectangular, aplica un modelo YOLOv8 para detectar especies marinas, y finalmente envía el vídeo procesado a YouTube Live mediante RTMP.

--Componentes Principales--

 Hardware:
 
  - Cámara OTAQ Eagle IP 360/180 (Lentes duales de 180º)
    
  - Servidor Local (Ubuntu)
     
 Software:

  - Python 3.10

  - OpenCV + NumPy (captura de imagen, remapeo)

  - YOLOv8 (detección de especies marinas)

  - FFmpeg (directo en vivo RTMP)

 Protocolos:

  - RTSP (input de las cameras)
    
  - RTMP (output hacia YouTube Live)

--Vídeo de Validación del Sistema--

  - https://www.youtube.com/watch?v=xVEqxOUHr8E (detectando desde un contexto estático)
  
  - https://www.youtube.com/watch?v=fI0Ck-72kJY (detectando desde un contexto dinámico)
    
  - https://www.youtube.com/watch?v=gWzluXTR3KM (Vídeo externo que no es de mi propiedad utilizado como material de pruebas)
