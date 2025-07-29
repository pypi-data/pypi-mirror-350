from yta_constants.enum import YTAEnum as Enum
# TODO: These 'yta_general_utils' dependencies must 
# dissappear
#from yta_general_utils.temp import Temp
#from yta_general_utils.random import Random
from yta_validation import PythonValidator
from yta_validation.parameter import ParameterValidator
from typing import Union

import os


class FileExtension(Enum):
    """
    Enum class to encapsulate all the file
    extensions that we are able to handle.

    These extensions come without the dot
    and in lower case.
    """

    # IMAGE
    PNG = 'png'
    """
    Portable Network Graphics
    """
    JPEG = 'jpeg'
    """
    Joint Photographic Experts Group
    """
    JPG = 'jpg'
    """
    Joint Photographic Experts Group
    """
    WEBP = 'webp'
    """
    Web Picture
    """
    BMP = 'bmp'
    """
    Bitmap Image File
    """
    GIF = 'gif'
    """
    Graphics Interchange Format
    """
    TIFF = 'tiff'
    """
    Tagged Image File
    """
    PSD = 'psd'
    """
    Photoshop Document
    """
    PDF = 'pdf'
    """
    Portable Document Format
    """
    DOC = 'doc'
    """
    Microsoft Word document old format.
    """
    DOCX = 'docx'
    """
    Microsoft Word document new format.
    """
    EPS = 'eps'
    """
    Encapsulated Postcript
    """
    AI = 'ai'
    """
    Adobe ILlustrator Document
    """
    INDD = 'indd'
    """
    Adobe Indesign Document
    """
    RAW = 'raw'
    """
    Raw Image Formats
    """
    CDR = 'cdr'
    """
    Corel Draw
    """
    # AUDIO
    WAV = 'wav'
    """
    Waveform Audio
    """
    MP3 = 'mp3'
    """
    MPEG Audio Layer 3.
    """
    M4A = 'm4a'
    """
    MPEG-4 Audio
    """
    FLAC = 'flac'
    """
    Free Lossless Audio Codec.
    """
    WMA = 'wma'
    """
    Windows Media Audio
    """
    AAC = 'aac'
    """
    Advanced Audio Coding
    """
    # VIDEO
    MOV = 'mov'
    """
    Apple video
    """
    MP4 = 'mp4'
    """
    MPEG-4
    """
    WEBM = 'webm'
    """
    Developed by Google, subgroup of the open and standard Matroska Video Container (MKV)
    """
    AVI = 'avi'
    """
    Audio Video Interleave
    """
    WMV = 'wmv'
    """
    Windows Media Video
    """
    AVCHD = 'avchd'
    """
    Advanced Video Coding High Definition
    """
    FVL = 'flv'
    """
    Flash Video
    """
    # SUBTITLES
    SRT = 'srt'
    """
    Srt subtitle file extension.

    This is the format:
    1
    00:00:00,000 --> 00:00:02,500
    Welcome to the Example Subtitle File!

    """
    JSON3 = 'json3'
    """
    Json3 subtitle file extension
    """
    SRV1 = 'srv1'
    """
    Srv1 subtitle file extension
    """
    SRV2 = 'srv2'
    """
    Srv2 subtitle file extension
    """
    SRV3 = 'srv3'
    """
    Srv3 subtitle file extension
    """
    TTML = 'ttml'
    """
    Ttml subtitle file extension
    """
    VTT = 'vtt'
    """
    Vtt subtitle file extension
    """
    # TEXT
    TXT = 'txt'
    """
    Txt text file extension
    """
    CSV = 'csv'
    """
    Csv text file extension
    """
    JSON = 'json'
    """
    Json text file extension
    """
    XML = 'xml'
    """
    Xml text file extension
    """
    HTML = 'html'
    """
    Html text file extension
    """
    MD = 'md'
    """
    Md text file extension
    """
    LOG = 'log'
    """
    Log text file extension
    """
    INI = 'ini'
    """
    Ini text file extension
    """
    YAML = 'yaml'
    """
    Yaml text file extension
    """
    YML = 'yml'
    """
    Yml text file extension
    """

    @property
    def with_dot(
        self
    ) -> str:
        """
        The extension, in lower case, but with the dot at the
        begining.
        """
        return f'.{self.value}'
    
    def get_temp_filename(
        self,
        filename: Union[str, None] = None
    ) -> str:
        """
        Get a temporary random filename with this file
        extension.

        The 'filename', if provided, will be forced to
        have this file extension but keeping the rest.
        If it is not provided, it will be a randomly
        generated string with this file extension.
        """
        return _get_temp_filename_for_file_extension(filename, self)
    
    # TODO: Add some utils  
    @staticmethod
    def is_filename_valid(
        filename: str
    ):
        """
        Check if the provided 'filename' is valid according
        to this file extension.
        """
        return _is_filename_valid_for_file_extension(filename, FileExtension)

