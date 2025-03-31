import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
from googletrans import Translator

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
CAPTION_FOLDER = "static/captions"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CAPTION_FOLDER"] = CAPTION_FOLDER

# Ensure required directories persist
def ensure_directories():
    """Creates required directories if they don't exist."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(CAPTION_FOLDER, exist_ok=True)

# Call the function at the start of the app
ensure_directories()

# Load AI model for image captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load AI-powered text enhancement model
text_enhancer = pipeline("text2text-generation", model="facebook/bart-large-cnn")

# Supported languages
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

translator = Translator()

def generate_caption(image_path):
    """Generates a caption for an uploaded image using BLIP AI model."""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    caption_ids = model.generate(**inputs)
    caption = processor.decode(caption_ids[0], skip_special_tokens=True)
    return caption

def enhance_caption(original_caption):
    """Uses AI to refine the caption for better readability and engagement."""
    enhanced_caption = text_enhancer(original_caption, max_length=50, truncation=True)[0]["generated_text"]
    return enhanced_caption

@app.route("/", methods=["GET", "POST"])
def home():
    """Handles uploading images, generating captions, enhancing captions, and translating them."""
    ensure_directories()
    captions = None
    enhanced_caption = None
    uploaded_file = None
    caption_file = None
    translated_caption = None
    selected_language = request.form.get("language", "en")  # Default to English
    enhance = request.form.get("enhance", "no")  # Check if enhancement is requested

    if request.method == "POST":
        if "image" not in request.files:
            return "No file uploaded", 400

        image = request.files["image"]
        if image.filename == "":
            return "No selected file", 400

        # Save uploaded image
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(image_path)

        # Generate caption in English
        caption = generate_caption(image_path)

        # Optionally enhance the caption
        if enhance == "yes":
            enhanced_caption = enhance_caption(caption)
        else:
            enhanced_caption = caption  # No enhancement applied

        # Translate the caption
        translated_caption = translator.translate(enhanced_caption, dest=selected_language).text

        # Extract image title (filename without extension)
        image_title = os.path.splitext(image.filename)[0]

        # Save caption as a text file
        caption_filename = f"{image_title}_{selected_language}.txt"
        caption_file_path = os.path.join(app.config["CAPTION_FOLDER"], caption_filename)

        with open(caption_file_path, "w") as file:
            file.write(f"Image Title: {image_title}\nEnhanced Caption ({LANGUAGES[selected_language]}): {translated_caption}")

        return render_template(
            "index.html",
            captions=caption,
            enhanced_caption=enhanced_caption,
            translated_caption=translated_caption,
            uploaded_file=image_path,
            caption_file=caption_filename,
            languages=LANGUAGES,
            selected_language=selected_language,
        )

    return render_template("index.html", captions=None, uploaded_file=None, caption_file=None, translated_caption=None, enhanced_caption=None, languages=LANGUAGES, selected_language="en")

@app.route("/download_caption/<filename>", methods=["GET"])
def download_caption(filename):
    """Allows users to download the enhanced captions as a text file."""
    ensure_directories()
    file_path = os.path.join(app.config["CAPTION_FOLDER"], filename)

    if not os.path.exists(file_path):
        return "File not found", 404

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
