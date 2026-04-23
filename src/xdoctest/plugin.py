"""
The Pytest XDoctest Plugin
--------------------------

This file is registered as a pytest plugin when you install xdoctest. By
executing pytest with ``--xdoctest-modules`` (or simply ``--xdoctest``), this
plugin will be enabled. This also disables the original builtin doctest plugin.

When xdoctest is enabled, pytest will discover and run doctests in modules and
test files using xdoctest's improved parser and runtime environment.

To ensure maximum backwards compatibility with the original doctest module,
this code is heavilly based on ``pytest/_pytest/doctest.py`` plugin file in
https://github.com/pytest-dev/pytest

"""

from __future__ import annotations

import typing
from typing import cast

import pytest
from _pytest import fixtures
from _pytest._code import code

try:
    from packaging import version as _packaging_version
except ImportError:  # nocover
    from distutils import (
        version as _distutils_version,  # type: ignore[unresolved-import]
    )

    def _parse_version(version_text):
        return _distutils_version.LooseVersion(version_text)
else:

    def _parse_version(version_text):
        return _packaging_version.parse(version_text)


_PYTEST_IS_GE_620 = _parse_version(pytest.__version__) >= _parse_version(
    '6.2.0'
)
_PYTEST_IS_GE_800 = _parse_version(pytest.__version__) >= _parse_version(
    '8.0.0'
)


if _PYTEST_IS_GE_800:
    from typing import Any, Callable, Dict, TypeVar

    try:
        from typing import override
    except ImportError:  # nocover
        try:
            from typing_extensions import override
        except ImportError:  # nocover
            _F = TypeVar('_F', bound=Callable[..., object])

            def override(method: _F, /) -> _F:
                """Fallback no-op decorator when typing override helpers are unavailable."""
                pass

    from _pytest.fixtures import TopRequest


# Ban-list: extend if other plugins are known to break `xdoctest`
_INCOMPATIBLE_PLUGINS = frozenset({'doctest'})


# def print(text):
#     """ Hack so we can get stdout when debugging the plugin file """
#     import os
#     fpath = os.path.expanduser('~/plugin.stdout.txt')
#     with open(fpath, 'a') as file:
#         file.write(str(text) + '\n')


def pytest_configure(config) -> None:
    pass


def pytest_addoption(parser) -> None:
    # TODO: make this programmatically mirror the argparse in __main__
    pass


if pytest.__version__ < '7.':  # nocover

    def pytest_collect_file(path, parent):
        pass

    def _suffix(path):
        pass

    def _match(path, glob):
        pass

else:

    def pytest_collect_file(file_path, parent):
        pass

    def _suffix(path):
        pass

    def _match(path, glob):
        pass


def _pytest_collect_file(file_path, parent, **path_args):
    pass


def _is_xdoctest(config, path, parent):
    pass


class ReprFailXDoctest(code.TerminalRepr):
    def __init__(self, reprlocation: typing.Any, lines: list[str]) -> None:
        """
        Args:
            reprlocation (Any):
                _pytest._code.code.ReprFileLocation where the error happened
            lines (List[str]): text of the error
        """
        self.reprlocation = reprlocation
        self.lines = lines

    def toterminal(self, tw) -> None:
        pass


