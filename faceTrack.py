from cvzone.FaceDetectionModule import FaceDetector
import cv2
import socket
import mediapipe as mp

# Configs
image_rows = 480
image_cols = 640
cap = cv2.VideoCapture(0)
cap.set(3, image_cols)
cap.set(4, image_rows)
detector = FaceDetector(minDetectionCon=0.8)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ('127.0.0.1', 5052)

mp_face_mesh = mp.solutions.face_mesh
# 初始化 Face Mesh 模型
face_mesh = mp_face_mesh.FaceMesh()


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# get face's coord on screen by FaceDetector
# return a tuple (x, y) on the scale of pixel
def getCenter(img):
    img, bboxs = detector.findFaces(img)
    if bboxs:
        # bboxInfo - "id","bbox","score","center"
        return bboxs[0]["center"]
    return (-1, -1)


# get depth of face
# return a integer on the scale of cm
def getDepth(img):
    results = face_mesh.process(img)
    if results.multi_face_landmarks:
        # 取得第一個偵測到的臉部關鍵點
        face_landmarks = results.multi_face_landmarks[0]
        # 取得眼睛的關鍵點索引
        left_eye_l_index = 362
        left_eye_r_index = 359
        right_eye_l_index = 133
        right_eye_r_index = 130
        # 取得左眼和右眼的座標
        left_eye_l = face_landmarks.landmark[left_eye_l_index]
        left_eye_r = face_landmarks.landmark[left_eye_r_index]
        right_eye_l = face_landmarks.landmark[right_eye_l_index]
        right_eye_r = face_landmarks.landmark[right_eye_r_index]
        # 將座標轉換為畫面上的位置
        left_eye_l = Coord(left_eye_l.x * image_cols,
                           left_eye_l.y * image_rows)
        left_eye_r = Coord(left_eye_r.x * image_cols,
                           left_eye_r.y * image_rows)
        right_eye_l = Coord(right_eye_l.x * image_cols,
                            right_eye_l.y * image_rows)
        right_eye_r = Coord(right_eye_r.x * image_cols,
                            right_eye_r.y * image_rows)
        # 計算距離
        dx = left_eye_r.x - left_eye_l.x
        dX = 3.5
        normalizedFocaleX = 1.40625
        fx = min(image_cols, image_rows) * normalizedFocaleX
        return int(fx * (dX / dx))
        # dZ = int(fx * (dX / dx))


if __name__ == '__main__':
    while True:
        success, image = cap.read()
        image = cv2.flip(image, flipCode=1)  # 左右翻轉圖像

        coord_data = getCenter(image) + (getDepth(image), )
        # getAxis(image)
        # print(coord_data)
        data = str.encode(str(coord_data))
        sock.sendto(data, serverAddressPort)

        cv2.imshow("image", image)
        if cv2.waitKey(1) == 27:  # press ESC to quit
            break
    # stop capturing and shut down
    cap.release()
    cv2.destroyAllWindows()
