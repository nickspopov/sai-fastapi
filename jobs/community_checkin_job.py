from config.database import engine
from database.community import Community
from database.community_checkin_job import CommunityCheckinJob

from datetime import datetime, timedelta

from database.user import User

from service.notifications import send_push_notification_to_tokens_list

async def community_checkin_push_job() -> None:
    jobs = await engine.find(CommunityCheckinJob, {"scheduledAt": {"$lte": datetime.now()}})

    if len(jobs) == 0:
        return

    for job in jobs:
        user = await engine.find_one(User, {"_id": job.memberId})
        community = await engine.find_one(Community, {"_id": job.communityId})
        
        if user is None or community is None or len(community.members) < 2:
            await engine.delete(job)
            continue
        
        members = await engine.find(User, {"_id": {"$in": [member.userId for member in community.members]}})

        member = next((member for member in community.members if member.userId == user.id), None)

        if member is None or member.lastCheckin is None:
            await engine.delete(job)
            continue
        
        if member.lastCheckin.date < datetime.now():
            await engine.delete(job)
            continue
        
        is_it_time = member.lastCheckin.date < datetime.now() + timedelta(minutes=15)

        if not is_it_time:
            continue
        
        tokens = []

        for member in members:
          tokens += member.pushTokens

        send_push_notification_to_tokens_list(tokens, "Pet friend go to a walk", f"{user.name} will be on {community.name} in 15 minutes")

        
        