class XDoctestItem(pytest.Item):
    def __init__(
        self,
        name: str,
        parent: typing.Any,
        runner: typing.Any = None,
        dtest: typing.Any = None,
    ) -> None:
        """
        Args:
            name (str):
            parent (Any | None):
            dtest (xdoctest.doctest_example.DocTest):
        """
        super(XDoctestItem, self).__init__(name, parent)
        self.cls = XDoctestItem
        self.dtest = dtest
        self.obj = None
        if _PYTEST_IS_GE_800:
            # Stuff needed for fixture support in pytest > 8.0.
            fm = self.session._fixturemanager
            fixtureinfo = fm.getfixtureinfo(node=self, func=None, cls=None)
            self._fixtureinfo = fixtureinfo
            self.fixturenames = fixtureinfo.names_closure
            self._initrequest()
        else:
            self.fixture_request = None

    if _PYTEST_IS_GE_800:

        @classmethod
        @override
        def from_parent(
            cls,
            parent,
            name,
            runner=None,
            dtest=None,
        ):  # type: ignore
            # incompatible signature due to imposed limits on subclass
            """The public named constructor."""
            pass

    @property
    def example(self):
        """
        Backwards compatibility with older pytest versions
        """
        pass

    def _initrequest(self) -> None:
        pass

    def setup(self) -> None:
        if _PYTEST_IS_GE_800:
            self._request._fillfixtures()
            globs = dict(getfixture=self._request.getfixturevalue)
            for name, value in self._request.getfixturevalue(
                'xdoctest_namespace'
            ).items():
                globs[name] = value
            self.dtest.globs.update(globs)
        else:
            if self.dtest is not None:
                self.fixture_request = _setup_fixtures(self)  # type: ignore
                global_namespace = dict(
                    getfixture=self.fixture_request.getfixturevalue  # type: ignore
                )
                for name, value in self.fixture_request.getfixturevalue(  # type: ignore
                    'xdoctest_namespace'
                ).items():
                    global_namespace[name] = value
                self.dtest.global_namespace.update(global_namespace)

    def runtest(self) -> None:
        pass

    def repr_failure(self, excinfo):  # type: ignore
        """
        # Args:
        #     excinfo (_pytest._code.code.ExceptionInfo):

        # Returns:
        #     ReprFailXDoctest | str | _pytest._code.code.TerminalRepr:
        """
        dtest = self.dtest
        if dtest.exc_info is not None:
            lineno = dtest.failed_lineno()
            type = dtest.exc_info[0]
            message = type.__name__
            reprlocation = code.ReprFileLocation(dtest.fpath, lineno, message)
            lines = dtest.repr_failure()

            return ReprFailXDoctest(reprlocation, lines)
        else:
            return super(XDoctestItem, self).repr_failure(excinfo)

    def reportinfo(self) -> tuple[typing.Any, int | None, str]:
        """
        Returns:
            Tuple[str, int, str]
        """
        pass


class _XDoctestBase(pytest.Module):
    def _prepare_internal_config(self) -> None:
        pass


class XDoctestTextfile(_XDoctestBase):
    obj = None

    def collect(self) -> typing.Iterator[XDoctestItem]:
        """
        Yields:
            XDoctestItem
        """
        pass


class XDoctestModule(_XDoctestBase):
    def collect(self):
        pass


def _setup_fixtures(xdoctest_item: XDoctestItem) -> fixtures.FixtureRequest:
    """
    Used by XDoctestTextfile and XDoctestItem to setup fixture information.

    Args:
        xdoctest_item (XDoctestItem):

    Returns:
        fixtures.FixtureRequest
    """

    def func() -> None:
        pass

    xdoctest_item.funcargs = {}
    fm = xdoctest_item.session._fixturemanager
    xdoctest_item._fixtureinfo = fm.getfixtureinfo(
        node=xdoctest_item,
        func=func,
        cls=None,
        funcargs=False,  # type: ignore
    )
    # Note: FixtureRequest may change in the future, we are using
    # private functionality. Hopefully it wont break, but we should
    # check to see if there is a better way to do this
    # https://github.com/pytest-dev/pytest/discussions/8512#discussioncomment-563347
    if _PYTEST_IS_GE_620:
        # The "_ispytest" arg was added in 3.6.1
        fixture_request = fixtures.FixtureRequest(xdoctest_item, _ispytest=True)  # type: ignore
    else:
        fixture_request = fixtures.FixtureRequest(xdoctest_item)  # type: ignore
    fixture_request._fillfixtures()  # type: ignore
    return fixture_request


@pytest.fixture(scope='session')
def xdoctest_namespace() -> dict[str, object]:
    """
    Inject names into the xdoctest namespace.

    Returns:
        Dict
    """
    pass
