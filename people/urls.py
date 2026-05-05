from django.urls import path

from . import views

app_name = 'people'

urlpatterns = [
    path('', views.PersonListView.as_view(), name='person_list'),
    path('new/', views.PersonCreateView.as_view(), name='person_create'),
    path('<int:pk>/', views.PersonDetailView.as_view(), name='person_detail'),
    path('<int:pk>/edit/', views.PersonUpdateView.as_view(), name='person_update'),
    path('<int:pk>/delete/', views.PersonDeleteView.as_view(), name='person_delete'),
    path(
        'vendors/<int:vendor_pk>/link/',
        views.VendorPersonRelationshipCreateView.as_view(),
        name='relationship_create',
    ),
    path(
        'relationships/<int:pk>/edit/',
        views.VendorPersonRelationshipUpdateView.as_view(),
        name='relationship_update',
    ),
    path(
        'relationships/<int:pk>/delete/',
        views.VendorPersonRelationshipDeleteView.as_view(),
        name='relationship_delete',
    ),
]
