import math
import cv2
import mediapipe as mp
import time
#+++find distance+++-+++fingersup+++-+++findposition+++-+++findhands+++
class HandDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,tracCon=0.5,modelC=1):
        self.mode=mode
        self.maxHands=maxHands
        self.modelC=modelC
        self.detectionCon=detectionCon
        self.trackCon=tracCon

        self.mpHands = mp.solutions.hands
        self.hands= self.mpHands.Hands(self.mode, self.maxHands,self.modelC ,self.detectionCon, self.trackCon)
        self.mdDrraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]
    def ekrandakafabul(self,frame,draw=True):
        lmList=[]
        mp_drawing=mp.solutions.drawing_utils
        mp_holistic=mp.solutions.holistic
        with mp_holistic.Holistic(min_detection_confidence=0.5,min_tracking_confidence=0.5)as holistic:
            imgrgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results=holistic.process(imgrgb)
            imgrgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(imgrgb,results.face_landmarks,mp_holistic.FACEMESH_TESSELATION)
            print("result_facelandmarks=",results.face_landmarks)
            if results.face_landmarks!=None:
                for i in results.face_landmarksa:
                    for id, lm in enumerate(i):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        x_List.append(cx)
                        y_List.append(cy)
                        # print(id, cx, cy)
                        lmList.append([id, cx, cy])
                    xmin, xmax = min(x_List), max(x_List)
                    ymin, ymax = min(y_List), max(y_List)
                    break
        return  imgrgb,lmList



    def ekrandanbul(self,frame,draw=True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for el in self.results.multi_hand_landmarks:
                if draw:
                    #elin noktalarının işaretlenmesi ve birleştirilmesi.
                    self.mdDrraw.draw_landmarks(frame, el, self.mpHands.HAND_CONNECTIONS)

        return frame

    def findHands(self,frame,draw=True):
        #elim tespiti ve basit işaretlenmesi gerçekleştiriliyor

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        # ELİMİZİN İŞARETLENMESİ:
        if self.results.multi_hand_landmarks:
            for el in self.results.multi_hand_landmarks:
                if draw:
                    #elin noktalarının işaretlenmesi ve birleştirilmesi.
                    self.mdDrraw.draw_landmarks(frame, el, self.mpHands.HAND_CONNECTIONS)

        return frame

    def findPosition(self,frame,handNo=0,draw=True):
        self.lmList=[]
        x_List=[]
        y_List=[]
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_List.append(cx)
                y_List.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin,xmax=min(x_List),max(x_List)
            ymin, ymax = min(y_List), max(y_List)
            if draw:
                #eli gösteren dikdörtgen çizimi: sürekli olarak verileri alır ve yer değiştirir
                cv2.rectangle(frame,(xmin-20,ymin-20),(xmax+20,ymax+20),
                              (0,255,0),2)
        return self.lmList


    def fingersup(self):
        fingers=[]
        #baş parmak
        if self.lmList[self.tipIds[0]][1]>self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #baş parmak haricindeki parmaklar
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2]< self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        return fingers





    def find_distance(self,p1,p2,img,draw=True,r=15,t=3):
        x1,y1=self.lmList[p1][1:]
        x2,y2=self.lmList[p2][1:]
        cx,cy=(x1+x2) // 2,(y1+y2)//2
        if draw:
            #parmaklar arası mesafenin işaretlenmesi:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),t)
            cv2.circle(img, (x1, y1),  r,(255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r,(255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r,(0, 0, 255), cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        return length,img,[x1,y1,x2,y2,cx,cy]

def main():
    movie = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = HandDetector()
    # DSHOW hatanın giderilmesi içindir.
    # 0 kaçıncı kameramız oladuğunu gösterir
    pTime = 0
    while True:
        # movie.read ile sonsuz döngü içerisinde okuma gerçekleştirilir.
        # iki değer döndürür
        # 1- görüntü 2- state
        state, frame = movie.read()
        if not state:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # frame'i flip ediyoruz ki normal görüntüyü elde edebilelim 1 arametresi de yatayda
        # aynalama sağlar. 0 ise dikey aynalama sağlar.
        frame = cv2.flip(frame, 1)
        frame = detector.findHands(frame)
        list=detector.findPosition(frame)
        #print(list)
        # ELİMİZİN İŞARETLENMESİ:
        # fps göstergesi:
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        # görüntünün gösterilmesi:
        cv2.imshow("kamera", frame)

        # herhangi bir tuşa basılınca kapatılması:
        if cv2.waitKey(50) & 0xFF == ord("q"):
            # q tuşuna basılınca program kapanacak
            break
    movie.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()