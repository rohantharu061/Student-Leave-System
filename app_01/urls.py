from django.urls import path
from .views import *

urlpatterns=[
    path('dashboard/', dashboard, name='dashboard'),
    path('form/', form, name='form'),
    path('contact/', contact, name='contact'),
  
    
    path('edit/<int:id>', edit, name='edit'),
    path('delete_data/<int:id>', delete_data, name='delete_data'),
    path('delete_all/', delete_all, name='delete_all'),
    
    path('recycle/', recycle, name='recycle'),
    path('restore/<int:id>', restore, name='restore'),
    path('restore_all/', restore_all, name='restore_all'),
]