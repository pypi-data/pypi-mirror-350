import json
import re

class DynamyqueObject:
    def __init__(self):
        self.__annotations__ = {}
class Config:

    def __init__(self,fileName):
        self.fileName = fileName
        self.extensions = self.findGoodExtensions()

        match self.extensions :
            case "json":
                self.data = self.getEnvDataFromJson()
            case "env" :
                self.data = self.getEnvFromDotEnv()
            case _ :
                self.data = {}
        self.setAttribute(self, self.data)

    def setAttribute(self,obj, data):
        for key, value in data.items():
            if isinstance(value, dict):
                sub_object = DynamyqueObject()
                setattr(obj, key, sub_object)
                self.setAttribute(sub_object, value)
            else:
                setattr(obj, key, value)

    def getEnvDataFromJson(self):
        with open(self.fileName, 'r') as f:
            return json.loads(f.read())

    def findGoodExtensions(self):
        extensions = re.findall(r"\.[a-zA-Z]+$", self.fileName)[0].split(".")[1]
        match extensions:
            case "env":
                return "env"
            case "json":
                return "json"
            case "yaml":
                return "yaml"
            case _:
                return False

    def getEnvFromDotEnv(self):
        dico = {}
        with open(self.fileName, "r") as f:
            data = f.readlines()
            cleanData = [line.replace("\n", "") for line in data]
            for line in cleanData:
                if re.match(r"^\s*#", line):
                    continue
                match = re.match(r"^\.?([a-zA-Z0-9_.-]+)=(.+)$", line)
                if match:
                    dico[match.group(1)] = match.group(2)
        return dico