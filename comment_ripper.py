import argparse
import os
import json
from abc import ABC, abstractmethod
from jsonschema import exceptions
from jsonschema import validate

#
#   Class Name:		LanguageConfig
#   Description:	The main objective of this class is to provide information regarding the configuration to be
#                   followed by the parser
#


class LanguageConfig:
    # LanguageConfig constructor
    # Input:
    #   json - json data that was previously parsed with the json library, it represents a single language
    # Output:
    #   N/A
    def __init__(self, json_obj):
        self.__name = None
        self.__single_line = []
        self.__multi_line_start = ""
        self.__multi_line_end = ""
        self.__position = []
        self.__extensions = []

        self.__name = json_obj["language"]
        if 'single-line' in json_obj:
            self.__single_line = json_obj["single-line"]

        if 'multi-line-start' in json_obj and 'multi-line-end' in json_obj:
            self.__multi_line_start = json_obj["multi-line-start"]
            self.__multi_line_end = json_obj["multi-line-end"]

        if 'position' in json_obj:
            self.__position = json_obj["position"]

        if 'extensions' in json_obj:
            self.__extensions = json_obj["extensions"]

    # get_type function
    # Description:
    #   Function to return a string that identifies the type
    # Input:
    #   N/A
    # Output:
    #   string with type name
    @staticmethod
    def get_type():
        return "LanguageConfig"

    # to_string function
    # Description:
    #   Function to return a string representation of the object
    # Input:
    #   N/A
    # Output:
    #   stringConcat - variable with the concatenation of all internal variables
    def to_string(self):
        string_concat = "Name: {}\n".format(self.__name)

        if len(self.__single_line) > 0:
            string_concat += "Single Line:\n"
            for sl in self.__single_line:
                string_concat += "\t {}\n".format(sl)

        string_concat += "Multi Line: Start: {} - End: {}\n".format(self.__multi_line_start, self.__multi_line_end)

        if len(self.__extensions) > 0:
            string_concat += "Extensions:\n"
            for e in self.__extensions:
                string_concat += "\t {}\n".format(e)

        return string_concat

    # get_extensions function
    # Description:
    #   Function that returns the list of extensions that were set
    # Input:
    #   N/A
    # Output:
    #   List with all extensions set for this language
    def get_extensions(self):
        return self.__extensions

    # get_name function
    # Description:
    #   Function that returns the name of the language that is represented in this object
    # Input:
    #   N/A
    # Output:
    #   String representing the name of the language
    def get_name(self):
        return self.__name

    # get_single_line function
    # Description:
    #   Function that returns a list of all single line comments starting strings
    # Input:
    #   N/A
    # Output:
    #   List containing strings with start string of single line comments
    def get_single_line(self):
        return self.__single_line

    # has_single_line function
    # Description:
    #   Function that return True if the language has single line comments
    # Input:
    #   N/A
    # Output:
    #   Boolean indicating whether if the language has single line comments in the configurations
    def has_single_line(self):
        return len(self.__single_line) > 0

    # get_multiline_start function
    # Description:
    #   Function that return a string list with all strings that can start a multi line comment
    # Input:
    #   N/A
    # Output:
    #   String of strings that starts a multi line comment
    def get_multiline_start(self):
        return self.__multi_line_start

    # get_multiline_end function
    # Description:
    #   Function that return a string list with all strings that can end a multi line comment
    # Input:
    #   N/A
    # Output:
    #   List of strings that ends a multi line comment
    def get_multiline_end(self):
        return self.__multi_line_end

    # has_multiline function
    # Description:
    #   Function that return True if the language has multi line comments
    # Input:
    #   N/A
    # Output:
    #   Boolean indicating whether if the language has multi line comments in the configurations
    def has_multiline(self):
        return len(self.__multi_line_start) > 0

    # get_position function
    # Description:
    #   Function that return a object list with all characteristics that must have a comment like character position
    # Input:
    #   N/A
    # Output:
    #   List of objects with all characteristics that must have a comment like character position
    def get_position(self):
        return self.__position

    # has_position function
    # Description:
    #   Function that return True if the language has positional conditions to be read
    # Input:
    #   N/A
    # Output:
    #   Boolean indicating whether if the language has positional configurations
    def has_position(self):
        return len(self.__position) > 0


