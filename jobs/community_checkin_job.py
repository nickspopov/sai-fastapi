from datetime import datetime, timedelta

from sqlmodel import Session, col, select

from config.database import engine
from database.models import Community, CommunityCheckinJob, CommunityMember, User
from service.notifications import send_push_notification_to_tokens_list


async def community_checkin_push_job() -> None:
    with Session(engine) as session:
        # Find jobs that are due
        query = select(CommunityCheckinJob).where(
            CommunityCheckinJob.scheduled_at <= datetime.now()
        )
        jobs = session.execute(query).scalars().all()

        if len(jobs) == 0:
            return

        for job in jobs:
            # Load user and community
            user = session.get(User, job.member_id)
            community = session.get(Community, job.community_id)

            if user is None or community is None:
                session.delete(job)
                session.commit()
                continue

            # Load community members
            member_query = select(CommunityMember).where(
                CommunityMember.community_id == community.id
            )
            members = session.execute(member_query).scalars().all()

            if len(members) < 2:
                session.delete(job)
                session.commit()
                continue

            # Find the member who checked in
            member = next((m for m in members if m.user_id == user.id), None)

            if member is None or member.last_checkin is None:
                session.delete(job)
                session.commit()
                continue

            if member.last_checkin < datetime.now():
                session.delete(job)
                session.commit()
                continue

            is_it_time = member.last_checkin < datetime.now() + timedelta(minutes=15)

            if not is_it_time:
                continue

            # Load all users for notification
            member_user_ids = [m.user_id for m in members if m.user_id]
            if member_user_ids:
                user_query = select(User).where(col(User.id).in_(member_user_ids))
                users = session.execute(user_query).scalars().all()

                # Collect all push tokens
                tokens = []
                for u in users:
                    if u.push_tokens:
                        tokens.extend(u.push_tokens)

                if tokens:
                    send_push_notification_to_tokens_list(
                        tokens,
                        "Pet friend go to a walk",
                        f"{user.name} will be on {community.name} in 15 minutes",
                    )

            session.delete(job)
            session.commit()
