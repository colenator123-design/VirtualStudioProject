from cvzone.FaceDetectionModule import FaceDetector
import cv2
import socket
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
detector=FaceDetector(minDetectionCon=0.8)
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAddressPort=('127.0.0.1',5052)
while True:
    success,img=cap.read()
    img = cv2.flip(img, flipCode=1) # 左右翻轉圖像
    img, bboxs = detector.findFaces(img)
    if bboxs:
        # bboxInfo - "id","bbox","score","center"
        center = bboxs[0]["center"]
        print(center)        
        data=str.encode(str(center))
        sock.sendto(data,serverAddressPort)
    cv2.imshow("image",img)
    if cv2.waitKey(1) == 27: # 按下 ESC 鍵退出程序並釋放攝像頭
        break

cap.release()  # 釋放攝像頭
cv2.destroyAllWindows()  # 關閉所有視窗