class ImageFileExtension(Enum):
    """
    Enum class to encapsulate all existing image file
    extensions.

    These extensions come without the dot
    and in lower case.
    """
    
    PNG = FileExtension.PNG.value
    """
    Portable Network Graphics
    """
    JPEG = FileExtension.JPEG.value
    """
    Joint Photographic Experts Group
    """
    JPG = FileExtension.JPG.value
    """
    Joint Photographic Experts Group
    """
    WEBP = FileExtension.WEBP.value
    """
    Web Picture
    """
    BMP = FileExtension.BMP.value
    """
    Bitmap Image File
    """
    GIF = FileExtension.GIF.value
    """
    Graphics Interchange Format
    """
    TIFF = FileExtension.TIFF.value
    """
    Tagged Image File
    """
    PSD = FileExtension.PSD.value
    """
    Photoshop Document
    """
    PDF = FileExtension.PDF.value
    """
    Portable Document Format
    """
    EPS = FileExtension.EPS.value
    """
    Encapsulated Postcript
    """
    AI = FileExtension.AI.value
    """
    Adobe Illustrator Document
    """
    INDD = FileExtension.INDD.value
    """
    Adobe Indesign Document
    """
    RAW = FileExtension.RAW.value
    """
    Raw Image Formats
    """
    CDR = FileExtension.CDR.value
    """
    Corel Draw
    """
    # TODO: Add more

    @property
    def with_dot(
        self
    ) -> str:
        """
        The extension, in lower case, but with the dot at the
        begining.
        """
        return f'.{self.value}'
    
    def get_temp_filename(
        self,
        filename: Union[str, None] = None
    ) -> str:
        """
        Get a temporary random filename with this file
        extension.

        The 'filename', if provided, will be forced to
        have this file extension but keeping the rest.
        If it is not provided, it will be a randomly
        generated string with this file extension.
        """
        return _get_temp_filename_for_file_extension(filename, self)

    @classmethod
    def default(cls):
        return cls.PNG

    # TODO: Add some utils 
    # TODO: I cannot inherit from FileExtension Enum :( 
    @staticmethod
    def is_filename_valid(
        filename: str
    ):
        """
        Check if the provided 'filename' is valid according
        to this file extension.
        """
        return _is_filename_valid_for_file_extension(filename, ImageFileExtension)

class AudioFileExtension(Enum):
    """
    Enum class to encapsulate all existing audio file
    extensions.

    These extensions come without the dot
    and in lower case.
    """

    WAV = FileExtension.WAV.value
    """
    Waveform Audio
    """
    MP3 = FileExtension.MP3.value
    """
    MPEG Audio Layer 3.
    """
    M4A = FileExtension.M4A.value
    """
    MPEG-4 Audio
    """
    FLAC = FileExtension.FLAC.value
    """
    Free Lossless Audio Codec.
    """
    WMA = FileExtension.WMA.value
    """
    Windows Media Audio
    """
    AAC = FileExtension.AAC.value
    """
    Advanced Audio Coding
    """
    WEBM = FileExtension.WEBM.value
    # TODO: Add more

    @property
    def with_dot(
        self
    ) -> str:
        """
        The extension, in lower case, but with the dot at the
        begining.
        """
        return f'.{self.value}'
    
    def get_temp_filename(
        self,
        filename: Union[str, None] = None
    ) -> str:
        """
        Get a temporary random filename with this file
        extension.

        The 'filename', if provided, will be forced to
        have this file extension but keeping the rest.
        If it is not provided, it will be a randomly
        generated string with this file extension.
        """
        return _get_temp_filename_for_file_extension(filename, self)

    @classmethod
    def default(cls):
        return cls.WAV
    
    # TODO: I cannot inherit from FileExtension Enum :( 
    @staticmethod
    def is_filename_valid(
        filename: str
    ):
        """
        Check if the provided 'filename' is valid according
        to this file extension.
        """
        return _is_filename_valid_for_file_extension(filename, AudioFileExtension)

