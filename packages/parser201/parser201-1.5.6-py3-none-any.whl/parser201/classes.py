"""LogParser Class."""

import datetime as dt
import re
from enum import Enum
from enum import auto
from typing import Union


class TZ(Enum):
    """Timestamp adjustment enum.

    Enum to determine the timezone adjustment of the timestamp property
    of a `LogParser` object.
    """

    original = auto()
    """Keep the original timezone from the log data."""
    utc = auto()
    """Convert the timezone from the log data to UTC."""

    def __eq__(self, other) -> bool:
        """Compare the values of two TZ Enums.

        Parameters
        ----------
        other : Any
            The right-hand side of the equality comparison.

        Returns
        -------
        bool
            True if two TZ Enums are equal, False otherwise.
        """
        return self.value == other.value


class FMT(Enum):
    """Timestamp format enum.

    Enum to determine the format for the timestamp attribute of a
    `LogParser` object.
    """

    string = auto()
    """Store the timestamp as a string."""
    date_obj = auto()
    """Store the timestamp as a python date-time object."""

    def __eq__(self, other) -> bool:
        """Compare the values of two FMT Enums.

        Parameters
        ----------
        other : Any
            The right-hand side of the equality comparison.

        Returns
        -------
        bool
            True if two FMT Enums are equal, False otherwise.
        """
        return self.value == other.value


