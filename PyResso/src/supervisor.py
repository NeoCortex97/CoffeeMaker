import os
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

hasTakenImage = False
startingTime = -1
waitingTime = 1000
destinationTimes = []
recognitionStartingTime = -1
recognitionTime = 2000
recognitionDestinationTime = -1
smileStartingTime = -1
smilingTime = 10000
smileDestinationTime = -1
smileGoalReached = False
hasTakenNeutralImage = False
neutral_mouth = 0
hasToTakePhotos = False
enableSmileDetection = True


def manageStream(b):
    # start the video stream thread
    conf = Manager()
    conf.load()
    vs = 0
    if b:
        print("[INFO] starting video stream thread...")
        # vs = VideoStream(src=args["webcam"]).start()
        vs = VideoStream(int(conf.get("CAMERA:device"))).start()
        time.sleep(1.0)
        return vs
    else:
        if not vs == 0:
            vs.stop()
            return True

vs = manageStream(True)


def takePhoto(path, frame, time):
    global hasTakenNeutralImage
    # global neutral_mouth
    conf = Manager()
    conf.load()
    if time == 0:
        cv2.imwrite(conf.get("PATHS:data") + "examples/current0.png", frame)
    elif time == 1:
        cv2.imwrite(conf.get("PATHS:data") + "examples/neutral0.png", frame)
        neutral_mouth = analyzePic(conf.get("PATHS:data") + "/examples/neutral0.png")
        hasTakenNeutralImage = True
    else:
        cv2.imwrite(path + str(time) + ".png", frame)
        print(path + str(time) + ".png created")


def takePhotos(path, frame):
    global startingTime, destinationTimes, waitingTime
    global hasToTakePhotos
    if startingTime == -1:
        startingTime = int(round(time.time() * 1000))
        for i in range(5):
            destinationTimes.append((waitingTime * i) + startingTime)

    currentTime = int(round(time.time() * 1000))
    if len(destinationTimes) > 0:
        if destinationTimes[0] - currentTime <= 0 < destinationTimes[0]:
            takePhoto(path, frame, destinationTimes[0])
            destinationTimes.pop(0)

    else:
        hasToTakePhotos = False
        startingTime = -1
        conf = Manager()
        conf.load()

        print("PATH: " + path)
        register_new(path, conf.get("FILES:pickle"))


def main():
    conf = Manager()
    conf.load()
    global hasToTakePhotos
    global recognitionStartingTime
    global recognitionDestinationTime
    global recognitionTime
    global smileStartingTime
    global smileDestinationTime
    global smilingTime
    global smileGoalReached

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()

    while True:
        currentTime = int(round(time.time() * 1000))
        frame = vs.read()
        frame = resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        predictor = dlib.shape_predictor(conf.get("FILES:landmarks"))
        rects = detector(gray, 0)

        if len(rects) > 0:
            shape = predictor(gray, rects[0])
            if hasToTakePhotos:
                takePhotos(user_path, frame)
            else:
                takePhoto(conf.get("PATHS:data") + "exampes/current0.png", frame, 0)
                recognizedFaces = recognize_face(conf.get("PATHS:data") + "/examples/current0.png")
                if recognizedFaces is not None:
                    if not hasTakenNeutralImage:
                        takePhoto(conf.get("PATHS:data") + "/exaples/neutral0.png", frame, 1)
                    first_name = recognizedFaces.split(" ")[0]
                    print("Hello " + first_name + "!")
                    recognitionDestinationTime = -1
                    recognitionStartingTime = -1

                    if enableSmileDetection:
                        if smileStartingTime == -1 and not smileGoalReached:
                            smileStartingTime = currentTime
                            smileDestinationTime = smileStartingTime + smilingTime
                        else:
                            if detectIsSmiling(shape, frame, neutral_mouth):
                                if smileDestinationTime - currentTime:
                                    smileGoalReached = True
                            else:
                                smileStartingTime = -1
                                smileDestinationTime = -1

                        if smileGoalReached:
                            break

                else:
                    smileGoalReached = False
                    smileDestinationTime = -1
                    smileStartingTime = -1
                    if recognitionStartingTime == -1:
                        recognitionStartingTime = currentTime
                        recognitionDestinationTime = recognitionStartingTime + recognitionTime
                    else:
                        if recognitionDestinationTime > -1 and recognitionDestinationTime - currentTime:
                            print("Hello! I seem to not know you!")
                            namesplit = enterName()
                            # user_path = createDir(conf.get("PATHS:dataset") + "/" + namesplit[0] + " " + namesplit[1])
                            user_path = Path(conf.get("PAHTS:dataset") + "/" + namesplit[0] + " " + namesplit[1]).mkdir(parents=False, exist_ok=True).absolute
                            # user_path = user_path + os.path.sep
                            hasToTakePhotos = True
                            recognitionDestinationTime = -1
                            recognitionStartingTime = -1
                        else:
                            print("...")

        if conf.getBool("DEFAULT:displayframes"):
            for rect in rects:
                cv2.imshow("Frame", frame)

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
    if choice == 1:
        final_choice = "FA:04\n"
    elif choice == 2:
        final_choice = "FA:03\n"
    else:
        final_choice = "FA:08\n"
    WireDriver().send(final_choice)


# Propper entrypoint.
# Otherwise this could blow up if the code would be used as a library.
if __name__ == "__main__":
    main()
