# Media Utility API

## Description

This project provides a Flask-based API for renaming, organizing, and managing media files, with a focus on preparing content for use with Jellyfin. It supports operations such as renaming files to Jellyfin conventions, creating comic volumes, and cleaning up filenames.

## Features

- **Rename Media Files**:

  - Rename video and comic files to Jellyfin-compatible naming conventions.
  - Clean up filenames by removing clutter and standardizing formats.

- **Volume Management**:

  - Organize chapters into volumes based on user-defined mappings.
  - Automatically create volume folders and move corresponding chapter files.
  - Re-zip chapters into single volume files.

- **API Endpoints**:
  - `/rename/process` (POST): Rename files based on a provided mapping.
  - `/rename/videos` (POST): Upload and rename video files for Jellyfin.
  - `/rename/comics` (POST): Upload and rename comic files for Jellyfin.
  - `/rename/read` (GET): List files available for renaming.
  - `/rename/push` (GET): Push files to a shared/output folder.
  - `/rename/delete` (POST): Delete a specified file.
  - `/manage/volumes` (POST): Create comic volumes from uploaded chapters and a volume mapping.

## Usage

1. **Start the API**  
   Run the Flask app with:

   ```
   python media_utility.py
   ```

2. **API Requests**  
   Use tools like `curl` or Postman to interact with the endpoints.  
   For example, to create volumes:

   ```
   POST /manage/volumes
   Form Data:
     - story title: <Your Story Title>
     - volume mapping: <JSON mapping of volumes to chapters>
     - files: <Upload chapter files>
   ```

3. **Environment Variables**
   - Set `PROCESS_DIRECTORY` in your environment or `.env` file to specify the working directory for uploads and processing.

## Requirements

- Python 3.10+
- Flask
- Pillow
- python-dotenv
- marshmallow-dataclass

## Development

- All core logic is in the `src/` directory.
- Tests are in the `test/` directory and use `pytest`.

## License

MIT