#
#   Class Name:		ConfigFile
#   Description:    This class consolidate all static functions to provide access and logic for the configuration file,
#                   so far it works only with JSON files
#
class ConfigFile:
    __path = os.getcwd() + os.sep + "config.json"
    __schema_path = os.getcwd() + os.sep + "comment_ripper_schema.json"

    # get_language_list static function
    # Description:
    #   Static function to return all available languages in the configuration file
    # Input:
    #   N/A
    # Output:
    #   language_names - list containing all available languages in the configuration file
    @staticmethod
    def get_language_list():
        language_names = []

        with open(ConfigFile.__path) as data_file:
            data = json.load(data_file)
        data_file.close()

        if data is not None:
            for language in data["languages"]:
                language_names.append(language["language"])

        return language_names

    # get_language_config static function
    # Description:
    #   Static function that search and return a LanguageConfig object required by the parser
    # Input:
    #   searched_language - string representing the name of the language to be used in the parser
    # Output:
    #   LanguageConfig - returns a LanguageConfig object containing al required information to parse comments. It
    #   returns None in case the language doesn't exist
    @staticmethod
    def get_language_config(searched_language):
        with open(ConfigFile.__path) as data_file:
            data = json.load(data_file)
        data_file.close()

        if data is not None:
            for language in data["languages"]:
                if language["language"] == searched_language:
                    return LanguageConfig(language)

        return None

    # validate_config_file static function
    # Description:
    #   Static function that validates if the configuration file has the corresponding format using the JSON Schema
    #   file.
    # Input:
    #   N/A
    # Output:
    #   N/A - It returns an exception in case something was found.
    @staticmethod
    def validate_config_file():
        config_file = File(ConfigFile.__path)
        config_file.open_for_read()
        schema_file = File(ConfigFile.__schema_path)
        schema_file.open_for_read()
        validate(json.load(config_file.get_file()), json.load(schema_file.get_file()))

    # get_type function
    # Description:
    #   Function to return a string that identifies the type
    # Input:
    #   N/A
    # Output:
    #   string with type name
    @staticmethod
    def get_type():
        return "ConfigFile"

#
#   Class Name:		FileAction
#   Description:	This is an abstract class to implement all classes that are capable of doing some action to a
#   single file
#


class FileAction(ABC):
    # Start function
    # Description:
    #   Abstract method to start an action to a file
    # Input:
    #   file - File object that represents the file into which an action will take place
    # Output:
    #   N/A
    @abstractmethod
    def start(self, file):
        raise NotImplementedError('subclasses must override Start()')


#
#   Class Name:		CommentParser
#   Description:	Abstract class for comment parsers
#
class CommentParser(ABC):
    # CommentParser abstract constructor
    # Input:
    #   language_config - LanguageConfig object with the configurations required to parse comments from a line
    # Output:
    #   N/A
    def __init__(self, language_config):
        self.__language_config = language_config

    # get_language_config function
    # Description:
    #   Method to return the configuration language object that was used to configured the comment parser
    # Input:
    #   N/A
    # Output:
    #   Language configuration object
    def get_language_config(self):
        return self.__language_config

    # Parse function
    # Description:
    #   Abstract method to start parsing a file
    # Input:
    #   line - String to be analysed
    # Output:
    #   N/A
    @abstractmethod
    def parse(self, line):
        raise Exception("subclasses must override Parse() method")