class VideoFileExtension(Enum):
    """
    Enum class to encapsulate all existing video file
    extensions.

    These extensions come without the dot
    and in lower case.
    """

    MOV = FileExtension.MOV.value
    """
    Apple video
    """
    MP4 = FileExtension.MP4.value
    """
    MPEG-4
    """
    WEBM = FileExtension.WEBM.value
    """
    Developed by Google, subgroup of the open and standard Matroska Video Container (MKV)
    """
    AVI = FileExtension.AVI.value
    """
    Audio Video Interleave
    """
    WMV = FileExtension.WMV.value
    """
    Windows Media Video
    """
    AVCHD = FileExtension.AVCHD.value
    """
    Advanced Video Coding High Definition
    """
    FVL = FileExtension.FVL.value
    """
    Flash Video
    """
    # TODO: Add more

    @property
    def with_dot(
        self
    ) -> str:
        """
        The extension, in lower case, but with the dot at the
        begining.
        """
        return f'.{self.value}'
    
    def get_temp_filename(
        self,
        filename: Union[str, None] = None
    ) -> str:
        """
        Get a temporary random filename with this file
        extension.

        The 'filename', if provided, will be forced to
        have this file extension but keeping the rest.
        If it is not provided, it will be a randomly
        generated string with this file extension.
        """
        return _get_temp_filename_for_file_extension(filename, self)

    @classmethod
    def default(cls):
        return cls.MP4
    
    # TODO: I cannot inherit from FileExtension Enum :( 
    @staticmethod
    def is_filename_valid(
        filename: str
    ):
        """
        Check if the provided 'filename' is valid according
        to this file extension.
        """
        return _is_filename_valid_for_file_extension(filename, VideoFileExtension)

class SubtitleFileExtension(Enum):
    """
    Enum class to encapsulate all existing subtitle
    file extensions.

    These extensions come without the dot
    and in lower case.
    """

    SRT = FileExtension.SRT.value
    """
    Srt subtitle file extension.

    This is the format:
    1
    00:00:00,000 --> 00:00:02,500
    Welcome to the Example Subtitle File!

    """
    JSON3 = FileExtension.JSON3.value
    """
    Json3 subtitle file extension
    """
    SRV1 = FileExtension.SRV1.value
    """
    Srv1 subtitle file extension
    """
    SRV2 = FileExtension.SRV2.value
    """
    Srv2 subtitle file extension
    """
    SRV3 = FileExtension.SRV3.value
    """
    Srv3 subtitle file extension
    """
    TTML = FileExtension.TTML.value
    """
    Ttml subtitle file extension
    """
    VTT = FileExtension.VTT.value
    """
    Vtt subtitle file extension
    """

    @property
    def with_dot(
        self
    ) -> str:
        """
        The extension, in lower case, but with the dot at the
        begining.
        """
        return f'.{self.value}'
    
    def get_temp_filename(
        self,
        filename: Union[str, None] = None
    ) -> str:
        """
        Get a temporary random filename with this file
        extension.

        The 'filename', if provided, will be forced to
        have this file extension but keeping the rest.
        If it is not provided, it will be a randomly
        generated string with this file extension.
        """
        return _get_temp_filename_for_file_extension(filename, self)

    @classmethod
    def default(cls):
        return cls.JSON3
    
    # TODO: I cannot inherit from FileExtension Enum :( 
    @staticmethod
    def is_filename_valid(
        filename: str
    ):
        """
        Check if the provided 'filename' is valid according
        to this file extension.
        """
        return _is_filename_valid_for_file_extension(filename, SubtitleFileExtension)
    
