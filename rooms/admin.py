from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    fieldsets = (
        (
            "기본 정보",
            {
                "fields": (
                    "name",
                    "description",
                    "price",
                    "room_type",
                )
            },
        ),
        ("예약 가능", {"fields": ("check_in", "check_out",)}),
        ("예약 시간", {"fields": ("check_in_time", "check_out_time")}),
        ("구성", {"fields": ("beds", "bedrooms", "baths")}),
        (
            "시설 및 이용규칙",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("세부사항", {"fields": ('photo','keyword')}),
    )

    list_displays = [
        "name",
        'photo',
        'keyword',
        "price",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "count_amenities",
        "count_photos",
        "total_rating",
        "check_in_time",
        "check_out_time",
    ]

    ordering = ("name", "price", "bedrooms")

    list_filter = [
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    ]



    search_fields = ("^keyword", "^name", "^check_in","^check_out")

    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "편의 시설 수"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "사진 개수"