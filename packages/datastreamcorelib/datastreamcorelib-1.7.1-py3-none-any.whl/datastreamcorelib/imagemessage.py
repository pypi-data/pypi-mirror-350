"""Image message types"""

import uuid
import math
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .abstract import TooFewPartsError
from .binpackers import msgpack_unpack
from .datamessage import BaseDataMessage, PubSubDataMessage

LOGGER = logging.getLogger(__name__)


class ImgFormatError(RuntimeError):
    """Image format errors"""


class MissingImgAttributeError(ImgFormatError):
    """Somthing is missing"""


@dataclass
class BaseImageMessage(BaseDataMessage):  # pylint: disable=W0223
    """
    Baseclass for image messages (extension to DataMessages)

    These are DataMessages with extra part for the image and well-known
    key in the data part for the image format data.

        data["imginfo"] = {
            "format": "bgr8",  # Some well known string, mono8 would be another example
            "bpp": 8,  # *bits* per pixel, assumed to be byte-aligned if not 8 (ie 12bits means 2 bytes/pixel/ch)
            "ch": 3,  # Number of channels, for mono8 this would be 1
            "w": 800,  # Width, pixels
            "h": 600,  # Height, pixels
            "compressed": False,  # Optional: if the format is compressed set to True, for example if format="png".
        }

    The bpp,ch,w and h are used for crude sanity-checking for uncompressed data, for compressed data a method
    named sanity_check_{format} SHOULD be defined (warning will be logged if it's not available).
    The check method must raise a ImgFormatError (or subclass thereof) or return None."""

    imginfo: Dict[str, Any] = field(compare=False, default_factory=dict)
    imgdata: bytes = field(default=b"", repr=False)

    def __post_init__(self) -> None:
        """Auto-decode dataparts from init."""
        super().__post_init__()
        if "imginfo" not in self.data:
            self.data["imginfo"] = {
                "format": "bgr8",
                "bpp": 8,  # bits not bytes
                "ch": 3,
                "w": 0,
                "h": 0,
            }
        self.imginfo = self.data["imginfo"]

    def sanity_check_imgdata(self) -> None:
        """Quick sanity-check the rawimg is at least in theory parseable"""
        if "format" not in self.imginfo or not self.imginfo["format"]:
            raise MissingImgAttributeError("Format not defined")
        checkmethodname = "sanity_check_{}".format(self.imginfo["format"])
        try:
            checkmethod = getattr(self, checkmethodname)
            # Method found, use it and skip rest of this method
            checkmethod()
            return
        except AttributeError:
            checkmethod = None

        if "compressed" in self.imginfo and self.imginfo["compressed"] and not checkmethod:
            # Compressed images must have a handler method for checking them.
            LOGGER.warning(
                "Cannot sanity-check, {} method not available".format(checkmethodname)  # pylint: disable=W1202
            )
            return

        for propkey in ("bpp", "ch", "w", "h"):
            if propkey not in self.imginfo or not self.imginfo[propkey]:
                raise ImgFormatError("{} not defined (or is empty)".format(propkey))

        bytes_pp = math.ceil(self.imginfo["bpp"] / 8)
        expected_len = bytes_pp * self.imginfo["ch"] * self.imginfo["w"] * self.imginfo["h"]
        if len(self.imgdata) != expected_len:
            LOGGER.debug("self.imginfo={}".format(self.imginfo))  # pylint: disable=W1202
            raise ImgFormatError("imgdata size ({}) does not match expected {}".format(len(self.imgdata), expected_len))


@dataclass
class PubSubImageMessage(BaseImageMessage, PubSubDataMessage):
    """
    Image messages handled via pub/sub (extension to PubSubDataMessage)

    The raw wire format for multipart is as follows:

        - topic: UTF-8 encoded string
        - message-id: UUIDv4 as binary
        - message-data: msgpack binary
          - This must contain "imginfo" key that defines how the image part is handled
            see BaseImageMessage for details
        - image-data: The actual image data, imginfo in the data dict defines how this is to be decoded.

    Rest of the parts are stored in the dataparts array and subclasses might do something
    with them but you should not access the dataparts array from outside or very unexpected results
    will follow."""

    @classmethod
    def zmq_decode(cls, raw_parts: List[bytes]) -> "PubSubImageMessage":
        """Decode raw message into class instance."""
        if len(raw_parts) < 4:
            raise TooFewPartsError("Need at least 4 message parts to decode into PubSubImageMessage")

        # Fail early for missing data
        decoded_data = msgpack_unpack(raw_parts[2])
        if "imginfo" not in decoded_data:
            raise MissingImgAttributeError("imginfo not defined in message-data")

        instance = cls(
            topic=raw_parts[0],
            dataparts=raw_parts[1:],
            messageid=uuid.UUID(bytes=raw_parts[1]),
            data=decoded_data,
            imgdata=raw_parts[3],
            _skip_auto_unpack=True,
        )
        # Sanity-check the image data
        instance.sanity_check_imgdata()
        return instance

    def zmq_encode(self) -> List[bytes]:
        """Encode for ZMQ transmission, pass this to socket.send_multipart."""
        # Make sure we're trying to send something sane
        self.sanity_check_imgdata()
        # Make sure underlying arrays are at least as big as needed
        if len(self.dataparts) < 3:
            self.dataparts = [b"", b"", b""]
        # Make sure imginfo is in data-part
        self.data["imginfo"] = self.imginfo
        self.dataparts[2] = self.imgdata
        return super().zmq_encode()
