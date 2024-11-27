import os
import cv2
import mediapipe as mp

# Suprimir advertencias de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def censor_faces_mediapipe(image_path, output_path, pixelado=False):
    # Inicializar el modelo de detección de rostros de MediaPipe
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

    # Leer la imagen
    image = cv2.imread(image_path)
    if image is None:
        print("Error: No se pudo cargar la imagen. Verifica la ruta.")
        return
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detectar rostros
    results = face_detection.process(image_rgb)

    if results.detections:
        for detection in results.detections:
            # Obtener las coordenadas del rostro
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = image.shape
            x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)

            if pixelado:
                # Aplicar pixelado
                face = image[y:y + h_box, x:x + w_box]
                face_pixeled = cv2.resize(face, (10, 10), interpolation=cv2.INTER_LINEAR)
                face_pixeled = cv2.resize(face_pixeled, (w_box, h_box), interpolation=cv2.INTER_NEAREST)
                image[y:y + h_box, x:x + w_box] = face_pixeled
            else:
                # Aplicar desenfoque
                face = image[y:y + h_box, x:x + w_box]
                face_blurred = cv2.GaussianBlur(face, (99, 99), 30)
                image[y:y + h_box, x:x + w_box] = face_blurred

    # Guardar la imagen censurada
    output_file = os.path.join(output_path, 'imagen_censurada_mediapipe.jpg')
    cv2.imwrite(output_file, image)
    print(f"Imagen censurada guardada en: {output_file}")

# Rutas de entrada y salida
route_input = r'C:\Users\Luis\Documents\Cursos EOI\Curso Python\Python\faceCensorship\Human_faces.jpg'
route_output = r'C:\Users\Luis\Documents\Cursos EOI\Curso Python\Python\faceCensorship'

censor_faces_mediapipe(route_input, route_output, pixelado=True)
