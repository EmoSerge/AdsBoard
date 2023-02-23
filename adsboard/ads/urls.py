from django.urls import path, include
from .views import *

urlpatterns = [
   path('', AdsList.as_view(), name='ads'),
   path('<int:pk>', Ad.as_view(), name='ad'),
   path('create/', AdCreate.as_view(), name='ad_create'),
   path('<int:pk>/update/', AdUpdate.as_view(), name='ad_update'),
   path('<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
   path('<int:pk>/create_resp/', ResponseCreate.as_view(), name='resp_create'),
   path('profile/', UserAdsList.as_view(), name='profile'),
   path('response/<int:pk>', Resp.as_view(), name='resp'),
   path('response/<int:pk>/accept', RespAccept.as_view(), name='resp_accept'),
   path('response/<int:pk>/delete', RespDelete.as_view(), name='resp_delete'),
   path('user_resp/', UserRespList.as_view(), name='user_resp'),

]