#
#   Class Name: 	LineCommentParser
#   Description:	Class to extract comments both single line and multi line
#
class LineCommentParser(CommentParser):
    # Private attribute shared by all instances off MultiLineCommentParser class
    __current_status = 0
    # Private attribute with the line that needs to be returned
    __return_line = ""

    #
    #   Class Name: 	Token
    #   Description:	Class that represents a token in the line
    #
    class Token:
        # Token constructor
        # Input:
        #   token_type - It can be a number or a string with the representation of the token
        #   token_text - It's the text that represents the token
        # Output:
        #   N/A
        def __init__(self, token_type, token_text):
            self.__tokenType = token_type
            self.__tokenText = token_text

        # get_token_type function
        # Decryption:
        #   Method that returns the type of token
        # Input:
        #   N/A
        # Output:
        #   String/Int - token type
        def get_token_type(self):
            return self.__tokenType

        # get_token_text function
        # Decryption:
        #   Method that returns the text of token
        # Input:
        #   N/A
        # Output:
        #   String - token text
        def get_token_text(self):
            return self.__tokenText

    # __copy_text function
    # Decryption:
    #   Method that copy the text extracted from the line of code that is not a comment
    # Input:
    #   text - String that needs to be saved and returned later
    # Output:
    #   N/A
    def __copy_text(self, text):
        # Replace the string &#59 to ";" to obtain the original text
        text = text.replace("&#59", ";")
        self.__return_line += text

    # LineCommentParser constructor
    # Input:
    #   language_config - LanguageConfig object with the configurations required to parse comments from a line
    # Output:
    #   N/A
    def __init__(self, language_config):
        super(LineCommentParser, self).__init__(language_config)
        self.__token_list = []

        # This is the state machine matrix with the status changes depending on the previous status and the token that
        # was found
        #               Other		S		E       SL      EOL
        self.__status = [
                        [0,         1,      -1,     2,      -2],  # I(0)
                        [1,         1,       0,     1,      -2],
                        [2,         2,       2,     2,       0]
                        ]

        # This is the matrix with the function to be called when transitioning from one status to the next
        self.__status_functions = [
                                  [self.__copy_text,    None,   None,   None,   None],
                                  [None,                None,   None,   None,   None],
                                  [None,                None,   None,   None,   None]
                                  ]

        # If we found that the language has single line comments then load the token to be searched
        if language_config.has_single_line():
            for sl in language_config.get_single_line():
                if language_config.has_position():
                    position = language_config.get_position()[0]["column"] - 1
                    self.__token_list.append(LineCommentParser.Token(token_type=";SL;",
                                                                     token_text=(" " * position) + sl))
                else:
                    self.__token_list.append(LineCommentParser.Token(token_type=";SL;",
                                                                     token_text=sl))

        # If we found that the language has multi line comments then load the token to be searched
        if language_config.has_multiline():
            self.__token_list.append(LineCommentParser.Token(";S;", language_config.get_multiline_start()))
            self.__token_list.append(LineCommentParser.Token(";E;", language_config.get_multiline_end()))

    # __tokenize function
    # Decryption:
    #   Method that gets a line of code and return the line divided by ";" separating each token
    # Input:
    #   line - String to be analysed
    # Output:
    #   List<Token> - List of all tokens that were found in the line of code.
    def __tokenize(self, line):
        # This loop ends when the end of line is found (EOL)
        while True:
            min_a = len(line)
            min_token = None
            for t in self.__token_list:
                min_aux = line.find(t.get_token_text())
                if min_aux < min_a and min_aux != -1:
                    min_a = min_aux
                    min_token = t

            if min_token is None:  # No token found
                break
            else:
                # Replace the token with the corresponding comma separated token type ex. ";S;"
                line = line.replace(min_token.get_token_text(), min_token.get_token_type(), 1)

        # Convert the string into a token list using the Token class
        tokens = []
        for t in line.split(";"):
            if t == "SL":
                tokens.append(LineCommentParser.Token(3, t))
            elif t == "S":
                tokens.append(LineCommentParser.Token(1, t))
            elif t == "E":
                tokens.append(LineCommentParser.Token(2, t))
            else:
                tokens.append(LineCommentParser.Token(0, t))

        tokens.append(LineCommentParser.Token(4, None))  # Add  EOL
        return tokens

    # Parse function
    # Decryption:
    #   Method to start parsing a file
    # Input:
    #   line - String to be analysed
    # Output:
    #   N/A
    def parse(self, line):
        # Load previous status
        status = LineCommentParser.__current_status

        # For each token found in the line of code change to the next status and execute if required a function
        for token in self.__tokenize(line):
            status = self.__status[status][token.get_token_type()]

            if status == -1:  # ERROR
                raise Exception("Comment parse error on line '{}'".format(line))

            if status == -2:  # EOL
                if self.__return_line[-1:] == "\n":
                    # opened, add an EOL
                    result_line = self.__return_line
                else:
                    result_line = self.__return_line + "\n"
                self.__return_line = ""
                return result_line
            else:
                LineCommentParser.__current_status = status
                if self.__status_functions[status][token.get_token_type()] is not None:  # If needed execute function
                    self.__status_functions[status][token.get_token_type()](token.get_token_text())

        # If no EOL present then add it
        if self.__return_line[-1:] == "\n":
            result_line = self.__return_line
        else:
            result_line = self.__return_line + "\n"

        self.__return_line = ""
        return result_line

    # get_type function
    # Description:
    #   Function to return a string that identifies the type
    # Input:
    #   N/A
    # Output:
    #   string with type name
    @staticmethod
    def get_type():
        return "LineCommentParser"