class LogParser:
    """Base class of all LogParser objects.

    LogParser objects are created using the class initializer, discussed
    below.
    """

    # Class variables

    # Behold the power of generative AI. I provided the following query
    # to ChatGPT: "Write a regular expression that recognizes a line
    # from an apache access log". I had to have a "conversation" with
    # ChatGPT to refine the regex with a few examples, but after a brief
    # exchange, it produced what you see below. This regex cleaned up my
    # previous solution and replace several lines of code. I split the
    # regex into individual match groups here to make it easier to
    # follow.
    _ip = r"^([^ ]+)"
    _ui = r"(\S+)"
    _un = r"(\S+)"
    _ts = r"\[([^\]]+)\]"
    _rl = r'"(.*?)"'
    _sc = r"(\d{3})"
    _ds = r"(\S+)"
    _re = r'"((?:[^"]|\")*?)"'
    _ua = r'"((?:[^"]|\")*?|-)"'
    _regex = rf"{_ip} {_ui} {_un} {_ts} {_rl} {_sc} {_ds} {_re} {_ua}"

    # A list of labels (in the correct order) used to render string
    # representations of LogParser objects. Also calculate the length of
    # the longest label so we can use f-strings to right-justify all the
    # labels.
    _labels = [
        "ipaddress",
        "userid",
        "username",
        "timestamp",
        "requestline",
        "statuscode",
        "datasize",
        "referrer",
        "useragent",
    ]
    _pad = len(max(_labels, key=len))

    def __init__(
        self,
        line,
        timezone=TZ.original,
        dts_format=FMT.string,
    ) -> None:
        """Initialize a LogParser object.

        The class initializer takes a single line (as a string) from an
        Apache access log file and extracts the individual fields into
        attributes within an object. Parameters to the initializer are
        discussed below.

        Parameters
        ---------
        line : str
            A single line from an Apache access log.
        timezone : TZ, optional
            During parsing, adjust the timestamp of the `LogParser`
            object to match a particular timezone. Default is
            *TZ.original* (no adjustment). *TZ.utc* adjusts the
            timestamp to [UTC](https:\
            //en.wikipedia.org/wiki/Coordinated_Universal_Time), default
            is TZ.original.
        dts_format : FMT, optional
            Set the format of the date timestamp attribute of the
            `LogParser` object. Default is *FMT.string*. Using
            *FMT.date_obj* will store the timestamp attribute as a
            Python [datetime object](https:\
            //docs.python.org/3/library/datetime.html), default is
            FMT.string.

        Attributes
        ----------
        datasize : int
            The size of the response to the client (in bytes).
        ipaddress : str
            The remote host (the client IP).
        referrer : str
            The referrer header of the HTTP request containing the URL
            of the page from which this request was initiated. If none
            is present, this attribute is set to `-`.
        requestline : str
            The request line from the client. (e.g. `"GET / HTTP/1.0"`).
        statuscode : int
            The status code sent from the server to the client (`200`,
            `404`, etc.).
        timestamp : str | dt.datetime
            The date and time of the request in the following format:

            `dd/MMM/YYYY:HH:MM:SS –hhmm`

            NOTE: `-hhmm` is the time offset from Greenwich Mean Time
            (GMT). Usually (but not always) `mm == 00`. Negative offsets
            (`-hhmm`) are west of Greenwich; positive offsets (`+hhmm`)
            are east of Greenwich.
        useragent : str
            The browser identification string if any is present, and `-`
            otherwise.
        userid : str
            The identity of the user determined by `identd` (not usually
            used since not reliable). If `identd` is not present, this
            attribute is set to `-`.
        username : str
            The user name determined by HTTP authentication. If no
            username is present, this attribute is set to `-`.

        Examples
        --------
        Creating a `LogParser` object with default options. The
        timestamp attribute will not be adjusted and will be stored as a
        string.
        >>> from parser201 import LogParser
        >>> line = # a line from an Apache access log
        >>> lp = LogParser(line)

        Creating a `LogParser` object with custom options. The timestamp
        attribute will be adjusted to UTC and will be stored as a Python
        [datetime object](https:\
        //docs.python.org/3/library/datetime.html).
        >>> from parser201 import LogParser, TZ, FMT
        >>> line = # a line from an Apache access log
        >>> lp = LogParser(line, timezone=TZ.utc, dts_format=FMT.date_obj)
        """
        # Initialize data fields
        self.ipaddress: str = ""
        self.userid: str = ""
        self.username: str = ""
        self.timestamp: Union[str, dt.datetime] = ""
        self.requestline: str = ""
        self.statuscode: int = 0
        self.datasize: int = 0
        self.referrer: str = ""
        self.useragent: str = ""

        if type(line) is not str:
            self.__none_fields()
            return

        if groups := re.match(LogParser._regex, line):
            self.ipaddress = groups.group(1)
            self.userid = groups.group(2)
            self.username = groups.group(3)
            self.timestamp = groups.group(4)
            self.requestline = groups.group(5)
            self.statuscode = int(groups.group(6))
            try:
                self.datasize = int(groups.group(7))
            except ValueError:
                self.datasize = 0
            self.referrer = groups.group(8)
            self.useragent = groups.group(9)
        else:
            self.__none_fields()
            return

        # This takes the work of ensuring valid date-time stamps from
        # the regex and guarantees things like "Feb 31" will be handled
        # as an invalid date.
        try:
            date_obj = dt.datetime.strptime(
                str(self.timestamp),
                "%d/%b/%Y:%H:%M:%S %z",
            )
        except ValueError:
            self.__none_fields()
            return

        if timezone == TZ.utc:
            date_obj = date_obj.astimezone(dt.timezone.utc)

        if dts_format == FMT.string:
            self.timestamp = date_obj.strftime("%d/%b/%Y:%H:%M:%S %z")
        else:  # dts_format == FMT.date_obj
            self.timestamp = date_obj

        return

    def __none_fields(self) -> None:
        """Set all properties to None."""
        for key in vars(self):
            setattr(self, key, None)
        return

    def __str__(self) -> str:
        """`LogParser` class str method.

        The class provides a `__str__` method which renders a
        `LogParser` object as string suitable for display.

        Examples
        --------
        Create a `LogParser` object like this:

        >>> from parser201 import LogParser
        >>> line = # a line from an Apache access log
        >>> lp = LogParser(line)

        When you print it, the following is displayed:

        >>> print(lp)
          ipaddress: 81.48.51.130
             userid: -
           username: -
          timestamp: 24/Mar/2009:18:07:16 +0100
        requestline: GET /images/puce.gif HTTP/1.1
         statuscode: 304
           datasize: 2454
           referrer: -
          useragent: Mozilla/4.0 compatible; MSIE 7.0; Windows NT 5.1;
        """
        lp_str = []
        for label in LogParser._labels:
            lp_str.append(f"{label:>{LogParser._pad}}: {getattr(self, label)}")
        return "\n".join(lp_str)

    def __eq__(self, other) -> bool:
        """Determine if two `LogParser` objects are equal.

        The class provides a `__eq__` method to test for equality
        between two `LogParser` objects.

        Parameters
        ----------
        other : Any
            An object used for comparison (the right-hand side of ==).

        Returns
        -------
        bool
            True it two `LogParser` objects are equal, False otherwise.
        """
        if type(self) is not type(other):
            return False
        return vars(self) == vars(other)


if __name__ == "__main__":
    pass
