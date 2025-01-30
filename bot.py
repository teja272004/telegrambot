import os
import logging
import io
import fitz  # PyMuPDF for PDF handling
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from PIL import Image
from dotenv import load_dotenv

# Import Gemini function & database collections
from gemini_chat import get_gemini_response
from database import users_collection, chat_collection, file_collection

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 📷 **Image Analysis Function**
async def analyze_image(update: Update, context: CallbackContext):
    message = update.message
    processing_message = await message.reply_text("🖼 *Analyzing image, please wait...*")

    try:
        # Download image
        file = await message.photo[-1].get_file()
        img_data = await file.download_as_bytearray()
        img = Image.open(io.BytesIO(img_data))

        # Use caption or default prompt
        prompt = message.caption or "Describe this image."

        # Get AI response
        response_text = get_gemini_response(prompt, img)

        # Store metadata in MongoDB
        file_collection.insert_one({
            "chat_id": message.from_user.id,
            "file_name": "photo.jpg",
            "file_type": "image",
            "description": response_text,
        })

        # Send response
        await message.reply_text(f"🖼 *Image Analysis:*\n{response_text}")

    except Exception as e:
        await message.reply_text(f"❌ Error analyzing image: {str(e)}")
    finally:
        await processing_message.delete()


# 📄 **PDF Analysis Function**
async def analyze_pdf(update: Update, context: CallbackContext):
    message = update.message
    processing_message = await message.reply_text("📄 *Processing PDF, please wait...*")

    try:
        # Download the PDF file
        file = await message.document.get_file()
        pdf_data = await file.download_as_bytearray()

        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_data)

        # If PDF is empty, return an error
        if not pdf_text.strip():
            await message.reply_text("⚠️ Could not extract text from the PDF.")
            return

        # Get AI response from Gemini
        response_text = get_gemini_response(f"Summarize this document:\n{pdf_text}")

        # Store in MongoDB
        file_collection.insert_one({
            "chat_id": message.from_user.id,
            "file_name": message.document.file_name,
            "file_type": "pdf",
            "description": response_text,
        })

        # Send response
        await message.reply_text(f"📄 *PDF Summary:*\n{response_text}")

    except Exception as e:
        await message.reply_text(f"❌ Error analyzing PDF: {str(e)}")
    finally:
        await processing_message.delete()


# 📝 **Extract Text from PDF**
def extract_text_from_pdf(pdf_data):
    """Extracts text from a PDF file."""
    doc = fitz.open(stream=pdf_data, filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text


# 🏁 **Start Command**
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Hello! Send me an image or a PDF, and I'll analyze it! You can also chat with me anytime.")


# 💬 **Chat Functionality**
async def chat(update: Update, context: CallbackContext):
    message = update.message
    user_message = message.text.strip()

    if user_message.lower() == "bye":
        await message.reply_text("Goodbye! See you next time!")
        return

    try:
        # Get Gemini AI response
        response_text = get_gemini_response(user_message)

        # Store chat history in MongoDB
        chat_collection.insert_one({
            "chat_id": message.from_user.id,
            "message": user_message,
            "response": response_text,
        })

        # Send response
        await message.reply_text(f"💬 *Chatbot Response:*\n{response_text}")

    except Exception as e:
        await message.reply_text(f"❌ Error in chatbot: {str(e)}")


# 🚀 **Main Function**
def main():
    app = Application.builder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))

    # Message Handlers
    app.add_handler(MessageHandler(filters.PHOTO, analyze_image))  # Image Handling
    app.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"), analyze_pdf))  # PDF Handling
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))  # Chat Handling

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
