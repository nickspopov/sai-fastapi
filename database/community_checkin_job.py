from datetime import datetime
from odmantic import Model

from bson import ObjectId

class CommunityCheckinJob(Model):
    communityId: ObjectId
    memberId: ObjectId
    scheduledAt: datetime

    class Config:
        collection = "community_checkin_jobs"