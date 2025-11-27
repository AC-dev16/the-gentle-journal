from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('entries/', views.entry_create, name='entries'),
    path('entries/delete/<int:entry_id>/', views.entry_delete, name='delete_entry'),
    path('list/', views.DiaryEntryListView.as_view(), name='diary_entry_list'),
]
