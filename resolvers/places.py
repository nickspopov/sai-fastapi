from datetime import datetime

from sqlmodel import Session, col, select

from config.authentication import check_authentication
from config.database import engine
from database.models import Community, CommunityCheckinJob, CommunityMember, CommunityPlace, User
from graphql_utils.community import CommunityPlaceInput, CommunityType
from graphql_utils.info import Info


async def get_communities_resolver(self, info: Info) -> list[CommunityType]:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")

    with Session(engine) as session:
        # Get all communities where the user is a member
        query = select(Community).join(CommunityMember).where(CommunityMember.user_id == user.id)
        communities = session.execute(query).scalars().all()

        # Load relationships for each community
        for community in communities:
            # Load owner
            community.owner = session.get(User, community.owner_id)
            if not community.owner:
                continue

            # Load members with their users
            member_query = select(CommunityMember).where(
                CommunityMember.community_id == community.id
            )
            members: list[CommunityMember] = list(session.execute(member_query).scalars().all())

            # Load users for members
            member_user_ids = [member.user_id for member in members if member.user_id]
            if member_user_ids:
                user_query = select(User).where(col(User.id).in_(member_user_ids))
                users = session.execute(user_query).scalars().all()

                # Assign users to members
                for member in members:
                    member.user = next((u for u in users if u.id == member.user_id), None)  # type: ignore[assignment]

            community.members = members

            # Load places
            place_query = select(CommunityPlace).where(CommunityPlace.community_id == community.id)
            places: list[CommunityPlace] = list(session.execute(place_query).scalars().all())
            community.places = places

        return [community.to_graphQL() for community in communities]


async def create_community_resolver(self, info: Info, name: str) -> CommunityType:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")

    # Create new community
    community = Community(name=name, owner_id=user.id)

    with Session(engine) as session:
        # Save community first to get its ID
        session.add(community)
        session.commit()
        session.refresh(community)

        if not community.id:
            raise Exception("Failed to create community")

        # Create community member for the owner
        member = CommunityMember(user_id=user.id, community_id=community.id)
        session.add(member)
        session.commit()

        # Load relationships
        community.owner = user
        community.members = [member]
        member.user = user  # Set the user relationship
        community.places = []

        return community.to_graphQL()


async def get_community_resolver(self, info: Info, id: str) -> CommunityType:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")

    with Session(engine) as session:
        # Get community with all relationships
        community = session.get(Community, id)
        if not community:
            raise Exception("Community not found")

        # Load owner
        community.owner = session.get(User, community.owner_id)  # type: ignore[assignment]
        if not community.owner:
            raise Exception("Community owner not found")

        # Load members
        member_query = select(CommunityMember).where(CommunityMember.community_id == community.id)
        members: list[CommunityMember] = list(session.execute(member_query).scalars().all())

        # Load users for members
        member_user_ids = [member.user_id for member in members if member.user_id]
        if member_user_ids:
            user_query = select(User).where(col(User.id).in_(member_user_ids))
            users = session.execute(user_query).scalars().all()

            # Assign users to members
            for member in members:
                member.user = next((u for u in users if u.id == member.user_id), None)  # type: ignore[assignment]

        community.members = members

        # Load places
        place_query = select(CommunityPlace).where(CommunityPlace.community_id == community.id)
        places: list[CommunityPlace] = list(session.execute(place_query).scalars().all())
        community.places = places

        return community.to_graphQL()


async def create_community_place(self, info: Info, input: CommunityPlaceInput) -> CommunityType:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")

    with Session(engine) as session:
        # Get community and check membership
        community = session.get(Community, input.communityId)
        if not community:
            raise Exception("Community not found")

        member_query = select(CommunityMember).where(
            CommunityMember.community_id == input.communityId, CommunityMember.user_id == user.id
        )
        is_member = session.execute(member_query).first() is not None

        if not is_member:
            raise Exception("User is not a member of this community")

        # Create new place
        place = CommunityPlace(
            name=input.name, latitude=input.lat, longitude=input.lon, community_id=input.communityId
        )
        session.add(place)

        # Load relationships
        community.owner = session.get(User, community.owner_id)  # type: ignore[assignment]

        # Load members
        member_query = select(CommunityMember).where(CommunityMember.community_id == community.id)
        members: list[CommunityMember] = list(session.execute(member_query).scalars().all())

        # Load users for members
        member_user_ids = [member.user_id for member in members if member.user_id]
        if member_user_ids:
            user_query = select(User).where(col(User.id).in_(member_user_ids))
            users = session.execute(user_query).scalars().all()

            # Assign users to members
            for member in members:
                member.user = next((u for u in users if u.id == member.user_id), None)  # type: ignore[assignment]

        community.members = members

        # Load places
        place_query = select(CommunityPlace).where(CommunityPlace.community_id == community.id)
        places: list[CommunityPlace] = list(session.execute(place_query).scalars().all())
        community.places = places

        session.commit()
        return community.to_graphQL()


async def checkin_community_place(
    self, info: Info, communityId: str, placeId: str, date: datetime
) -> CommunityType:
    user = await check_authentication(info)
    if not user.id:
        raise Exception("User not found")

    with Session(engine) as session:
        # Get community and check membership
        community = session.get(Community, communityId)
        if not community:
            raise Exception("Community not found")

        # Find member and check membership
        member_query = select(CommunityMember).where(
            CommunityMember.community_id == communityId, CommunityMember.user_id == user.id
        )
        member = session.execute(member_query).scalar_one_or_none()

        if not member:
            raise Exception("User is not a member of this community")

        if not member.id:
            raise Exception("Invalid member ID")

        # Find place
        place = session.get(CommunityPlace, placeId)
        if not place or place.community_id != communityId:
            raise Exception("Place not found")

        # Update member's last checkin
        member.last_checkin = date

        # Create checkin job
        checkin_job = CommunityCheckinJob(
            community_id=communityId, member_id=member.id, scheduled_at=date
        )
        session.add(checkin_job)

        # Load relationships
        community.owner = session.get(User, community.owner_id)  # type: ignore[assignment]

        # Load members
        member_query = select(CommunityMember).where(CommunityMember.community_id == community.id)
        members: list[CommunityMember] = list(session.execute(member_query).scalars().all())

        # Load users for members
        member_user_ids = [member.user_id for member in members if member.user_id]
        if member_user_ids:
            user_query = select(User).where(col(User.id).in_(member_user_ids))
            users = session.execute(user_query).scalars().all()

            # Assign users to members
            for member in members:
                member.user = next((u for u in users if u.id == member.user_id), None)  # type: ignore[assignment]

        community.members = members

        # Load places
        place_query = select(CommunityPlace).where(CommunityPlace.community_id == community.id)
        places: list[CommunityPlace] = list(session.execute(place_query).scalars().all())
        community.places = places

        session.commit()
        return community.to_graphQL()
