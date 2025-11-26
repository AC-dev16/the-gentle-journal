from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('list/', views.DiaryEntryListView.as_view(), name='diary_entry_list'),
]