#
#   Class Name:		CommentParserFactory
#   Description:	Factory class with static method to create a comment parser depending on the type of language
#                   configurations
#
class CommentParserFactory:
    # create_comment_parser static function
    # Description:
    #   Static function to create the corresponding comment parser
    # Input:
    #   language_config - LanguageConfig object with the configuration required to parse the file
    # Output:
    #   it return a list of all available parsers for the language
    @staticmethod
    def create_comment_parser(language_config):
        comment_parsers = [LineCommentParser(language_config)]

        # if language_config.has_position() or language_config.has_single_line():
        #     comment_parsers.append(InLineCommentParser(language_config))

        # if language_config.has_multiline():
        #    comment_parsers.append(MultiLineCommentParser(language_config))

        return comment_parsers

    # get_type function
    # Description:
    #   Function to return a string that identifies the type
    # Input:
    #   N/A
    # Output:
    #   string with type name
    @staticmethod
    def get_type():
        return "CommentParserFactory"


#
#   Class Name:		CommentParserAction
#   Description:	Class based on FileAction that parse comments of a file depending on the language configured
#
class CommentParserAction(FileAction):
    # CommentParserAction constructor
    # Input:
    #   language_config - LanguageConfig object with the configurations required to parse comments from a file
    # Output:
    #   N/A
    def __init__(self, language_config):
        if language_config.get_type() == "LanguageConfig":
            self._language_config = language_config
        else:
            raise Exception("language_config parameter is not from LanguageConfig type")

    # Start function
    # Description:
    #   Abstract method to parse a file and return a string with the result
    # Input:
    #   language_config - LanguageConfig object with the configuration required to parse the file
    #   file - File object that represents the file to be parsed
    # Output:
    #   it must return the text after being parsed and modified
    def start(self, file):
        if file.get_type() == "File":
            content = ""
            parsers_list = CommentParserFactory.create_comment_parser(self._language_config)
            file.open_for_read()

            for line in file.get_file():
                line_aux = line
                for commentParser in parsers_list:
                    line_aux = commentParser.parse(line_aux)
                content += line_aux

            file.close()

            Directory.create_directory(file.get_folder_path() + "output")
            save = File(file.get_folder_path() + "output" + os.sep + file.get_file_name())
            save.open_for_write()
            save.write(content)
            save.close()
        else:
            raise Exception("file parameter is not from File type")

    # get_type function
    # Description:
    #   Function to return a string that identifies the type
    # Input:
    #   N/A
    # Output:
    #   string with type name
    @staticmethod
    def get_type():
        return "CommentParserAction"


