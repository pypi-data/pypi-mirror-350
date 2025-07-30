import logging
import os
import subprocess
import tempfile
import threading
from io import BytesIO
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple

import openpyxl
import patoolib  # type: ignore
from tenacity import retry, stop_after_attempt, wait_fixed

from util_common.io import guess_file_extension
from util_common.path import (
    ARCHIVE_EXTS,
    DOCUMENT_EXTS,
    IGNORE_NAMES,
    FileExt,
    get_basename,
    get_basename_without_extension,
    get_parent,
    guess_extension_from_mime,
    split_basename,
)
from util_intelligence.char_util import normalize_char_text
from util_intelligence.regex import replace_multiple_spaces

io_lock = threading.Lock()


def get_bytes_and_basename(
    file: str | Path | bytes, filename: Optional[str | Path] = None
) -> Tuple[bytes, str]:
    _filename = ""
    if isinstance(file, str):
        file = Path(file)
    if isinstance(file, Path) and file.is_file():
        _filename = file.name
        file = file.read_bytes()
    if isinstance(file, bytes):
        if filename is not None:
            _filename = get_basename(filename)
        return file, _filename
    raise FileNotFoundError(f"Check if {file} exists")


def normalize_stem(name: str) -> str:
    return replace_multiple_spaces(normalize_char_text(name)).strip()


def fix_extension(
    ext: str,
    content: Optional[bytes],
    mime_type: Optional[str],
) -> str:
    guessed_ext = None
    if content is not None:
        guessed_ext = guess_file_extension(content)
    if guessed_ext is None and isinstance(mime_type, str) and len(mime_type) > 0:
        guessed_ext = guess_extension_from_mime(mime_type)
    if isinstance(guessed_ext, str) and len(guessed_ext) > 0:
        return guessed_ext
    return ext


def fix_filename_and_extension(
    content: Optional[bytes] = None,
    filename: Optional[str] = None,
    mime_type: Optional[str] = None,
    fix_stem: bool = False,
    fix_ext: bool = False,
) -> Tuple[str, str, str]:
    """To fix basename.
    fix_stem:
        if set True, will normalize filename text.
    fix_ext:
        if set True, ext will be replaced by guessed ext.
        if set False but no ext found in filename, still add guessed ext.
    """

    if content is None and mime_type is None:
        if fix_ext is True:
            raise ValueError("Can't fix ext, both content and mime_type is None!")
        else:
            fix_ext = False

    if filename is None:
        if fix_stem is True:
            raise ValueError("Can't fix stem, filename is None!")
        else:
            fix_stem = False

    stem, ext = "", ""
    if isinstance(filename, str) and len(filename) > 0:
        stem, ext = split_basename(filename)
        ext = ext.lower().strip('. ')
        stem = stem.strip('. ')

    if len(stem) > 0 and fix_stem is True:
        stem = normalize_stem(stem)

    if len(ext) == 0 or fix_ext is True:
        ext = fix_extension(ext, content, mime_type)

    if len(ext) > 0:
        _filename = f"{stem}.{ext}"
    else:
        _filename = stem

    if _filename != filename:
        logging.info(f"Fixed filename: {filename} -> {_filename}")

    return stem, ext, _filename


def recursive_yield_file_bytes(
    folder_path: str | Path,
    include_archive_exts: Sequence[FileExt] = ARCHIVE_EXTS,
    include_document_exts: Sequence[FileExt] = DOCUMENT_EXTS,
) -> Iterable[Tuple[bytes, str]]:
    """Recursively yield file bytes from a folder.

    include_archive_exts:
       if archive is included, the archive will be treated as folder.
    include_document_exts:
        only matched document type will be yield.
    """
    for root, _, files in os.walk(folder_path):
        if any([x in root for x in IGNORE_NAMES]):
            continue

        files = [x for x in files if x not in IGNORE_NAMES]
        for filename in files:
            file_bytes = Path(os.path.join(root, filename)).read_bytes()
            stem, ext, filename = fix_filename_and_extension(
                file_bytes,
                filename,
                fix_stem=False,
                fix_ext=False,
            )
            if ext and ext in include_document_exts:
                yield file_bytes, filename

            if ext in include_archive_exts:
                yield from yield_files_from_archive(
                    file_bytes,
                    filename=filename,
                    include_archive_exts=include_archive_exts,
                    include_document_exts=include_document_exts,
                    recursive=True,
                )


