# Mario Bros Face Filter

Este demo utiliza **OpenCV** y la cámara web para detectar rostros en tiempo real y colocar sobre ellos un **sombrero de Mario o Luigi** y un **bigote** utilizando imágenes con transparencia.

El programa detecta automáticamente los rostros mediante un clasificador Haar Cascade y ajusta el tamaño y posición de los accesorios según el tamaño del rostro detectado.

## Requisitos

Se necesita:

- Python 3
- OpenCV
- NumPy
- Una cámara web
- Linux con acceso a `/dev/video0`

Se recomienda utilizar un entorno virtual de Python.

### Instalar las dependencias

Si todavía no están instaladas:

```bash
pip install opencv-python numpy
```

## Estructura de archivos

Los archivos deben estar en la misma carpeta:

```text
Demostracion/
├── mario.py
├── mario_hat.png
├── luigi_hat.png
└── bigote.png
```

### Importante

Las imágenes `mario_hat.png`, `luigi_hat.png` y `bigote.png` deben tener **transparencia (canal Alpha)**.

Si alguna imagen no tiene transparencia, el programa mostrará un mensaje de error y finalizará.

## Ejecución

Primero se debe entrar en la carpeta donde se encuentra el programa (la dirección que se muestra abajo es un ejemplo, puede cambiarla a conveniencia):

```bash
cd ~/Desktop/Taller\ embebidos/OpenCV/Demostracion
```
Si se está utilizando un entorno virtual, activarlo:

```bash
source .venv/bin/activate
```

Luego ejecutar:

```bash
python mario.py
```

Al iniciar correctamente aparecerá el mensaje:

```text
Visión Mario iniciada.
Presiona 'q' o ESC para salir.
```

Se abrirá una ventana mostrando la imagen de la cámara.

## Funcionamiento

El programa realiza los siguientes pasos:

1. Carga el detector de rostros de OpenCV.
2. Carga la imagen `mario_hat.png`.
3. Carga la imagen `bigote.png`.
4. Abre la cámara `/dev/video0`.
5. Captura imágenes continuamente.
6. Convierte cada frame a escala de grises.
7. Detecta los rostros presentes.
8. Coloca el sombrero sobre cada rostro.
9. Coloca el bigote debajo de la nariz y encima del labio.
10. Muestra el resultado en tiempo real.

El tamaño de los accesorios se calcula proporcionalmente al tamaño del rostro detectado.

## Controles

Durante la ejecución:

- **Q** → salir del programa.
- **ESC** → salir del programa.

Al salir, OpenCV libera la cámara y cierra la ventana automáticamente.

## Cambiar el sombrero de Mario por el de Luigi

Para utilizar un sombrero de Luigi, solamente se debe cambiar el nombre del archivo utilizado en esta línea:

```python
hat = cv.imread('mario_hat.png', cv.IMREAD_UNCHANGED)
```

por:

```python
hat = cv.imread('luigi_hat.png', cv.IMREAD_UNCHANGED)
```


De esta manera, **no es necesario modificar la función que coloca el sombrero**. El programa utilizará automáticamente la imagen de `luigi_hat.png`.

También se puede volver a Mario simplemente cambiando:

```python
hat = cv.imread('luigi_hat.png', cv.IMREAD_UNCHANGED)
```

por:

```python
hat = cv.imread('mario_hat.png', cv.IMREAD_UNCHANGED)
```

## Cámara

El programa utiliza específicamente:

```python
cap = cv.VideoCapture('/dev/video0')
```

Por lo tanto, `/dev/video0` debe corresponder a la cámara que se desea utilizar.

Para comprobar las cámaras disponibles en Linux:

```bash
ls /dev/video*
```

Por ejemplo:

```text
/dev/video0
/dev/video1
```

Si la cámara utilizada es `/dev/video0`, no es necesario realizar ningún cambio.

## Solución de problemas

### No se puede acceder a la cámara

Si aparece:

```text
Error: No se pudo acceder a la cámara.
```

comprobar que `/dev/video0` existe:

```bash
ls /dev/video*
```

También se puede comprobar que ninguna otra aplicación esté utilizando la cámara, como un navegador, Zoom u otra aplicación de videollamadas.

### No se puede cargar el sombrero

Si aparece:

```text
Error: No se pudo cargar mario_hat.png
```

comprobar que el archivo exista en la misma carpeta:

```bash
ls
```

Debe aparecer:

```text
mario_hat.png
```

### No se puede cargar el bigote

Si aparece:

```text
Error: No se pudo cargar bigote.png
```

comprobar que el archivo exista:

```bash
ls
```

Debe aparecer:

```text
bigote.png
```

### Error relacionado con Alpha

Si aparece:

```text
mario_hat.png debe tener transparencia (canal Alpha).
```

o:

```text
bigote.png debe tener transparencia (canal Alpha).
```

significa que la imagen no tiene un cuarto canal de transparencia.

Las imágenes utilizadas deben estar en formato RGBA, es decir:

```text
B → Blue
G → Green
R → Red
A → Alpha (transparencia)
```

## Resumen

Este proyecto demuestra el uso de diferentes funcionalidades básicas de OpenCV:

- `cv.VideoCapture()` → captura de video desde la cámara.
- `cv.CascadeClassifier()` → detección de rostros.
- `cv.cvtColor()` → conversión a escala de grises.
- `detectMultiScale()` → detección de rostros.
- `cv.resize()` → cambio de tamaño de los accesorios.
- `cv.imshow()` → visualización del resultado.
- Canal **Alpha** → combinación de imágenes transparentes con el video.
- `cv.waitKey()` → detección de teclas para controlar la aplicación.

El resultado es un filtro en tiempo real que transforma el video de la cámara colocando accesorios de Mario sobre los rostros detectados.