#
#   Class Name:		File
#   Description:	The objective of this class is to interact with the OS library, read, move, copy and parse a file.
#                   It loads everything into memory
#
class File:
    # CheckFile static function
    # Description:
    #   Static function that checks if the file exists and that the path is valid for a file
    # Input:
    #   value - string that represents the path
    # Output:
    #   value - returns a string containing the path validated and correctly set. If a criteria was not meet it raises
    #           an exception
    @staticmethod
    def check_file(value):
        value = value.strip()
        if not os.path.exists(value):
            raise argparse.ArgumentTypeError("'%s' is not a valid path" % value)
        elif os.path.isdir(value):
            raise argparse.ArgumentTypeError("'%s' is not a file" % value)

        return value

    # File constructor
    # Input:
    #   path - string witch represents the starting path to read
    # Output:
    #   N/A
    def __init__(self, path):
        self.__path = path
        self.__filename, self.__file_extension = os.path.splitext(self.__path)
        self.__file = None

    def get_folder_path(self):
        result_path = os.path.dirname(self.__path)

        if result_path[-1:] != os.sep:
            result_path = result_path + os.sep

        return result_path

    def get_file_name(self):
        return os.path.basename(self.__path)

    def get_file_extension(self):
        return self.__file_extension

    def open_for_read(self):
        self.close()
        self.__file = open(self.__path, 'r')

    def open_for_write(self):
        self.close()
        self.__file = open(self.__path, 'w')

    def open_for_append(self):
        self.close()
        self.__file = open(self.__path, 'a')

    def open(self):
        self.close()
        self.__file = open(self.__path, 'r+')

    def close(self):
        if self.__file is not None:
            self.__file.close()
            self.__file = None

    def read_line(self):
        if self.__file is None:
            raise Exception("File is closed")
        elif self.can_read():
            raise Exception("File is open but in mode {}".format(self.__file.mode))
        else:
            return self.__file.readline()

    def write(self, value):
        if self.__file is None:
            raise Exception("File is closed")
        elif self.can_write():
            self.__file.write(value)
        else:
            raise Exception("File is open but in mode {}".format(self.__file.mode))

    def can_write(self):
        if self.__file is None:
            return False
        else:
            return self.__file.mode in ["r+", "rb+", "w", "wb", "w+", "wb+", "a", "ab", "a+", "ab+"]

    def can_read(self):
        if self.__file is None:
            return False
        else:
            return self.__file.mode in ["r", "rb", "r+", "rb+", "a+", "ab+"]

    def get_content(self):
        if self.__file is None:
            raise Exception("File is closed")
        elif self.can_read():
            return self.__file.read()
        else:
            raise Exception("File is open but in mode {}".format(self.__file.mode))

    def get_file(self):
        return self.__file

    # get_type function
    # Description:
    #   Function to return a string that identifies the type
    # Input:
    #   N/A
    # Output:
    #   string with type name
    @staticmethod
    def get_type():
        return "File"

    # to_string function
    # Description:
    #   Function to return a string representation of the object
    # Input:
    #   N/A
    # Output:
    #   string_concat - variable with the concatenation of all internal variables
    def to_string(self):
        string_concat = "Path: {}\n".format(self.__path)
        string_concat += "Name: {}\n".format(self.__filename)
        string_concat += "Extension: {}\n".format(self.__file_extension)
        string_concat += "Folder: {}\n".format(os.path.dirname(self.__path))

        return string_concat


