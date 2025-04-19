
# FaceFinder

A simple mini project inspired by [PartypixAi](https://github.com/SwastikKaushal1/PartypixAi) — allowing users to upload a face image and retrieve matching event photos using **face recognition** from either a **Google Drive folder** or a **ZIP upload**.

---

## ✨ Why This Project?

- 🧠 **Learned How to Use APIs**: This project was mainly created to understand how public APIs (like Google Drive) work in Python.
- 🔬 **Experimentation**: A lightweight version of PartypixAi to test face recognition using public image sets.
- 🧪 **Proof of Concept**: Before scaling, this served as a functional prototype to validate key features.

---

## 🧩 Features

- 📂 **Upload ZIP / Use Google Drive**: Fetch photos either from a Google Drive folder or directly upload a zip of event images.
- 🧠 **Face Recognition**: Upload a face image and get all matching photos from the dataset.
- ⬇️ **Download ZIP**: Easily download all the matched images in one zip file.
- 📡 **Discord Logging**: Every session is logged into a Discord server via webhook.
- 🛡️ **Session Cleanup**: Temporary images and folders are auto-deleted after processing.

---

## 🛠️ Technologies Used

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-red?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)  
[![Google Drive API](https://img.shields.io/badge/Google%20Drive%20API-active-blue?style=for-the-badge&logo=google-drive&logoColor=white)](https://developers.google.com/drive)  
[![Face Recognition](https://img.shields.io/badge/Face%20Recognition-blueviolet?style=for-the-badge)](https://github.com/ageitgey/face_recognition)  

---

## 🚀 How to Use

### 1. 🔑 Set Up Secrets

Create a `.streamlit/secrets.toml` file with the following:

```toml
API_KEY = "YOUR_GOOGLE_DRIVE_API_KEY"
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
```

### 2. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. ▶️ Run the Streamlit App

```bash
streamlit run app.py
```

---

## 💡 How It Works

1. Upload your **face image**.
2. Choose between:
   - **Google Drive link** to a shared folder (up to 50 photos supported).
   - **ZIP upload** of unlimited photos.
3. System compares faces using `face_recognition` and filters matches.
4. Matched photos are displayed and available for download in a zip file.
5. Discord logs keep track of usage sessions.

---

## 📸 Sample Use Case

- Event Host uploads all event photos to a Google Drive folder or zips them into a file.
- Guest uploads their face image.
- System returns all photos in which their face appears.
- They download a zip with their matching moments.

---


## 👨‍💻 Author & Credits

Made with ❤️ by [Swastik Kaushal](https://github.com/SwastikKaushal1)

[![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/users/751334414914420767)  
[![Instagram](https://img.shields.io/badge/Instagram-ff5e5b?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/swastikkaushal_/)  
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@DefenderXD)

---

## 📬 Support

For support, suggestions, or feedback:  
📧 **Email**: swastik2022008@gmail.com  
💬 **Discord**: [Join Here](https://discord.gg/UnNd95u3Fg)

---

