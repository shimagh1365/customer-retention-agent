from src.email.gmail_sender import GmailDraftSender

def main():
    gmail = GmailDraftSender()

    draft = gmail.create_draft(
        sender_email="yourgmail@gmail.com",
        to_email="yourgmail@gmail.com",
        subject="TEST DRAFT FROM AGENT",
        body_text="This is a test draft created automatically."
    )

    print("DRAFT CREATED:")
    print(draft)

if __name__ == "__main__":
    main()
