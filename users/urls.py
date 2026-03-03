from django.urls import path
from . import views

urlpatterns=[
    path("",views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    
    path("seeker_profile/", views.seeker_profile, name="seeker_profile"),
    path("employer_profile/", views.employer_profile, name="employer_profile"),
    
    path("seeker_dashboard/", views.seeker_dashboard, name="seeker_dashboard"),
    path("edit_seeker_profile", views.edit_seeker_profile, name="edit_seeker_profile"),
    path("interview_details/<int:id>/", views.interview_details, name="interview_details"),
    path("add_comments/<int:id>/", views.add_comments, name="add_comments"),
    path("delete_comment/<int:id>/", views.delete_comment, name="delete_comment"),
    path("edit_comment/<int:id>/", views.edit_comment, name="edit_comment"),
    path("update_comment/<int:id>/", views.update_comment, name="update_comment"),
    path("toggle_like/<int:id>/", views.toggle_like, name="toggle_like"),
        
    path("employer_dashboard/", views.employer_dashboard,name="employer_dashboard"),
    path("post_interviews/", views.post_interviews, name="post_interviews"),
    path("my_interviews/", views.my_interviews , name="my_interviews"),
    path("edit_interview/<int:id>/", views.edit_interview , name="edit_interview"),
    path("delete_interview/<int:id>/", views.delete_interview , name="delete_interview"),    
    path("view_applicants/", views.view_applicants, name="view_applicants"),
]