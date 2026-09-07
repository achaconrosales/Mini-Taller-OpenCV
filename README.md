# Guía Práctica de Visión Artificial con OpenCV

**Diseñado por:** Alvaro Chacon Rosales
**Duración estimada:** 30 minutos

## 1. Introducción y Objetivos del Tutorial

OpenCV (Open Source Computer Vision Library) es la biblioteca de visión por computadora y procesamiento de imágenes de código abierto más utilizada en el mundo académico e industrial. Originalmente diseñada en C++ para maximizar la eficiencia computacional en tiempo real, hoy cuenta con excelentes interfaces para Python que permiten un rápido desarrollo y experimentación en computadoras personales. En este laboratorio, aprenderás cómo las imágenes no son representadas como 'fotografías' por la computadora, sino como matrices numéricas multidimensionales (NumPy Arrays), donde cada celda representa un píxel con información de brillo y color en formato BGR (Azul, Verde, Rojo) por defecto.

### Objetivos de Aprendizaje

1. Configurar un entorno virtual aislado en Python 3 para desarrollo científico.
2. Adquirir transmisiones de video en vivo utilizando la cámara web integrada de la laptop.
3. Aplicar un pipeline de preprocesamiento espacial: Conversión de color, Suavizado Gaussiano y Detección de Bordes con el Operador Canny.
4. Manipular y alterar matrices de píxeles en memoria de manera directa y eficiente (in-place processing) para emular efectos visuales (Filtro Neón y Cámara Térmica).

## 2. Requerimientos de Software y Hardware

| Componente / Recurso | Especificación Requerida | Tipo |
|---|---|---|
| Laptop para Estudiante | Cualquier laptop convencional equipada con cámara web integrada o USB externa | Hardware |
| Python | Versión 3.8 o superior, instalada de manera nativa en el sistema | Software |
| Gestor de paquetes | pip actualizado a la versión más reciente | Software |
| Librería OpenCV | opencv-python versión 4.x (específicamente menor a 5.0) | Software |
| Librería NumPy | numpy instalada automáticamente con OpenCV para operaciones de matrices | Software |

## 3. Instrucciones Paso a Paso

Sigue detenidamente los comandos e instrucciones en la terminal de tu sistema operativo para configurar el entorno e implementar los algoritmos:

### Paso 0: Verificar la cámara del dispositivo

Abre la terminal y ejecuta:

```bash
v4l2-ctl --list-devices
```

Salida esperada:

```
Integrated_Webcam_HD: Integrate (usb-0000:04:00.3-4):
    /dev/video0
    /dev/video1
    /dev/media0
```

### Paso 1: Creación del directorio de trabajo

Abre la terminal (en macOS/Linux) y crea una carpeta dedicada para el proyecto:

```bash
mkdir Opencv
cd Opencv
```

### Paso 2: Creación del entorno virtual aislado

Para garantizar que las dependencias de OpenCV no entren en conflicto con otras librerías globales del sistema, crearemos un entorno virtual (venv):

```bash
python3 -m venv .venv
```

### Paso 3: Activación del entorno virtual

Activa el entorno virtual:

- En Linux / macOS:

```bash
source .venv/bin/activate
```

### Paso 4: Actualización de pip e instalación de OpenCV 4

Actualizaremos el gestor de paquetes de Python e instalaremos OpenCV versión 4 y NumPy (la librería para el cómputo de matrices numéricas):

```bash
pip install --upgrade pip
pip install "opencv-python<5" numpy
```

### Paso 5: Creación del Filtro "Neón" en Tiempo Real (`neon_filter.py`)

Este primer script implementa el pipeline básico de visión artificial. Convierte el video a escala de grises, aplica un desenfoque para eliminar ruido Gaussiano y extrae los bordes estructurales de la escena usando el operador Canny:

Crea un archivo llamado `neon_filter.py` y escribe el siguiente código:

