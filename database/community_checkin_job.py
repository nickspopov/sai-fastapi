from datetime import datetime
from odmantic import Model

from bson import ObjectId

class CommunityCheckinJob(Model):
    communityId: ObjectId
    memberId: ObjectId
    scheduledAt: datetime

    model_config = {
        "collection": "community_checkin_jobs"
    }