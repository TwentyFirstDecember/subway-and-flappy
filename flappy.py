import mediapipe as mp
import cv2
import pyautogui as pg

class PoseC:
    def __init__(self) -> None:
        self.sol = mp.solutions.pose
        self.model = self.sol.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.7,
                                            min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

    def detectPose(self, image):
        result = self.model.process(image)
        self.mp_drawing.draw_landmarks(image=image, landmark_list=result.pose_landmarks,
                                      connections=self.sol.POSE_CONNECTIONS,
                                      landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 255, 255),
                                                                                   thickness=3, circle_radius=3),
                                      connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(49, 125, 237),
                                                                       thickness=2, circle_radius=2))
        return result
    def cal_Vertical(self, mid_y, mid_height):
        if (mid_y < mid_height):
            return -1
        return 1
    def cal_mid_point(self, result, height, width):
        left_x = int(result.pose_landmarks.landmark[self.sol.PoseLandmark.RIGHT_SHOULDER].x * width)
        right_x = int(result.pose_landmarks.landmark[self.sol.PoseLandmark.LEFT_SHOULDER].x * width)
        left_y = int(result.pose_landmarks.landmark[self.sol.PoseLandmark.RIGHT_SHOULDER].y * height)
        right_y = int(result.pose_landmarks.landmark[self.sol.PoseLandmark.LEFT_SHOULDER].y * height)
        mid_x = (left_x + right_x) // 2
        mid_y = (left_y + right_y) // 2
        return mid_x, mid_y

class flappy:

    def __init__(self) -> None:
        self.PoseC = PoseC()
        self.cal_Vertical = self.PoseC.cal_Vertical
        self.cal_mid_point = self.PoseC.cal_mid_point

    def play(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280 // 2)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720 // 2)
        # cv2.namedWindow('flappy Surfer', cv2.WINDOW_NORMAL)
        prev = 1
        while True:
            ret, image = cap.read()
            image = cv2.flip(image, 1)

            result = self.PoseC.detectPose(image)
            image_height, image_width, _ = image.shape
            

            mid_height = image_height // 2
            cv2.line(image, (0, mid_height), (image_width, mid_height), (0, 255, 0), 2)

            if (result.pose_landmarks):
                mid_x, mid_y = self.cal_mid_point(result, image_height, image_width)
                cv2.circle(image, (mid_x, mid_y), radius=8, color=(255, 255, 255), thickness=-1)

                player_act = self.cal_Vertical(mid_y, mid_height)
                if (player_act == -1 and prev != -1):
                    prev = -1
                    pg.press("space")
                if (player_act == 1):
                    prev = 1
            cv2.imshow("flappy", image)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break

        cap.release()
        cv2.destroyAllWindows()

            

Game = flappy()
Game.play()