class TextFileExtension(Enum):
    """
    Enum class to encapsulate all existing text
    file extensions.

    These extensions come without the dot
    and in lower case.
    """

    TXT = FileExtension.TXT.value
    """
    Txt subtitle file extension
    """
    JSON = FileExtension.JSON.value
    """
    Json text file extension
    """
    XML = FileExtension.XML.value
    """
    Xml text file extension
    """
    HTML = FileExtension.HTML.value
    """
    Html text file extension
    """
    MD = FileExtension.MD.value
    """
    Md text file extension
    """
    LOG = FileExtension.LOG.value
    """
    Log text file extension
    """
    INI = FileExtension.INI.value
    """
    Ini text file extension
    """
    YAML = FileExtension.YAML.value
    """
    Yaml text file extension
    """
    YML = FileExtension.YML.value
    """
    Yml text file extension
    """

    @property
    def with_dot(
        self
    ) -> str:
        """
        The extension, in lower case, but with the dot at the
        begining.
        """
        return f'.{self.value}'
    
    def get_temp_filename(
        self,
        filename: Union[str, None] = None
    ) -> str:
        """
        Get a temporary random filename with this file
        extension.

        The 'filename', if provided, will be forced to
        have this file extension but keeping the rest.
        If it is not provided, it will be a randomly
        generated string with this file extension.
        """
        return _get_temp_filename_for_file_extension(filename, self)

    @classmethod
    def default(cls):
        return cls.TXT
    
    # TODO: I cannot inherit from FileExtension Enum :( 
    @staticmethod
    def is_filename_valid(
        filename: str
    ):
        """
        Check if the provided 'filename' is valid according
        to this file extension.
        """
        return _is_filename_valid_for_file_extension(filename, TextFileExtension)
    
# TODO: I've been able to inherit from another custom
# YTAEnum classes when creating a new one, but here I
# had some troubles recently so I decided to continue
# and fix it later. Please, review it and refactor
# because I'm repeating a lot of code

# These classes above should be used by the ffmpeg_handler and other
# declarations I make in our app to be consistent and reuse the code

class FileType(Enum):
    """
    TODO: Check original FileType
    """

    IMAGE = 'image'
    AUDIO = 'audio'
    VIDEO = 'video'
    SUBTITLE = 'subtitle'
    TEXT = 'text'

    def is_filename_valid(
        self,
        filename: str
    ):
        """
        Check if the provided 'filename' is valid according
        to this file extension.
        """
        return _is_filename_valid_for_file_extension(filename, self.get_file_extension_enum_class())
    
    def get_file_extension_enum_class(
        self
    ) -> Union[VideoFileExtension, ImageFileExtension, AudioFileExtension]:
        """
        Get the file extension YTAEnum class associated
        with this file type YTAEnum instance.
        """
        return {
            FileType.VIDEO: VideoFileExtension,
            FileType.IMAGE: ImageFileExtension,
            FileType.AUDIO: AudioFileExtension,
            FileType.SUBTITLE: SubtitleFileExtension,
            FileType.TEXT: TextFileExtension
        }[self]

    def get_default_file_extension(
        self
    ) -> Union[VideoFileExtension, ImageFileExtension, AudioFileExtension]:
        """
        Get the default file extension of this file type.
        """
        return self.get_file_extension_enum_class().default()

    def get_temp_filename(self, filename: Union[str, None]):
        """
        Get a temporary random filename for this file type.
        """
        return _get_temp_filename_for_file_extension(filename, self.get_default_file_extension())
    
    @staticmethod
    def get_type_from_filename(
        filename: str
    ) -> Union['FileType', None]:
        for type in FileType.get_all():
            if type.is_filename_valid(filename):
                return type

        return None

def _is_filename_valid_for_file_extension(
    filename: str,
    file_extension_enum_class: Union[FileExtension, TextFileExtension, AudioFileExtension, ImageFileExtension, VideoFileExtension, SubtitleFileExtension] 
):
    """
    Check if the provided 'filename' is valid for
    the also given 'file_extension_enum_class'.
    """
    # TODO: Fix this, 'is_class' is not accepting arrays
    # if not PythonValidator.is_class(file_extension_enum_class, [FileExtension, TextFileExtension, AudioFileExtension, ImageFileExtension, VideoFileExtension, SubtitleFileExtension]):
    #     raise Exception('The "file_extension_enum" is not valid.')

    ParameterValidator.validate_mandatory_string('filename', filename, do_accept_empty = False)

    # TODO: I cannot import from 'file.filename' because of
    # cyclic import issue
    extension = os.path.splitext(filename)[1]

    return (
        False
        if extension == '' else
        file_extension_enum_class.is_valid(extension.replace('.', ''))
    )

