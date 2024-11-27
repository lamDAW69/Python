import cv2
import mediapipe as mp
import os

def censor_faces_mediapipe(input_path, output_path, pixelado=True):
    """
    Censura rostros en una imagen usando MediaPipe.
    
    Args:
        input_path (str): Ruta de la imagen de entrada
        output_path (str): Directorio donde se guardará la imagen censurada
        pixelado (bool): True para pixelar, False para desenfoque
        
    Returns:
        str: Ruta del archivo censurado o None si hay error
    """
    try:
        # Inicializar MediaPipe Face Detection
        mp_face_detection = mp.solutions.face_detection
        
        # Leer la imagen
        image = cv2.imread(input_path)
        if image is None:
            print("Error: No se pudo cargar la imagen")
            return None
            
        # Convertir BGR a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detectar rostros
        with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(image_rgb)
            
        # Si no se detectaron rostros, devolver None
        if not results.detections:
            print("No se detectaron rostros en la imagen")
            return None
            
        # Procesar cada rostro detectado
        for detection in results.detections:
            # Obtener las coordenadas del rostro
            bboxC = detection.location_data.relative_bounding_box
            h, w, _ = image.shape
            x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                                int(bboxC.width * w), int(bboxC.height * h)
            
            # Asegurar que las coordenadas estén dentro de los límites
            x = max(0, x)
            y = max(0, y)
            w_box = min(w_box, w - x)
            h_box = min(h_box, h - y)
            
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
        
        # Generar nombre único para el archivo de salida
        output_filename = f'censored_{os.path.basename(input_path)}'
        output_file = os.path.join(output_path, output_filename)
        
        # Guardar la imagen censurada
        cv2.imwrite(output_file, image)
        print(f"Imagen censurada guardada en: {output_file}")
        
        return output_file
        
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")
        return None