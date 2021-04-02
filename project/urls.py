from django.contrib import admin
from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from tickets.views import (
    no_rest_no_model,
    no_rest_from_model,
    FBV_list,
    FBV_pk,
    CBVList,
    CBV_Pk,
    MixinsList,
    MixinsPk,
    GenericsList,
    GenericPk,
    # ViewsetsMovie,
    GenericsListMovie,
    GenericPkMovie,
    GenericsListReservation,
    GenericPkReservation,
    find_movie,
    new_reservation,
)

# router = DefaultRouter()
# router.register('movies', ViewsetsMovie)




urlpatterns = [
    # viewsets
    # path("", include(router.urls)),

    path('admin/', admin.site.urls),

    # without rest and model query FBV
    path("no-rest-no-model/", no_rest_no_model),

    # with model query and without rest
    path("no-rest-from-model/", no_rest_from_model),

    # rest FBV
    path("FBV-list/", FBV_list),
    path("FBV-pk/<int:pk>/", FBV_pk),

    # rest CBV
    path("CBV-List/", CBVList.as_view()),
    path("CBV-Pk/<int:pk>/", CBV_Pk.as_view()),


    # rest mixins
    path("MixinsList/", MixinsList.as_view()),
    path("MixinsPk/<int:pk>/", MixinsPk.as_view()),

    # generics
    path("GenericsList/", GenericsList.as_view()),
    path("GenericPk/<int:pk>/", GenericPk.as_view()),

    path("GenericsListMovie/", GenericsListMovie.as_view()),
    path("GenericPkMovie/<int:pk>/", GenericPkMovie.as_view()),

    path("GenericsListReservation/", GenericsListReservation.as_view()),
    path("GenericPkReservation/<int:pk>/", GenericPkReservation.as_view()),

    # find movie
    path("find-movie/", find_movie),

    # new reservation
    path("new-reservation", new_reservation),


    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # auth token
    path('api-token-auth/', views.obtain_auth_token)
]


urlpatterns = format_suffix_patterns(urlpatterns)