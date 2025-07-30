# This file is part of beets.
# Copyright 2016, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Allows inline path template customization code in the config file."""

import itertools
import traceback

from beets import config
from beets.plugins import BeetsPlugin

# Name for function in compiled code to make code callable
FUNC_NAME = "__INLINE_FUNC__"


class InlineError(Exception):
    """Raised when a runtime error occurs in an inline expression."""

    def __init__(self, code, exc):
        super().__init__(
            ("error in inline path field code:\n%s\n%s: %s")
            % (code, type(exc).__name__, str(exc))
        )


def _compile_func(body):
    """Given Python code for a function body, return a compiled
    callable that invokes that code.
    """
    body = "def {}():\n    {}".format(FUNC_NAME, body.replace("\n", "\n    "))
    code = compile(body, "inline", "exec")
    env = {}
    eval(code, env)
    return env[FUNC_NAME]


class InlinePlugin(BeetsPlugin):

    def __init__(self):
        super().__init__()

        config.add(
            {
                "fields_base": None,
                "pathfields": {},  # Legacy name.
                "item_fields": {},
                "album_fields": {},
            }
        )

        # Common snippet
        self.fields_base = config["fields_base"].get()
        if self.fields_base:
            # Test compile to get errors early
            self._log.debug("adding common snippet")
            try:
                env = {}
                exec(self.fields_base, env)
            except SyntaxError:
                self._log.error(
                    "syntax error in inline field definition for 'fields_base':\n{0}",
                    traceback.format_exc(),
                )
                return

        # Item fields.
        for key, view in itertools.chain(
            config["item_fields"].items(), config["pathfields"].items()
        ):
            self._log.debug("adding item field {0}", key)
            func = self.compile_inline(view.as_str(), self.fields_base, False)
            if func is not None:
                self.template_fields[key] = func

        # Album fields.
        for key, view in config["album_fields"].items():
            self._log.debug("adding album field {0}", key)
            func = self.compile_inline(view.as_str(), self.fields_base, True)
            if func is not None:
                self.album_template_fields[key] = func

    def compile_inline(self, python_code, common_snippet, album):
        """Given a Python expression or function body `python_code`,
        compile it together with the `common_snippet` as a path field
        function. The returned function takes a single argument, an Item,
        and returns a Unicode string. If the expression cannot be compiled,
        then an error is logged and this function returns None.
        """

        def _dict_for(obj):
            """Helper to create dict from item object or album object"""
            out = dict(obj)
            if album:
                out["items"] = list(obj.items())
            return out

        # If we have a common snippet it has to be
        # First, try compiling as a single function.
        try:
            code = compile(f"({python_code})", "inline", "eval")
        except SyntaxError:
            # Fall back to a function body.
            try:
                func = _compile_func(python_code)
            except SyntaxError:
                field_type = "album_fields" if album else "item_fields"
                self._log.error(
                    "syntax error in inline field definition for '{1}':\n{0}",
                    (traceback.format_exc(), field_type)
                )
                return
            else:
                is_expr = False
        else:
            is_expr = True

        if is_expr:
            # For expressions, just evaluate and return the result.
            def _expr_func(obj):
                values = _dict_for(obj)
                try:
                    if common_snippet:
                        exec(common_snippet, values)
                    return eval(code, values)
                except Exception as exc:
                    raise InlineError(python_code, exc)

            return _expr_func
        else:
            # For function bodies, invoke the function with values as global
            # variables.
            def _func_func(obj):
                old_globals = dict(func.__globals__)
                try:
                    values = _dict_for(obj) 
                    if common_snippet:
                        exec(common_snippet, values)
                    func.__globals__.update(values)
                    return func()
                except Exception as exc:
                    raise InlineError(python_code, exc)
                finally:
                    func.__globals__.clear()
                    func.__globals__.update(old_globals)

            return _func_func
