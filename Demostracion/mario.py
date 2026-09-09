import cv2 as cv
import numpy as np



# 1. Cargar detector de rostros
face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
)



# 2. Cargar el gorro
hat = cv.imread('mario_hat.png', cv.IMREAD_UNCHANGED)

if hat is None:
    print("Error: No se pudo cargar mario_hat.png")
    exit()

if hat.shape[2] != 4:
    print("Error: mario_hat.png debe tener transparencia (canal Alpha).")
    exit()

# 3. Cargar el bigote
mustache = cv.imread('bigote.png', cv.IMREAD_UNCHANGED)

if mustache is None:
    print("Error: No se pudo cargar bigote.png")
    exit()

if mustache.shape[2] != 4:
    print("Error: bigote.png debe tener transparencia (canal Alpha).")
    exit()

# 3. Función para colocar el gorro
def poner_gorro(img, hat, x, y, w, h):

    # Ancho del gorro proporcional al rostro
    hat_width = int(w * 1.4)

    # Mantener proporción original
    escala = hat_width / hat.shape[1]
    hat_height = int(hat.shape[0] * escala)

    hat_resized = cv.resize(
        hat,
        (hat_width, hat_height),
        interpolation=cv.INTER_AREA
    )

    # Centrar el gorro sobre el rostro
    hat_x = x + w // 2 - hat_width // 2

    # Colocar el gorro un poco por encima del rostro
    hat_y = y - int(hat_height * 0.75)

    # Si queda fuera de la imagen, no hacer nada
    if hat_x < 0 or hat_y < 0:
        return img

    # Evitar que se salga por la derecha o abajo
    if hat_x + hat_width > img.shape[1]:
        return img

    if hat_y + hat_height > img.shape[0]:
        return img

    # Separar canales BGR y Alpha
    hat_bgr = hat_resized[:, :, :3]
    alpha = hat_resized[:, :, 3]

    # Convertir Alpha de 0-255 a 0.0-1.0
    alpha = alpha.astype(np.float32) / 255.0

    # Hacer que Alpha tenga 3 canales
    alpha = cv.merge([alpha, alpha, alpha])

    # Región de la imagen donde irá el gorro
    roi = img[
        hat_y:hat_y + hat_height,
        hat_x:hat_x + hat_width
    ]

    # Mezclar gorro e imagen usando transparencia
    resultado = (
        hat_bgr.astype(np.float32) * alpha
        + roi.astype(np.float32) * (1 - alpha)
    )

    resultado = resultado.astype(np.uint8)

    # Colocar resultado en la imagen original
    img[
        hat_y:hat_y + hat_height,
        hat_x:hat_x + hat_width
    ] = resultado

    return img

# Función para colocar el bigote
def poner_bigote(img, mustache, x, y, w, h):

    # Ancho del bigote proporcional al rostro
    mustache_width = int(w * 0.55)

    # Mantener proporción original
    escala = mustache_width / mustache.shape[1]
    mustache_height = int(mustache.shape[0] * escala)

    mustache_resized = cv.resize(
        mustache,
        (mustache_width, mustache_height),
        interpolation=cv.INTER_AREA
    )

    # Centrar el bigote horizontalmente
    mustache_x = x + w // 2 - mustache_width // 2

    # Colocar el bigote debajo de la nariz y sobre el labio
    mustache_y = y + int(h * 0.50)

    # Si queda fuera de la imagen, no hacer nada
    if mustache_x < 0 or mustache_y < 0:
        return img

    if mustache_x + mustache_width > img.shape[1]:
        return img

    if mustache_y + mustache_height > img.shape[0]:
        return img

    # Separar canales BGR y Alpha
    mustache_bgr = mustache_resized[:, :, :3]
    alpha = mustache_resized[:, :, 3]

    # Convertir Alpha de 0-255 a 0.0-1.0
    alpha = alpha.astype(np.float32) / 255.0

    # Hacer que Alpha tenga 3 canales
    alpha = cv.merge([alpha, alpha, alpha])

    # Región donde irá el bigote
    roi = img[
        mustache_y:mustache_y + mustache_height,
        mustache_x:mustache_x + mustache_width
    ]

    # Mezclar bigote e imagen usando transparencia
    resultado = (
        mustache_bgr.astype(np.float32) * alpha
        + roi.astype(np.float32) * (1 - alpha)
    )

    resultado = resultado.astype(np.uint8)

    # Colocar resultado en la imagen
    img[
        mustache_y:mustache_y + mustache_height,
        mustache_x:mustache_x + mustache_width
    ] = resultado

    return img
# 4. Abrir cámara
cap = cv.VideoCapture('/dev/video0')
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

print("Visión Mario iniciada.")
print("Presiona 'q' o ESC para salir.")


# 5. Procesamiento en tiempo real
while True:

    ret, frame = cap.read()

    if not ret:
        print("Error al recibir el frame.")
        break

    # Convertir a escala de grises
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detectar rostros
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    # Procesar cada rostro encontrado
    for (x, y, w, h) in faces:

        frame = poner_gorro(
            frame,
            hat,
            x, y, w, h
        )

        frame = poner_bigote(
            frame,
            mustache,
            x, y, w, h
        )
    # Mostrar resultado
    cv.imshow('Mario Bros Face Filter', frame)

    # Salir con Q o ESC
    key = cv.waitKey(1) & 0xFF

    if key == ord('q') or key == 27:
        break


# 6. Liberar recursos
cap.release()
cv.destroyAllWindows()

print("Programa terminado.")
