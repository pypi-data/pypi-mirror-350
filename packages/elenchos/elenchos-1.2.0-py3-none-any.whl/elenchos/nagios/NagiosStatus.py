from enum import Enum


class NagiosStatus(Enum):
    """
    The possible statuses of a Nagios elenchos.
    """

    # ------------------------------------------------------------------------------------------------------------------
    OK = 0
    """
    Status OK.
    """

    WARNING = 1
    """
    Status warning.
    """

    CRITICAL = 2
    """
    Status critical.
    """

    UNKNOWN = 3
    """
    Status unknown.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def worst(self, status):
        """
        Returns the worst status of this status and another status.

        :param status: The other status.
        """
        if self.value < status.value:
            return status

        return self

# ----------------------------------------------------------------------------------------------------------------------
