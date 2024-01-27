from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from . import views

urlpatterns = [
    path('',views.Home,name='Home'),
    path('auth/createUser/',views.createUser,name="createUser"),
    path('auth/loginUser/',views.loginUser,name="loginUser"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/turoCards/',views.turoCards.as_view()),
    path('api/turoCards/likeStatus/',views.likeStatus,name="likeStatus"),
    path('api/turoCards/comment/<id>',views.commentCard,name="commentCard"),
    path('api/turoCards/addComment/',views.addComment,name="addComment"),
    path('api/turoCards/swaprequest/',views.RegisterSwapRequest,name="RegisterSwapRequest"),
    path('api/allswaprequests/',views.AllSwapRequests,name="AllSwapRequests"),
    path('api/swaprequest/cards/',views.SwapCardDetails,name="SwapCardDetails"),
    path('api/cancelswaprequest/',views.CancelSwapRequest,name="CancelSwapRequest"),
    path('api/acceptswaprequest/',views.AcceptSwapRequest,name="AcceptSwapRequest"),
]
