"""Utilities"""

from .datamessage import PubSubDataMessage, utctimestamp

try:
    import resource

    MODRESOURCE_AVAILABLE = True
except ImportError:
    MODRESOURCE_AVAILABLE = False

RESOURCE_KEYS = (
    "ru_utime",
    "ru_stime",
    "ru_maxrss",
    "ru_ixrss",
    "ru_idrss",
    "ru_isrss",
    "ru_minflt",
    "ru_majflt",
    "ru_nswap",
    "ru_inblock",
    "ru_oublock",
    "ru_msgsnd",
    "ru_msgrcv",
    "ru_nsignals",
    "ru_nvcsw",
    "ru_nivcsw",
)


def create_heartbeat_message() -> PubSubDataMessage:
    """Create a heartbeat message"""
    msg = PubSubDataMessage(b"HEARTBEAT")
    msg.data["systemtime"] = utctimestamp()
    if MODRESOURCE_AVAILABLE:
        rudata = resource.getrusage(resource.RUSAGE_SELF)
        msg.data["resources"] = {}
        for key in RESOURCE_KEYS:
            msg.data["resources"][key[3:]] = getattr(rudata, key)
    return msg
