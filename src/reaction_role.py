import asyncio as _asyncio
from threading import Lock as _Lock
from typing import List as _List
from typing import Optional as _Optional

import database as _database




class ReactionRole(_database.DatabaseRowBase):
    TABLE_NAME: str = 'reaction_role'
    ID_COLUMN_NAME: str = 'reaction_role_id'

    def __init__(self, reaction_role_id: int, message_id: int, name: str, reaction: str, is_active: bool) -> None:
        super().__init__(reaction_role_id)
        self.__message_id: int = message_id
        self.__name: str = name
        self.__reaction: str = reaction
        self.__is_active: bool = is_active
        self.__role_changes: _List['ReactionRoleChange'] = []
        self.__role_requirements: _List['ReactionRoleRequirement'] = []
        self.__edit_changes_lock: _Lock = _Lock()
        self.__edit_requirements_lock: _Lock = _Lock()


    @property
    def is_active(self) -> bool:
        super()._assert_not_deleted()
        return self.__is_active

    @property
    def message_id(self) -> bool:
        super()._assert_not_deleted()
        return self.__message_id

    @property
    def name(self) -> bool:
        super()._assert_not_deleted()
        return self.__name

    @property
    def reaction(self) -> bool:
        super()._assert_not_deleted()
        return self.__reaction

    @property
    def role_changes(self) -> _List['ReactionRoleChange']:
        super()._assert_not_deleted()
        return list(self.__role_changes)

    @property
    def role_requirements(self) -> _List['ReactionRoleRequirement']:
        super()._assert_not_deleted()
        return list(self.__role_requirements)


    async def add_change(self, role_id: int, add: bool, allow_toggle: bool, message_channel_id: int = None, message_content: str = None) -> 'ReactionRoleChange':
        super()._assert_not_deleted()
        with self.__edit_changes_lock:
            for change in self.role_requirements:
                if change.id == role_id:
                    return change

            result = await _db_create_reaction_role_change(self.id, role_id, add, allow_toggle, message_channel_id, message_content)
            self.__role_changes.append(result)
            return result


    async def add_requirement(self, required_role_id: int) -> 'ReactionRoleRequirement':
        super()._assert_not_deleted()
        with self.__edit_requirements_lock:
            for requirement in self.role_requirements:
                if requirement.id == required_role_id:
                    return requirement

            result = await _db_create_reaction_role_requirement(self.id, required_role_id)
            self.__role_requirements.append(result)
            return result


    async def delete(self) -> bool:
        super()._assert_not_deleted()
        result = await _db_delete_reaction_role(self.id)
        if result:
            for requirement in self.role_requirements:
                await requirement._delete()
            self.__role_requirements.clear()
            for change in self.role_changes:
                await change._delete()
            self.__role_changes.clear()
            super()._set_deleted()
        return result


    async def remove_change(self, reaction_role_change_id: int) -> bool:
        super()._assert_not_deleted()
        with self.__edit_changes_lock:
            change = None
            found_change = False
            for change in self.role_changes:
                if change.id == reaction_role_change_id:
                    found_change = True
                    break

            if not found_change:
                return True

            self.__role_changes.remove(change)
            success = await change._delete()
            return success


    async def remove_requirement(self, reaction_role_requirement_id: int) -> bool:
        super()._assert_not_deleted()
        with self.__edit_requirements_lock:
            requirement = None
            found_requirement = False
            for requirement in self.role_requirements:
                if requirement.id == reaction_role_requirement_id:
                    found_requirement = True
                    break

            if not found_requirement:
                return True

            self.__role_requirements.remove(requirement)
            success = await requirement._delete()
            return success


    async def update(self, message_id: int = None, name: str = None, reaction: str = None, is_active: bool = None) -> bool:
        super()._assert_not_deleted()
        if message_id is None and name is None and reaction is None and is_active is None:
            return True
        message_id = message_id or self.message_id
        name = name or self.name
        reaction = reaction or self.reaction
        is_active = is_active or self.is_active
        updated = await _db_update_reaction_role(self.id, message_id, name, reaction, is_active)
        if updated:
            self.__message_id = message_id
            self.__name = name
            self.__reaction = reaction
            self.__is_active = is_active
        return updated


    @staticmethod
    async def create(message_id: int, name: str, reaction: str, is_active: bool = True) -> _Optional['ReactionRole']:
        record = await _database.insert_row(
            ReactionRole.TABLE_NAME,
            ReactionRole.ID_COLUMN_NAME,
            message_id=message_id,
            name=name,
            reaction=reaction,
            is_active=is_active,
        )
        if record:
            return ReactionRole(record[0], message_id, name, reaction, is_active)
        return None