```python

import cv2
import numpy as np


def main():
    # 1. Inicializar la cámara web de la laptop.
    cap = cv2.VideoCapture('/dev/video0')

    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara web.")
        return

    print("--- Filtro de Neón Iniciado ---")
    print("Presiona 'q' o ESC para cerrar la aplicación.")

    try:
        while True:
            # 2. Adquisición: capturar el fotograma actual
            ret, frame = cap.read()

            if not ret:
                print("Error al recibir el stream de video.")
                break

            # 3. Preprocesamiento: Convertir el fotograma de color (BGR) a escala de grises
            # Esto reduce el canal de color 3D a una matriz plana de 2D, acelerando el proceso
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 4. Suavizado: Aplicar Gaussian Blur para eliminar el "ruido visual"
            # Usamos un kernel de 5x5. Esto hace que los bordes finales se vean más limpios
            blurred = cv2.GaussianBlur(
                gray,
                (5, 5),
                1.5
            )

            # 5. Extracción de Características: Detectar contornos usando el Operador Canny
            # Analiza los gradientes de intensidad y detecta dónde cambian bruscamente los píxeles
            # Parámetros: imagen suavizada, umbral mínimo (30) y umbral máximo (90)
            edges = cv2.Canny(
                blurred,
                30,
                90
            )

            # 6. Efecto estético "Neón" (Opcional):
            # El resultado de Canny es blanco y negro. Podemos darle color de neón (ej. verde)
            # Creamos una matriz vacía del mismo tamaño que la original en color
            neon_frame = np.zeros_like(frame)

            # Asignamos el canal verde (índice 1 en BGR) donde se detectaron bordes
            neon_frame[edges > 0] = [0, 255, 0]

            # 7. Visualización: Mostrar las ventanas con los resultados en tiempo real   
            cv2.imshow('Filtro Neon en Tiempo Real (Canny)', neon_frame)

            # 8. Control del teclado
            # q = salir
            # ESC = salir
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q') or key == 27:
                break

    except KeyboardInterrupt:
        # Permite cerrar el programa con Ctrl+C desde la terminal
        print("\nPrograma detenido con Ctrl+C.")

    finally:
        # 9. Liberar recursos siempre, incluso si ocurre un error
        cap.release()
        cv2.destroyAllWindows()

        # Dar tiempo a OpenCV para cerrar las ventanas
        cv2.waitKey(1)

        print("Cámara liberada. Programa terminado.")


if __name__ == '__main__':
    main()
```

Tome en cuenta que la cámara en `cap = cv2.VideoCapture('/dev/video0')` debe de ser la misma que obtuvo en el paso 0.

Ejecuta el script desde la terminal activa de tu entorno virtual:

```bash
python neon_filter.py
```

### Paso 6: Creación de la Simulación Térmica (`vision_termica.py`)

Para este segundo experimento, utilizaremos conversiones de mapas de color para simular una visualización infrarroja/térmica basada en los gradientes de luminosidad de la escena en tiempo real.

Crea un archivo llamado `vision_termica.py` e introduce el siguiente código:

