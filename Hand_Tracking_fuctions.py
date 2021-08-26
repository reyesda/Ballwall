import cv2
import mediapipe as mp
import math


def norm(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


class hands_traking:
    def __init__(self, show=False, angulo=22.5):

        # take photo to camera
        self.cap = cv2.VideoCapture(0)
        # run model hands
        self.mpHands = mp.solutions.hands
        # make model object
        self.hands = self.mpHands.Hands(False, 1)
        # take draw function
        self.mpDraw = mp.solutions.drawing_utils
        # save fingers position
        self.positions = []
        # True: show image on screen
        self.show = show
        # where returned is true
        self.angulo = angulo
        self.angle_result = 150
        self.diferencias_neta = 0

    def camera_modelhand(self):
        # take photo to camera
        # self.cap = cv2.VideoCapture(0)
        anterior = 0
        if self.positions:
            anterior = self.positions[8][0]
        self.positions = []
        # take image and if it was success
        success, img = self.cap.read()
        # transform image to rpg
        imRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # take result of model
        results = self.hands.process(imRGB)

        if results.multi_hand_landmarks:
            # iterate results in landmarks
            for handLms in results.multi_hand_landmarks:
                # iterate position x and y of marks. add id
                for ids, lm in enumerate(handLms.landmark):
                    self.positions.append([lm.x, lm.y])

                    if self.show:
                        # take size of image
                        h, w, c = img.shape

                        # show figers point on screen
                        cv2.putText(img, str(ids), (int(lm.x * w), int(lm.y * h)), cv2.FONT_HERSHEY_PLAIN,
                                    1, (0, 0, 0), 2)

                self.diferencias_neta = self.positions[8][0] - anterior

                if self.show:
                    # draw conection between points
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

                    # show and stay camera image on screen
                    cv2.imshow("Image", img)
                    cv2.waitKey(1)

        #  self.cap.release()
        self.positions *= 100

    def actived(self):
        self.camera_modelhand()

        if self.positions:
            self.angle_result = math.acos((norm(self.positions[4], self.positions[8]) ** 2 -
                                           norm(self.positions[0], self.positions[4]) ** 2 -
                                           norm(self.positions[0], self.positions[8]) ** 2) /
                                          (-2 * norm(self.positions[0], self.positions[4]) *
                                           norm(self.positions[0], self.positions[8])))

            self.angle_result = math.degrees(self.angle_result)

            if self.angle_result < 0:
                self.angle_result = 90 - self.angle_result

            # self.angle_result = norm(self.positions[4], self.positions[8])

            if self.angle_result <= self.angulo:
                return True
            else:
                return False
        else:
            pass
            # return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()


# mano = hands_traking(True, 25)
# px_anterior = 0
# px_siguiente = 0
# diferencias = 0
# while True:
#     px_siguiente = mano.positions[8][0] if mano.positions else 0
#     mano.actived()
#     diferencias = px_siguiente - px_anterior
#     px_anterior = px_siguiente
#     print(diferencias)
