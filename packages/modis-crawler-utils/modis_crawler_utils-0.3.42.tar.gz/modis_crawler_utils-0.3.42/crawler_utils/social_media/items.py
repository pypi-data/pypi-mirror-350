import time
from datetime import date, datetime
from enum import Enum
from typing import Annotated, Any, List, Optional, Sequence

from dateparser import parse
from dateparser.date import DateDataParser
from pydantic import AfterValidator, FileUrl, BaseModel, ConfigDict, Field, model_validator
from pydantic.networks import UrlConstraints

from crawler_utils.misc import compact


class BaseSMModel(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        validate_assignment=True,
        populate_by_name=True,
        extra='allow'
    )

class FileOrAnyUrl(FileUrl):
    #NOTE: like pydantic.AnyUrl but with optional host
    _constraints = UrlConstraints() # disable FileUrl's limitation on allowed schemas 

def validate_url(url: str) -> str:
    return FileOrAnyUrl(url) and url


URL = Annotated[str, AfterValidator(validate_url)]


class SocialMediaItem(BaseSMModel):
    url: URL = Field(alias='_url')
    platform: str = Field()
    type: str = Field()
    timestamp: int = Field(alias='_timestamp', default_factory=lambda: int(time.time()))
    attachments: List['Attachment'] = Field(alias='_attachments', default_factory=list)

    # Pydantic does not consider underscore attributes as fields
    # Expose them as properties for backwards compatibility
    def _get_url(self) -> URL:
        return self.url

    def _set_url(self, value: URL):
        self.url = value

    _url = property(_get_url, _set_url)

    def _get_timestamp(self) -> int:
        return self.timestamp

    def _set_timestamp(self, value: int):
        self.timestamp = value

    _timestamp = property(_get_timestamp, _set_timestamp)

    def _get_attachments(self):
        return self.attachments

    def _set_attachments(self, value: List['Attachment']):
        self.attachments = value

    _attachments = property(_get_attachments, _set_attachments)


UnixTimestamp = int  # Имитация типа timestamp
Count = Annotated[int, Field(ge=0)]


def class_output(item: BaseSMModel) -> dict:
    """
    Serializes item to dict, removing None or empty values
    """
    serialized_item = item.model_dump(by_alias=True)
    item.model_validate(serialized_item)  # to revalidate mutable fields, e.g. lists of attachments
    if isinstance(item, SocialMediaItem) and not isinstance(item, SocialConnection):
        serialized_item.setdefault('url', item.url)  # ensure sm entities have url field
    return compact(serialized_item)


def list_of_types_output(list_of_objects: Sequence[BaseSMModel]) -> list[dict]:
    """
    Serializes list of items, removing None or empty values
    """
    return list(filter(bool, map(class_output, list_of_objects)))


def validate_enum_or_raw_present(model: BaseSMModel, enum_field_name: str) -> BaseSMModel:
    raw_field_name = f'{enum_field_name}_raw'
    if not (getattr(model, enum_field_name) or getattr(model, raw_field_name)):
        raise ValueError(f'Either {enum_field_name} or {raw_field_name} must be defined')
    return model


