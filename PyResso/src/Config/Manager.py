from configparser import ConfigParser, ExtendedInterpolation

class Manager:
    def __init__(self, path=""):
        self.configpath = path
        self.config = ConfigParser(interpolation=ExtendedInterpolation())

    def load(self):
        self.config.read(self.configpath)
        if len(self.config.sections()) > 0:
            pass
        else:
            secs = ["PATHS", "FILES", "DATABASE", "TABLES", "MESSAGES"]

            # {"section": "", "text": ""}
            comments = [{"section": "DATABASE", "text": "# The url key is the location of the database."},
                        {"section": "DATABASE", "text": "# The user key is the username used to access the database."},
                        {"section": "DATABASE", "text": "# The password key is the password used to access the database."},
                        {"section": "MESSAGES", "text": "# The coffe key is the string you have to send to the coffemachine to get a normal coffe."},
                        {"section": "MESSAGES", "text": "# The espresso key is the string you have to send to get an espresso."},
                        {"section": "MESSAGES", "text": "# The water key is the string you have to send to get tea water."},
                        {"section": "DEFAULT", "text": "# The camera key is represents the enumeration of the Camera."},
                        {"section": "DEFAULT", "text": "# The displayFrames key is a boolean to determine if the camera images will be shown."},
                        {"section": "TABLES", "text": "# The user key is the name of the table containing user data."},
                        {"section": "TABLES", "text": "# The prices key is the name of the table containing pricing information."},
                        {"section": "TABLES", "text": "# The billing key is the name of the table containing the billing information."},
                        {"section": "PATHS", "text": "# The base key is the base path of the project."},
                        {"section": "PATHS", "text": "# The config key is the path to the configuration files."},
                        {"section": "PATHS", "text": "# The data key is the path to the data directory"},
                        {"section": "PATHS", "text": "# The dataset key is the path to the dataset directory."},
                        {"section": "FILES", "text": "# The pickle key is the path to the pickle file."},
                        {"section": "FILES", "text": "# The landmarks key is the path to the landmarks.dat file."}]

            # {"section": "", "key": "", "value": ""}
            opts = [{"section": "DATABASE", "key": "url", "value": "127.0.0.1"},
                    {"section": "DATABASE", "key": "user", "value": "default"},
                    {"section": "DATABASE", "key": "password", "value":"default"},
                    {"section": "MESSAGES", "key": "coffee", "value": "FA:04\n"},
                    {"section": "MESSAGES", "key": "espresso", "value": "FA:03\n"},
                    {"section": "MESSAGES", "key": "water", "value": "FA:08\n"},
                    {"section": "DEFAULT", "key": "camera", "value": "0"},
                    {"section": "DEFAULT", "key": "displayFrames", "value": "false"},
                    {"section": "TABLES", "key": "user", "value": "Users"},
                    {"section": "TABLES", "key": "prices", "value": "Prices"},
                    {"section": "TABLES", "key": "billing", "value": "Billing"},
                    {"section": "PATHS", "key": "base", "value": "~/CoffeMaker/PyResso"},
                    {"section": "PATHS", "key": "config", "value": "${base}/configuration"},
                    {"section": "PATHS", "key": "data", "value": "${base}/data"},
                    {"section": "PATHS", "key": "dataset", "value": "${data}/dataset"},
                    {"section": "FILES", "key": "pickle", "value": "${PATHS:data}/encodings.pickle"},
                    {"section": "FILES", "key": "landmarks", "value": "${PATHS:data}/shape_predictor_68_face_landmarks.dat"}]

            for sec in secs:
                self.config.add_section(sec)

            for opt, com in zip(opts, comments):
                #self.config.set(com["section"], com["text"])
                self.config.set(opt["section"], opt["key"], opt["value"])


            with open(self.config.get("PATHS", "config") + "/Template.conf", "w") as file:
                self.config.write(file)

