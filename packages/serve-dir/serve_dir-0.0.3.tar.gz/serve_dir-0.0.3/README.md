# ServeDir 🚀

A lightweight, feature-rich HTTP server for serving directories with **byte-range support**, **CGI scripting**, and **multi-threading**.

Perfect for:  
✔ Local development  
✔ Sharing files quickly  
✔ Testing large file downloads  
✔ Serving static websites

---

## Features ✨

✅ **Directory Listing** – Clean HTML interface with navigation links.  
✅ **Byte-Range Support** – Partial downloads & streaming (`Range` header).  
✅ **CGI Support** – Execute scripts with `--cgi`.  
✅ **Multi-Threaded** – Handles concurrent requests efficiently.  
✅ **Configurable** – Custom port, bind address, and root directory.  
✅ **Segment Support** – Serve split/partial files (e.g., `.parts.json`).

## ☕ Support

If you find this project helpful, consider supporting me:

## [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B01E8SY7)

## Usage 🛠

### Basic Command

```sh
python -m serve_dir [DIR]  # Serve current dir (or DIR) on http://0.0.0.0:8058
```

### Options

| Flag           | Description                       | Default       |
| -------------- | --------------------------------- | ------------- |
| `-p`, `--port` | Port to listen on.                | `8058`        |
| `-b`, `--bind` | Bind address (e.g., `127.0.0.1`). | `0.0.0.0`     |
| `--byte-range` | Enable byte-range support.        | `None` (auto) |
| `--cgi`        | Enable CGI script execution.      | `None` (auto) |

### Examples

1. **Serve a specific directory on port 9000**:
   ```sh
   python -m serve_dir /path/to/files -p 9000
   ```
2. **Enable byte-range support for media streaming**:
   ```sh
   python -m serve_dir --byte-range
   ```
3. **Bind to localhost only**:
   ```sh
   python -m serve_dir -b 127.0.0.1
   ```

## Segment Support 🔗

ServeDir includes **built-in support for segmented files**, making it ideal for serving large files split into smaller parts (e.g., downloads, media, or backups).

### How It Works

- **Detects segmented files** automatically (e.g., `.parts.json` metadata files).
- **Seamlessly stitches parts** when requested, acting like a single file.
- **Supports byte-range requests** even across segments (e.g., streaming partial content).

### Use Cases

- **Large file downloads**: Split a 10GB file into manageable chunks, but serve it as one.
- **Resumable transfers**: Byte-range support works across segments.
- **Bandwidth efficiency**: Clients download only the needed segments.

### Example: Serving Segmented Files

1. **Prepare segments**:  
   Split a file (e.g., `bigfile.zip`) into parts and create a `bigfile.parts.json.zip` manifest:
   ```json
   {
     "length": 1024000000, // Total file size
     "parts": [
       [0, 1000000, "bigfile.zip.001"], // [start,  start+size, path]
       [1000000, 1999999, "bigfile.zip.002"]
     ]
   }
   ```
2. **Serve**:  
   Place all parts + `bigfile.parts.json.zip` in your directory. ServeDir will handle the rest!
   ```sh
   python -m serve_dir /path/to/segmented_files --byte-range
   ```
3. **Clients see one file**:  
   Requests to `bigfile.parts.json.zip` will transparently combine segments.

---

## Why Not Just `python -m http.server`? 🤔

This project extends Python’s built-in server with:  
🔹 **Better performance** (threaded requests).  
🔹 **Byte-range support** (e.g., for video streaming).  
🔹 **Nicer directory listings** (with HTML/CSS).  
🔹 **CGI scripting** out of the box.  
🔹 **Segment File Support** Serve split/partial files.
