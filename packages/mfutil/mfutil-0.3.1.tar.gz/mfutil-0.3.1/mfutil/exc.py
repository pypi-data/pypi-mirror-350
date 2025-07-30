class MFUtilException(Exception):
    """Generic exception class with a way to wrap original exceptions.

    Very interesting reading about exceptions in Python:
    https://julien.danjou.info/python-exceptions-guide/

    Usage example:

    ```python
    from mfutil import MFUtilException

    try:
        1/0
    except Exception as e:
        raise MFUtilException("something was wrong", original_exception=e)
    ```

    Output example:
    ```
    [...]
    mfutil.exc.MFUtilException: something was wrong: division by zero
    ```

    """

    def __init__(self, msg=None, original_exception=None, **kwargs):
        """

        Args:
            msg (string): a custom message for this exception.
            original_exception (Exception): an Exception object to wrap.

        """
        if msg is not None:
            self.message = msg
        else:
            self.message = "mfplugin_exception"
        if original_exception is not None:
            Exception.__init__(
                self, self.message + (": %s" % original_exception), **kwargs
            )
        else:
            Exception.__init__(self, self.message, **kwargs)
