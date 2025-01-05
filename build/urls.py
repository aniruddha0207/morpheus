from django.contrib import admin
from django.urls import path
from builder import views  # Adjust 'builder' to the name of your app

urlpatterns = [
    path('', views.home, name='home'),  # Root URL
    path('form/<int:form_id>/', views.form_view, name='form_view'),
    path('analytics/<int:form_id>/', views.analytics_view, name='analytics_view'),
    path('admin/', admin.site.urls),
]
