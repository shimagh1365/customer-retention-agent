from src.email.gmail_sender import GmailDraftSender


def main():
    print("\n=== MINIMAL GMAIL TEST STARTED ===\n")

    gmail = GmailDraftSender()

    # Update these emails to your own addresses
    sender = "nafiseh.ghasemi65@gmail.com"
    recipient = "ginger.ginger1287@gmail.com"

    subject = "Test Draft from AI Sales Agent"
    body = "This is a test draft created by the minimal Gmail script."

    print("\nCreating draft...\n")

    draft = gmail.create_draft(
        sender_email=sender,
        to_email=recipient,
        subject=subject,
        body_text=body
    )

    print("\n=== DRAFT CREATED SUCCESSFULLY ===")
    print(draft)


if __name__ == "__main__":
    main()
