from datetime import datetime
from bson import ObjectId
from config.database import engine
from config.authentication import check_authentication
from database.community import Community, CommunityMember, CommunityMemberLastCheckin, CommunityPlace
from database.user import User
from graphql_utils.community import CommunityPlaceInput, CommunityType
from graphql_utils.types import Info
from service.notifications import send_push_notification_to_tokens_list

from utils.pydantic import PydanticObjectId


async def get_communities_resolver(self, info: Info) -> list[CommunityType]:
    user = await check_authentication(info)

    communities = await engine.find(Community, {"members.userId": ObjectId(user.id)})
    for community in communities:
        owner = await engine.find_one(User, {"_id": ObjectId(community.ownerId)})
        community.owner = owner
        member_users = await engine.find(User, {"_id": {"$in": [member.userId for member in community.members]}})

        for member in community.members:
            member.user = next(
                (user for user in member_users if user.id == member.userId), None)
            if member.lastCheckin:
                member.lastCheckin.place = next(
                    (place for place in community.places if place.id == member.lastCheckin.placeId), None)

    return [community.to_graphQL() for community in communities]


async def create_community_resolver(self, info: Info, name: str) -> CommunityType:
    user = await check_authentication(info)

    community = Community(
        name=name,
        ownerId=ObjectId(user.id),
        members=[CommunityMember(userId=ObjectId(user.id), lastCheckin=None)],
        places=[]
    )

    await engine.save(community)

    community.owner = user
    community.members[0].user = user
    return community.to_graphQL()


async def get_community_resolver(self, info: Info, id: str) -> CommunityType:
    user = await check_authentication(info)

    community = await engine.find_one(Community, {"_id": ObjectId(id)})

    if not community:
        raise Exception("Community not found")

    owner = await engine.find_one(User, {"_id": ObjectId(community.ownerId)})
    community.owner = owner
    member_users = await engine.find(User, {"_id": {"$in": [member.userId for member in community.members]}})

    for member in community.members:
        member.user = next(
            (user for user in member_users if user.id == member.userId), None)
        if member.lastCheckin:
            member.lastCheckin.place = next(
                (place for place in community.places if place.id == member.lastCheckin.placeId), None)

    return community.to_graphQL()


async def create_community_place(self, info: Info, input: CommunityPlaceInput) -> CommunityType:
    user = await check_authentication(info)

    community = await engine.find_one(Community, {"_id": ObjectId(input.communityId)})

    if not community:
        raise Exception("Community not found")

    is_user_member = next(
        (member for member in community.members if member.userId == ObjectId(user.id)), None)

    if not is_user_member:
        raise Exception("User is not a member of this community")

    community.places.append(CommunityPlace(
        id=PydanticObjectId(),
        name=input.name,
        lat=input.lat,
        lon=input.lon
    ))

    await engine.save(community)

    owner = await engine.find_one(User, {"_id": ObjectId(community.ownerId)})
    community.owner = owner
    member_users = await engine.find(User, {"_id": {"$in": [member.userId for member in community.members]}})

    for member in community.members:
        member.user = next(
            (user for user in member_users if user.id == member.userId), None)
        if member.lastCheckin:
            member.lastCheckin.place = next(
                (place for place in community.places if place.id == member.lastCheckin.placeId), None)

    return community.to_graphQL()


async def checkin_community_place(self, info: Info, communityId: str, placeId: str, date: datetime) -> CommunityType:
    user = await check_authentication(info)

    community = await engine.find_one(Community, {"_id": ObjectId(communityId)})

    if not community:
        raise Exception("Community not found")

    is_user_member = next(
        (member for member in community.members if member.userId == ObjectId(user.id)), None)

    if not is_user_member:
        raise Exception("User is not a member of this community")

    place = next((place for place in community.places if place.id ==
                 PydanticObjectId(placeId)), None)

    if not place:
        raise Exception("Place not found")

    community.members = [member if member.userId != ObjectId(user.id) else
                         CommunityMember(
        userId=ObjectId(user.id),
        lastCheckin=CommunityMemberLastCheckin(date=date, placeId=PydanticObjectId(placeId)))
        for member in community.members
    ]

    await engine.save(community)

    owner = await engine.find_one(User, {"_id": ObjectId(community.ownerId)})
    community.owner = owner
    member_users = await engine.find(User, {"_id": {"$in": [member.userId for member in community.members]}})

    for member in community.members:
        member.user = next(
            (user for user in member_users if user.id == member.userId), None)
        if member.lastCheckin:
            member.lastCheckin.place = next(
                (place for place in community.places if place.id == member.lastCheckin.placeId), None)

    return community.to_graphQL()
