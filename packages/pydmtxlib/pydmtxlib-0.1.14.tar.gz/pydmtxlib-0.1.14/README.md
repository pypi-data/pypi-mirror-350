# pydmtx 🐍📦

*Forked from [`pylibdmtx`](https://github.com/NaturalHistoryMuseum/pylibdmtx) 🔀*

Read and write Data Matrix barcodes in Python 3.8+ using the  
[`libdmtx`](http://libdmtx.sourceforge.net/) library. 🎯

---

## Features ✨

- 🐍 Pure Python interface for `libdmtx`  
- 🖼️ Supports PIL/Pillow images, OpenCV/numpy arrays, and raw bytes  
- 🔍 Decodes barcode data and locations  
- ⚙️ Minimal dependencies (only `libdmtx` native library required)  

## Installation 💻

### macOS 🍎

```bash
brew install libdmtx gettext
````

### Linux (Ubuntu/Debian) 🐧

```bash
sudo apt-get install libdmtx0t64
```

### Windows 🪟

Windows Python wheels include the required `libdmtx` DLLs.

### Python package 📦

```bash
pip install pydmtx
```

## Notes 📝

* ⚠️ On Windows, if you get import errors, install the Visual C++ Redistributable
* 🐍 Supports Python 3.8 and newer

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

The `libdmtx` shared library is distributed under its own license. Please refer to the `libdmtx` project for its license terms.