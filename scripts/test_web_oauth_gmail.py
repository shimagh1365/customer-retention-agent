from src.email.gmail_sender import GmailDraftSender

def main():
    sender = GmailDraftSender()

    draft = sender.create_draft(
        sender_email="your_email@gmail.com",
        to_email="your_email@gmail.com",
        subject="Web OAuth Test Draft",
        body_text="Draft created successfully via Web OAuth Client."
    )

    print("\n✔ Draft created successfully:")
    print(draft)

if __name__ == "__main__":
    main()
