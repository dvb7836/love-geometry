from __future__ import annotations
from typing import Optional

from pypeg2 import Namespace, Symbol

import love_geometry.peg_parser.consts as consts

from .love_case import LoveCase
from .people import People


class ExtendedNamespace(Namespace):
    def mutual_feelings_check(self, value) -> Optional[bool]:
        for feeling in consts.FEELINGS:
            has_mutual_feeling = value.data.get(feeling) and getattr(value.data.get(feeling),
                                                                     consts.DOUBLE_ENDED_RELATIONSHIP_FLAG_KEYWORD)
            if has_mutual_feeling:
                person1 = str(value.name)
                person2 = str(value.data.get(feeling)[0])

                self._add_love_cases_for_both_persons(person1, person2, feeling)

                return True

    def existing_feelings_check(self, origin_name: Symbol, value: LoveCase) -> Optional[bool]:
        if origin_name in self.data:
            if not self._extend_existing_names_for_that_feeling(origin_name, value):
                self.data[origin_name].data = {**self.data[origin_name].data, **value.data}
            return True

    def _extend_existing_names_for_that_feeling(self, origin_name: Symbol, value: LoveCase) -> Optional[bool]:
        for feeling in consts.FEELINGS:
            feeling_should_be_extended = self.data[origin_name].data.get(feeling) and value.data.get(feeling)
            if feeling_should_be_extended:
                new_name_to_add = value.data[feeling][0]
                existing_names_for_that_feeling = self.data[origin_name].data[feeling]
                existing_names_for_that_feeling.append(new_name_to_add)

                return True

    def _add_love_cases_for_both_persons(self, person1: str, person2: str, feeling: str) -> None:
        love_case1 = self._generate_persons_love_case(person1, person2, feeling)
        love_case2 = self._generate_persons_love_case(person2, person1, feeling)
        self._add_love_case_for_person(person1, love_case1)
        self._add_love_case_for_person(person2, love_case2)

    @staticmethod
    def _generate_persons_love_case(person1: str, person2: str, feeling: str) -> LoveCase:
        return LoveCase(
            [Symbol(feeling), People([person2], name=Symbol(feeling))], name=Symbol(person1)
        )

    def _add_love_case_for_person(self, person: str, love_case: LoveCase):
        if not self.data.get(person):
            self.data[person] = love_case
        else:
            self.data[person].data = {**self.data[person].data, **love_case.data}

    def __setitem__(self, key: Symbol, value: LoveCase) -> None:
        if self.mutual_feelings_check(value):
            return

        elif self.existing_feelings_check(key, value):
            return

        super().__setitem__(key, value)
