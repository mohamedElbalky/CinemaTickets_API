from django.http.response import JsonResponse, Http404


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import Guest, Reservation, Movie
from .serializers import MovieSerializer, GuestSerializer, ReservationSerializer




# without rest and model query FBV
def no_rest_no_model(request):
    guests = [
        {
            "id": 1,
            "name": "mohamed",
            "phone": "01064339829"
        },
        {
            "id": 2,
            "name": "ali",
            "phone": "01120293933"
        }
    ]

    return JsonResponse(guests, safe=False)


# with model query and without rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        "guests": list(data.values("name", "phone"))
    }

    return JsonResponse(response)


# FBV REST
# 1. GET POST
@api_view(["GET", "POST"])
def FBV_list(request, format=None):
    """
    List all guests, or create a new guest.
    """
    # GET
    if request.method == "GET":
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 2. GET PUT DELETE
@api_view(["GET", "PUT", "DELETE"])
def FBV_pk(request, pk=None,format=None):
    try:
        guest = Guest.objects.get(id=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        guest.dalete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ------------------------------------------------------------

# CBV REST
# 1. list, create
class CBVList(APIView):
    """
    List all guests, or create a new guest.
    """
    def get(self, request, format=None):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 2. retrive, update, delete
class CBV_Pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------------------------------------

# mixins
# 1. list, create
class MixinsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# 2. retrive, update, delete
class MixinsPk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# -----------------------------------------------------------------------

# generics
# 1. list, create
class GenericsList(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# 2. retrive, update, delete
class GenericPk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer



class GenericsListMovie(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


# 2. retrive, update, delete
class GenericPkMovie(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class GenericsListReservation(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# 2. retrive, update, delete
class GenericPkReservation(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
# --------------------------------------------------------


# viewsets
# class ViewsetsGuest(viewsets.ModelViewSet):
#     queryset = Guest.objects.all()
#     serializer_class = GuestSerializer


# class ViewsetsMovie(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer



@api_view(["GET"])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data.get("hall"),
        movie = request.data.get("movie")
    )

    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def new_reservation(request):
    movie = Movie.objects.get(
        hall = request.data.get("hall"),
        movie = request.data.get("movie")
    )
    guest = Guest()
    guest.name = request.data.get("name")
    guest.phone = request.data.get("phone")
    guest.save()

    reservation = Reservation()
    reservation.movie = movie
    reservation.guest = guest
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)







