import os
import posixpath
import shutil
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Literal, Optional, Tuple, Union, get_args

import natsort

from util_common._log import log

TextExt = Literal[
    "txt",
    "json",
    "html",
]
TEXT_EXTS: List[TextExt] = [*get_args(TextExt)]

ArchiveExt = Literal[
    "7z",
    "rar",
    "zip",
]
ARCHIVE_EXTS: List[ArchiveExt] = [*get_args(ArchiveExt)]

ImageExt = Literal[
    "jpg",
    "jpeg",
    "png",
]
IMAGE_EXTS: List[ImageExt] = [*get_args(ImageExt)]

PdfExt = Literal["pdf"]
PDF_EXTS: List[PdfExt] = [*get_args(PdfExt)]

WordExt = Literal[
    "doc",
    "docx",
]
WORD_EXTS: List[WordExt] = [*get_args(WordExt)]

ExcelExt = Literal[
    "xls",
    "xlsx",
]
EXCEL_EXTS: List[ExcelExt] = [*get_args(ExcelExt)]

OfficeExt = Union[WordExt, ExcelExt]
OFFICE_EXTS: List[OfficeExt] = WORD_EXTS + EXCEL_EXTS

DocumentExt = Union[TextExt, ImageExt, PdfExt, OfficeExt]
DOCUMENT_EXTS: List[DocumentExt] = TEXT_EXTS + IMAGE_EXTS + PDF_EXTS + OFFICE_EXTS

FileExt = Union[ArchiveExt, TextExt, ImageExt, PdfExt, OfficeExt]
FILE_EXTS: List[FileExt] = ARCHIVE_EXTS + TEXT_EXTS + IMAGE_EXTS + PDF_EXTS + OFFICE_EXTS

IGNORE_NAMES = [
    "__MACOSX",
    ".DS_Store",
]
MIME_TYPES: Dict[str, str] = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    # Add more as needed
}


def get_base64_header(file_extension: str) -> str:
    """
    Adds a Base64 header to the provided file content.

    Parameters:
    - file_content: The raw bytes of the file.
    - file_extension: The file extension (e.g., 'png', 'pdf').

    Returns:
    - A Base64 string header.

    Usage:
    get_base64_header(file_extension) + ',' + {base64_string}
    """
    # Get the MIME type for the file extension
    mime_type = MIME_TYPES.get(file_extension.lower())
    if not mime_type:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    # Create the Base64 data URL with the appropriate header
    base64_string = f"data:{mime_type};base64"
    return base64_string


def normalize_path(
    raw_path: str | Path,
    name_process_fn: Optional[Callable] = None,
) -> Tuple[str, Path]:
    if isinstance(raw_path, str):
        raw_path = Path(raw_path).expanduser()
    name, parent, root = (
        raw_path.name,
        str(raw_path.parent),
        raw_path.root,
    )
    if name_process_fn is not None:
        name = name_process_fn(name)
    if root == "/":
        absolute_path = Path(parent).joinpath(name)
    elif parent == ".":
        absolute_path = get_absolute_cwd_path().joinpath(name)
    else:
        absolute_path = Path(
            posixpath.normpath(
                get_absolute_cwd_path().joinpath(parent).joinpath(name),
            )
        )
    return name, absolute_path


def get_absolute_cwd_path() -> Path:
    return Path(os.path.abspath(os.getcwd()))


def sort_paths(path_iter: Iterable[str | Path]) -> List[Path]:
    return [
        Path(x)
        for x in natsort.natsorted(
            list(path_iter),
            key=lambda x: str(x),
        )
    ]


def ensure_parent(path: Path | str) -> None:
    Path(path).parent.mkdir(exist_ok=True, parents=True)


def ensure_folder(path: Path | str) -> None:
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True)
    elif path.is_file():
        raise FileExistsError()


def move(src_path: Path | str, dst_path: Path | str) -> None:
    ensure_parent(dst_path)
    try:
        shutil.move(src_path, dst_path)
    except Exception as e:
        log.warning(f"move failed: {e}")


def duplicate(src_path: Path | str, dst_path: Path | str) -> None:
    ensure_parent(dst_path)
    if Path(src_path).is_file():
        shutil.copyfile(src_path, dst_path)
    elif Path(src_path).is_dir():
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
    else:
        raise FileNotFoundError(f"{src_path}: Not exists!")


def remove_folder(path: Path | str, trash_dir: Optional[Path | str] = None) -> None:
    path = Path(path)
    if path.exists():
        if path.is_dir():
            if trash_dir is None:
                shutil.rmtree(path)
            else:
                move(path, Path(trash_dir).joinpath(path.name))
        else:
            log.warning(f"{path} is a file!")
    else:
        log.warning(f"{path} not exists!")


def remove_file(path: Path | str, trash_dir: Optional[Path | str] = None, exists=False) -> None:
    path = Path(path)
    if path.exists():
        if path.is_file():
            if trash_dir is None:
                os.remove(path)
            else:
                move(path, Path(trash_dir).joinpath(path.name))
        else:
            if exists is False:
                log.warning(f"{path} is a folder!")
    else:
        if exists is False:
            log.warning(f"{path} not exists!")


def clear_folder(path: Path | str) -> Path:
    path = Path(path)
    remove_folder(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_parent(path: str | Path) -> str:
    return os.path.dirname(str(path))


def get_basename(path: str | Path) -> str:
    return os.path.basename(str(path))


def split_basename(path: str | Path, strip_dot: bool = True) -> Tuple[str, str]:
    name, ext = os.path.splitext(get_basename(path))
    if strip_dot is True:
        ext = ext.strip(".")
    return name, ext.lower()


def get_basename_without_extension(path: str | Path) -> str:
    return split_basename(path)[0]


def get_extension(path: str | Path, strip_dot=True) -> str:
    return split_basename(path, strip_dot)[1]


def guess_extension_from_mime(mime: Optional[str]) -> Optional[FileExt]:
    if isinstance(mime, str):
        if "zip" in mime:
            return "zip"

        if "rar" in mime:
            return "rar"

        if "7z" in mime:
            return "7z"

        if "word" in mime and "document" not in mime:
            return "doc"

        if "word" in mime and "document" in mime:
            return "docx"

        if "excel" in mime:
            return "xls"

        if "sheet" in mime:
            return "xlsx"

        if "jpeg" in mime or "jpg" in mime:
            return "jpg"

        if "png" in mime:
            return "png"

        if "pdf" in mime:
            return "pdf"

    return None


def recursive_list_named_children(
    folder: str | Path,
    filename: str,
) -> Iterable[Path]:
    paths = Path(folder).glob(f"**/{filename}")
    return paths


def recursive_list_files(folder: str | Path) -> Iterable[Path]:
    for root, _, files in os.walk(folder):
        for file_name in [x for x in files if x not in IGNORE_NAMES]:
            yield Path(os.path.join(root, file_name))
