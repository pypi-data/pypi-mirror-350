import base64
import os
import uuid
from datetime import datetime
from hashlib import sha256
from typing import Any, List, Literal, Optional, Sequence, Union, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Entity.SerializableContent import SerializableClass


class FingerprintFragment(SerializableClass):
    offset: int = 0
    length: int = 0
    bytes: str = ""


class FileFragment(SerializableClass):
    _typeMapper = {"fragments": FingerprintFragment}
    id: str = ""
    fragments: List[FingerprintFragment] = []


FormatFileState = Literal["NEW", "UNCHANGED", "NEEDSUPDATE", "DELETE"]


class FileEntry(SerializableClass):
    _typeMapper = {"fragments": FingerprintFragment}
    _noSerialize = ["isDir", "name"]
    id: Optional[str] = None
    fullPath: str = ""
    path: str = ""
    isDir: bool = False
    name: str = ""
    fragments: Optional[List[FingerprintFragment]] = None
    hash: Optional[str] = None
    state: Optional[FormatFileState] = None
    mtime: Optional[datetime] = None

    def __init__(
        self,
        ref: Any = None,
        fullPath: Optional[str] = None,
        state: Optional[FormatFileState] = None,
    ):
        _path: str = ""
        if isinstance(ref, (str, os.DirEntry, FileEntry)):
            if isinstance(ref, FileEntry):
                _path = ref.path
                ref = ref.fullPath
            elif isinstance(ref, os.DirEntry) and ref.path:
                _path = ref.path

            _fullPath = os.path.realpath(ref)
            ref = {
                "id": uuid.uuid4().hex,
                "fullPath": _fullPath,
                "isDir": os.path.isdir(_fullPath),
                "name": os.path.basename(_fullPath),
            }
        super().__init__(ref)
        if fullPath is not None:
            self.fullPath = fullPath
        self.path = _path
        if state is not None:
            self.state = state

    def __str__(self):
        return "<%s %s%a>" % (
            type(self).__name__,
            ("<dir> " if self.isDir else ""),
            self.fullPath,
        )

    def addFragment(self, fragments: List[FingerprintFragment]):
        with open(self.fullPath, "rb") as read:
            if self.fragments is None:
                self.fragments = []
            for fragment in fragments:
                read.seek(fragment.offset)
                fragment.bytes = base64.b64encode(read.read(fragment.length)).decode(
                    "utf-8"
                )
                self.fragments.append(fragment)

    def addHash(self):
        with open(self.fullPath, "rb") as read:
            self.hash = sha256(read.read()).hexdigest()

    def addMtime(self):
        self.mtime = datetime.fromtimestamp(os.path.getmtime(self.fullPath))

    @classmethod
    def entriesFromFiles(
        cls,
        files: Union[Constants.FILE_TYPE, Sequence[Constants.FILE_TYPE]],
        ignoreReadErrors=False,
    ):
        if files == None:
            raise FileNotFoundError("Could not read file or directory from 'None' path")
        if not isinstance(files, list):
            files = [cast(Constants.FILE_TYPE, files)]

        result: List[FileEntry] = []

        while len(files) > 0:
            file = files.pop(0)
            if isinstance(file, (str, os.DirEntry, FileEntry)):
                f = FileEntry(file)
                if f.isDir:
                    with os.scandir(f.fullPath) as entries:
                        files.extend(entries)
                else:
                    if not os.path.isfile(f.fullPath) or not os.access(
                        f.fullPath, os.R_OK
                    ):
                        if not ignoreReadErrors:
                            raise PermissionError("Could not read file %a" % f.fullPath)
                    else:
                        f.id = f.fullPath
                        result.append(f)

        return result