```python

import cv2
import numpy as np


def main():
    # 1. Inicializar la cámara web de la laptop.
    # El índice '/dev/video0' indica el dispositivo de cámara
    # que verificamos previamente que funciona correctamente.
    cap = cv2.VideoCapture('/dev/video0')

    # Verificar si la cámara se abrió correctamente.
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara web.")
        return

    print("--- Visión Térmica Iniciada ---")
    print("Presiona 'q' o ESC para cerrar la aplicación.")
    print("Presiona '1' para usar el mapa JET.")
    print("Presiona '2' para usar el mapa INFERNO.")
    print("Presiona '3' para usar el mapa TURBO.")

    # Variable que almacena el mapa de colores que utilizaremos.
    # Inicialmente utilizamos JET.
    current_colormap = cv2.COLORMAP_JET

    try:
        while True:
            # 2. Adquisición: Capturar el fotograma (frame) actual de la cámara.
            # 'ret' indica si la captura fue exitosa y 'frame' contiene
            # la imagen obtenida de la cámara.
            ret, frame = cap.read()

            if not ret:
                print("Error al recibir el stream de video.")
                break

            # 3. Preprocesamiento: Convertir el fotograma de color
            # (BGR) a escala de grises.
            # En lugar de trabajar con tres canales de color (B, G y R),
            # ahora trabajamos con una matriz 2D de intensidades.
            # Esto simplifica las operaciones posteriores.
            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            # 4. Suavizado: Aplicar un filtro Gaussiano.
            # El desenfoque reduce pequeñas variaciones y ruido en la imagen.
            # Esto ayuda a obtener una imagen más estable para los siguientes
            # pasos de procesamiento.
            blurred = cv2.GaussianBlur(
                gray,
                (7, 7),
                0
            )

            # 5. Visualización mediante un mapa de colores.
            # La imagen en escala de grises contiene diferentes niveles
            # de intensidad. applyColorMap transforma esos niveles
            # de intensidad en colores.
            #
            # Importante: esto NO convierte la cámara en una cámara térmica.
            # Es solamente una representación visual de las intensidades
            # de la imagen utilizando colores.
            thermal = cv2.applyColorMap(
                blurred,
                current_colormap
            )

            # 6. Extracción de características: Detectar bordes
            # utilizando el Operador Canny.
            #
            # Canny busca cambios bruscos de intensidad entre píxeles.
            # Estos cambios suelen corresponder a los límites de objetos
            # presentes en la imagen.
            edges = cv2.Canny(
                blurred,
                50,
                150
            )

            # La salida de Canny es una imagen en escala de grises.
            # Convertimos esa imagen nuevamente a BGR para poder
            # combinarla posteriormente con la imagen coloreada.
            edges_color = cv2.cvtColor(
                edges,
                cv2.COLOR_GRAY2BGR
            )

            # 7. Composición: Combinar la imagen coloreada con los bordes.
            #
            # addWeighted permite mezclar dos imágenes.
            # La primera imagen aporta principalmente los colores,
            # mientras que la segunda aporta los bordes detectados.
            #
            # El resultado es un efecto visual parecido a una
            # "visión de energía".
            result = cv2.addWeighted(
                thermal,
                0.85,
                edges_color,
                0.5,
                0
            )

            # 8. Anotación: Agregar información sobre la imagen.
            # putText permite dibujar texto directamente sobre el frame.
            # Esto es útil para mostrar información al usuario
            # sin necesidad de crear otra interfaz.
            cv2.putText(
                result,
                "VISION TERMICA",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            # Mostrar las teclas disponibles directamente en la ventana.
            cv2.putText(
                result,
                "1:JET  2:INFERNO  3:TURBO",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            # 9. Visualización: Mostrar el resultado final.
            # imshow crea una ventana y muestra el frame procesado.
            # Como estamos dentro de un bucle, la imagen se actualiza
            # continuamente y obtenemos video en tiempo real.
            cv2.imshow(
                'Vision Termica - OpenCV',
                result
            )

            # 10. Control del teclado.
            # waitKey permite que OpenCV procese eventos de la ventana
            # y nos permite detectar teclas presionadas.
            #
            # 'q' o ESC → salir del programa.
            # '1' → seleccionar el mapa JET.
            # '2' → seleccionar el mapa INFERNO.
            # '3' → seleccionar el mapa TURBO.
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q') or key == 27:
                break

            elif key == ord('1'):
                current_colormap = cv2.COLORMAP_JET

            elif key == ord('2'):
                current_colormap = cv2.COLORMAP_INFERNO

            elif key == ord('3'):
                current_colormap = cv2.COLORMAP_TURBO

    except KeyboardInterrupt:
        # Permitir cerrar el programa utilizando Ctrl+C
        # desde la terminal.
        print("\nPrograma detenido con Ctrl+C.")

    finally:
        # 11. Liberar recursos.
        # release() libera la cámara para que otros programas
        # puedan utilizarla nuevamente.
        cap.release()

        # destroyAllWindows() cierra todas las ventanas creadas
        # por OpenCV.
        cv2.destroyAllWindows()

        # Procesar los últimos eventos de la interfaz gráfica
        # para asegurarnos de que las ventanas se cierren correctamente.
        cv2.waitKey(1)

        print("Cámara liberada. Programa terminado.")


# Esta condición garantiza que main() se ejecute solamente
# cuando este archivo se ejecuta directamente.
if __name__ == '__main__':
    main()
```

