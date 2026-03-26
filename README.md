# 📧 Smart Email Classification System for College Communication

## 🎯 Project Overview

College students receive numerous emails related to classes, events, internships, and holidays. These emails often get mixed up, making it difficult to track important information.

This project is a **Python-based Smart Email Organizer** that automatically reads emails from a Gmail account and classifies them into meaningful categories for better organization and productivity.

---

## 💡 Problem Statement

Students struggle to manage large volumes of college emails, leading to:

* Missed important updates
* Difficulty in finding relevant information
* Poor organization of inbox

---

## 🚀 Solution

This system:

* Fetches emails using IMAP
* Extracts subject lines
* Classifies emails using keyword-based logic
* Organizes them into categories

---

## 📂 Categories

* 📘 Classes
* 🎉 Events / Hackathons
* 💼 Internships
* 🌴 Holidays
* 📁 Others

---

## ⚙️ Features

✔ Automatic email fetching
✔ Keyword-based classification
✔ Simple and beginner-friendly implementation
✔ Organized output for better readability
✔ Error handling for login and empty inbox

---

## 🧠 Technologies Used

* Python
* IMAP (imaplib)
* Email parsing (email library)

---

## 🏗️ Project Structure

```
email-organizer/
│
├── main.py              # Main script to run the project
├── classifier.py       # Email classification logic
├── config.py           # Email credentials (App Password)
└── README.md           # Project documentation
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/your-username/email-organizer.git
cd email-organizer
```

---

### 2. Install Requirements

(No external libraries required for basic version)

---

### 3. Enable Gmail Access

* Enable **IMAP** in Gmail settings
* Enable **2-Step Verification**
* Generate **App Password**

---

### 4. Update Credentials

Open `config.py` and add:

```python
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"
```

---

### 5. Run the Project

```
python main.py
```

---

## 🧪 Sample Output

```
Subject: Hackathon Announcement
→ Category: Events

Subject: Class Rescheduled
→ Category: Classes
```

---

## 🔥 Future Enhancements

* 🤖 Machine Learning-based classification
* 🌐 Web dashboard using Flask
* 🔔 Email notifications for important updates
* 📊 Analytics for email trends

---

## 🎓 Use Case

This project helps:

* Students manage emails efficiently
* Avoid missing important updates
* Improve productivity

---

## 🏆 Conclusion

The Smart Email Classification System simplifies email management by automatically organizing academic and non-academic emails, making student life more efficient and structured.

---

## 👤 Author

**Name:** Shri Devith
**Course:** Fundamentals of AI/ML
**Branch:** CSE (Health Informatics)
