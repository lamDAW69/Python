import cv2
import cvlib as cv 
from cvlib.object_detection import draw_bbox
import os

# Rutas de modelo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models')

# Actualizar rutas para tiny-yolo
cfg_path = os.path.join(MODEL_PATH, 'yolov4-tiny.cfg')
weights_path = os.path.join(MODEL_PATH, 'yolov4-tiny.weights')

# Verificar archivos
if not os.path.exists(cfg_path) or not os.path.exists(weights_path):
    print("Error: Archivos del modelo tiny no encontrados")
    exit()

try:
    # Inicializar cámara
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("Error: No se pudo acceder a la cámara")
        exit()

    print("Iniciando detección de objetos... Presiona 'q' para salir")
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
            
        try:
            # Detección con YOLOv4-tiny
            bbox, label, conf = cv.detect_common_objects(
                frame,
                confidence=0.5,
                model='yolov4-tiny'
            )
            
            # Dibujar detecciones
            output_image = draw_bbox(frame, bbox, label, conf)
            
            # Mostrar objetos detectados
            if label:
                print(f"Objetos detectados: {set(label)}")
            
            # Mostrar imagen
            cv2.imshow("Object Detection", output_image)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        except Exception as e:
            print(f"Error en detección: {str(e)}")
            break

finally:
    video.release()
    cv2.destroyAllWindows()