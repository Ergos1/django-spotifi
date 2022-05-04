from django.urls import include, path
from api.views import views_fbv, viewsets, views_cbv, file_upload
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = "api"
router = routers.DefaultRouter()
router.register(r'musics', viewsets.MusicViewSet, basename="Music")

urlpatterns = [
    path('', include(router.urls)),

    path('user/profile_image', file_upload.upload_image),
    path('music/like/', views_fbv.like_music),
    path('music/view/', views_fbv.view_music),
    path('categories/', views_cbv.CategoryList.as_view(), name="category_list"),
    path('albums/', views_cbv.AlbumList.as_view(), name="album_list"),
    path('artists/', views_cbv.ArtistList.as_view(), name="artist_list"),
    path('playlists/', views_cbv.PlaylistList.as_view(), name="artist_list"),
    path('sign-up/', views_fbv.sign_up_user, name="user_create"),
    path('sign-in/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify")
]