def parse_partial_date(text: str, **dateparser_kwargs) -> Optional['Date']:
    """
    Parses possibly incomplete absolute dates, e.g. "7 марта" => Date(month=3, day=7).

    Uses dateparser library, applies it with different settings to determine which date fields were missing.

    Relative dates parsing is not supported, use dateparser.parse() directly.

    :param text:
        String with possibly incomplete absolute date

    :param dateparser_kwargs:
        Keyword arguments that can be supplied to dateparser.parse() function (e.g. date_formats, languages).
        See https://dateparser.readthedocs.io/en/latest/dateparser.html#dateparser.parse for reference.
        Note that settings related to incomplete dates parsing (PREFER_XXX, RELATIVE_BASE) are used internally
        and will be overridden
    """
    base_settings = dateparser_kwargs.pop('settings', {})
    date_formats = dateparser_kwargs.pop('date_formats', None)

    def _parse(**settings):
        parser = DateDataParser(**dateparser_kwargs,
                                settings={**base_settings, **settings,
                                          'RETURN_TIME_AS_PERIOD': True})
        date_data = parser.get_date_data(text, date_formats)
        if not date_data or not (date_obj := date_data.date_obj):
            return None
        return Date(
            year=date_obj.year,
            month=date_obj.month,
            day=date_obj.day,
            hour=date_obj.hour if date_data.period == 'time' else None,
            minutes=date_obj.minute if date_data.period == 'time' else None
        )

    if not (past_date := _parse(PREFER_DATES_FROM='past', PREFER_MONTH_OF_YEAR='first', PREFER_DAY_OF_MONTH='first')):
        return None
    if not (future_date := _parse(PREFER_DATES_FROM='future', PREFER_MONTH_OF_YEAR='last', PREFER_DAY_OF_MONTH='last',
                                  RELATIVE_BASE=datetime(year=datetime.now().year + 1, month=12, day=31))):
        return None

    day = past_date.day if past_date.day == future_date.day else None
    month = past_date.month if past_date.month == future_date.month else None
    year = past_date.year if (future_date.year - past_date.year) in (0, 100) else None  # 100 for 2-digit years
    hour = past_date.hour
    minutes = past_date.minutes

    if all(x is None for x in (day, month, year, hour, minutes)):
        return None

    return Date(day=day, month=month, year=year, hour=hour, minutes=minutes)


# TODO move all utility functions to separate module
def parse_birth_date(text: str, **dateparser_kwargs) -> Optional['BirthDay']:
    """
    Parses possibly incomplete birth dates using dateparser library.

    :param text:
        String with possibly incomplete birth date

    :param dateparser_kwargs:
        Keyword arguments that can be supplied to dateparser.parse() function (e.g. date_formats, languages).
        See https://dateparser.readthedocs.io/en/latest/dateparser.html#dateparser.parse for reference.
        Note that settings related to incomplete dates parsing (PREFER_XXX, RELATIVE_BASE) are used internally
        and will be overridden.
        Assumes DMY date order by default.
    """
    base_settings = dateparser_kwargs.pop('settings', {})
    base_settings.setdefault('DATE_ORDER', 'DMY')  # disputable

    normalized_text = text.replace('.', '-')  # day.month may be parsed as time
    partial_date = parse_partial_date(normalized_text, settings=base_settings, **dateparser_kwargs)

    if not partial_date:
        return None
    if all(x is None for x in (partial_date.day, partial_date.month, partial_date.year)):
        return None
    if any(x is not None for x in (partial_date.hour, partial_date.minutes)):
        # birth date should not have time component
        return None

    return BirthDay(day=partial_date.day, month=partial_date.month, year=partial_date.year)


parse_birth_date_to_class = parse_birth_date


def parse_date(date_text):
    if date_text is None:
        return None
    dt = parse(date_text.rstrip())
    return int(time.mktime(dt.timetuple()))


class AccountStatus(Enum):
    ACTIVE = "Active"
    DELETED = "Deleted"
    BANNED = "Banned"
    CLOSED = "Closed"
    NOT_SPECIFIED = None


class AttachmentType(Enum):
    FILE = "file"
    DOCUMENT = "document"
    IMAGE = "image"
    LINK = "link"
    VIDEO = "video"
    AUDIO = "audio"
    NOT_SPECIFIED = None


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    NOT_SPECIFIED = None


class NameType(Enum):
    MAIDEN_NAME = "Maiden Name"
    NICKNAME = "Nickname"
    NOT_SPECIFIED = None


class EducationalInstitutionType(Enum):
    SCHOOL = "School"
    COLLEGE = "College"
    INSTITUTE = "Institute"
    UNIVERSITY = "University"
    ACADEMY = "Academy"
    COURSES = "Courses"
    NOT_SPECIFIED = None


class EducationStatus(Enum):
    PUPIL = "Pupil"
    STUDENT = "Student"
    GRADUATE = "Graduate"
    NOT_SPECIFIED = None


