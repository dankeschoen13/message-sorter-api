import click
from flask.cli import with_appcontext
from app.services import categorize_message, AICategory, MessageSvc


@click.command('retry-ai')
@with_appcontext
def retry_ai_command():
    """Finds all PENDING_RETRY messages and runs them through Gemini again."""

    # 1. Fetch via Service Layer
    pending_messages = MessageSvc.fetch_pending_categorization()

    if not pending_messages:
        click.echo("No pending messages to retry. Exiting.")
        return

    click.echo(f"Found {len(pending_messages)} messages to retry. Starting...")

    success_count = 0

    # 2. Modify objects in memory
    for msg in pending_messages:
        new_category = categorize_message(msg.content)

        if new_category != AICategory.PENDING_RETRY.value:
            msg.category = new_category
            msg.ai_processed = True
            success_count += 1
            click.echo(f"Message ID {msg.id} successfully categorized as {new_category}.")
        else:
            click.echo(f"Message ID {msg.id} failed again.")

    # 3. Commit via Service Layer
    if success_count > 0:
        success, error_msg = MessageSvc.save_changes()

        if success:
            click.echo(f"Successfully updated {success_count} messages in the database.")
        else:
            click.echo(f"Database error during commit: {error_msg}")
    else:
        click.echo("No messages were successfully categorized. Nothing to commit.")