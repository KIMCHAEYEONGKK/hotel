from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from . import models

class SearchForm(forms.Form):
    # ROOM_CHOICES = (
    #     ('Kids', 'Kids'),
    #     ('Spring', 'Spring'),
    #     ('Summer', 'Summer'),
    #     ('Autumn', 'Autumn'),
    #     ('Winter', 'Winter'),
    #     ('Room Only', 'Room Only'),
    #     ('Couple', 'Couple'),
    #     ('Spa', 'Spa'),
    #     ('Suite', 'Suite'),
    #     ('HoneyMoon', 'HoneyMoon'),
    #     ('Early Check-in', 'Early Check-in'),
    #     ('Late Check-out','Late Check-out'),
    #     ('Breakfast', 'Breakfast'),
    #     ('Dinning', 'Dinning')
    # )
    #
    #
    # keyword = forms.ChoiceField(label='키워드',widget=forms.Select(), choices=ROOM_CHOICES)
    # check_in = forms.CharField(label='체크인',required=True)
    # check_out = forms.CharField(label='체크아웃',required=True)
    search = forms.CharField(label='search', required=True)


    # adult = forms.IntegerField(label="어른",min_value=1, max_value=5,required=True)
    # child = forms.IntegerField(label="아이",min_value=1, max_value=5,required=True)
    # room_type = forms.ModelChoiceField(
    #     label="숙소 유형",
    #     required=False,
    #     empty_label="모든 숙소 유형",
    #     queryset=models.RoomType.objects.all(),
    # )
    # amenities = forms.ModelMultipleChoiceField(
    #     label="편의시설",
    #     required=False,
    #     queryset=models.Amenity.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    # )
    # facilities = forms.ModelMultipleChoiceField(
    #     label=("시설"),
    #     required=False,
    #     queryset=models.Facility.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    # )
    # beds = forms.IntegerField(label="침대", required=True, min_value=1,max_value=3)
    # bedrooms = forms.IntegerField(label='침실',required=True, min_value=1,max_value=3)
    # baths = forms.IntegerField(label="욕실",required=True, min_value=1, maz_value=3)


# class CreatePhotoForm(forms.ModelForm):
#     class Meta:
#         model = models.Photo
#         fields = ("caption", "file")
#
#         widgets = {
#             "caption": forms.TextInput(attrs={"autocomplete": "off"}),
#         }
#
#     def save(self,pk,*args, **kwargs):
#         photo = super().save(commit=False)
#         room = models.Room.objects.get(pk=pk)
#         photo.room = room
#         photo.save()
#

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "price",
            "keyword",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
            "check_in_time",
            "check_out_time",
            # 'adult',
            # "child"
        )

        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "off"}),
            "check_in": forms.TextInput(
                attrs={"placeholder": "17:12:34", "autocomplete": "off"}
            ),
            "check_out": forms.TextInput(
                attrs={"placeholder": "17:12:34", "autocomplete": "off"}
            ),
        }

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room