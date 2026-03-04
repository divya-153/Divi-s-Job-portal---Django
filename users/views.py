from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import SeekerProfile,EmployerProfile,Interview,Comments,Like



# Create your views here.

User=get_user_model()

def index(request):
    return render(request,"index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        profile=request.POST.get("profile")

        username_exits=User.objects.filter(username=username).exists()
        email_exists  =User.objects.filter(email=email).exists()    # model=view
        
        if (username_exits):
                return render(request,"signup.html",{"username_error":"Username Already taken try different"})
        if (email_exists):
                return render(request,"signup.html",{"email_error":"Email Already registerd"})
        
        else:
                User.objects.create_user(username=username,email=email,password=password,profile=profile)
                messages.success(request,"Acccount Created Successfully")
                return redirect("login")
        
    else:
        return render(request,"signup.html")
   
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  #return the object of authenticated user

        if user is not None:
            login(request, user)

            p = user.profile.lower() 

            if not user.is_profile_completed:
                return redirect(f"{p}_profile")
            else:
                return redirect(f"{p}_dashboard")

        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")
         

@login_required                                      #decorators used for redicrect to loign page but mention url in setting.py
def seeker_profile(request):
    if request.method == "POST":

        # Get form data
        mobile = request.POST.get("mobile")
        country_code = request.POST.get("country_code")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        locality = request.POST.get("locality")
        preferred_job = request.POST.get("preferred_job")
        experience = request.POST.get("experience")
        qualification = request.POST.get("qualification")
        degree = request.POST.get("degree")
        college = request.POST.get("college")
        year_of_passing = request.POST.get("year_of_passing")
        relocate = request.POST.get("relocate") == "True"

        resume = request.FILES.get("resume")
        photo = request.FILES.get("photo")

        try:
            profileData = request.user.seeker_profile
        except SeekerProfile.DoesNotExist:
            profileData = SeekerProfile(user=request.user)

        # Assign values
        profileData.mobile = mobile
        profileData.country_code = country_code
        profileData.country = country
        profileData.state = state
        profileData.city = city
        profileData.locality = locality
        profileData.preferred_job = preferred_job
        profileData.experience = experience
        profileData.qualification = qualification
        profileData.degree = degree
        profileData.college = college
        profileData.year_of_passing = year_of_passing

        if resume:
            profileData.resume = resume
        if photo:
            profileData.photo = photo

        profileData.relocate = relocate
        profileData.save()

        # Mark user profile completed
        request.user.is_profile_completed = True
        request.user.save()

        return redirect("seeker_dashboard")

    return render(request, "seeker_profile.html")

@login_required
def seeker_dashboard(request):

    profile = request.user.seeker_profile

    # Start with all interviews
    interviews = Interview.objects.all().order_by("-start_date")

    employer = EmployerProfile.objects.all()

    # ===== GET FILTER VALUES =====
    job_title = request.GET.get("job_title")
    city = request.GET.get("city")
    experience = request.GET.get("experience")
    job_type = request.GET.get("job_type")

    # ===== APPLY FILTERS =====
    if job_title:
        interviews = interviews.filter(job_title__icontains=job_title)

    if city:
        interviews = interviews.filter(venue__icontains=city)

    if experience:
        interviews = interviews.filter(experience__icontains=experience)

    if job_type:
        interviews = interviews.filter(job_type__icontains=job_type)

    # Count AFTER filtering
    interview_count = interviews.count()

    return render(request, "seeker_dashboard.html", {
        "profile": profile,
        "interviews": interviews,
        "employer": employer,
        "interview_count": interview_count
    })

 
@login_required
def edit_seeker_profile(request):
    try:
        profile = request.user.seeker_profile
    except SeekerProfile.DoesNotExist:
        profile = SeekerProfile.objects.create(user=request.user)
        
    if request.method == "POST":

        # Get form data
        mobile = request.POST.get("mobile")
        country_code = request.POST.get("country_code")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        locality = request.POST.get("locality")
        preferred_job = request.POST.get("preferred_job")
        experience = request.POST.get("experience")
        qualification = request.POST.get("qualification")
        degree = request.POST.get("degree")
        college = request.POST.get("college")
        year_of_passing = request.POST.get("year_of_passing")
        relocate = request.POST.get("relocate") == "True"

        resume = request.FILES.get("resume")
        photo = request.FILES.get("photo")
        
         # Assign values
        profile.mobile = mobile
        profile.country_code = country_code
        profile.country = country
        profile.state = state
        profile.city = city
        profile.locality = locality
        profile.preferred_job = preferred_job
        profile.experience = experience
        profile.qualification = qualification
        profile.degree = degree
        profile.college = college
        profile.year_of_passing = year_of_passing

        if resume:
            profile.resume = resume
        if photo:
            profile.photo = photo

        profile.relocate = relocate
        profile.save()


        return redirect("seeker_dashboard")
        
    return render(request,"edit_seeker_profile.html" , {"profile":profile})




@login_required
def employer_profile(request):
    
    if request.user.profile != "employer":
        return redirect("index")
    if request.method == "POST":

        # Get form data
        request.user.username = request.POST.get("name")
        mobile = request.POST.get("mobile")
        country_code = request.POST.get("country_code")
        role=request.POST.get("role")
        photo = request.FILES.get("photo")
                
        company_name = request.POST.get("company_name") 
        company_logo=request.FILES.get("company_logo")
        company_type = request.POST.get("company_type")   
        company_size = request.POST.get("company_size")   
                     
        office_city = request.POST.get("office_city")
        office_address = request.POST.get("office_address")   
        
        
        try:
            profileData = request.user.employer_profile
        except EmployerProfile.DoesNotExist:
            profileData = EmployerProfile(user=request.user)

        # Assign values
        profileData.mobile = mobile
        profileData.country_code = country_code
        profileData.role=role
        
        profileData.company_name=company_name
        profileData.company_type=company_type
        profileData.company_size=company_size
        
        profileData.office_city = office_city
        profileData.office_address=office_address
        
      
     
        if photo:
            profileData.photo = photo
        if company_logo:
            profileData.company_logo=company_logo

       
        profileData.save()

        # Mark user profile completed
        request.user.is_profile_completed = True
        request.user.save()

        return redirect("employer_dashboard")
    return render(request, "employer_profile.html")


@login_required
def interview_details(request,id):
    profile=request.user.seeker_profile
    interview=Interview.objects.get(id=id)
    employer=EmployerProfile.objects.all()
    
    comments=Comments.objects.all()
    comments = Comments.objects.filter(interview=interview)
    comment_count = comments.count()
    
    
    is_liked = Like.objects.filter(
        seeker=profile,
        interview=interview
    ).exists()

    
    return render(request,"interview_details.html",{"profile":profile, "interview":interview, "employer":employer, "comments":comments, "comment_count":comment_count,  "is_liked": is_liked})

@login_required
def add_comments(request,id):
    
    if request.method=="POST":
        seeker_profile=SeekerProfile.objects.get(user=request.user)
        interview=Interview.objects.get(id=id)
        comment=request.POST.get("writeComment")
        
        if comment:
            Comments.objects.create(
                seeker=seeker_profile,
                comment=comment,
                interview=interview,
                )
    return redirect("interview_details",id=id)

from django.shortcuts import get_object_or_404
@login_required
def delete_comment(request, id):

    if request.method == "POST":

        comment = get_object_or_404(Comments, id=id)

        if request.user == comment.seeker.user:
            comment.delete()
            return JsonResponse({"success": True})

        else:
            return JsonResponse({"success": False, "error": "Not allowed"})

    return JsonResponse({"success": False, "error": "Invalid request"})


def edit_comment(request, id):
    comment = Comments.objects.get(id=id)

    if request.method == "POST":
        comment.comment = request.POST.get("comment")
        comment.save()
        return redirect("interview_detail", id=comment.interview.id)

    return render(request, "edit_comment.html", {"comment": comment})    



def update_comment(request, id):
    if request.method == "POST":
        comment = Comments.objects.get(id=id)

        if request.user == comment.seeker.user:
            comment.comment = request.POST.get("comment")
            comment.save()

            return JsonResponse({
                "updated_comment": comment.comment
            })

    return JsonResponse({"error": "Not allowed"})


@login_required
def toggle_like(request, id):

    interview = Interview.objects.get(id=id)
    seeker = SeekerProfile.objects.get(user=request.user)

    like = Like.objects.filter(seeker=seeker, interview=interview)

    if like.exists():
        like.delete()
        liked = False
    else:
        Like.objects.create(seeker=seeker, interview=interview)
        liked = True

    return JsonResponse({
        "liked": liked,
        "like_count": interview.like_set.count()
    })
    
@login_required
def employer_dashboard(request):
    profile=request.user.employer_profile
    return render(request,"employer_dashboard.html", {"profile":profile})
 
@login_required
def post_interviews(request):
    profile=request.user.employer_profile
    
    if request.method == "POST":
        employer_profile = EmployerProfile.objects.get(user=request.user)
        end_date = request.POST.get("end_date")
        
        if end_date == "":
             end_date = None
             
        Interview.objects.create(
            employer = employer_profile,
            job_title = request.POST.get("job_title"),
            experience = request.POST.get("experience"),
            job_type = request.POST.get("job_type"),
            qualification = request.POST.get("qualification"),
            job_mode = request.POST.get("job_mode"),
            why_join_us = request.POST.get("why_join_us"),
            application_link = request.POST.get("application_link"),
            start_date = request.POST.get("start_date"),
            end_date=end_date,
            time = request.POST.get("time"),
            venue = request.POST.get("venue"),
            contact_phone = request.POST.get("contact_phone"),
            contact_email = request.POST.get("contact_email"),
            poster = request.FILES.get("poster")   # 🔥 VERY IMPORTANT
        )

        return redirect("employer_dashboard")
    
    return render(request,"post_interviews.html", {"profile":profile})
 
@login_required
def my_interviews(request):

    employer_profile = EmployerProfile.objects.get(user=request.user)

    interviews = Interview.objects.filter(employer=employer_profile)

    return render(request, "my_interviews.html", { "interviews": interviews   })
 
@login_required
def edit_interview(request,id):
    
    employer_profile = EmployerProfile.objects.get(user=request.user)
    data = Interview.objects.get(id=id, employer=employer_profile)
    
    if not data:
     return redirect("my_interviews")
             
    if request.method=="POST":
        end_date = request.POST.get("end_date")
    
        if end_date == "":
             end_date = None
             
        job_title = request.POST.get("job_title")
        experience = request.POST.get("experience")
        job_type = request.POST.get("job_type")
        qualification = request.POST.get("qualification")
        job_mode = request.POST.get("job_mode")
        why_join_us = request.POST.get("why_join_us")
        application_link = request.POST.get("application_link")
        start_date = request.POST.get("start_date")
        end_date=end_date
        time = request.POST.get("time")
        venue = request.POST.get("venue")
        contact_phone = request.POST.get("contact_phone")
        contact_email = request.POST.get("contact_email")
        poster = request.FILES.get("poster")
    
    
        data.job_title = job_title
        data.experience = experience
        data.job_type = job_type
        data.qualification = qualification
        data.job_mode = job_mode 
        data.why_join_us = why_join_us
        data.application_link = application_link
        data.start_date = start_date
        data.end_date=end_date
        data.time = time
        data.venue = venue
        data.contact_phone =contact_phone
        data.contact_email = contact_email
        
        if poster:
            data.poster = poster
        
        data.save()
        
        return redirect("my_interviews")
    return render(request, "edit_interview.html", {"data":data})
    
@login_required
def delete_interview(request,id):
    if request.method=="POST":
        employer_profile=EmployerProfile.objects.get(user=request.user)
        try:
            data=Interview.objects.get(id=id,employer=employer_profile)
            data.delete()
        except Interview.DoesNotExist:
            pass
    return redirect("my_interviews")

@login_required
def view_applicants(request):
     return render(request,"employer_dashboard.html")