def yield_files_from_archive(
    archive: bytes,
    filename: str,
    password: Optional[str] = None,
    include_archive_exts: Sequence[FileExt] = ARCHIVE_EXTS,
    include_document_exts: Sequence[FileExt] = DOCUMENT_EXTS,
    recursive: bool = False,
) -> Iterable[Tuple[bytes, str]]:
    """Yield file bytes from archive

    include_exts:
        only matched type of archive will be processed.
    recursive:
        if True, nested archive will be processed.
    """
    arch_stem, arch_ext, arch_name = fix_filename_and_extension(
        archive,
        filename,
        fix_stem=False,
        fix_ext=False,
    )

    if isinstance(arch_ext, str) and arch_ext in ARCHIVE_EXTS:
        tmp_prefix = "archive-"
        with tempfile.TemporaryDirectory(
            delete=True,
            prefix=tmp_prefix,
        ) as tmp_dirname:
            with tempfile.NamedTemporaryFile(
                delete=True,
                suffix=f".{arch_ext}",
                prefix=tmp_prefix,
            ) as tmp_arch:
                tmp_arch.write(archive)
                try:
                    print(f"> 解压 {tmp_arch.name}")
                    patoolib.extract_archive(
                        tmp_arch.name,
                        outdir=tmp_dirname,
                        interactive=False,
                        password=password,
                        verbosity=True,
                    )
                    print("< 解压成功")
                except Exception as e:
                    raise e
                finally:
                    include_archive_exts = [] if recursive is False else include_archive_exts
                    for _file_bytes, _filename in recursive_yield_file_bytes(
                        folder_path=tmp_dirname,
                        include_archive_exts=include_archive_exts,
                        include_document_exts=include_document_exts,
                    ):
                        if len(arch_stem) > 0:
                            # 每次解压会在子文件名前加上父级前缀避免重名
                            if _filename == arch_stem:
                                # 如果解压后文件名和父级文件名相同, 说明是单文件压缩
                                _filename = _filename
                            elif not _filename.startswith(arch_stem):
                                _filename = f"{arch_stem}-{_filename}"
                            else:
                                _filename = f"{arch_stem}-{_filename[len(arch_stem):]}"
                            # 去掉两端的-_, 避免后续连接名字时多出-_
                            _filename = _filename.strip("-_")
                        yield _file_bytes, _filename
    else:
        logging.warning(f"Not archive: {arch_name}!")
        yield archive, arch_name


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), reraise=True)
def run_subprocess(command) -> str:
    with io_lock:
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=3.0,
            )
            try:
                return result.stdout
            except Exception:
                return ""
        except subprocess.TimeoutExpired:
            raise TimeoutError("The conversion process timed out.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Conversion failed: {e}")


def libreoffice_save_as(
    content: bytes,
    src_ext: str,
    dst_ext: str,
) -> Optional[bytes]:
    """
    Only one thread a time, so if GUI of libreoffice is in using,
    the conversion will return None.
    """
    new_content = None
    with tempfile.NamedTemporaryFile(
        suffix=f".{src_ext}",
    ) as file:
        file.write(content)

        filename = file.name
        dir = get_parent(filename)
        stem = get_basename_without_extension(filename)
        save_path = Path(os.path.join(dir, f"{stem}.{dst_ext}"))

        command = [
            "libreoffice",
            "--headless",
            "--convert-to",
            dst_ext,
            "--outdir",
            dir,
            filename,
        ]
        run_subprocess(command)

        try:
            new_content = save_path.read_bytes()
            for path in save_path.parent.glob(f"{stem}*"):
                os.remove(path)
        except Exception:
            pass
        if new_content is not None:
            return new_content
        else:
            raise IOError(f"Failed convert {filename} to .{dst_ext}!")


def try_open_xlsx_by_openpyxl(content: bytes):
    try:
        book = openpyxl.load_workbook(BytesIO(content), read_only=True, data_only=True)
        book.close()
        return content
    except Exception as e:
        logging.error(f"Conversion failed: {e}")
        return None


def libre_xls2xlsx(content: bytes) -> Optional[bytes]:
    _content = libreoffice_save_as(content, "xls", "xlsx")
    if _content is not None:
        _content = try_open_xlsx_by_openpyxl(_content)
    return _content


def libre_doc2docx(content: bytes) -> Optional[bytes]:
    return libreoffice_save_as(content, "doc", "docx")


def libre_xls2html(content: bytes) -> Optional[bytes]:
    return libreoffice_save_as(content, "xls", "html")


def libre_xlsx2html(content: bytes) -> Optional[bytes]:
    return libreoffice_save_as(content, "xlsx", "html")


def libre_doc2html(content: bytes) -> Optional[bytes]:
    return libreoffice_save_as(content, "doc", "html")


def libre_docx2html(content: bytes) -> Optional[bytes]:
    return libreoffice_save_as(content, "docx", "html")


def libre_docx2pdf(content: bytes) -> Optional[bytes]:
    return libreoffice_save_as(content, "docx", "pdf")


def libre_xlsx2pdf(content: bytes) -> Optional[bytes]:
    return libreoffice_save_as(content, "xlsx", "pdf")
