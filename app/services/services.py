from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import Message

import logging

logger = logging.getLogger(__name__)

class MessageSvc:

    @classmethod
    def new_message(cls, email: str, content: str, category: str, ai_processed: bool):
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