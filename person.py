from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import overload, Literal

@dataclass(frozen=True, slots=True)
class PronounSet:
    # TODO: write docstring
    subject: str                # she
    object_: str                # her
    possessive_adjective: str   # her book
    possessive_pronoun: str     # the book is hers
    reflexive: str              # herself
    
    def __str__(self) -> str:
        return f"{self.subject}/{self.object_}/{self.possessive_pronoun}"

class PronounPreset(Enum):
    #TODO: docstring
    HE_HIM = PronounSet("he", "him", "his", "his", "himself")
    SHE_HER = PronounSet("she", "her", "her", "hers", "herself")
    THEY_THEM = PronounSet("they", "them", "their", "theirs", "themself")
    IT_IT = PronounSet("it", "it", "its", "its", "itself")

    @property
    def pronouns(self) -> PronounSet:
        return self.value

    def __str__(self) -> str:
        return str(self.value)

NameInput = str | list[str] | None
PronounInput = PronounSet | PronounPreset | None

class Person:
    """Bloated class storing info about a person
    
    A Person class stores all data that can be known about a person for the
    purpose of archival.
    
    Attributes: (all attributes are optional unless noted otherwise)
        first_name: a string of the Person's first name
        middle_name: a list of strings of the Person's middle name(s)
        last_name: a string of the Person's last name
        preferred_name: a string of the Person's preferred name. Will be used
            in place of the Person's first name in most cases
        nickname: a list of strings of the Person's nickname(s). If the Person 
            has multiple nicknames, their "primary" nickname is listed in the 
            0th index
        former_first_name: a list of strings of the Person's previous first
            names
        former_last_name: a list of strings of the Person's previous last names
            
        pronouns: a PronounSet of the Person's pronouns
        gender: a string of the Person's gender
        sex: a string of the Person's sex
        sexuality: a string of the Person's personality
        age: an int of the Person's age. If the person's birthdate is set, 
            their age will be set automatically and cannot be changed
        birthdate: a Birthdate of the Person's birthdate. type verified
        height: an int of the Person's height in inches. type verified
        weight: an int of the Person's weight in pounds. type verified
        
        genitals: a string reperesenting the Person's genitals. A value of None
            does not represent that the Person has no genitals but rather that
            their genitals are unknown. No genitals should be represented as
            a string.
        
        is_real: a non-optional bool of whether the Person is real or not
    
    Properties:
        full_name: a stylised full name from the Person's names and nicknames
    
    Methods:
        #TODO: refurbish docstrings for methods
        format_height: a Person's height printed prettily. defaults to imperial
        format_weight: a Person's weight printed prettily. defaults to imperial
        #TODO: add _calculate_age() docstring
        #TODO: add _clean_name() docstring
        #TODO: add _coerce_names to docstring (static method)
        #TODO: add _coerce_pronouns to docstring (static method)
        #TODO: add _check_optional_positive_int to docstring (static method)
    """    
    def __init__(self,
        first_name: str | None = None,
        middle_name: NameInput = None,
        last_name: str | None = None,
        preferred_name: str | None = None,
        nickname: NameInput = None,
        former_first_name: NameInput = None,
        former_last_name: NameInput = None,
        
        pronouns: PronounInput = None,
        gender: str | None = None,
        sex: str | None = None,
        sexuality: str | None = None,
        age: int | None = None,
        birthdate: date | None = None,
        height: int | None = None,
        weight: int | None = None,
        
        genitals: str | None = None,
        
        is_real: bool=True,
    ):
        if age is not None and birthdate is not None:
            raise ValueError("Cannot provide both age and birthdate")
        
        self.first_name = self._coerce_names(first_name)
        self.middle_name = self._coerce_names(middle_name, force_list=True)
        self.last_name = self._coerce_names(last_name)
        self.preferred_name = self._coerce_names(preferred_name)
        self.nickname = self._coerce_names(nickname, force_list=True)
        self.former_first_name = self._coerce_names(former_first_name, 
                                                    force_list=True)
        self.former_last_name = self._coerce_names(former_last_name, 
                                                   force_list=True)
        
        self.pronouns = self._coerce_pronouns(pronouns)
        self.gender = gender
        self.sex = sex
        self.sexuality = sexuality
        self.__birthdate = None # so the age setter doesnt break
        self.age = age # using the setter to verify validity
        self.birthdate = birthdate
        self.height = height
        self.weight = weight
        
        self.genitals = genitals
        
        self.is_real = is_real
    
    def __repr__(self) -> str:
        return (f'Person(name={self.preferred_name or self.first_name!r})')
    
    def __str__(self) -> str:
        return self.full_name or "noname"
    
    # == getters/setters ==
    @property
    def age(self) -> int | None:
        if self.birthdate is None:
            return self.__age
        else: # calculates age using birthdate and date.today()
            return self._calculate_age()
    @age.setter
    def age(self, value: int | None):
        if self.birthdate is not None:
            raise ValueError("Cannot set age if birthdate is already set")
        elif not self._check_optional_positive_int(value):
            raise ValueError("age must be a non-negative int or None")
        self.__age = value
    
    @property
    def birthdate(self) -> date | None:
        return self.__birthdate
    @birthdate.setter
    def birthdate(self, value: date | None):
        if not isinstance(value, date) and value is not None:
            raise TypeError("birthdate must be a date or None")
        
        if value is None:
            # if changing the birthdate from a date to None, sets the age first
            if self.__birthdate is not None:
                self.__age = self._calculate_age()
                
        elif self.__age is not None:
            self.__age = None
            
        self.__birthdate = value
    
    @property
    def height(self) -> int | None:
        return self.__height
    @height.setter
    def height(self, value: int | None):
        if not self._check_optional_positive_int(value):
            raise ValueError("height must be a non-negative int or None")
        self.__height = value
    @property
    def weight(self) -> int | None:
        return self.__height
    @weight.setter
    def weight(self, value: int | None):
        if not self._check_optional_positive_int(value):
            raise ValueError("weight must be a non-negative int or None")
        self.__weight = value
    
    # == properties ==
    @property
    def full_name(self) -> str:
        name = []
        if self.preferred_name is not None:
            name.append(self.preferred_name)
            if self.first_name is not None:
                name.append(f"({self.first_name})")
        elif self.first_name is not None:
            name.append(self.first_name)
            
        if self.nickname: # checks for both None and empty list
            name.append(f'"{self.nickname[0]}"')
        
        if self.middle_name is not None:
            name += self.middle_name
            
        if self.last_name is not None:
            name.append(self.last_name)
            
        return " ".join(name)
    
    # == public methods ==
    def format_height(self, use_metric = False) -> str | None:
        # TODO: add docstring
        if self.height is not None:
            if not use_metric:
                return f"{self.height // 12}'{self.height % 12}\""
            return f"{round(self.height * 2.54)} cm"
        return None
    
    def format_weight(self, use_metric = False) -> str | None:
        # TODO: add docstring
        if self.weight is not None:
            if not use_metric:
                return f"{self.weight} lb{'' if self.weight == 1 else 's'}"
            return f"{round(self.weight * 0.45359237)} kg"
        return None

    # == private methods ==

    def _calculate_age(self) -> int:
        #TODO: add docstring
        if self.birthdate is None:
            raise AttributeError("Cannot calculate age with no birthdate set")
        
        today = date.today()
        
        return (today.year - self.birthdate.year - (
            (self.birthdate.month, self.birthdate.day) > 
            (today.month, today.day)
                ))
    
    @staticmethod
    def _check_optional_positive_int(value) -> bool:
        return value is None or (type(value) == int and value >= 0)
    
    @staticmethod
    def _clean_name(name: str) -> str | None:
        # TODO: docstring
        return name.strip() or None
    
    @overload
    @staticmethod
    def _coerce_names(name: NameInput, 
                      force_list: Literal[True]) -> list[str] | None:
        ...

    @overload
    @staticmethod
    def _coerce_names(name: str | None, 
                      force_list: Literal[False] = False) -> str | None:
        ...
    
    @staticmethod
    def _coerce_names(name: NameInput, 
                      force_list: bool = False) -> str | list[str] | None:
        # TODO: add docstring
        if isinstance(name, str):
            cleaned = Person._clean_name(name)
            return ([cleaned] if force_list else cleaned) if cleaned else None
        if isinstance(name, list) and force_list:
            if not all(isinstance(i, str) for i in name):
                raise TypeError("names must be strings")
            # remove blank strings
            return [cleaned for n in name if 
                    (cleaned := Person._clean_name(n))]
        if name is None:
            return None
        
        if force_list:
            raise TypeError("name must be string, list of strings, or None")
        raise TypeError("name must be string or None")
        
    @staticmethod
    def _coerce_pronouns(pronouns: PronounInput | list[str]
                         ) -> PronounSet | None:
        # TODO: add docstring
        if isinstance(pronouns, PronounPreset):
            return pronouns.pronouns
        if isinstance(pronouns, PronounSet):
            return pronouns
        if (isinstance(pronouns, list) 
                and all(isinstance(n, str) for n in pronouns) 
                and len(pronouns) == 5):
            return PronounSet(*pronouns)
        if pronouns is None:
            return None
        raise TypeError("pronouns must be a PronounSet, PronounPreset, "
                        "or None")