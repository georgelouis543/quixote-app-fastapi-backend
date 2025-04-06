import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.datetime_parser import parse_datetime
from app.models.newsletter import Newsletter, Distribution, Subscriber, EmailAnalytics


async def save_analytics_data_handler(newsletter_id: str, analytics_data: list[dict], db: AsyncSession):
    try:
        # Ensure Newsletter exists
        newsletter = await db.execute(select(Newsletter).filter_by(id=newsletter_id))
        newsletter = newsletter.scalars().first()
        if not newsletter:
            db.add(Newsletter(id=newsletter_id, title=f"Newsletter_{newsletter_id}"))
            await db.flush()

        # Bulk insert distributions
        distributions = {}
        subscribers = {}
        email_analytics = []
        emails_temp_list = []

        for record in analytics_data:
            dist_id = record.get("distribution_id")
            email = record.get("email_address")

            if not dist_id or not email:
                continue

            # Add Distribution if missing
            if dist_id not in distributions:
                distributions[dist_id] = Distribution(
                    id=dist_id,
                    newsletter_id=newsletter_id,
                    scheduled_date=parse_datetime(record.get("scheduled_date")),
                    subject=record.get("subject"),
                    status=record.get("status"),
                )

            # Add Subscriber if missing
            if email not in subscribers:
                subscribers[email] = Subscriber(email_address=email)

            # Add Email Analytics
            email_analytics.append(EmailAnalytics(
                distribution_id=dist_id,
                subscriber_id=None,  # To be filled later
                opened=record["opened"],
                clicked=record["clicked"],
                bounced=record["bounced"],
                blocked=record["blocked"],
                delivered=record["delivered"]
            ))

            emails_temp_list.append(email)

        # Save Data in Bulk
        db.add_all(distributions.values())  # Save distributions
        db.add_all(subscribers.values())  # Save subscribers
        await db.commit()

        # Map Subscribers to IDs for analytics
        subscriber_map = {sub.email_address: sub.id for sub in subscribers.values()}
        for i, entry in enumerate(email_analytics):
            entry.subscriber_id = subscriber_map[emails_temp_list[i]]

        # Save Email Analytics in Bulk
        db.add_all(email_analytics)
        await db.commit()

    except Exception as e:
        logging.warning(f"An error occurred when inserting into Database: {e}")
        logging.info(f"ROLLING BACK CHANGES")
        await db.rollback()