class ReactionRoleChange(_database.DatabaseRowBase):
    TABLE_NAME: str = 'reaction_role_change'
    ID_COLUMN_NAME: str = 'reaction_role_change_id'

    def __init__(self, reaction_role_change_id: int, reaction_role_id: int, role_id: int, add: bool, allow_toggle: bool, message_channel_id: int, message_content: str) -> None:
        super().__init__(reaction_role_change_id)
        self.__reaction_role_id: int = reaction_role_id
        self.__role_id: int = role_id
        self.__add: bool = add
        self.__allow_toggle: bool = allow_toggle
        self.__message_channel_id: int = message_channel_id
        self.__message_content: int = message_content


    @property
    def add(self) -> bool:
        super()._assert_not_deleted()
        return self.__add

    @property
    def allow_toggle(self) -> bool:
        super()._assert_not_deleted()
        return self.__allow_toggle

    @property
    def message_channel_id(self) -> int:
        super()._assert_not_deleted()
        return self.__message_channel_id

    @property
    def message_content(self) -> str:
        super()._assert_not_deleted()
        return self.__message_content

    @property
    def reaction_role_id(self) -> int:
        super()._assert_not_deleted()
        return self.__reaction_role_id

    @property
    def role_id(self) -> int:
        super()._assert_not_deleted()
        return self.__role_id


    async def _delete(self) -> bool:
        super()._assert_not_deleted()
        result = await _db_delete_reaction_role_change(self.id)
        if result:
            super()._set_deleted()
        return result


    async def update(self, role_id: int = None, add: bool = None, allow_toggle: bool = None, message_channel_id: int = None, message_content: str = None) -> bool:
        super()._assert_not_deleted()
        if role_id is None and add is None and allow_toggle is None and message_channel_id is None and message_content is None:
            return True
        role_id = role_id or self.role_id
        add = add or self.add
        allow_toggle = allow_toggle or self.allow_toggle
        message_channel_id = message_channel_id or self.message_channel_id
        message_content = message_content or self.message_content
        updated = await _db_update_reaction_role_change(self.id, role_id, add, allow_toggle, message_channel_id, message_content)
        if updated:
            self._role_id = role_id
            self.__add = add
            self.__allow_toggle = allow_toggle
            self.__message_channel_id = message_channel_id
            self.__message_content = message_content
        return updated





class ReactionRoleRequirement(_database.DatabaseRowBase):
    TABLE_NAME: str = 'reaction_role_requirement'
    ID_COLUMN_NAME: str = 'reaction_role_requirement_id'

    def __init__(self, reaction_role_requirement_id: int, reaction_role_id: int, role_id: int) -> None:
        super().__init__(reaction_role_requirement_id)
        self.__reaction_role_id: int = reaction_role_id
        self.__role_id: int = role_id


    @property
    def reaction_role_id(self) -> int:
        super()._assert_not_deleted()
        return self.__reaction_role_id

    @property
    def role_id(self) -> int:
        super()._assert_not_deleted()
        return self.__role_id


    async def _delete(self) -> bool:
        super()._assert_not_deleted()
        result = await _db_delete_reaction_role_requirement(self.id)
        if result:
            super()._set_deleted()
        return result


    async def update(self, role_id: str = None) -> bool:
        super()._assert_not_deleted()
        if role_id is None:
            return True
        role_id = role_id or self.role_id
        updated = await _db_update_reaction_role_requirement(self.id, role_id)
        if updated:
            self.__role_id = role_id
        return updated




# ---------- Static functions ----------

async def _db_delete_reaction_role(reaction_role_id: int) -> bool:
    result = await _database.delete_rows(
        ReactionRole.TABLE_NAME,
        ReactionRole.ID_COLUMN_NAME,
        [reaction_role_id],
    )
    return bool(result)


async def _db_update_reaction_role(reaction_role_id: int, message_id: int, name: str, reaction: str, is_active: bool) -> bool:
    result = await _database.update_row(
        ReactionRole.TABLE_NAME,
        ReactionRole.ID_COLUMN_NAME,
        reaction_role_id,
        message_id=message_id,
        name=name,
        reaction=reaction,
        is_active=is_active,
    )
    return bool(result)


