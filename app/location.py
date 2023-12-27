"""Location dataclass."""
from dataclasses import dataclass


@dataclass
class Location:
    """Defines an object for checking location current time by its timezone

    Parameters:
        city(str):
            City name. You're free to decide the string format
            as it will only used for presentation.
        timezone(str):
            Pytz timezone name. Check here
            https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
            for a full list.
    """

    city: str
    timezone: str