class MessageType(Enum):
    POST = "Post"
    COMMENT = "Comment"
    VIDEO = "Video"
    PHOTO = "Photo"
    AUDIO = "Audio"
    NEWS = "News"
    NOT_SPECIFIED = None


class AccessType(Enum):
    PUBLIC = "Public"
    CLOSED = "Closed"
    NOT_SPECIFIED = None


class RelationshipStatus(Enum):
    NOT_MARRIED = "Not married"
    DATING = "Dating"
    ENGAGED = "Engaged"
    MARRIED = "Married"
    IN_A_CIVIL_MARRIAGE = "In a civil marriage"
    IN_LOVE = "In love"
    ITS_DIFFICULT = "It's difficult"
    IN_ACTIVE_SEARCH = "In active search"
    SEPARATED = "Separated"
    IN_A_FREE_RELATIONSHIP = "In a free relationship"
    IN_A_HOME_PARTNERSHIP = "In a home partnership"
    WIDOWED = "Widowed"
    NOT_SPECIFIED = None


class FriendsOrFollowers(Enum):  # TODO replace with SocialConnectionType
    # В ОК бывают Либо друзья Либо подписчики, в то время, как в модели есть и поле
    # followers и поле friends , поэтому при выставлении этих полей необходимо определить
    # какое поле используется на ресурсе
    FOLLOWERS = "Subscribers"
    FRIENDS = "Friends"


class RelativesAndMaritalStatusType(Enum):
    CHILD = "Child"
    SIBLING = "Sibling"
    PARENT = "Parent"
    GRANDCHILD = "Grandchild"
    GRANDPARENT = "Grandparent"
    RELATION_PARTNER = "Relation partner"
    NOT_SPECIFIED = None


class ContactType(Enum):
    PHONE = 'Phone'
    EMAIL = 'Email'
    WEBSITE = 'Website'
    SKYPE = 'Skype'
    TELEGRAM = 'Telegram'
    WHATSAPP = 'WhatsApp'
    VIBER = 'Viber'
    VK = 'VK'
    OK = 'OK'
    FACEBOOK = 'Facebook'
    INSTAGRAM = 'Instagram'
    TWITTER = 'Twitter'
    TIKTOK = 'TikTok'
    NOT_SPECIFIED = None


class SocialConnectionType(Enum):
    FOLLOWER = 'Follower'
    FRIEND = 'Friend'
    ADMIN = 'Admin'
    REACTION = 'Reaction'
    NOT_SPECIFIED = None


class SmokingAlcoholAttitude(Enum):
    POSITIVE = 'Positive'
    NEUTRAL = 'Neutral'
    COMPROMISE = 'Compromise'
    NEGATIVE = 'Negative'
    VERYNEGATIVE = 'Sharply negative'
    NOT_SPECIFIED = None


class PoliticalView(Enum):
    COMMUNIST = 'Communist'
    SOCIALIST = 'Socialist'
    MODERATE = 'Moderate'
    LIBERAL = 'Liberal'
    CONSERVATIVE = 'Conservative'
    MONARCHICAL = 'Monarchical'
    ULTRACONSERVATIVE = 'Ultraconservative'
    INDIFFERENT = 'Indifferent'
    LIBERTARIAN = 'Libertarian'
    NOT_SPECIFIED = None


class LastOnlinePlatform(Enum):
    MOBILE = 'The mobile version'
    IPHONE = 'Application for iPhone'
    IPAD = 'App for iPad'
    ANDROID = 'Application for Android'
    WIN_PHONE = 'Application for Windows Phone'
    WIN_10 = 'Application for Windows 10'
    FULL_SITE = 'Full version of the site'


class BirthDay(BaseSMModel):
    day: Optional[int] = Field(default=None, ge=1, le=31)
    month: Optional[int] = Field(default=None, ge=1, le=12)
    year: Optional[int] = Field(default=None, ge=0)

    @model_validator(mode='after')
    def validate_birth_day(self):
        date(
            year=self.year or 1970,
            month=self.month or 1,
            day=self.day or 1
        )
        return self