async def _db_create_reaction_role_change(reaction_role_id: int, role_id: int, add: bool, allow_toggle: bool, message_channel_id: int, message_content: str) -> 'ReactionRoleChange':
    record = await _database.insert_row(
        ReactionRoleChange.TABLE_NAME,
        ReactionRoleChange.ID_COLUMN_NAME,
        reaction_role_id=reaction_role_id,
        role_id=role_id,
        add=add,
        allow_toggle=allow_toggle,
        message_channel_id=message_channel_id,
        message_content=message_content,
    )
    if record:
        return ReactionRoleChange(record[0], reaction_role_id, role_id, add, allow_toggle, message_channel_id, message_content)
    return None


async def _db_delete_reaction_role_change(reaction_role_change_id: int) -> bool:
    result = await _database.delete_rows(
        ReactionRoleChange.TABLE_NAME,
        ReactionRoleChange.ID_COLUMN_NAME,
        [reaction_role_change_id],
    )
    return bool(result)


async def _db_update_reaction_role_change(reaction_role_change_id: int, role_id: int, add: bool, allow_toggle: bool, message_channel_id: int, message_content: str) -> bool:
    result = await _database.update_row(
        ReactionRoleChange.TABLE_NAME,
        ReactionRoleChange.ID_COLUMN_NAME,
        reaction_role_change_id,
        role_id=role_id,
        add=add,
        allow_toggle=allow_toggle,
        message_channel_id=message_channel_id,
        message_content=message_content,
    )
    return bool(result)


async def _db_create_reaction_role_requirement(reaction_role_id: int, role_id: int) -> 'ReactionRoleRequirement':
    record = await _database.insert_row(
        ReactionRoleRequirement.TABLE_NAME,
        ReactionRoleRequirement.ID_COLUMN_NAME,
        reaction_role_id=reaction_role_id,
        role_id=role_id,
    )
    if record:
        return ReactionRoleRequirement(record[0], reaction_role_id, role_id)
    return None


async def _db_delete_reaction_role_requirement(reaction_role_requirement_id: int) -> bool:
    result = await _database.delete_rows(
        ReactionRoleRequirement.TABLE_NAME,
        ReactionRoleRequirement.ID_COLUMN_NAME,
        [reaction_role_requirement_id],
    )
    return bool(result)


async def _db_update_reaction_role_requirement(reaction_role_requirement_id: int, role_id: int) -> bool:
    result = await _database.update_row(
        ReactionRoleRequirement.TABLE_NAME,
        ReactionRoleRequirement.ID_COLUMN_NAME,
        reaction_role_requirement_id,
        role_id=role_id,
    )
    return bool(result)





# ---------- Testing ----------

async def test() -> bool:
    await _database.init()
    try:
        rr = await ReactionRole.create(1234, 'RR1234', '🙂')
    except Exception as e:
        return False

    try:
        await rr.update(message_id=1345, name='RR1345', reaction='🙃', is_active=False)
    except Exception as e:
        await rr.delete()
        return False

    try:
        ch_1 = await rr.add_change(2345, True, False)
    except Exception as e:
        await rr.delete()
        rr = None
        return False

    try:
        await ch_1.update(role_id=2456, add=False, allow_toggle=True, message_channel_id=3456, message_content='Test')
    except Exception as e:
        await ch_1._delete()
        await rr.delete()
        return False

    try:
        await rr.remove_change(ch_1.id)
        ch_1 = None
    except Exception as e:
        await ch_1._delete()
        await rr.delete()
        return False

    try:
        req_1 = await rr.add_requirement(6789)
    except Exception as e:
        await rr.delete()
        rr = None
        return False

    try:
        await req_1.update(role_id=6890)
    except Exception as e:
        await req_1._delete()
        await rr.delete()
        return False

    try:
        await rr.remove_requirement(req_1.id)
        req_1 = None
    except Exception as e:
        await req_1._delete()
        await rr.delete()
        return False

    ch_2 = await rr.add_change(2345, True, False)
    req_2 = await rr.add_requirement(6789)

    await rr.delete()
    print('All tests ran sucessfully!')


if __name__ == '__main__':
    _asyncio.get_event_loop().run_until_complete(test())