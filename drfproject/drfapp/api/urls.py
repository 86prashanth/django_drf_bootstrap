from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

# routers 
router=DefaultRouter()
router.register('stream',Streamplatformv,basename='streamplatform'),
router.register('streamvs',StreamplatformMvs,basename='streamplatformmvs'),


urlpatterns = [
    path('',include(router.urls)),
    path('movie/list/',movie_list,name='home'),
    path('movie/<int:pk>/',movie_details,name='movie_details'),
    path('movielist/',MovieListAv.as_view(),name='movie_list'),
    path('watchlist/',Watchlistav.as_view(),name='watchlist'),
    path('movielist/<int:pk>/',MovieDetailAV.as_view(),name='movie_detail'),
    path('streamplatform/',StreamplatformAv.as_view(),name='streamplatform'),
    path('stream/<int:pk>',StreamplatformdetailAv.as_view(),name='streamplatform-detail'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    path('<int:pk>/review/',ReviewList.as_view(),name='review-list'),
    # path('review/<int:pk>/review/',ReviewLists.as_view(),name='review-list'),
    path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail'),
    # path('reviewg/<int:pk>/review',Reviewlistg.as_view(),name='review-listg'),
    path('reviewd/<int:pk>',ReviewDetailg.as_view(),name='review-detail'),
    path('review/<str:username>/',UserReview.as_view(),name='user-review-detail'),
]

