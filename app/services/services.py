from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Message
from app.services import AICategory

import logging

logger = logging.getLogger(__name__)

class MessageSvc:

    @classmethod
    def _active_messages_query(cls):

        return db.select(Message)

    @classmethod
    def new_message(cls, email: str, content: str, category: str, ai_processed: bool) -> Message:
        new_msg = Message(
            email=email,
            content=content,
            category=category,
            ai_processed=ai_processed
        )

        try:
            db.session.add(new_msg)
            db.session.commit()

        except IntegrityError as e:
            logger.error(f"Unable to store message: {e}")

            db.session.rollback()
            raise ValueError("Unable to store message.")

        return new_msg

    @classmethod
    def fetch_pending_categorization(cls) -> list[Message]:

        stmt = cls._active_messages_query().where(
            Message.category == AICategory.PENDING_RETRY.value
        )
        return db.session.scalars(stmt).all()

    @classmethod
    def save_changes(cls) -> tuple[bool, str | None]:
        """
        Commits any pending session changes to the database safely.

        Returns:
            tuple[bool, str | None]: Boolean value and error string
            if failed or None if successful
        """
        try:
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return False, str(e)

        return True, None