class Date(BaseSMModel):
    day: Optional[int] = Field(default=None, ge=1, le=31)
    month: Optional[int] = Field(default=None, ge=1, le=12)
    year: Optional[int] = Field(default=None, ge=0)
    hour: Optional[int] = Field(default=None, ge=0, le=23)
    minutes: Optional[int] = Field(default=None, ge=0, le=59)

    @model_validator(mode='after')
    def validate_datetime(self):
        datetime(
            year=self.year or 1970,
            month=self.month or 1,
            day=self.day or 1,
            hour=self.hour or 0,
            minute=self.minutes or 0
        )
        return self


class Location(BaseSMModel):
    raw: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)  # Вместо double
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)  # Вместо double
    street: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None
    # ____________Other Fields_________
    url: Optional[URL] = None


class OtherName(BaseSMModel):
    name: str
    other_name_type: Optional[NameType] = None
    other_name_type_raw: Optional[str] = None


class EducationalInstitution(BaseSMModel):
    name: str
    edu_id: Optional[str] = None
    education_institution_type: Optional[EducationalInstitutionType] = None
    education_institution_type_raw: Optional[str] = None
    from_date: Optional[Date] = None
    until_date: Optional[Date] = None
    city: Optional[str] = None
    country: Optional[str] = None
    status: Optional[EducationStatus] = None
    status_raw: Optional[str] = None
    faculty: Optional[str] = None
    chair: Optional[str] = None
    speciality: Optional[str] = None
    # __________Other Fields____________
    url: Optional[URL] = None  # FB
    description: Optional[str] = None  # FB


class RelativesAndMaritalStatus(BaseSMModel):
    name: str
    relatives_and_marital_status_type: Optional[RelativesAndMaritalStatusType] = None
    relatives_and_marital_status_type_raw: Optional[str] = None
    relative_id: Optional[str] = None
    url: Optional[URL] = None


class Workplace(BaseSMModel):
    name: str
    career_id: Optional[str] = None
    from_date: Optional[Date] = None
    until_date: Optional[Date] = None
    city: Optional[str] = None
    country: Optional[str] = None
    position: Optional[str] = None
    # __________Other Fields____________
    url: Optional[URL] = None  # FB
    description: Optional[str] = None  # FB
    location: Optional[Location] = None  # FB


class MilitaryUnit(BaseSMModel):
    unit: str
    unit_id: Optional[str] = None
    from_date: Optional[Date] = None
    until_date: Optional[Date] = None


class VolunteerExperience(BaseSMModel):
    name: Optional[str] = None
    position: Optional[str] = None
    description: Optional[str] = None
    from_date: Optional[Date] = None
    until_date: Optional[Date] = None


class Projects(BaseSMModel):
    title: Optional[str] = None
    url: Optional[URL] = None
    from_date: Optional[Date] = None
    until_date: Optional[Date] = None


class Certificate(BaseSMModel):
    name: Optional[str] = None
    url: Optional[URL] = None
    company_url: Optional[URL] = None
    authority: Optional[str] = None
    from_date: Optional[Date] = None
    until_date: Optional[Date] = None


class Contact(BaseSMModel):
    value: str
    contact_type: Optional[ContactType] = None
    contact_type_raw: Optional[str] = None
    contact_subtype: Optional[str] = None  # e.g. mobile/home/etc for phones

    @model_validator(mode='after')
    def validate_contact_type(self):
        return validate_enum_or_raw_present(self, 'contact_type')


class Attachment(BaseSMModel):
    url: URL
    attachment_type: Optional[AttachmentType] = None
    attachment_type_raw: Optional[str] = None
    title: Optional[str] = None
    path: Optional[str] = None
    filename: Optional[str] = None
    checksum: Optional[str] = None
    status: Optional[str] = None
    to_be_downloaded: bool = True
    # __________Other Fields____________
    attachment_id: Optional[str] = None  # VK
    owner_id: Optional[str] = None  # VK
    image_url: Optional[URL] = None  # VK
    duration: Optional[float] = None  # VK
    artist: Optional[str] = None  # VK

    @model_validator(mode='after')
    def validate_attachment_type(self):
        return validate_enum_or_raw_present(self, 'attachment_type')


