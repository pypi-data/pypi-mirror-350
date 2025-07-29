from enum import Enum


class IncludeInDescription(Enum):
    """
    The possible values to include performance data in the description.
    """

    # ------------------------------------------------------------------------------------------------------------------
    ALWAYS = 1
    """
    Always add the performance data to the description.
    """

    WARNING = 2
    """
    Only add the performance data to the description when the status of the performance data is warning or critical.
    """

    CRITICAL = 3
    """
    Only add the performance data to the description when the status of the performance data is critical.
    """

    NEVER = 4
    """
    Never add the performance data to the description.
    """

# ----------------------------------------------------------------------------------------------------------------------
