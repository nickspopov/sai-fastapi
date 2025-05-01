from datetime import datetime, timedelta
from typing import Optional, List
from sqlmodel import select, Session, col
from sqlalchemy import desc
from config.authentication import check_authentication
from database.models import Walk, WalkInterval
from graphql_utils.types import Info
from graphql_utils.walk import CreateWalkInput, WalkDayActivity, WalkIntervalActivity, WalkIntervalActivityItem, WalkType
from config.database import engine


async def get_walks_resolver(self, info: Info, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None, limit: Optional[int] = 10) -> list[WalkType]:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")
    
    query = select(Walk).where(Walk.user_id == user.id)
    if from_date and to_date:
        query = query.where(Walk.started_at >= from_date, Walk.started_at < to_date)
    query = query.order_by(desc(col(Walk.started_at))).limit(limit)
    
    with Session(engine) as session:
        db_walks = session.execute(query).scalars().all()
        return [walk.to_graphQL() for walk in db_walks]


async def get_walk_resolver(self, info: Info, id: str) -> Optional[WalkType]:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")
    
    with Session(engine) as session:
        db_walk = session.get(Walk, id)
        if not db_walk:
            raise Exception("Not found")
        
        if db_walk.user_id != user.id:
            raise Exception("You are not allowed to access this walk")
        
        return db_walk.to_graphQL()


async def create_walk_resolver(self, info: Info, input: CreateWalkInput) -> WalkType:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")
    
    # Create new walk first to get its ID
    walk = Walk(
        started_at=input.startedAt,
        finished_at=input.finishedAt,
        user_id=user.id
    )
    
    with Session(engine) as session:
        session.add(walk)
        session.commit()
        session.refresh(walk)
        
        if not walk.id:
            raise Exception("Failed to create walk")
        
        # Create walk intervals with the walk's ID
        intervals = [
            WalkInterval(
                latitude=item.latitude,
                longitude=item.longitude,
                timestamp=item.timestamp,
                walk_id=walk.id
            )
            for item in input.walkHistory.history
        ]
        
        # Add intervals to the walk
        walk.intervals = intervals
        session.commit()
        session.refresh(walk)
        
        return walk.to_graphQL()


async def get_walk_day_activity_resolver(self, info: Info, date: datetime) -> WalkDayActivity:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")
    
    query = select(Walk).where(
        Walk.user_id == user.id,
        Walk.started_at >= date,
        Walk.started_at < date + timedelta(hours=24)
    )
    
    walk_day_activity = WalkDayActivity(
        date=date, totalDistance=0.0, totalDuration=0.0, avgSpeed=0.0, avgPace=0.0)
    
    with Session(engine) as session:
        db_walks = session.execute(query).scalars().all()
        
        if not db_walks:
            return walk_day_activity
        
        total_avg_speed = 0.0
        total_avg_pace = 0.0
        
        for walk in db_walks:
            walk_day_activity.totalDistance += walk.get_distance()
            walk_day_activity.totalDuration += walk.get_duration()
            total_avg_speed += walk.get_avg_speed()
            total_avg_pace += walk.get_avg_pace()
        
        walk_day_activity.avgSpeed = total_avg_speed / len(db_walks)
        walk_day_activity.avgPace = total_avg_pace / len(db_walks)
        
        return walk_day_activity


async def get_walk_interval_activity_by_day(self, info: Info, from_date: datetime, to_date: datetime) -> WalkIntervalActivity:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")
    
    query = select(Walk).where(
        Walk.user_id == user.id,
        Walk.started_at >= from_date,
        Walk.started_at < to_date
    )
    
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
    
    with Session(engine) as session:
        db_walks = session.execute(query).scalars().all()
        
        for walk in db_walks:
            walk_interval_activity.totalDistance += walk.get_distance()
            walk_interval_activity.totalDuration += walk.get_duration()
            
            date_map_key = walk.started_at.replace(
                hour=from_date.hour, minute=from_date.minute, second=from_date.second, microsecond=from_date.microsecond, tzinfo=from_date.tzinfo
            ) + timedelta(days=day_adjustment)
            walk_interval_activity_date_map[date_map_key] += walk.get_duration()
        
        for key, value in walk_interval_activity_date_map.items():
            walk_interval_activity.items.append(WalkIntervalActivityItem(
                duration=value, date=datetime.fromtimestamp(key.timestamp(), tz=from_date.tzinfo)))
        
        return walk_interval_activity
