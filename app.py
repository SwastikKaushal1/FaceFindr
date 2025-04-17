import streamlit as st
import os
import shutil
import zipfile
import face_recognition
import uuid
from PIL import Image
import time
import requests
from dotenv import load_dotenv


# ========== CONFIG ==========

load_dotenv()  
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# ========== UTILS ==========
def send_discord_log(message):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"[Discord Log Failed]: {e}")

def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def find_matching_photos_and_transfer(guest_image_path, photo_folder):
    guest_image = face_recognition.load_image_file(guest_image_path)
    guest_encoding = face_recognition.face_encodings(guest_image)

    if len(guest_encoding) == 0:
        return [], "No face found in the image."

    guest_encoding = guest_encoding[0]
    matching_photos = []

    for root, dirs, files in os.walk(photo_folder):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)
                face_encodings = face_recognition.face_encodings(image, face_locations)

                for face_encoding in face_encodings:
                    distance = face_recognition.face_distance([guest_encoding], face_encoding)[0]
                    accuracy = round(1 - distance, 2)
                    if accuracy >= 0.6:
                        matching_photos.append(image_path)
                        break

    return matching_photos, None if matching_photos else "No matching photos found."

# ========== STREAMLIT UI ==========
st.title("Face Recognition from Google Drive or ZIP Upload")

method = st.radio("Choose Input Method", ["Google Drive Link (Up to 50 photos)", "Upload ZIP File (Unlimited photos)"])

uploaded_face_image = st.file_uploader("Upload your face image", type=["jpg", "jpeg", "png"])
session_id = str(uuid.uuid4())

if method == "Google Drive Link (Up to 50 photos)":
    st.info("⚠️ Currently supports up to 50 images from Google Drive using free `gdown`. If you have more, please zip and upload.")
    drive_link = st.text_input("Paste Google Drive folder link (Shared)")
    if st.button("Start"):
        if drive_link and uploaded_face_image:
            st.warning("Google Drive method disabled due to gdown limitation. Please use ZIP upload for more than 50 files.")
else:
    uploaded_zip = st.file_uploader("Upload a ZIP file of images", type=["zip"])
    if st.button("Start"):
        if uploaded_face_image and uploaded_zip:
            with st.spinner("⏳ This project was made by a normal 12th-pass student 🙃 and is hosted on a free server. Please be patient while your data is being processed..."):
                total_start = time.time()

                # Save face image
                face_path = f"temp_face_{session_id}.jpg"
                with open(face_path, "wb") as f:
                    f.write(uploaded_face_image.getbuffer())

                # Extract zip
                zip_folder = f"extracted_{session_id}"
                os.makedirs(zip_folder, exist_ok=True)
                extract_zip(uploaded_zip, zip_folder)

                # Run recognition
                recognition_start = time.time()
                matching_photos, error = find_matching_photos_and_transfer(face_path, zip_folder)
                recognition_end = time.time()

                # Cleanup
                # Show results BEFORE cleanup
                if error:
                    st.error(error)
                else:
                    for photo in sorted(matching_photos):
                        st.image(photo, use_container_width=True)

                    if matching_photos:
                        zip_filename = f"matched_{session_id}.zip"
                        temp_zip_folder = f"matched_photos_{session_id}"
                        os.makedirs(temp_zip_folder, exist_ok=True)
                        for path in matching_photos:
                            shutil.copy(path, temp_zip_folder)

                        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', temp_zip_folder)

                        with open(zip_filename, "rb") as f:
                            st.download_button("Download Matching Photos", f, file_name=zip_filename)

                        shutil.rmtree(temp_zip_folder)
                        os.remove(zip_filename)

                # Now safely clean up
                try:
                    os.remove(face_path)
                    shutil.rmtree(zip_folder)
                except Exception as e:
                    print(f"Cleanup error: {e}")
                total_end = time.time()
                # Discord log
                send_discord_log(
                    f"📤 **New Session**\n"
                    f"🛠️ Method: ZIP Upload\n"
                    f"🖼️ Uploaded ZIP: `{uploaded_zip.name}`\n"
                    f"🧠 Face Recognition Time: {round(recognition_end - recognition_start, 2)} sec\n"
                    f"📦 Total Matching Photos: {len(matching_photos)}\n"
                    f"🧹 Deleted uploaded/extracted photo folder.\n"
                    f"🧹 Deleted temporary face image.\n"
                    f"🕒 Total Time: {round(total_end - total_start, 2)} sec"
)

                if error:
                    st.error(error)
                else:
                    for photo in matching_photos:
                        st.image(photo, use_column_width=True)

                    if matching_photos:
                        zip_filename = f"matched_{session_id}.zip"
                        temp_zip_folder = f"matched_photos_{session_id}"
                        os.makedirs(temp_zip_folder, exist_ok=True)
                        for path in matching_photos:
                            shutil.copy(path, temp_zip_folder)

                        shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', temp_zip_folder)

                        with open(zip_filename, "rb") as f:
                            st.download_button("Download Matching Photos", f, file_name=zip_filename)

                        shutil.rmtree(temp_zip_folder)
                        os.remove(zip_filename)
        else:
            st.warning("Please upload both a face image and a zip file to start.")
