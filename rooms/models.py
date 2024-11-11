
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel


class AbstractItem(TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    objects = None

    class Meta:
        verbose_name = ("편의시설")
        db_table="UserAmenity"
        ordering = ["name"]


class Facility(AbstractItem):

    """ Facility Model Definition """

    objects = None

    class Meta:
        verbose_name = ("시설")
        db_table="UserFacility"
        ordering = ["name"]


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = ("숙소 이용규칙")
        verbose_name_plural = ("숙소 이용규칙")
        ordering = ["name"]


# class Photo(TimeStampedModel):
#
#     """ Photo Model Definition """
#     caption = models.CharField(("설명"), max_length=80)
#     file = models.ImageField(("이미지"), upload_to="room_photos")
#     room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.caption
#
#     class Meta:
#         verbose_name = "사진"
#         verbose_name_plural = "사진"
# Create your models here.

ROOM_CHOICES = (
    ('Kids','Kids'),
    ('Spring','Spring'),
    ('Summer','Summer'),
    ('Autumn','Autumn'),
    ('Winter','Winter'),
    ('Room Only','Room Only'),
    ('Couple','Couple'),
    ('Spa','Spa'),
    ('Suite','Suite'),
    ('HoneyMoon','HoneyMoon'),
    ('Early Check-in', 'Early Check-in'),
    ('Late Check-out', 'Late Check-out'),
    ('Breakfast','Breakfast'),
    ('Dinning','Dinning')
)

ROOM_TYPE=(
    ('Deluxe','Deluxe'),
    ('Studio Suite', 'Studio Suite'),
    ('Premier Suite', 'Premier Suite'),
    ('Luxury Suite','Luxury Suite'),
    ('The Suite','The Suite'),
    ('Hill Suite','Hill Suite'),
    ('Prestige Hill Suite', 'Prestige Hill Suite'),
    ('Superior Room','Superior Room'),
    ('Executive Room','Executive Room')
)
class Room(models.Model):
    DoesNotExist = None
    objects = None
    name=models.CharField(max_length=20, verbose_name="숙소명")
    photo = models.ImageField(verbose_name="사진")
    description=models.TextField(verbose_name='설명')
    price=models.IntegerField(verbose_name="가격")
    keyword = models.CharField(verbose_name='키워드',choices=ROOM_CHOICES,max_length=100)
    check_in = models.CharField(verbose_name="체크인",max_length=20)
    check_out = models.CharField(verbose_name="체크아웃",max_length=20)
    check_in_time = models.CharField(verbose_name="체크인 시간",max_length=20)
    check_out_time = models.CharField(verbose_name="체크아웃 시간",max_length=20)
    # host = models.ForeignKey(
    #     "accounts.Account", related_name="rooms", verbose_name="호스트", on_delete=models.CASCADE
    # )
    beds = models.IntegerField(
        verbose_name="침대", validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    bedrooms = models.IntegerField(
        verbose_name="침실", validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    baths = models.IntegerField(
        verbose_name="욕실", validators=[MinValueValidator(1), MaxValueValidator(3)]
    )


    room_type = models.CharField(verbose_name="숙소유형",choices=ROOM_TYPE, max_length=100)
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", verbose_name="편의시설", blank=True
    )
    facilities = models.ManyToManyField(
        "Facility", related_name="rooms", verbose_name="시설", blank=True
    )
    house_rules = models.ManyToManyField(
        "HouseRule", related_name="rooms", verbose_name="숙소 이용규칙", blank=True
    )

    def __str__(self):
        return self.name

    def get_first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_second_photo(self):
        try:
            (photo,) = self.photos.all()[1:2]
            return photo.file.url
        except ValueError:
            return None

    def get_third_photo(self):
        try:
            (photo,) = self.photos.all()[2:3]
            return photo.file.url
        except ValueError:
            return None

    def get_fourth_photo(self):
        try:
            (photo,) = self.photos.all()[3:4]
            return photo.file.url
        except ValueError:
            return None

    def get_fifth_photo(self):
        try:
            (photo,) = self.photos.all()[4:5]
            return photo.file.url
        except ValueError:
            return None

    # def get_calendars(self):
    #     now = timezone.now()
    #     this_year = now.year
    #     this_month = now.month
    #     next_month = this_month + 1
    #     if this_month == 12:
    #         next_month = 1
    #     this_month_cal = Calender(this_year, this_month)
    #     next_month_cal = Calendar(this_year, next_month)
    #     return [this_month_cal, next_month_cal]

    class Meta:
        db_table="UserRooms"
        verbose_name="rooms"

class Keyword(models.Model):
    objects = None
    ROOM_CHOICES = (
        ('Kids', 'Kids'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
        ('Winter', 'Winter'),
        ('Room Only', 'Room Only'),
        ('Couple', 'Couple'),
        ('Spa', 'Spa'),
        ('Suite', 'Suite'),
        ('HoneyMoon', 'HoneyMoon'),
        ('Early Check-in', 'Early Check-in'),
        ('Late Check-out', 'Late Check-out'),
        ('Breakfast', 'Breakfast'),
        ('Dinning', 'Dinning')
    )
    keyword = models.CharField(verbose_name='키워드', choices=ROOM_CHOICES, max_length=100)
    class Meta:
        db_table="UserKeywords"
        verbose_name="keywords"