#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Tags and set of it.

Used by optimization to keep track of the current state of optimization, these
tags trigger the execution of optimization steps, which in turn may emit these
tags to execute other steps.

"""

allowed_tags = (
    # New code means new statements.
    # Could be an inlined exec statement.
    "new_code",
    # Added new import.
    "new_import",
    # New statements added, removed.
    "new_statements",
    # New expression added.
    "new_expression",
    # Loop analysis is incomplete, or only just now completed.
    "loop_analysis",
    # TODO: A bit unclear what this it, potentially a changed variable.
    "var_usage",
    # Detected module variable to be read only.
    "read_only_mvar",
    # Trusting module variables in functions.
    "trusted_module_variables",
    # New built-in reference detected.
    "new_builtin_ref",
    # New built-in call detected.
    "new_builtin",
    # New raise statement detected.
    "new_raise",
    # New constant introduced.
    "new_constant",
)


class TagSet(set):
    def onSignal(self, signal):
        if type(signal) is str:
            signal = signal.split()

        for tag in signal:
            self.add(tag)

    def check(self, tags):
        for tag in tags.split():
            assert tag in allowed_tags, tag

            if tag in self:
                return True
        return False

    def add(self, tag):
        assert tag in allowed_tags, tag

        set.add(self, tag)



