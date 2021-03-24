from __future__ import annotations
from typing import Optional

from pypeg2 import Namespace, Symbol

import love_geometry.peg_parser.consts as consts
from love_geometry.server.services.validator import LoveStoryValidator
import love_geometry.server.consts as server_consts


class ExtendedNamespace(Namespace):
    def __init__(self, *args, **kwargs):
        self._love_case = kwargs.get("love_case")
        self.errors = list()
        self._validate = server_consts.VALIDATE_LOVE_STORIES
        super().__init__(*args, **kwargs)

    def mutual_feelings_check(self, value) -> Optional[bool]:
        for feeling in consts.FEELINGS:
            has_mutual_feeling = value.data.get(feeling) and getattr(value.data.get(feeling),
                                                                     consts.DOUBLE_ENDED_RELATIONSHIP_FLAG_KEYWORD)
            if has_mutual_feeling:
                person1 = str(value.name)
                person2 = str(value.data.get(feeling)[0])
                if server_consts.VALIDATE_LOVE_STORIES:
                    existing_data1 = self.data.get(person1)
                    existing_names_for_that_feeling1 = list(existing_data1.data.values())[0] if existing_data1 else []
                    existing_data2 = self.data.get(person2)
                    existing_names_for_that_feeling2 = list(existing_data2.data.values())[0] if existing_data2 else []
                    if existing_names_for_that_feeling1:
                        existing_feeling = list(existing_data1.data.keys())[0]
                        error = LoveStoryValidator.check_for_duplicate(
                            existing_names_for_that_feeling1,
                            person2,
                            f"{consts.DOUBLE_ENDED_RELATIONSHIP_FLAG_KEYWORD} {feeling} / {existing_feeling}",
                            person1)
                        if error:
                            self.errors.append(error)
                    elif existing_names_for_that_feeling2:
                        existing_feeling = list(existing_data2.data.keys())[0]
                        error = LoveStoryValidator.check_for_duplicate(
                            existing_names_for_that_feeling2,
                            person1,
                            f"{consts.DOUBLE_ENDED_RELATIONSHIP_FLAG_KEYWORD} {feeling} / {existing_feeling}",
                            person2)
                        if error:
                            self.errors.append(error)

                love_case1 = self._love_case.generate_persons_love_case(person1, person2, feeling)
                love_case2 = self._love_case.generate_persons_love_case(person2, person1, feeling)

                self._save_persons_love_case(person1, love_case1)
                self._save_persons_love_case(person2, love_case2)

                return True

    def existing_feelings_check(self, key: Symbol, value: LoveCase) -> Optional[bool]:
        name = key
        all_feelings_exist = False
        if name in self.data:
            for feeling in consts.FEELINGS:
                feeling_should_be_extended = self.data[name].data.get(feeling) and value.data.get(feeling)
                if feeling_should_be_extended:
                    existing_names_for_that_feeling = self.data[name].data[feeling]
                    new_name_to_add = value.data[feeling][0]
                    if server_consts.VALIDATE_LOVE_STORIES:
                        error = LoveStoryValidator.check_for_duplicate(
                            existing_names_for_that_feeling,
                            new_name_to_add,
                            feeling,
                            key)
                        if error:
                            self.errors.append(error)
                    existing_names_for_that_feeling.extend(new_name_to_add)
                    all_feelings_exist = True

            if not all_feelings_exist:
                if server_consts.VALIDATE_LOVE_STORIES:
                    existing_names_for_that_feeling = list(self.data[name].data.values())
                    new_name_to_add = list(value.data.values())[0][0]
                    existing_feeling = list(self.data[name].data.keys())[0]
                    new_feeling = list(value.data.keys())[0]
                    error = LoveStoryValidator.check_for_duplicate(
                        existing_names_for_that_feeling,
                        new_name_to_add,
                        f"{existing_feeling} / {new_feeling}",
                        key)
                    if error:
                        self.errors.append(error)
                self.data[name].data = self.data[name].data | value.data

            return True

    def _save_persons_love_case(self, person: Person, love_case: LoveCase) -> None:
        if not self.data.get(person):
            self.data[str(person)] = love_case
        else:
            self.data[str(person)].data = self.data[str(person)].data | love_case.data

    def __setitem__(self, key: Symbol, value: LoveCase) -> None:
        if server_consts.VALIDATE_LOVE_STORIES and not consts.ALLOW_HIGH_SELF_ESTEEM:
            related_name = list(value.data.values())[0][0]
            related_feeling = list(value.data.keys())[0]
            error = LoveStoryValidator.check_for_duplicate(key, related_name, related_feeling)
            if error:
                self.errors.append(error)

        if self.mutual_feelings_check(value):
            return
        elif self.existing_feelings_check(key, value):
            return

        super().__setitem__(key, value)
