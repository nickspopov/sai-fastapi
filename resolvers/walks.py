from datetime import date, datetime, timedelta
from typing import Optional
from bson import ObjectId
from config.authentication import check_authentication
from database.walk import Walk, WalkHistory
from graphql_utils.types import Info
from graphql_utils.walk import CreateWalkInput, WalkDayActivity, WalkIntervalActivity, WalkIntervalActivityItem, WalkType
from config.database import engine


async def get_walks_resolver(self, info: Info) -> list[WalkType]:
    user = await check_authentication(info)

    db_walks = await engine.find(Walk, {"userId": {"$in": [ObjectId(user.id)]}})

    return [walk.to_graphQL() for walk in db_walks]


async def get_walk_resolver(self, info: Info, id: str) -> Optional[WalkType]:
    user = await check_authentication(info)
    db_walk = await engine.find_one(Walk, {"_id": ObjectId(id)})

    if not db_walk:
        raise Exception("Not found")

    if db_walk.userId != ObjectId(user.id):
        raise Exception("You are not allowed to access this walk")

    return db_walk.to_graphQL()


async def create_walk_resolver(self, info: Info, input: CreateWalkInput) -> WalkType:
    user = await check_authentication(info)
    db_walk = await engine.save(
        Walk(
            startedAt=input.startedAt,
            finishedAt=input.finishedAt,
            walkHistory=WalkHistory.from_graphQL_input_type(input.walkHistory),
            userId=ObjectId(user.id)
        )
    )
    if db_walk:
        return db_walk.to_graphQL()
    else:
        raise Exception("Failed to create walk")


async def get_walk_day_activity_resolver(self, info: Info, date: datetime) -> WalkDayActivity:
    user = await check_authentication(info)

    query = {"userId": ObjectId(user.id), "startedAt": {
        "$gte": date, "$lt": date + timedelta(hours=24)}}
    db_walks = await engine.find(Walk, query)

    walk_day_activity = WalkDayActivity(
        date=date, totalDistance=0.0, totalDuration=0.0, avgSpeed=0.0, avgPace=0.0)

    if not db_walks:
        return walk_day_activity

    for walk in db_walks:
        walk_day_activity.totalDistance += walk.get_distance()
        walk_day_activity.totalDuration += walk.get_duration()
        walk_day_activity.avgSpeed += walk.get_avg_speed()
        walk_day_activity.avgPace += walk.get_avg_speed()

    return walk_day_activity


async def get_walk_interval_activity_by_day(self, info: Info, from_date: datetime, to_date: datetime) -> WalkIntervalActivity:
    user = await check_authentication(info)

    query = {"userId": ObjectId(user.id), "startedAt": {
        "$gte": from_date, "$lt": to_date}}
    db_walks = await engine.find(Walk, query)

    walk_interval_activity = WalkIntervalActivity(
        totalDistance=0.0, totalDuration=0.0, items=[])

    walk_interval_activity_date_map: dict[datetime, float] = {}

    for i in range((to_date - from_date).days):
        walk_interval_activity_date_map[(
            from_date + timedelta(days=i))] = 0.0
    
    day_adjustment = 0
    if from_date.hour > 0 and from_date.hour < 12:
        day_adjustment = 1
    if from_date.hour > 12:
        day_adjustment = -1


    for walk in db_walks:
        walk_interval_activity.totalDistance += walk.get_distance()
        walk_interval_activity.totalDuration += walk.get_duration()
        walk_interval_activity_date_map[walk.startedAt.replace(
            day=walk.startedAt.day + day_adjustment, hour=from_date.hour, minute=from_date.minute, second=from_date.second, microsecond=from_date.microsecond, tzinfo=from_date.tzinfo
            )] += walk.get_duration()

    for key, value in walk_interval_activity_date_map.items():
        walk_interval_activity.items.append(WalkIntervalActivityItem(
            duration=value, date=datetime.fromtimestamp(key.timestamp(), tz=from_date.tzinfo)))

    return walk_interval_activity
