import math
from cvzone.FaceDetectionModule import FaceDetector
import cv2
import socket
import mediapipe as mp
import numpy as np

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


def getAxis(img):
    # setup sampling landmarks
    indexes = [1, 33, 263, 61, 291, 199]
    objPts = np.array([[0.4941680431365967, 0.6710584759712219, -0.08302542567253113],
                       [0.3756912052631378, 0.5486021041870117, 0.025898095220327377],
                       [0.6125413179397583, 0.5426622629165649, 0.022610986605286598],
                       [0.43580639362335205, 0.7722113132476807,
                           0.0031681121326982975],
                       [0.5561882257461548, 0.7670935988426208,
                           0.0017560963751748204],
                       [0.49711552262306213, 0.8604360818862915, -0.007275797426700592]
                       ])
    imgPts = []
    # process through mediapipe and get face mesh
    results = face_mesh.process(img)
    if results.multi_face_landmarks is None:
        print("No faces detected")
        return
    face_landmarks = results.multi_face_landmarks[0]
    # print("----------")
    # update coords of 6 sampling points
    for i in indexes:
        # print([face_landmarks.landmark[i].x,
        #         face_landmarks.landmark[i].y, face_landmarks.landmark[i].z])
        imgPts.append([face_landmarks.landmark[i].x,
                       face_landmarks.landmark[i].y])
    imgPts = np.array(imgPts)
    # setup camera matrix
    normalizedFocaleY = 1.28  # Logitech 922
    focalLength = image_rows * normalizedFocaleY
    camMat = np.array([[focalLength, 0, image_cols / 2.0],
                       [0, focalLength, image_rows / 2.0],
                       [0, 0, 1]])
    # get rotation matrix, transform matrix by comparing inital coords (3D) to updated coords (on image, 2D)
    # then decompose Euler angles from rotation matrix
    success, rvec, tvec = cv2.solvePnP(objPts, imgPts, camMat, None)
    if (not success):
        print("sth went run with solvePnP")
        return
    rmat, _ = cv2.Rodrigues(rvec)
    sy = math.sqrt(rmat[0, 0] * rmat[0, 0] + rmat[1, 0] * rmat[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(rmat[2, 1], rmat[2, 2])
        y = math.atan2(-rmat[2, 0], sy)
        z = math.atan2(rmat[1, 0], rmat[0, 0])
    else:
        x = math.atan2(-rmat[1, 2], rmat[1, 1])
        y = math.atan2(-rmat[2, 0], sy)
        z = 0
    # print(x / 3.14 * 180,y/ 3.14 * 180,z/ 3.14 * 180)
    # roll = y
    # pitch = x
    # yaw = z

    # extend landmark1 (nose) by 0.2 on x, y, z, to make it 3 basis
    worldPts = np.array([objPts[0], objPts[0], objPts[0]])
    worldPts[0][0] += 0.2
    worldPts[1][1] += 0.2
    worldPts[2][2] += 0.2
    worldPts = np.append(worldPts, objPts, axis=0)
    # project the basis and draw it
    imagePointsProjected, _ = cv2.projectPoints(
        worldPts, rvec, tvec, camMat, None)
    imagePointsProjected = imagePointsProjected.reshape(-1, 2)
    drawAxis(img, imagePointsProjected)
    return


# show the axis calculated fom getAxis()
# red one as x-axis, green one as y-axis, blue as z-axis
def drawAxis(img, projectedPts):
    line_width = 3
    red = (0, 0, 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)
    # x-axis
    cv2.line(img,
             (int(projectedPts[3][0] * image_cols),
              int(projectedPts[3][1] * image_rows)),
             (int(projectedPts[0][0] * image_cols),
              int(projectedPts[0][1] * image_rows)),
             red, line_width)
    # y-axis
    cv2.line(img,
             (int(projectedPts[3][0] * image_cols),
              int(projectedPts[3][1] * image_rows)),
             (int(projectedPts[1][0] * image_cols),
                 int(projectedPts[1][1] * image_rows)),
             green, line_width)
    # z-axis
    cv2.line(img,
             (int(projectedPts[3][0] * image_cols),
              int(projectedPts[3][1] * image_rows)),
             (int(projectedPts[2][0] * image_cols),
                 int(projectedPts[2][1] * image_rows)),
             blue, line_width)
    return


if __name__ == '__main__':
    while True:
        success, image = cap.read()
        image = cv2.flip(image, flipCode=1)  # 左右翻轉圖像

        coord_data = getCenter(image) + (getDepth(image), )
        getAxis(image)
        # print(coord_data)
        data = str.encode(str(coord_data))
        sock.sendto(data, serverAddressPort)

        cv2.imshow("image", image)
        if cv2.waitKey(1) == 27:  # press ESC to quit
            break
    # stop capturing and shut down
    cap.release()
    cv2.destroyAllWindows()
