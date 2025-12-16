class SalesFeedbackHandler:
    """
    Handles the human-in-the-loop workflow between the sales team
    and the autonomous customer intelligence agent.
    """

    def __init__(self, agent_instance):
        """
        agent_instance: an initialized CustomerAgent
        """
        self.agent = agent_instance

    # ---------------------------------------------------------
    # FEEDBACK APPLICATION
    # ---------------------------------------------------------
    def apply_feedback(self, draft_packet, feedback_type, feedback_text=None):
        """
        Apply sales feedback to a draft email packet.

        feedback_type:
            - "APPROVE" → salesperson approves the draft
            - "REJECT"  → salesperson rejects & requests revision
            - "REVISE"  → salesperson suggests specific changes

        feedback_text: string message from salesperson
        """
        packet = draft_packet.copy()

        if feedback_type == "APPROVE":
            packet["status"] = "SALES_APPROVED"
            packet["sales_feedback"] = "Approved by sales"
            return packet

        if feedback_type in ["REJECT", "REVISE"]:
            packet["status"] = "REVISION_REQUIRED"
            packet["sales_feedback"] = feedback_text or "No additional comments"

            # Generate revised email
            revised_email = self.revise_email(packet, feedback_text)
            packet["email_to_sales"] = revised_email

            # Track revision count
            packet["revision_count"] = packet.get("revision_count", 0) + 1

            return packet

        # Unknown feedback type
        packet["status"] = "INVALID_FEEDBACK"
        return packet

    # ---------------------------------------------------------
    # EMAIL REVISION LOGIC
    # ---------------------------------------------------------
    def revise_email(self, packet, feedback_text=None):
        """
        Revise the email draft based on sales feedback.
        This is a simple version. Later we can add:
        - tone adjustment
        - offer update logic
        - LLM rewrite engine (GPT-based)
        """

        original_email = packet.get("email_to_sales", "")

        feedback_note = (
            f"\n\n---\n"
            f"Sales requested changes:\n"
            f"{feedback_text or 'No comments provided'}\n"
            f"---\n"
            f"Agent revision:\n"
            f"(The agent can modify tone, add details, or adjust offer here.)"
        )

        revised_email = original_email + feedback_note

        return revised_email

    # ---------------------------------------------------------
    # HISTORY TRACKING (OPTIONAL)
    # ---------------------------------------------------------
    def log_feedback_event(self, log_store, draft_packet):
        """
        Save feedback events into a list or database for audit purposes.

        log_store: list OR database handler
        draft_packet: updated packet after feedback
        """
        entry = {
            "customer_id": draft_packet["customer_id"],
            "name": draft_packet["name"],
            "status": draft_packet["status"],
            "revision_count": draft_packet.get("revision_count", 0),
            "feedback": draft_packet.get("sales_feedback", ""),
        }

        log_store.append(entry)
        return log_store