def _get_temp_filename_for_file_extension(
    filename: Union[str, None] = None,
    file_extension: Union[FileExtension, TextFileExtension, AudioFileExtension, ImageFileExtension, VideoFileExtension, SubtitleFileExtension] = FileExtension
) -> str:
    """
    Get a temporary random filename with this file
    extension.

    The 'filename', if provided, will be forced to
    have this file extension but keeping the rest.
    If it is not provided, it will be a randomly
    generated string with this file extension.
    """
    if not PythonValidator.is_instance(file_extension, [FileExtension, TextFileExtension, AudioFileExtension, ImageFileExtension, VideoFileExtension, SubtitleFileExtension]):
        raise Exception('The "file_extension_enum" is not valid.')

    # TODO: This line has been commented due to 'yta_general_utils'
    # dependency we want to avoid
    #filename = Temp.create_filename(f'{Random.characters()}.noext') if filename is None else filename
    filename = (
        filename.split('.')[0]
        if '.' in filename else
        filename
    )

    return f'{filename}.{file_extension.value}'

class FileSearchOption(Enum):
    """
    Enum that allows us setting the strategy dynamically when 
    searching for files.
    """

    FILES_AND_FOLDERS = 'fifo'
    """
    This option, when set, will return files and folders.
    """
    FILES_ONLY = 'fi'
    """
    This option, when set, will return files only.
    """
    FOLDERS_ONLY = 'fo'
    """
    This option, when set, will return folders only.
    """

class FileEncoding(Enum):
    """
    The different file encoding we accept. This Enum
    has been created to be used as encoding when
    writing on a file.

    # TODO: Maybe rename to 'TextEncoding'? Maybe use
    # an external library or move this to another
    # module (not library) (?)
    """

    UTF8 = 'utf8'

