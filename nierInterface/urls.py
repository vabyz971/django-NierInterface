# @Author: Jahleel Lacascade <jahleel>
# @Date:   2020-11-17T07:05:55-04:00
# @Email:  vabyz971@gmail.com
# @Last modified by:   jahleel
# @Last modified time: 2020-11-17T08:03:18-04:00
# @License: GPLv3

from django.urls import path
from . import views

app_name = 'nierInterface'
urlpatterns = [
    path('theme/', views.ElementTheme.as_view(), name="element"),
    path('modal/', views.ModalTheme.as_view(), name="modal"),
]
