from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('entries/', views.DiaryEntryListView.as_view(), name='entries'),
    path('entries/new/', views.entry_create, name='entry_create'),
    path('entries/edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('entries/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('entries/list/', views.DiaryEntryListView.as_view(), name='diary_entry_list'),
    path('contact/', views.contact, name='contact_email'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('api/analytics-data/', views.analytics_data_api, name='analytics_data_api'),
]
