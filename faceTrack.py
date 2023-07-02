from cvzone.FaceDetectionModule import FaceDetector
import cv2
import socket
import mediapipe as mp

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
detector=FaceDetector(minDetectionCon=0.8)
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAddressPort=('127.0.0.1',5052)
dZ = 3.0
mp_face_mesh = mp.solutions.face_mesh
# 初始化Face Mesh模型
face_mesh = mp_face_mesh.FaceMesh()

while True:
    success,img=cap.read()
    img = cv2.flip(img, flipCode=1) # 左右翻轉圖像
    img, bboxs = detector.findFaces(img)
    
    results = face_mesh.process(img)
    if bboxs:
        # bboxInfo - "id","bbox","score","center"
        center = bboxs[0]["center"]
        print(center)        
        data=str.encode(str(center))
        sock.sendto(data,serverAddressPort)
    if results.multi_face_landmarks:
        # 取得第一個偵測到的臉部關鍵點
        face_landmarks = results.multi_face_landmarks[0]
        # 取得眼睛的關鍵點索引
        left_eye_landmark_index = 362
        left = 359
        right_eye_landmark_index = 133
        right = 130
        # 取得左眼和右眼的座標
        left_eye_coords = face_landmarks.landmark[left_eye_landmark_index]
        left_coords = face_landmarks.landmark[left]
        right_eye_coords = face_landmarks.landmark[right_eye_landmark_index]
        right_coords = face_landmarks.landmark[right]
        # 將座標轉換為畫面上的位置
        image_rows, image_cols, _ = img.shape
        left_eye_x, left_eye_y = int(left_eye_coords.x * image_cols), int(left_eye_coords.y * image_rows)
        right_eye_x, right_eye_y = int(right_eye_coords.x * image_cols), int(right_eye_coords.y * image_rows)
        left_x, left_y = int(left_coords.x * image_cols), int(left_coords.y * image_rows)
        right_x, right_y = int(right_coords.x * image_cols), int(right_coords.y * image_rows)
        #計算距離
        width = image_cols
        height = image_rows 
        dx = left_x - left_eye_x
        dX = 3.5
        normalizedFocaleX = 1.40625
        fx = min(width, height) * normalizedFocaleX
        dZ = (fx * (dX / dx))   
        print("dZ:")
        print(dZ)         

    cv2.imshow("image",img)
    if cv2.waitKey(1) == 27: # 按下 ESC 鍵退出程序並釋放攝像頭
        break

cap.release()  # 釋放攝像頭
cv2.destroyAllWindows()  # 關閉所有視窗
    