class FileOpenMode(Enum):
    """
    The mode we want to use to open a file.

    Please, check line 200 in 
    'stdlib/_typeshed/__init__.pyi' file.

    If you need more information about Windows-only
    open mode and other systems please, check this
    link:

    - https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
    """

    WRITE_ONLY = 'w'
    """
    The file content, which is a string text, will
    overwrite any previous content in the file.

    The file is created if it does not exist or it
    is overwritten if existing.
    """
    WRITE_ONLY_BINARY = 'wb'
    """
    The file content, which is binary, will overwrite
    any previous content in the file. This option is
    only for Windows systems.

    The file is created if it does not exist or it
    is overwritten if existing.
    """
    APPEND_ONLY = 'a'
    """
    The file content, which is a string text, will
    be appended to any previous content in the file.

    The file is created if it does not exist or the
    content is appended to the end of the previous
    content if existing.
    """
    APPEND_ONLY_BINARY ='ab'
    """
    The file content, which is binary, will be
    appended to any previous content in the file.
    This option is only for Windows systems.

    The file is created if it does not exist or the
    content is appended to the end of the previous
    content if existing.
    """
    READ_ONLY = 'r'
    """
    The file content will be read as a string text.

    The file must exist.
    """
    READ_ONLY_BINARY = 'rb'
    """
    The file content will be read as binary. This
    option is only for Windows systems.

    The file must exist.
    """
    READ_AND_WRITE = 'r+'
    """
    The file content will be read or written as text.
    If written, it will replace the previous content.
    
    The file must exist.
    """
    READ_AND_WRITE_BINARY = 'r+b'
    """
    The file content will be read or written as binary.
    If written, it will replace the previous content.
    This option is only for Windows systems.
    
    The file must exist.
    """
    READ_AND_WRITE_CREATING = 'w+'
    """
    The file content will be read or written as text.
    If written, it will replace the previous content.

    The file is created if it does not exist or it
    is overwritten if existing.
    """
    READ_AND_WRITE_BINARY_CREATING = 'w+b'
    """
    The file content will be read or written as binary.
    If written, it will replace the previous content.
    This option is only for Windows systems.

    The file is created if it does not exist or it
    is overwritten if existing.
    """
    READ_AND_APPEND_CREATING = 'a+'
    """
    The file content will be read or appended as text
    to the previous existing content.

    The file is created if it does not exist or the
    content is appended to the end of the previous
    content if existing.
    """
    READ_AND_APPEND_BINARY_CREATING = 'a+b'
    """
    The file content will be read or appended as binary
    to the previous existing content. This option is 
    only for Windows systems.

    The file is created if it does not exist or the
    content is appended to the end of the previous
    content if existing.
    """

    @staticmethod
    def get_read_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to read the file (text or binary).
        """
        return [
            FileOpenMode.READ_ONLY,
            FileOpenMode.READ_ONLY_BINARY,
            FileOpenMode.READ_AND_WRITE,
            FileOpenMode.READ_AND_WRITE_BINARY,
            FileOpenMode.READ_AND_WRITE_CREATING,
            FileOpenMode.READ_AND_WRITE_BINARY_CREATING,
            FileOpenMode.READ_AND_APPEND_CREATING,
            FileOpenMode.READ_AND_APPEND_BINARY_CREATING
        ]
    
    @staticmethod
    def get_read_text_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to read the file (only text).
        """
        return [
            FileOpenMode.READ_ONLY,
            FileOpenMode.READ_AND_WRITE,
            FileOpenMode.READ_AND_WRITE_CREATING,
            FileOpenMode.READ_AND_APPEND_CREATING
        ]
    
    @staticmethod
    def get_read_binary_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to read the file (only binary).
        """
        return [
            FileOpenMode.READ_ONLY_BINARY,
            FileOpenMode.READ_AND_WRITE_BINARY,
            FileOpenMode.READ_AND_WRITE_BINARY_CREATING,
            FileOpenMode.READ_AND_APPEND_BINARY_CREATING
        ]
    
    @staticmethod
    def get_write_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to write the file (text or binary).
        """
        return [
            FileOpenMode.WRITE_ONLY,
            FileOpenMode.WRITE_ONLY_BINARY,
            FileOpenMode.READ_AND_WRITE,
            FileOpenMode.READ_AND_WRITE_BINARY,
            FileOpenMode.READ_AND_WRITE_CREATING,
            FileOpenMode.READ_AND_WRITE_BINARY_CREATING
        ]
    
    @staticmethod
    def get_write_text_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to write the file (only text).
        """
        return [
            FileOpenMode.WRITE_ONLY,
            FileOpenMode.READ_AND_WRITE,
            FileOpenMode.READ_AND_WRITE_CREATING
        ]
    
    @staticmethod
    def get_write_binary_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to write the file (only binary).
        """
        return [
            FileOpenMode.WRITE_ONLY_BINARY,
            FileOpenMode.READ_AND_WRITE_BINARY,
            FileOpenMode.READ_AND_WRITE_BINARY_CREATING
        ]
    
    @staticmethod
    def get_append_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to append content to the file (text or
        binary).
        """
        return [
            FileOpenMode.APPEND_ONLY,
            FileOpenMode.APPEND_ONLY_BINARY,
            FileOpenMode.READ_AND_APPEND_CREATING,
            FileOpenMode.READ_AND_APPEND_BINARY_CREATING
        ]
    
    @staticmethod
    def get_append_text_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to append content to the file (only
        text).
        """
        return [
            FileOpenMode.APPEND_ONLY,
            FileOpenMode.READ_AND_APPEND_CREATING
        ]
    
    @staticmethod
    def get_append_binary_options(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        allows us to append content to the file (only
        binary).
        """
        return [
            FileOpenMode.APPEND_ONLY_BINARY,
            FileOpenMode.READ_AND_APPEND_BINARY_CREATING
        ]

    @staticmethod
    def get_options_that_create_file(
    ) -> list['FileOpenMode']:
        """
        Get the list that contains all the options that
        will create the file if it doesn't exist.
        """
        return [
            FileOpenMode.WRITE_ONLY,
            FileOpenMode.WRITE_ONLY_BINARY,
            FileOpenMode.APPEND_ONLY,
            FileOpenMode.APPEND_ONLY_BINARY,
            FileOpenMode.READ_AND_WRITE_CREATING,
            FileOpenMode.READ_AND_APPEND_CREATING,
            FileOpenMode.READ_AND_WRITE_BINARY_CREATING,
            FileOpenMode.READ_AND_APPEND_BINARY_CREATING
        ]