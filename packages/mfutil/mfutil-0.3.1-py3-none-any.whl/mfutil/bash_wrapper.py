import bash


class BashWrapperException(Exception):
    """Specific exception class for BashWrapper objects."""

    __message = None
    __bash_wrapper = None

    def __init__(self, message, bash_wrapper=None):
        """Constructor.

        Args:
            message (string): exception message
            bash_wrapper (BashWrapper): bash wrapper object

        """
        super(BashWrapperException, self).__init__(message)
        self.__message = message
        self.__bash_wrapper = bash_wrapper

    def __repr__(self):
        if self.__bash_wrapper is not None:
            return "%s exception with message: %s and debug: %s" % \
                (self.__class__.__name__, self.__message, self.__bash_wrapper)
        else:
            return Exception.__repr__(self)

    def __str__(self):
        return self.__repr__()


class BashWrapper(object):
    """Bash command/output wrapper."""

    __bash_cmd = None
    __bash_result_object = None

    def __init__(self, bash_cmd):
        """Constructor.

        The constructor executes the given bash command and store result code
        and stdout/stderr inside the object.

        You can use this object like this::

            bash_wrapper = BashWrapper("ls /tmp")
            if bash_wrapper:
                print("execution was ok (status_code == 0)")
            else:
                print("execution was not ok (status_code != 0)")
            status_code = bash_wrapper.code
            stdout_output = bash_wrapper.stdout
            stderr_output = bash_wrapper.stderr
            print("full representation with command/code/stdout/stderr: %s" %
                  bash_wapper)

        Args:
            bash_cmd (string): complete bash command to execute.

        """
        self.__bash_cmd = bash_cmd
        self.__bash_result_object = bash.bash(bash_cmd)

    def __bool__(self):
        return (self.__bash_result_object.code == 0)

    def __nonzero__(self):
        # python2 compatibility
        return self.__bool__()

    @property
    def code(self):
        """Return the status code of the command as int (0 => ok)."""
        return self.__bash_result_object.code

    @property
    def stdout(self):
        """Return the stdout output of the command stripped and utf8 decoded.

        Returns:
            (string) stdout output (stripped and utf8 decoded).

        """
        return self.__bash_result_object.stdout.strip().decode('UTF-8')

    @property
    def stderr(self):
        """Return the stderr output of the command stripped and utf8 decoded.

        Returns:
            (string) stderr output (stripped and utf8 decoded).

        """
        return self.__bash_result_object.stderr.strip().decode('UTF-8')

    def __repr__(self):
        result = []
        result.append("")
        result.append("===== BASH COMMAND =======================")
        result.append(self.__bash_cmd)
        result.append("===== BASH RETURN CODE ===================")
        result.append(str(self.code))
        stdout = self.stdout
        if stdout and len(stdout) > 0:
            result.append("===== BASH STDOUT ========================")
            result.append(self.stdout)
        stderr = self.stderr
        if stderr and len(stderr) > 0:
            result.append("===== BASH STDERR ========================")
            result.append(self.stderr)
        return "\n".join(result)


class BashWrapperOrRaise(BashWrapper):
    """BashWrapper subclass which raise an exception if status_code != 0."""

    def __init__(self, bash_cmd, exception_class=BashWrapperException,
                 exception_msg="bad return code"):
        """Constructor.

        The constructor executes the given bash command and store result code
        and stdout/stderr inside the object.

        If the status_code is != 0, an exception is raised with all
        informations (stdout/stderr/code) inside.

        If the status_code is 0, you can use this object like a BashWrapper
        one.

        Example::

            try:
                x = BashWrapperOrRaise("ls /foo/bar")
            except BashWrapperException as e:
                print("exception with all details: %s" % e)
            else:
                # here, we have x.code == 0
                print("stdout: %s" % x.stdout)

        Args:
            bash_cmd (string): complete bash command to execute.
            exception_class (BashWrapperException): exception class to raise
                in case of status_code !=0 (must be a subclass of
                BashWrapperException).
            exception_msg (string): exception message in case of
                status_code != 0.

        """
        super(BashWrapperOrRaise, self).__init__(bash_cmd)
        if self.code != 0:
            raise exception_class(exception_msg, self)