class SocialConnection(SocialMediaItem):
    from_id: str = Field()
    to_id: str = Field()
    social_connection_type: Optional[SocialConnectionType] = None
    social_connection_type_raw: Optional[str] = None
    type: str = Field(default='social_connection', init_var=False)
    # __________Other Fields____________
    from_url: Optional[URL] = None  # FB
    to_url: Optional[URL] = None  # FB
    relation_type: Optional[str] = None  # FB
    role: Optional[str] = None  # FB
    liked_type: Optional[str] = None  # FB
    like_type: Optional[str] = None  # FB

    @model_validator(mode='after')
    def validate_social_connection_type(self):
        return validate_enum_or_raw_present(self, 'social_connection_type')


class Company(SocialMediaItem):
    name: str
    company_id: Optional[int] = None
    type: str = Field(default='company_profile', init_var=False)
    # ______________Main Info__________________
    is_snippet: bool = False
    main_photo: Optional[URL] = None
    location: Optional[Location] = None
    contact_info: Optional[List[Contact]] = None
    start_date: Optional[Date] = None
    # __________Other Fields____________
    description: Optional[str] = None
    members_count: Optional[Count] = None
    category: Optional[List[str]] = None


class MessageAuthor(BaseSMModel):
    name: str
    id: Optional[str] = None
    url: Optional[URL] = None
    email: Optional[str] = None
    main_photo: Optional[URL] = None


class HistoryMessage(SocialMediaItem):
    message_id: str = Field()
    text: Optional[str] = None
    date: Optional[UnixTimestamp] = None
    type: str = Field(default='message', init_var=False)
    owner_id: Optional[str] = None
    message_type: Optional[MessageType] = None
    author: Optional[List[MessageAuthor]] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    replies_to: Optional[str] = None
    replies_count: Optional[Count] = None
    reactions_count: Optional[Count] = None
    comments_count: Optional[Count] = None
    views_count: Optional[Count] = None
    location: Optional[Location] = None
    category: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    agency: Optional[str] = None
    language: Optional[str] = None
    main_photo: Optional[URL] = None
    # __________Other Fields____________
    is_shared: bool = False  # OK
    shared_in: Optional[str] = None  # OK
    image_caption: Optional[str] = None  # Instagram
    is_pinned: bool = False  # VK
    replies_to_user: Optional[str] = None  # VK
    scope: Optional[str] = None  # FB
    quotes_count: Optional[Count] = None  # Twitter
    retweet_count: Optional[Count] = None  # Twitter
    story_url: Optional[URL] = None  # yandex_news
    description: Optional[str] = None  # TASS
    modification_date: Optional[UnixTimestamp] = None  # RIA, Vedomosti

    def model_post_init(self, __context: Any) -> None:
        if self.message_type:
            if isinstance(self.message_type, MessageType) and self.message_type != MessageType.NOT_SPECIFIED:
                self.type = self.message_type.value.lower()
            elif isinstance(self.message_type, str):
                self.type = self.message_type.lower()


class Message(HistoryMessage):
    copy_history: Optional[List[HistoryMessage]] = None


