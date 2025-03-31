# AI-Powered Image Captioning App

A simple Flask-based web application that:
1. Uploads an image.
2. Generates an **English caption** using a pre-trained **BLIP** model from Salesforce.
3. Optionally **enhances** the generated caption using a **BART** transformer.
4. **Translates** the final caption into multiple languages via **Googletrans**.
5. Allows users to **download** the final caption as a text file.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration Details](#configuration-details)
- [Endpoints](#endpoints)
- [Possible Improvements](#possible-improvements)

---

## Features

1. **Image Captioning**: Uses the [BLIP model](https://github.com/salesforce/BLIP) (`Salesforce/blip-image-captioning-base`) to automatically generate an English caption from uploaded images.
2. **Caption Enhancement**: Optionally refines the caption for better readability and engagement using a [BART model](https://github.com/facebookresearch/bart) (`facebook/bart-large-cnn`).
3. **Translation**: Translates the final (original or enhanced) caption into a user-selected language (supported by [Googletrans](https://py-googletrans.readthedocs.io/)).
4. **Downloadable Captions**: Saves the translated caption as a text file, which can be downloaded by the user.

---

## Tech Stack

- **Python** (Flask)
- **[Pillow](https://pillow.readthedocs.io/)** for image handling
- **[Transformers](https://github.com/huggingface/transformers)** library by Hugging Face
  - BLIP model for image captioning
  - BART model for text enhancement
- **[Googletrans](https://py-googletrans.readthedocs.io/)** for language translation
- **HTML/CSS** (Jinja2 templates) for the front-end

---

## Prerequisites

1. **Python 3.7+** (recommended)
2. **pip** (for installing Python dependencies)
3. A **virtual environment** (optional but recommended)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>   ```
2. (Optional) Create a Virtual Environment:
   ```bash
   python -m venv venv 
   source venv/bin/activate  # On Windows: venv\Scripts\activate ```
3. Install Dependencies:
```bash
   pip install -r requirements.txt
```
Ensure you have the following libraries (included in requirements.txt):
- Flask
- Pillow
- torch
- transformers
- googletrans==4.0.0-rc1 (Version pinned due to potential compatibility issues)
(Any other relevant dependencies)

## Usage

1. Run the Flask App:
```bash
  python app.py
```
By default, the app starts in debug mode on http://127.0.0.1:5000 or http://localhost:5000.

2. Open the App:

- Go to http://localhost:5000 in your web browser.

- You’ll see a simple interface to upload your image, select a target language, and opt for caption enhancement.

3. Upload an Image:

- Select an image file using the form.

- Choose a Language for translation (e.g., English, Spanish, French, etc.).

- Check the Enhance box if you want to use the BART model to refine your caption.

- Click Submit.

4. View and Download Caption:

- The page displays the Generated Caption, Enhanced Caption, and Translated Caption.

- You can click the Download Caption link to save the translated caption as a text file.

## File Structure
```php
.
├─ app.py                 # Main Flask application
├─ requirements.txt       # Python dependencies
├─ static
│   ├─ uploads            # Uploaded images are stored here
│   └─ captions           # Generated/translated caption text files are stored here
├─ templates
│   └─ index.html         # Front-end page for uploading & displaying captions
└─ README.md              # This README file
```
## Configuration Details
- UPLOAD_FOLDER (static/uploads): Where uploaded images are saved.

- CAPTION_FOLDER (static/captions): Where caption text files are saved.

- BLIP Model: Loaded from Salesforce/blip-image-captioning-base.

- BART Model: Loaded from facebook/bart-large-cnn (used for text enhancement).

- Googletrans: Provides translation support.

- LANGUAGES dictionary in app.py defines supported languages:

```python
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "zh-cn": "Chinese (Simplified)",
    "hi": "Hindi",
    "ar": "Arabic",
}
```
Make sure you have a stable internet connection for the Googletrans API calls to succeed (if required).

The script automatically creates the uploads and captions directories if they don’t exist.

## Endpoints

| Endpoint                     | Methods      | Description                                                                                                                          |
|-----------------------------|--------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `/`                         | GET, POST    | **GET**: Renders the home page with upload form. <br> **POST**: Handles image upload, captioning, optional enhancement, and translation. |
| `/download_caption/<file>`  | GET          | Returns the caption `.txt` file for download.                                                                                       |


## Possible Improvements
- Model Customization: Fine-tune BLIP or BART for specific domains (e.g., product images, specific vocabulary).

- Advanced Translations: Implement offline translation or alternative translation services for better reliability.

- Caching / Database: Store past captions in a database to avoid regenerating them for the same image.

- Containerization: Deploy using Docker for easy environment management.

- Authentication: Add user accounts to track usage or save personal libraries of images/captions.
