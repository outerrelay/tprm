from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('', views.VendorListView.as_view(), name='vendor_list'),
    path('new/', views.VendorCreateView.as_view(), name='vendor_create'),
    path('<int:pk>/', views.VendorDetailView.as_view(), name='vendor_detail'),
    path('<int:pk>/edit/', views.VendorUpdateView.as_view(), name='vendor_update'),
    path('<int:vendor_pk>/assessments/new/', views.AssessmentCreateView.as_view(), name='assessment_create'),
    path('assessments/<int:pk>/', views.AssessmentDetailView.as_view(), name='assessment_detail'),
    path('assessments/<int:pk>/edit/', views.AssessmentUpdateView.as_view(), name='assessment_update'),
]
