
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import tempfile
import sys
import os, json
import shutil, wget
from util.DateUtils import DateUtils
import csv

class FileUtil :

    def __init__(
        self
    ) -> None:
        self._init_config()

    def _init_config(self):
        load_dotenv()
        self.counter = 0
        self.timestampString = ""
        self.fileRootFolder = ""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self.TEMP_FOLDER = os.environ.get('TEMP_FOLDER', '')

    def writeInFile(self, fileName, fileText):
        file = open(fileName,"w")
        file.write(fileText)
        file.close()
        return None
    
    def start(self):
        self.counter = 0
        ### Interim files
        WRITE_INTERIM_FILES = os.environ.get('WRITE_INTERIM_FILES', 'FALSE').upper()
        if WRITE_INTERIM_FILES == "FALSE":
            self.write_interim_files = False
            print("The string is 'FALSE'")
        else:
            self.write_interim_files = True
            print("The string is not 'FALSE'")

        self.timestampString = DateUtils.getCurrentDateTimeString()

        temp_folder = tempfile.gettempdir()

        filePath = os.environ.get('OUTPUT_FOLDER', temp_folder)
        filePath = os.path.join(filePath, "results-" + self.timestampString)
        self.logger.info("Output folder : %s " % filePath)

        ### Create folder
        try:
            os.makedirs(filePath)
            self.logger.info("Folder %s created!" % filePath)
            self.fileRootFolder = filePath
        except Exception as e:
            self.logger.error(f' Error in creating folder : {e} ')

    def writeInFileWithCounter(self, fileName, fileText):
        if (self.write_interim_files == True) :
            fileNameWithPath = self.getFileNameWithCounter(fileName)
            self.writeInFile(fileNameWithPath, fileText)
        return None

    def getFileName(self, fileNamePrefix, fileName):
        fileNameWithPath = os.path.join(self.fileRootFolder, fileNamePrefix + fileName)
        self.logger.debug("fileNameWithPath :" + fileNameWithPath)
        return fileNameWithPath

    def getFileNameWithCounter(self, fileName):
        self.counter = self.counter + 1    
        fileNamePrefix = str(self.counter).zfill(4) + "-"
        return self.getFileName (fileNamePrefix, fileName)

    def getFileNameWithoutCounter(self, fileName):
        return self.getFileName ("", fileName)

    @staticmethod
    def extractFilename(filepath):
        return os.path.basename(filepath)

    def loadJsonFileContent(self, fileName):
        self.logger.info("loadJsonFileContent  ... :  " + fileName)
        data = {}
        try:
            with open(fileName, "r") as json_file:
                data = json.load(json_file)
                self.logger.debug(data)
        except FileNotFoundError:
            self.logger.error(f"The file '{fileName}' does not exist.")
        except json.JSONDecodeError:
            self.logger.error(f"The file '{fileName}' is not valid JSON.")

        return data
    
    def split_filename_and_extension(self, file_name):
        # Split the file name into root (name without extension) and extension
        root, extension = os.path.splitext(file_name)
        return root, extension
    

    def copy_file(self, file_mname) :
        shutil.copy(file_mname, self.fileRootFolder)

    def download_file(self, file_url):
        self.logger.info("download_file  ... URL :  " + file_url)

        ### Extract file name from file_url
        file_name = FileUtil.extractFilename(file_url)

        ### Generate the name for the temporary local file
        file_name_with_path = self.TEMP_FOLDER + "/" + file_name

        self.logger.debug(f"file_url : {file_url} ")
        self.logger.debug(f"file_name : {file_name} ")
        self.logger.debug(f"file_name_with_path : {file_name_with_path} ")

        ### Download file from the url
        if not os.path.isfile(file_name_with_path):
            wget.download(file_url, out=file_name_with_path)

        self.logger.info("download_file  ... FileName :  " + file_name_with_path)
        return file_name_with_path
    
    @staticmethod
    def csv_to_json(csv_file):
        data = []

        # Read CSV file
        with open(csv_file, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)  # Read as dictionary
            for row in csv_reader:
                data.append(row)

        return json.dumps(data, indent=4)  # Return JSON as a string

    @staticmethod
    def loadJsonAsObject(fileName):
        data = {}
        try:
            with open(fileName, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print(f"The file '{fileName}' does not exist.")
        except json.JSONDecodeError:
            print(f"The file '{fileName}' is not valid JSON.")

        return data        