#
#   Class Name:		Directory
#   Description:	The objective of this class is to interact with the OS library, read all files, filter the ones
#                   that are searched for and list all sub-directories
#
class Directory:
    # __read_dir function
    # Description:
    #   "Private" function that reads a directory and obtain all files and directories
    # Input:
    #   N/A
    # Output:
    #   N/A
    def __read_dir(self):
        dir_content = os.listdir(self.__path)
        for element in dir_content:
            if os.path.isdir(self.__path + element):
                self.__subdirs.append(self.__path + element)
                self.__subdir_index = 0
            else:
                filename, file_extension = os.path.splitext(self.__path + element)
                if file_extension in self.__include_extensions:
                    self.__files.append(self.__path + element)
                    self.__file_index = 0

    # Directory constructor
    # Input:
    #   path - string witch represents the starting path to read
    # Output:
    #   N/A
    def __init__(self, path):
        self.__subdirs = []
        self.__files = []
        self.__include_extensions = []
        self.__path = Directory.check_directory(path)
        self.__subdir_index = None
        self.__file_index = None
        self.__pre_process_function = None
        self.__process_function = None
        self.__post_process_function = None

        # set_include_subdir function
    # Description:
    #   Function to set the list of extensions to be read
    # Input:
    #   extensions - list
    # Output:
    #   N/A
    def set_include_extensions_list(self, extensions):
        self.__include_extensions = extensions

        for i in range(len(self.__include_extensions)):
            self.__include_extensions[i] = self.__include_extensions[i].replace(" ", "")
            self.__include_extensions[i] = self.__include_extensions[i].replace("*", "")

    # get_include_extensions_list function
    # Description:
    #   Function to obtain the list of extensions that were set
    # Input:
    #   N/A
    # Output:
    #   List containing all extensions set to the directory object
    def get_include_extensions_list(self):
        return self.__include_extensions

    # get_include_extensions function
    # Description:
    #   Function that gets the extensions as a String separted by ";"
    # Input:
    #   N/A
    # Output:
    #   String with all accepted extensions
    def get_include_extensions(self):
        extensions = ""

        for ext in self.__include_extensions:
            extensions = extensions + ext + ";"

        return extensions[:-1]

    # set_include_extensions function
    # Description:
    #   Function that sets the extensions from a String "value" into the list of accepted extensions
    # Input:
    #   value - String with the accepted extensions separated by ";"
    # Output:
    #   N/A
    def set_include_extensions(self, value):
        if len(value.strip()) > 0:
            value = value.replace(" ", "")
            value = value.replace("*", "")

            if len(value.split(";")) > 0:
                self.__include_extensions = value.split(";")
            else:
                self.__include_extensions = []
        else:
            self.__include_extensions = []

    # get_path function
    # Description:
    #   Function that return the path set when the Directory object was constructed
    # Input:
    #   N/A
    # Output:
    #   String representing the starting path of this object
    def get_path(self):
        return self.__path

    # get_subdirs function
    # Description:
    #   Function that return all subdirectories listed withing the directory set on path
    # Input:
    #   N/A
    # Output:
    #   List of subdirectory paths
    def get_subdirs(self):
        return self.__subdirs

    #################################################################################
    #                   Section for subdirectoryloop helpers						#
    #################################################################################

    # get_subdirectory function
    # Description:
    #   Function that return a Directory object from the subdirectory on index
    # Input:
    #   index - integer with the index withing the sub directory list. If the index is out of range it returns None
    # Output:
    #   Directory object of the subdirectory.
    def get_subdirectory(self, index):
        if 0 <= index < len(self.__subdirs):
            dir_obj = Directory(self.__subdirs[index])
            dir_obj.set_include_extensions_list(self.__include_extensions)
            dir_obj.read()

            return dir_obj
        else:
            return None

    # subdirectory_count function
    # Description:
    #   Function that return the number of sub directories included in the current folder
    # Input:
    #   N/A
    # Output:
    #   Integer that represents the count of sub folders
    def subdirectory_count(self):
        return len(self.__subdirs)

    # is_first_subdirectory function
    # Description:
    #   Function that indicates whether the pointer is set to the first subfolder
    # Input:
    #   N/A
    # Output:
    #   Boolean, True if is the first subfolder and False if is not
    def is_first_subdirectory(self):
        if self.__subdir_index is None:
            return False
        elif self.__subdir_index == 0:
            return True
        else:
            return False

    # is_last_subdirectory function
    # Description:
    #   Function that indicates whether the pointer is set to the last sub folder
    # Input:
    #   N/A
    # Output:
    #   Boolean, True if is the last sub folder and False if is not
    def is_last_subdirectory(self):
        if self.__subdir_index is None:
            return True
        elif self.__subdir_index < len(self.__subdirs):
            return False
        else:
            return True

    # next_subdirectory function
    # Description:
    #   Function to move folder pointer to the next position in the list
    # Input:
    #   N/A
    # Output:
    #   Directory object representing the sub folder being read and return
    def next_subdirectory(self):
        if self.is_last_subdirectory() is False:
            dir_obj = self.get_subdirectory(self.__subdir_index)
            self.__subdir_index += 1
            return dir_obj
        else:
            return None

    # restart_subdirectory function
    # Description:
    #   Function to restart sub folder pointer
    # Input:
    #   N/A
    # Output:
    #   N/A
    def restart_subdirectory(self):
        if self.__subdir_index is None:
            self.__subdir_index = None
        else:
            self.__subdir_index = 0

    #################################################################################
    #                   End section for subdirectory loop helpers					#
    #################################################################################

    #################################################################################
    #                   Section for files loop helpers							    #
    #################################################################################

    # get_file function
    # Description:
    #   Function that return a File object from the files on index
    # Input:
    #   index - integer with the index withing the files list. If the index is out of range it returns None
    # Output:
    #   File object of the inner file.
    def get_file(self, index):
        if 0 <= index < len(self.__files):
            file = File(self.__files[index])
            return file
        else:
            return None

    # files_count function
    # Description:
    #   Function that return the number of files included in the current folder
    # Input:
    #   N/A
    # Output:
    #   Integer that represents the count of files
    def files_count(self):
        return len(self.__files)

    # is_first_file function
    # Description:
    #   Function that indicates whether the pointer is set to the first file in the list
    # Input:
    #   N/A
    # Output:
    #   Boolean, True if is the first file and False if is not
    def is_first_file(self):
        if self.__file_index is None:
            return False
        elif self.__file_index == 0:
            return True
        else:
            return False

    # is_last_file function
    # Description:
    #   Function that indicates whether the pointer is set to the last file in the list
    # Input:
    #   N/A
    # Output:
    #   Boolean, True if is the last file and False if is not
    def is_last_file(self):
        if self.__file_index is None:
            return True
        elif self.__file_index < len(self.__files):
            return False
        else:
            return True

    # next_file function
    # Description:
    #   Function to move files pointer to the next position in the list
    # Input:
    #   N/A
    # Output:
    #   File object representing the file being read and return
    def next_file(self):
        if self.is_last_subdirectory() is False:
            file = self.get_file(self.__file_index)
            self.__file_index += 1
            return file
        else:
            return None

    # restart_files function
    # Description:
    #   Function to restart files pointer
    # Input:
    #   N/A
    # Output:
    #   N/A
    def restart_files(self):
        if self.__file_index is None:
            self.__file_index = None
        else:
            self.__file_index = 0

    #################################################################################
    #                       End section for files loop helpers						#
    #################################################################################

    # get_files function
    # Description:
    #   Function that return all files listed with the corresponding extension
    # Input:
    #   N/A
    # Output:
    #   List of files paths
    def get_files(self):
        return self.__files

    # get_type function
    # Description:
    #   Function to return a string that identifies the type
    # Input:
    #   N/A
    # Output:
    #   string with type name
    @staticmethod
    def get_type():
        return "Directory"

    # to_string function
    # Description:
    #   Function to return a string representation of the object
    # Input:
    #   N/A
    # Output:
    #   stringConcat - variable with the concatenation of all internal variables
    def to_string(self):
        string_concat = "Path: {}\n".format(self.__path)

        if len(self.__include_extensions) > 0:
            string_concat += "Extensions:\n"
            for ie in self.__include_extensions:
                string_concat += "\t {}\n".format(ie)

        if len(self.__subdirs) > 0:
            string_concat += "SubDirs:\n"
            for sd in self.__subdirs:
                string_concat += "\t {}\n".format(sd)

        if len(self.__files) > 0:
            string_concat += "Files:\n"
            for f in self.__files:
                string_concat += "\t {}\n".format(f)

        return string_concat

    # read function
    # Description:
    #   Function to load all folders and files locations from the path set at the beginning
    # Input:
    #   N/A
    # Output:
    #   N/A
    def read(self):
        self.__read_dir()

    #################################################################################
    #   Setters and Getters for pre-process, process and post-process functions     #
    #################################################################################

    def set_pre_process_function(self, pre_process_function):
        self.__pre_process_function = pre_process_function

    def set_post_process_function(self, post_process_function):
        self.__post_process_function = post_process_function

    def set_process_function(self, process_function):
        self.__process_function = process_function

    #################################################################################
    #   End Setters and Getters for pre-process, process and post-process functions #
    #################################################################################

    # for_each_file function
    # Description:
    #   Function that loops through out all files and do an action to each file
    # Input:
    #   include_subdir - boolean that indicates if the action performed to all files include sub folder files
    #   file_action - object of parent class FileAction which is the task to be executed to all files in the folder
    # Output:
    #   N/A
    def for_each_file(self, include_subdir, file_action):
        if not isinstance(file_action, FileAction):
            raise Exception("fileAction must be a class base")

        if not isinstance(include_subdir, int):
            raise Exception("includeSubDir must be boolean")

        for file in self.__files:
            file_action.start(File(file))

        if include_subdir is True:
            for dir_obj in self.__subdirs:
                directory = Directory(dir_obj)
                directory.set_include_extensions_list(self.get_include_extensions_list())
                directory.read()
                directory.for_each_file(include_subdir, file_action)

    # check_directory static function
    # Description:
    #   Static function that checks if the directory exists and that the path is valid for a directory, it also
    #   standardized that the last character is an os path separator
    # Input:
    #   value - string that represents the path
    # Output:
    #   value - returns a string containing the path validated and correctly set. If a criteria was not meet it raises
    #           an exception
    @staticmethod
    def check_directory(value):
        value = value.strip()
        if not os.path.exists(value):
            raise argparse.ArgumentTypeError("'%s' is not a valid path" % value)
        elif not os.path.isdir(value):
            raise argparse.ArgumentTypeError("'%s' is not a directory" % value)

        if value[-1:] != os.sep:
            value = value + os.sep

        return value

    # CreateDirectory static function
    # Description:
    #   Static function that checks if the directory exists and if not it creates it
    # Input:
    #   path - string that represents the path
    # Output:
    #   boolean - returns a boolean which if true then it created the directory and if false it exists or couldn't
    #             create it
    @staticmethod
    def create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        else:
            return False


