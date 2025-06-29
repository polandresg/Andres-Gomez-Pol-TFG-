TFG – Sistema de Monitorización Submarina

Este proyecto tiene como objetivo desarrollar un sistema no invasivo para monitorizar la biodiversidad marina. Captura vídeo en tiempo real desde dos cámaras ojo de pez de 180º (formando una vista de 360º) a través de RTSP y después transforma las imágenes a formato equirectangular, aplica un modelo YOLOv8 para detectar especies marinas, y finalmente envía el vídeo procesado a YouTube Live mediante RTMP.

--Componentes Principales--

 Hardware:
 
  - OTAQ Eagle IP 360/180 cameras (dual 180º lenses)
  - Local server (Ubuntu)
     
 Software:

  - Python 3.10

  - OpenCV + NumPy (image capture, remapping)

  - YOLOv8 (marine species detection)

  - FFmpeg (live RTMP streaming)

 Protocols:

  - RTSP (input de las cameras)
    
  - RTMP (output hacia YouTube Live)
