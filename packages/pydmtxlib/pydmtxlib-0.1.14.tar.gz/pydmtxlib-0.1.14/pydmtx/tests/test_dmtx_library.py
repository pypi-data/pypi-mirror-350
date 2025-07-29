# pylint: disable=missing-docstring
import unittest
from pathlib import Path
from unittest.mock import call, patch

from pydmtx import dmtx_library


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)
        self.cdll = patch("pydmtx.dmtx_library.cdll", autospec=True).start()
        self.find_library = patch(
            "pydmtx.dmtx_library.find_library", autospec=True
        ).start()
        self.platform = patch("pydmtx.dmtx_library.platform", autospec=True).start()
        self.windows_fname = patch(
            "pydmtx.dmtx_library._windows_fname",
            autospec=True,
            return_value="dll fname",
        ).start()

    def test_found_non_windows(self):
        self.platform.system.return_value = "Not windows"

        res = dmtx_library.load()

        self.platform.system.assert_called_once_with()
        self.find_library.assert_called_once_with("dmtx")
        self.cdll.LoadLibrary.assert_called_once_with(self.find_library.return_value)
        self.assertEqual(self.cdll.LoadLibrary.return_value, res)
        self.assertEqual(0, self.windows_fname.call_count)

    def test_not_found_non_windows(self):
        self.platform.system.return_value = "Not windows"
        self.find_library.return_value = None

        with self.assertRaises(ImportError):
            dmtx_library.load()

        self.platform.system.assert_called_once_with()
        self.find_library.assert_called_once_with("dmtx")

    def test_found_windows(self):
        self.platform.system.return_value = "Windows"

        res = dmtx_library.load()

        self.platform.system.assert_called_once_with()
        self.cdll.LoadLibrary.assert_called_once_with(self.windows_fname.return_value)
        self.assertEqual(self.cdll.LoadLibrary.return_value, res)

    def test_found_second_attempt_windows(self):
        self.platform.system.return_value = "Windows"
        self.cdll.LoadLibrary.side_effect = [
            OSError,  # First call fails
            "loaded library",  # Second call succeeds
        ]

        res = dmtx_library.load()

        self.platform.system.assert_called_once_with()
        self.cdll.LoadLibrary.assert_has_calls(
            [
                call(self.windows_fname.return_value),
                call(
                    str(
                        Path(dmtx_library.__file__).parent.joinpath(
                            self.windows_fname.return_value
                        )
                    )
                ),
            ]
        )
        self.assertEqual("loaded library", res)

    def test_not_found_windows(self):
        self.platform.system.return_value = "Windows"
        self.cdll.LoadLibrary.side_effect = OSError

        with self.assertRaises(OSError):
            dmtx_library.load()

        self.platform.system.assert_called_once_with()
        self.cdll.LoadLibrary.assert_has_calls(
            [
                call(self.windows_fname.return_value),
                call(
                    str(
                        Path(dmtx_library.__file__).parent.joinpath(
                            self.windows_fname.return_value
                        )
                    )
                ),
            ]
        )


class TestWindowsFname(unittest.TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)
        self.mock_sys = patch("pydmtx.dmtx_library.sys", autospec=True).start()
        self.mock_platform = patch(
            "pydmtx.dmtx_library.platform", autospec=True
        ).start()

    def test_32bit(self):
        self.mock_sys.maxsize = 2**32 - 1
        self.mock_platform.machine.return_value = "AMD64"
        self.assertEqual(dmtx_library._windows_fname(), "libdmtx-32.dll")

    def test_64bit(self):
        self.mock_sys.maxsize = 2**33
        self.mock_platform.machine.return_value = "AMD64"
        self.assertEqual(dmtx_library._windows_fname(), "libdmtx-64.dll")

    def test_arm64(self):
        self.mock_sys.maxsize = 2**33
        self.mock_platform.machine.return_value = "ARM64"
        self.assertEqual(dmtx_library._windows_fname(), "libdmtx-arm64.dll")


if __name__ == "__main__":
    unittest.main()
