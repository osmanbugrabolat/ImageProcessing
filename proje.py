import cv2
import numpy as np
import mainn as mn
import time
import autopy

wcam,hcam=640,480
movie = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = mn.HandDetector()
wekran, hekran=autopy.screen.get_size()
imgR=100
#imlecin yumuşatılması için oluşturulmuş veriler
smoothing=5
plocX,plocY=0,0
clocX,xloxY=0,0
#imlecin yumuşatılması için oluşturulmuş veriler
# DSHOW hatanın giderilmesi içindir.
# 0 kaçıncı kameramız oladuğunu gösterir
pTime = 0
#mn.main()

while True:
     # movie.read ile sonsuz döngü içerisinde okuma gerçekleştirilir.
     # iki değer döndürür
     # 1- görüntü 2- state
    state, frame = movie.read()
    if not state:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv2.flip(frame, 1)
    frame=detector.findHands(frame)
    lmlist=detector.findPosition(frame)

    # 1 orta ve işaret parmağın indexlreinin alınması
    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        #print(x1,y1,x2,y2)
        #parmakların indexlerinin yazdırılması
        fingers=detector.fingersup()
        #print(fingers)
        #ölçülerin uyuşması için ayarlanan alanın çizilmesi:
        cv2.rectangle(frame, (imgR, imgR), (wcam - imgR, hcam - imgR), (255, 0, 255), 2)
    #2 işaret parmağın yukarda olduğunu belirlemek
        if fingers[1]==1 and fingers[2]==0:
            # 4 koordinatların convert edilmesi

            x3 = np.interp(x1,(imgR,wcam-imgR),(0,wekran))
            y3 = np.interp(y1, (imgR, hcam-imgR), (0, hekran))

            #print("işaret armağın açık orta parmak kapalı")
            # 5 veri ile imleç kontrolü
            clocX=plocX+(x3-plocX)/smoothing
            clocY = plocY + (y3 - plocY) / smoothing
            if lmlist!=0:

                #parmakların olma durumu kontrolü ile parmağın imleci yönlendirmesi:

                autopy.mouse.move(clocX, clocY)
                cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)

                plocX,plocY=clocX,clocY
                #parmak imleç ile yönlendirilirken parmağın ucuna mavi bir daire çizilmesi:
        if fingers[1] == 1 and fingers[2] == 1:
            #iki parmak da havada iseq
            length, frame,lineinfo=detector.find_distance(8,12,frame)
            print(length)
            if length<30:
                #aradaki fark 30 dan küçük ise tıklama gerçekleştir
                cv2.circle(frame,(lineinfo[4],lineinfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()
                time.sleep(0.1)

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