class UserProfile(SocialMediaItem):
    user_id: str = Field()
    name: str = Field()
    type: str = Field(default='user_profile', init_var=False)
    account_status: Optional[AccountStatus] = None
    # ______________Main Info__________________
    is_snippet: bool = False
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    login: Optional[str] = None
    gender: Optional[Gender] = None
    current_place: Optional[Location] = None
    birth_place: Optional[Location] = None
    places_lived: Optional[List[Location]] = None
    birth_day: Optional[BirthDay] = None
    other_names: Optional[List[OtherName]] = None
    # _______________Relationship_______________
    relation_status: Optional[RelationshipStatus] = None
    relatives: Optional[List[RelativesAndMaritalStatus]] = None
    interested_in: Optional[Gender] = None
    friends_count: Optional[Count] = None
    followers_count: Optional[Count] = None
    # _________________Education_________________
    education: Optional[List[EducationalInstitution]] = None
    career: Optional[List[Workplace]] = None
    military: Optional[List[MilitaryUnit]] = None
    # ____________Religion and Political_________
    religion: Optional[str] = None
    political: Optional[PoliticalView] = None
    political_raw: Optional[str] = None
    smoking: Optional[SmokingAlcoholAttitude] = None
    smoking_raw: Optional[str] = None
    alcohol: Optional[SmokingAlcoholAttitude] = None
    alcohol_raw: Optional[str] = None
    # ____________Hobbies and interests___________
    interests: Optional[str] = None
    music: Optional[str] = None
    movies: Optional[str] = None
    tv: Optional[str] = None
    books: Optional[str] = None
    games: Optional[str] = None
    quotes: Optional[str] = None
    activities: Optional[str] = None
    sports: Optional[str] = None
    teams: Optional[str] = None
    about: Optional[str] = None
    # __________Other Fields____________
    languages: Optional[List[str]] = None
    contacts: Optional[List[Contact]] = None
    main_photo: Optional[URL] = None
    cover_photo: Optional[URL] = None
    created: Optional[UnixTimestamp] = None  # Вместо ts
    updated: Optional[UnixTimestamp] = None  # Вместо ts
    last_logged_in: Optional[UnixTimestamp] = None  # Вместо ts
    last_logged_in_platform: Optional[LastOnlinePlatform] = None
    verified: Optional[bool] = None
    status: Optional[str] = None
    # _________Resource-specific Fields_________
    volunteer_experience: Optional[List[VolunteerExperience]] = None  # Linkedin
    projects: Optional[List[Projects]] = None  # Linkedin
    courses: Optional[List[str]] = None  # Linkedin
    certificates: Optional[List[Certificate]] = None  # Linkedin
    values_in_life: Optional[str] = None  # VK
    values_in_people: Optional[str] = None  # VK
    inspired_by: Optional[str] = None  # VK
    skills: Optional[List[str]] = None  # FB, Linkedin


class GroupProfile(SocialMediaItem):
    comm_id: str = Field()
    name: str = Field()
    type: str = Field(default='group_profile', init_var=False)
    is_snippet: bool = False
    account_status: Optional[AccountStatus] = None
    description: Optional[str] = None
    members_count: Optional[Count] = None
    main_photo: Optional[URL] = None
    cover_photo: Optional[URL] = None
    place: Optional[Location] = None
    start_date: Optional[UnixTimestamp] = None
    # __________Other Fields____________
    access_type: Optional[AccessType] = None  # FB
    page_type: Optional[str] = None  # FB
    categories: Optional[List[str]] = None  # FB
    contacts: Optional[List[Contact]] = None  # FB
    other_information: Optional[dict] = None  # FB
    business_info: Optional[dict] = None  # FB
    members: Optional[List[SocialConnection]] = None  # FB
    milestones: Optional[dict] = None  # FB
    page_story_url: Optional[URL] = None  # FB
    activity_status: Optional[dict] = None  # FB


def set_friends_or_followers(followers_or_friend_field_text,
                             followers_or_friend_count,
                             friends_or_followers_field: FriendsOrFollowers):
    if followers_or_friend_count and \
            followers_or_friend_field_text == friends_or_followers_field.value:
        return int(followers_or_friend_count.replace(" ", ""))
    else:
        return None


def set_gender(gender):
    if gender is None:
        return Gender.NOT_SPECIFIED.value
    gender = gender.upper()
    if gender == str(Gender.MALE.value).upper():
        return Gender.MALE.value
    if gender == str(Gender.FEMALE.value).upper():
        return Gender.FEMALE.value
    else:
        return Gender.OTHER.value
