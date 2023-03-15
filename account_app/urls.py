from django.urls import path, include
from account_app import views

app_name = "account_app"

urlpatterns =[ path("", include("django.contrib.auth.urls")),
    path("profile/create/", views.ProfileCreateView.as_view(), name="profile_create"),
    path(
        "profile/<int:pk>/detail/",
        views.ProfileDetailView.as_view(),
        name="profile_detail",
    ),
    path("profile/signup/", views.SignupView.as_view(), name="signup"),
    path("profile/login/", views.CustomLoginView.as_view(), name="login"),
    path("profile/logout/", views.LogoutView.as_view(), name="logout"),
     path("profile/login/data", views.Dataview.as_view(), name="data"),
    
]
