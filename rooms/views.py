from datetime import date, timedelta

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from rooms.models import Room,Keyword
from . import models, forms
from rooms.forms import CreateRoomForm,SearchForm
from django.contrib import messages
# from users import mixins as user_mixins
# Create your views here.


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

def RoomDetail(request,pk):
    try:
        rooms = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return redirect('rooms:room_create')
    return render(request,'rooms/room_detail.html',{'rooms':rooms})


# def SearchView(request):
    # if request.method == "POST":
    #     form = SearchForm(request.POST)
    #     if form.is_valid():
    #         search = form.cleaned_data.get('search')
    #         # keyword = form.cleaned_data.get('keyword')
    #         # check_in = form.cleaned_data.get('check_in')
    #
    #         # check_out = form.cleaned_data.get('check_out')
    #         # room_type = form.cleaned_data.get('room_type')
    #
    #         filter_args = {}
    #         if search is not None:
    #             filter_args['search'] = search
    #
    #
    #         qs = models.Room.objects.filter(**filter_args).order_by("-created")
    #         paginator = Paginator(qs, 10, orphans=5)
    #
    #         page = request.GET.get("page", 1)
    #         rooms = paginator.get_page(page)
    #         return redirect('rooms:room_result', {"form": form, "rooms": rooms,'search':search})
    # else:
    #     form = forms.SearchForm()
    #
    # return render(request, "rooms/room_search.html", {"form": form})


def SearchView(request):
    roomlist = Room.objects.all()
    if request.method =="POST":
        search = request.POST['search']
        keyword = request.GET.getlist('keyword')
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']

        # key_list = Room.keyword.objects.all()
        # room_list = roomlist.objects.filter(keyword__icontains=search)
        # type = roomlist.objects.filter(room_type__icontains=search)
        # name1 = roomlist.objects.filter(name__icontains=search)
        name=Room.objects.filter(Q(keyword__contains=search) | Q(room_type__contains=search) | Q(name__contains=search) | Q(check_in__gte=check_in, check_out__lte=check_out)).all()
        dates = Room.objects.filter(check_in__gte=check_in, check_out__lte=check_out).values().all()

        return render(request, 'rooms/room_search.html', {'roomlist':roomlist,'query':search, 'keyword':keyword,'name':name,'range':dates})
    else:
        return render(request, 'rooms/room_search.html',{})

def CreateRoomView(request):
    if request.method == "POST":
        form = CreateRoomForm(request.POST, request.FIELES)
        if form.is_valid():
            room = Room()
            room.name = form.cleaned_data.get('name')
            room.price = form.cleaned_data.get('price')
            room.photo = form.cleaned_data.get('photo')
            room.description = form.cleaned_data.get('description')
            room.keyword = form.cleaned_data.get('keyword')
            room.check_in = form.cleaned_data.get('check_in')
            room.check_out = form.cleaned_data.get('check_out')
            room.amenities = form.cleaned_data.get("amenities")
            room.facilities = form.cleaned_data.get("facilities")
            room.beds = form.cleaned_data.get('beds')
            room.bedrooms = form.cleaned_data.get('bedrooms')
            room.baths = form.cleaned_data.get('baths')
            room.room_type = form.cleaned_data.get('room_type')
            room.check_in_time = form.cleaned_data.get('check_in_time')
            room.check_out_time = form.cleaned_data.get('check_out_time')
            room.host = request.user
            room.save()
            messages.success(request,"숙소가 등록되었습니다.")
            return redirect("rooms:room_detail")
    else:
        form = CreateRoomForm()
    return render(request, 'rooms/room_create',{'form':form})

# def result(request):
#     if request.method =='POST':
#         search = request.POST.get('search')
#         room = Room.objects.filter(name__contains=search)
#         return render(request, 'rooms/room_result.html',{'room':room})
#     else:
#         return render(request,'rooms/room_search.html',{})

def UpdateRoomView(request,pk):
    Rooms = Room.objects.get(pk=pk)
    if request.method == "POST":
        Rooms.name = request.POST['name']
        Rooms.price = request.POST['price']
        Rooms.photo = request.POST['photo']
        Rooms.description = request.POST['description']
        Rooms.keyword = request.POST['keyword']
        Rooms.check_in = request.POST['check_in']
        Rooms.check_out = request.POST['check_out']
        Rooms.amenities = request.POST['amenities']
        Rooms.beds =request.POST['beds']
        Rooms.bedrooms = request.POST['bedrooms']
        Rooms.baths = request.POST['baths']
        Rooms.room_type = request.POST['room_type']
        Rooms.check_in_time = request.POST['check_in_time']
        Rooms.check_out_time = request.POST['check_out_time']
        Rooms.host = request.user
        Rooms.save()
        return redirect('rooms:room_detail')
    return render(request, 'rooms/room_update.html',{"Rooms":Rooms})