# Main function
# Description:
#   This function is to emulate a C kind of start where all main activities are executed here, including argument
#   parsing, validations, etc.
# Input:
#   N/A
# Output:
#   N/A
# def main():
#     try:
#         # Validate if the configuration file complies with the schema
#         ConfigFile.validate_config_file()
#
#         # Set argument parser object
#         parser = argparse.ArgumentParser(description='Strip comments from files in a folder')
#
#         parser.add_argument('-p', '--path', metavar='PATH',
#                             type=Directory.check_directory,
#                             help='Directory to be read')
#         parser.add_argument('-s', "--subdir", action="store_true",
#                             help='Include sub-directories')
#         parser.add_argument('-l', "--language", action="store",
#                             help='Set the language that is going to be analyse')
#         parser.add_argument('-ll', "--list", action="store_true",
#                             help='List all available languages')
#         parser.add_argument('-v', '--version',
#                             action='version',
#                             version='%(prog)s 0.1')
#
#         # Parse arguments from command prompt
#         args = parser.parse_args()
#
#         # If the user request the list of current languages, ignore all other commands and print list
#         if args.list:
#             print(ConfigFile.get_language_list())
#         elif args.path is None:  # If the path argument is empty, print help text and an error message
#             parser.print_help()
#             raise Exception("Path argument must be set")
#         elif args.language is None:  # If the language argument is empty, print help text and an error message
#             parser.print_help()
#             raise Exception("Language argument must be set")
#         else:  # If all mandatory arguments are present, create a language conf object and set the directory object.
#             language_config = ConfigFile.get_language_config(args.language)
#             if language_config is None:
#                 raise Exception("'%s' is not a valid language" % args.language)
#
#             dir_obj = Directory(args.path)
#             dir_obj.set_include_extensions_list(language_config.get_extensions())
#             dir_obj.read()
#
#             parser = CommentParserAction(language_config)
#             dir_obj.for_each_file(args.subdir, parser)
#
#     except exceptions.ValidationError as valEx:
#         exception_string = "Configuration File Error: {}\n".format(valEx.message)
#         for i in range(0, len(valEx.absolute_path)):
#             if (i % 2) == 0:
#                 exception_string += valEx.absolute_path[i] + "["
#             else:
#                 exception_string += str(valEx.absolute_path[i] + 1) + "] "
#
#         print(exception_string)
#     except Exception as ex:
#         print("\nERROR: " + ex.args[0] + "\n")

# DON'T MODIFY ANYTHING FROM THIS POINT ON!
#main()
