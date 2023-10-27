# Calibre Rename PNG Utility

## Description

this project was created to assist in creating png files to bundle them into a cbz file for calibre.

## Using Utility

calibre can convert pdf manga pages into zip of individual jpg. Once the jpgs are created.

1. add the jpgs into the `images_in` directory
2. set the `.env` with the credentials for calibre to process; the images by default have the format of `<story name> - c<chapter number> - p<page number>.png`

3. run the utility using the `main.py` file

new png files will be created with the naming schema that can be then used to convert into cbz file for calibre to add as an ebook