De igual manera verifique que la cámara en `cap = cv2.VideoCapture('/dev/video0')` debe de ser la misma que obtuvo en el paso 0.

Ejecuta el script desde la terminal:

```bash
python vision_termica.py
```

## 4. Resultados Esperados y Criterios de Éxito

Un estudiante ha completado con éxito la práctica si:

- **Fluidez de Video:** Ambas aplicaciones se ejecutan en tiempo real sin congelar la laptop, manteniendo una tasa de refresco constante cercana a los 30 FPS permitidos por el hardware de la cámara web integrada.
- **Aislamiento de Bordes:** La ventana del filtro neón muestra un fondo completamente negro y delinea con precisión las siluetas de rostros, manos y objetos físicos móviles cercanos en color verde fosforescente.
- **Gradiente de Calor:** En la simulación térmica, las fuentes de luz directa (como focos de techo o la pantalla de un teléfono móvil) se visualizan en color rojo brillante o blanco, mientras que las sombras proyectadas se renderizan en azul profundo.
- **Cierre Limpio:** Al presionar la tecla 'q' con el foco sobre cualquiera de las ventanas activas, la aplicación se cierra de inmediato liberando el recurso de la cámara para el sistema operativo sin dejar procesos huérfanos.

## 5. Troubleshooting (Solución de problemas comunes)

### Error: "No se pudo acceder a la cámara web"

**Causa:** Otro programa (como Zoom, Teams, Discord o Skype) está utilizando la cámara web de tu laptop en segundo plano.

**Solución:** Cierra por completo todas las aplicaciones que hagan uso del video y vuelve a ejecutar tu script de Python.

### La ventana se abre pero se queda congelada en color gris o negro

**Causa:** OpenCV requiere procesar los eventos gráficos de manera síncrona en cada ciclo de iteración. Si omites la función `cv2.waitKey(1)`, la ventana no podrá actualizar su búfer de renderizado.

**Solución:** Verifica que la línea `if cv2.waitKey(1) & ...` esté correctamente escrita dentro del bucle principal `while True`.

### Error de sintaxis o importación de librerías

**Causa:** No activaste el entorno virtual antes de ejecutar el archivo o instalaste las librerías de forma global fuera del contenedor aislado.

**Solución:** Comprueba que al inicio de la línea de comandos de tu terminal figure la etiqueta de activación `(.venv)`. Si no es así, repite el Paso 3.

## 6. Referencias Bibliográficas y Recursos Adicionales

- Bradski, G. (2000). *The OpenCV Library.* Dr. Dobb's Journal of Software Tools. (Artículo seminal y obligatorio para la citación científica de proyectos basados en OpenCV).
- Saif, Y., Yusof, Y., Rus, A. Z. M., et al. (2023). Implementing circularity measurements in industry 4.0-based manufacturing metrology using MQTT protocol and Open CV. *PLoS ONE*, 18(10), e0292814. (Análisis avanzado del uso de OpenCV en la calibración y metrología industrial de precisión).
- Răileanu, S., Borangiu, T., Anton, F., & Anton, S. (2021). Open source machine vision platform for manufacturing and robotics. *IFAC PapersOnLine*, 54(1), 522–527. (Guía de diseño para la intercomunicación entre buffers gráficos de OpenCV y actuadores de robots mediante sockets TCP/IP).
- Raspberry Pi Ltd. (2026). *The Picamera2 Library: A libcamera-based Python library for Raspberry Pi cameras.* Release 3. (Manual técnico de referencia para el tratamiento en memoria de matrices de píxeles, buffers y hilos asíncronos).