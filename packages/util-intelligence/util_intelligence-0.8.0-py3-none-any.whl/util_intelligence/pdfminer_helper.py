import logging
from io import BytesIO
from pathlib import Path
from typing import Literal, Tuple

import numpy as np
from pdfminer.image import ImageWriter
from pdfminer.jbig2 import JBIG2StreamReader, JBIG2StreamWriter
from pdfminer.layout import LTImage
from pdfminer.pdfcolor import PREDEFINED_COLORSPACE
from pdfminer.pdftypes import LITERALS_JBIG2_DECODE, PDFObjRef, PDFStream
from pdfminer.psparser import LIT, PSLiteral
from PIL import Image, ImageCms


class PILImageWriter(ImageWriter):
    INDEXED = LIT("Indexed")

    def _save_raw(self, image: LTImage) -> str:
        if len(image.colorspace) == 1 and isinstance(
            image.colorspace[0],
            PDFObjRef,
        ):
            colorspace = self._resolve_recursively(image.colorspace[0])
        else:
            colorspace = self._resolve_recursively(image.colorspace)
        if colorspace[0] == PILImageWriter.INDEXED:
            return self._save_bytes(image)
        return super()._save_raw(image)

    def _save_jbig2(self, image: LTImage) -> str:
        """Save a JBIG2 encoded image"""
        name, path = self._create_unique_image_name(image, ".jb2")
        with open(path, "wb") as fp:
            input_stream = BytesIO()

            global_streams = []
            filters = image.stream.get_filters()
            for filter_name, params in filters:
                # this line is modified for checking KeyError
                if filter_name in LITERALS_JBIG2_DECODE and "JBIG2Globals" in params.keys():
                    global_streams.append(params["JBIG2Globals"].resolve())

            if len(global_streams) > 1:
                msg = (
                    "There should never be more than one JBIG2Globals "
                    "associated with a JBIG2 embedded image"
                )
                raise ValueError(msg)
            if len(global_streams) == 1:
                input_stream.write(global_streams[0].get_data().rstrip(b"\n"))
            input_stream.write(image.stream.get_data())
            input_stream.seek(0)
            reader = JBIG2StreamReader(input_stream)
            segments = reader.get_segments()

            writer = JBIG2StreamWriter(fp)
            writer.write_file(segments)
        return name

    def _save_bmp(
        self,
        image: LTImage,
        width: int,
        height: int,
        bytes_per_line: int,
        bits: int,
    ) -> str:
        name = super()._save_bmp(image, width, height, bytes_per_line, bits)
        image_file_path = Path(self.outdir).joinpath(name)
        with Image.open(image_file_path) as image_pil:
            image_pil.load()
        if image_pil.mode == "RGB":
            # BGR -> RGB
            b, g, r = image_pil.split()
            image_pil = Image.merge("RGB", (r, g, b))
        image_pil.save(image_file_path)  # This will fix bad EOF in align32
        return name

    def _save_bytes(self, image: LTImage) -> str:
        """Save an image without encoding, just bytes"""

        name, path = self._create_unique_image_name(image, ".jpg")
        width, height = image.srcsize
        data = image.stream.get_data()

        if len(image.colorspace) == 1 and isinstance(
            image.colorspace[0],
            PDFObjRef,
        ):
            colorspace = self._resolve_recursively(image.colorspace[0])
        else:
            colorspace = self._resolve_recursively(image.colorspace)

        if colorspace[0] == PILImageWriter.INDEXED:
            num_channels = self._get_num_channels(colorspace[1])  # type: ignore
            indexed_colors = self._get_indexed_colors(
                colorspace[2],
                colorspace[3],  # type: ignore
                num_channels,
            )
            image_array = self._frombuffer_with_bits(data, image.bits)
            image_np = self._reshape_with_srcsize(image_array, image.srcsize)
            image_np = indexed_colors[image_np]
            image_pil = Image.fromarray(image_np[:, :width])
        else:
            num_channels = self._get_num_channels(colorspace)  # type: ignore
            mode: Literal["1", "L", "RGB", "CMYK"]
            if image.bits == 1:
                mode = "1"
            elif image.bits == 8 and num_channels == 1:
                mode = "L"
            elif image.bits == 8 and num_channels == 3:
                mode = "RGB"
            elif image.bits == 8 and num_channels == 4:
                mode = "CMYK"
            else:
                raise NotImplementedError(
                    f"does not support bits={image.bits}" " in pre-checking Image.frombytes"
                )
            image_pil = Image.frombytes(mode, (width, height), data, "raw")

        with open(path, "wb") as fp:
            image_pil.save(fp)

        return name

    def _resolve_recursively(self, object_to_resolve):
        if isinstance(object_to_resolve, PDFObjRef):
            object_to_resolve = object_to_resolve.resolve()

        if isinstance(object_to_resolve, PDFStream):
            object_value = object_to_resolve.get_data()
        elif isinstance(object_to_resolve, dict):
            object_value = {
                k: self._resolve_recursively(
                    v,
                )
                for k, v in object_to_resolve.items()
            }
        elif isinstance(object_to_resolve, list):
            object_value = [
                self._resolve_recursively(
                    v,
                )
                for v in object_to_resolve
            ]
        else:
            object_value = object_to_resolve

        return object_value

    def _get_num_channels(self, colorspace: PSLiteral | list):
        if (
            isinstance(
                colorspace,
                PSLiteral,
            )
            and colorspace in PREDEFINED_COLORSPACE
        ):
            num_channels = PREDEFINED_COLORSPACE[colorspace].ncomponents  # type: ignore
        elif isinstance(colorspace, list) and colorspace[0] == LIT("ICCBased"):
            icc_profile = ImageCms.core.profile_frombytes(colorspace[1])
            if icc_profile.xcolor_space == "GRAY":
                num_channels = 1
            elif icc_profile.xcolor_space == "CMYK":
                num_channels = 4
            else:
                num_channels = 3
        else:
            num_channels = 3
        return num_channels

    def _get_indexed_colors(self, max_index: int, data: bytes, num_channels: int = 3) -> np.ndarray:
        array = np.frombuffer(data, dtype=np.uint8)
        indexed_colors = array[: num_channels * (max_index + 1)].reshape(-1, num_channels)
        return indexed_colors

    def _frombuffer_with_bits(self, data: bytes, bits: int) -> np.ndarray:
        if bits == 8:
            array = np.frombuffer(data, dtype=np.uint8)
            return array
        elif bits == 4:
            array = np.frombuffer(data, dtype=np.uint8)
            return np.stack([array >> 4, array & 0x0F], axis=1).reshape(-1)
        else:
            raise NotImplementedError(
                f"does not support bits={bits} in _decode_image",
            )

    def _reshape_with_srcsize(
        self,
        image_array: np.ndarray,
        srcsize: Tuple[int, int],
    ):
        width, height = srcsize
        if image_array.size % height != 0:
            logging.warning(
                f"misalignment size={image_array.size} width={width} height={height}"  # noqa
            )
            image_array = image_array[: (image_array.size // height * height)]
        image_np = image_array.reshape(height, -1)
        image_np = image_np[:, :width]
        return image_np
