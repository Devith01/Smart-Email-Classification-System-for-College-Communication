import imaplib
import email
import logging
import re
from email.header import decode_header
from datetime import datetime

# Replace these with your actual details
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_app_password"  # 16-character App Password
IMAP_URL = "imap.gmail.com"

# Setup Logging to track what the script does
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("organizer.log"), logging.StreamHandler()]
)

class EmailClassifier:
    """
    A keyword-frequency based classifier that mimics Naive Bayes logic
    to determine the category of an email based on subject and body snippet.
    """
    def __init__(self):
        self.categories = {
            "Classes": ["lecture", "assignment", "quiz", "syllabus", "professor", "module", "lab", "zoom", "midterm"],
            "Events": ["hackathon", "workshop", "seminar", "webinar", "register", "club", "fest", "symposium"],
            "Internships": ["career", "hiring", "job", "intern", "stipend", "application", "interview", "linkedin"],
            "Holidays": ["vacation", "break", "holiday", "recess", "leave", "closed", "festive"],
            "Others": []
        }

    def clean_text(self, text):
        """Standardizes text for better matching."""
        if not text: return ""
        text = text.lower()
        return re.sub(r'[^a-z\s]', '', text)

    def classify(self, subject, snippet=""):
        combined_text = self.clean_text(f"{subject} {snippet}")
        scores = {cat: 0 for cat in self.categories}

        for cat, keywords in self.categories.items():
            for word in keywords:
                if word in combined_text:
                    scores[cat] += 1
        
        # Determine the winner
        best_cat = max(scores, key=scores.get)
        
        # If no keywords matched, default to Others
        if scores[best_cat] == 0:
            return "Others"
        return best_cat

class SmartOrganizer:
    def __init__(self):
        self.mail = None
        self.classifier = EmailClassifier()
        self.stats = {"Classes": 0, "Events": 0, "Internships": 0, "Holidays": 0, "Others": 0}

    def connect(self):
        """Establishes a secure connection to the IMAP server."""
        try:
            logging.info(f"Attempting to connect to {IMAP_URL}...")
            self.mail = imaplib.IMAP4_SSL(IMAP_URL)
            self.mail.login(EMAIL_USER, EMAIL_PASS)
            logging.info("Successfully authenticated.")
            return True
        except Exception as e:
            logging.error(f"Connection Failed: {e}")
            return False

    def ensure_labels_exist(self):
        """Checks if Gmail labels exist; if not, creates them."""
        for label in self.stats.keys():
            status, _ = self.mail.select(label)
            if status != 'OK':
                logging.info(f"Creating missing label: {label}")
                self.mail.create(label)

    def get_email_body(self, msg):
        """Extracts a small snippet of the body for better classification."""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode(errors='ignore')[:200]
        else:
            return msg.get_payload(decode=True).decode(errors='ignore')[:200]
        return ""

    def process_inbox(self):
        """Main loop to fetch, classify, and move emails."""
        self.ensure_labels_exist()
        self.mail.select("inbox")
        
        # Search for all unread emails
        status, data = self.mail.search(None, 'UNSEEN')
        if status != 'OK' or not data[0]:
            logging.info("No new unread emails found in Inbox.")
            return

        email_ids = data[0].split()
        logging.info(f"Found {len(email_ids)} emails to organize.")

        for e_id in email_ids:
            try:
                # Fetch full email message
                res, msg_data = self.mail.fetch(e_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Decode Subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                # Get body snippet for ML context
                body_snippet = self.get_email_body(msg)
                
                # Classify
                category = self.classifier.classify(subject, body_snippet)
                
                # Log action
                logging.info(f"MATCH: '{subject[:40]}...' -> [{category}]")

                # Move Operation
                copy_status = self.mail.copy(e_id, category)
                if copy_status[0] == 'OK':
                    self.mail.store(e_id, '+FLAGS', '\\Deleted')
                    self.stats[category] += 1

            except Exception as e:
                logging.error(f"Error processing email ID {e_id}: {e}")

        # Finalize deletion from Inbox
        self.mail.expunge()
        self.print_summary()

    def print_summary(self):
        """Prints a professional report of the session."""
        print("\n" + "="*40)
        print(f"   ORGANIZATION SUMMARY - {datetime.now().strftime('%Y-%m-%d')}")
        print("="*40)
        total = sum(self.stats.values())
        for cat, count in self.stats.items():
            bar = "■" * count
            print(f"{cat:12} | {count:2} {bar}")
        print("-" * 40)
        print(f"Total Emails Processed: {total}")
        print("="*40 + "\n")

    def disconnect(self):
        if self.mail:
            self.mail.logout()
            logging.info("Disconnected from server.")

if __name__ == "__main__":
    organizer = SmartOrganizer()
    if organizer.connect():
        organizer.process_inbox()
        organizer.disconnect()