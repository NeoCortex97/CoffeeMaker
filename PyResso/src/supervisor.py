import time
import cv2
import dlib
from imutils import resize
from pathlib import Path
from imutils.video import VideoStream
from src.Communication.wiredriver import WireDriver
from src.create_new import register_new
from src.recognize_faces_image import recognize_face
from src.smile_detection import analyzePic
from src.smile_detection import detectIsSmiling
from src.Config.manager import Manager
from src.util.interaction import makeChoice, chooseStrength, enterName

class Supervisor:
    def __init__(self):
        self.conf = Manager()
        self.conf.load()

        self.hasTakenImage = False
        self.startingTime = -1
        self.waitingTime = 1000
        self.destinationTimes = list()
        self.recognitionStartingTime = -1
        self.recognitionTime = 2000
        self.recognitionDestinationTime = -1
        self.smileStartingTime = -1
        self.smilingTime = 1000
        self.smileDestinationTime = -1
        self.smileGoalReached = False
        self.hasTakenNeutralImage = False
        self.neutral_mouth = None
        self.hasToTakePhotos = False
        self.enableSmileDetection = True
        self.vs = VideoStream(int(self.conf.get("CAMERA:device")))


    def manageStream(self, b):
        # start the video stream thread
        if b:
            print("[INFO] starting video stream thread...")
            # vs = VideoStream(src=args["webcam"]).start()
            self.vs.start()
            # time.sleep(1.0)
        else:
            self.vs.stop()

    def takePhoto(self, path, frame, time):
        # global neutral_mouth
        if time == 0:
            cv2.imwrite(self.conf.get("PATHS:data") + "examples/current0.png", frame)
        elif time == 1:
            cv2.imwrite(self.conf.get("PATHS:data") + "examples/neutral0.png", frame)
            self.neutral_mouth = analyzePic(self.conf.get("PATHS:data") + "/examples/neutral0.png")
            self.hasTakenNeutralImage = True
        else:
            cv2.imwrite(path + str(time) + ".png", frame)
            print(path + str(time) + ".png created")

    def takePhotos(self, path, frame):
        if self.startingTime == -1:
            self.startingTime = int(round(time.time() * 1000))
            self.destinationTimes = [self.startingTime + (self.waitingTime * i) for i in range(5)]
            # for i in range(5):
            #     self.destinationTimes.append((self.waitingTime * i) + self.startingTime)

        currentTime = int(round(time.time() * 1000))
        if len(self.destinationTimes) > 0:
            if self.destinationTimes[0] - currentTime <= 0 < self.destinationTimes[0]:
                self.takePhoto(path, frame, self.destinationTimes[0])
                self.destinationTimes.pop(0)

        else:
            self.hasToTakePhotos = False
            self.startingTime = -1

            print("PATH: " + path)
            register_new(path, self.conf.get("FILES:pickle"))

    def mainLoop(self):
        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()

        while True:
            currentTime = int(round(time.time() * 1000))
            frame = self.vs.read()
            frame = resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            predictor = dlib.shape_predictor(self.conf.get("FILES:landmarks"))
            rects = detector(gray, 0)

            if len(rects) > 0:
                shape = predictor(gray, rects[0])
                if self.hasToTakePhotos:
                    self.takePhotos(user_path, frame)
                else:
                    self.takePhoto(self.conf.get("PATHS:data") + "exampes/current0.png", frame, 0)
                    recognizedFaces = recognize_face(self.conf.get("PATHS:data") + "/examples/current0.png")
                    if recognizedFaces is not None:
                        if not self.hasTakenNeutralImage:
                            self.takePhoto(self.conf.get("PATHS:data") + "/exaples/neutral0.png", frame, 1)
                        first_name = recognizedFaces.split(" ")[0]
                        print("Hello " + first_name + "!")
                        self.recognitionDestinationTime = -1
                        self.recognitionStartingTime = -1

                        if self.enableSmileDetection:
                            smileGoalReached = False
                            if self.smileStartingTime == -1 and not self.smileGoalReached:
                                self.smileStartingTime = currentTime
                                self.smileDestinationTime = self.smileStartingTime + self.smilingTime
                            else:
                                if detectIsSmiling(shape, frame, self.neutral_mouth):
                                    if self.smileDestinationTime - currentTime:
                                        smileGoalReached = True
                                else:
                                    self.smileStartingTime = -1
                                    self.smileDestinationTime = -1

                            if smileGoalReached:
                                break

                    else:
                        self.smileGoalReached = False
                        self.smileDestinationTime = -1
                        self.smileStartingTime = -1
                        if self.recognitionStartingTime == -1:
                            self.recognitionStartingTime = currentTime
                            self.recognitionDestinationTime = self.recognitionStartingTime + self.recognitionTime
                        else:
                            if self.recognitionDestinationTime > -1 and self.recognitionDestinationTime - currentTime:
                                print("Hello! I seem to not know you!")
                                name = enterName()
                                # user_path = createDir(conf.get("PATHS:dataset") + "/" + namesplit[0] + " " + namesplit[1])
                                user_path = Path(self.conf.get("PAHTS:dataset") + "/" + name).mkdir(parents=False, exist_ok=True).absolute
                                # user_path = user_path + os.path.sep
                                self.hasToTakePhotos = True
                                self.recognitionDestinationTime = -1
                                self.recognitionStartingTime = -1
                            else:
                                print("...")

            if self.conf.getBool("DEFAULT:displayframes"):
                # for rect in rects:
                #     cv2.imshow("Frame", frame)
                pass

            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        choice = makeChoice()
        if choice != 3:
            strength = chooseStrength()
        else:
            strength = 0

        print("You ordered %s in strength %s" % (choice, strength))
        WireDriver().send(["FA:04\n", "FA:03\n", "FA:08\n"][choice - 1])


# Propper entrypoint.
# Otherwise this could blow up if the code would be used as a library.
if __name__ == "__main__":
    sup = Supervisor()
    sup.mainLoop()
