from django.urls import path
from .views import RoleListView, RoleDetailView, UserListView, UserDetailView, SignupView, LoginView, AccessModuleView, BulkUserUpdateView

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='role_list'),
    path('role/<int:pk>/', RoleDetailView.as_view(), name='role_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),    
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('access_modules/<int:pk>/', AccessModuleView.as_view(), name='access_modules'),
    path('bulk_user_update/', BulkUserUpdateView.as_view(), name='bulk_user_update'),
    
]
