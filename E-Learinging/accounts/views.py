from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, CustomUserCreationForm
from django.contrib import messages
from courses.models import Course, Enrollment
from progress.models import Progress
from results.models import Result
from django.contrib.auth import get_user_model
from college.models import College, Branch, Year

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.role == 'superadmin' or user.is_superuser:
        context['total_colleges'] = College.objects.count()
        context['colleges'] = College.objects.all()
        context['total_students'] = User.objects.filter(role='student').count()
        context['total_faculty'] = User.objects.filter(role='faculty').count()
        context['total_courses'] = Course.objects.count()
        return render(request, 'dashboard/superadmin.html', context)
    
    elif user.role == 'admin':
        if not user.college:
            messages.warning(request, "Your account is not linked to a college.")
            return render(request, 'dashboard/admin.html', context)
        
        context['college'] = user.college
        context['total_students'] = User.objects.filter(role='student', college=user.college).count()
        context['total_faculty'] = User.objects.filter(role='faculty', college=user.college).count()
        context['branches'] = Branch.objects.filter(college=user.college)
        context['courses'] = Course.objects.filter(branch__college=user.college)
        context['total_enrollments'] = Enrollment.objects.filter(course__branch__college=user.college).count()
        context['faculty_members'] = User.objects.filter(role='faculty', college=user.college)
        return render(request, 'dashboard/admin.html', context)
    
    elif user.role == 'faculty':
        courses = Course.objects.filter(faculty=user)
        context['courses'] = courses
        from videos.models import Video
        from materials.models import Material
        context['total_videos'] = Video.objects.filter(course__in=courses).count()
        context['total_materials'] = Material.objects.filter(course__in=courses).count()
        context['total_students'] = Enrollment.objects.filter(course__in=courses).count()
        return render(request, 'dashboard/faculty.html', context)
    
    elif user.role == 'student':
        enrollments = Enrollment.objects.filter(student=user)
        results = Result.objects.filter(student=user)
        from quiz.models import Quiz
        quizzes = Quiz.objects.filter(course__enrollment__student=user).distinct()
        
        context['enrollments'] = enrollments
        context['results'] = results
        context['quizzes'] = quizzes
        
        if user.college:
            context['available_courses'] = Course.objects.filter(branch__college=user.college)
        else:
            context['available_courses'] = Course.objects.all()
            
        return render(request, 'dashboard/student.html', context)
    
    return render(request, 'dashboard/student.html', context)

@login_required
def create_college(request):
    if not (request.user.role == 'superadmin' or request.user.is_superuser):
        messages.error(request, "Permission Denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        if name:
            College.objects.create(name=name, location=location)
            messages.success(request, f"College {name} created successfully!")
            return redirect('dashboard')
            
    return render(request, 'dashboard/create_college.html')

@login_required
def create_admin(request):
    if not (request.user.role == 'superadmin' or request.user.is_superuser):
        messages.error(request, "Permission Denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'admin'
            user.save()
            messages.success(request, f"College Admin {user.username} created successfully!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm(initial={'role': 'admin'})
        
    return render(request, 'dashboard/create_admin.html', {'form': form})

@login_required
def create_faculty(request):
    if request.user.role != 'admin':
        messages.error(request, "Permission Denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'faculty'
            user.college = request.user.college
            user.save()
            messages.success(request, f"Faculty {user.username} created successfully!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm(initial={'role': 'faculty', 'college': request.user.college})
        
    return render(request, 'dashboard/create_admin.html', {'form': form, 'title': 'Register Faculty'})

@login_required
def create_branch(request):
    if request.user.role != 'admin':
        messages.error(request, "Permission Denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Branch.objects.create(name=name, college=request.user.college)
            messages.success(request, f"Branch {name} created successfully!")
            return redirect('dashboard')
            
    return render(request, 'dashboard/create_college.html', {'title': 'Create Branch', 'label': 'Branch Name'})

@login_required
def provision_student(request):
    if request.user.role != 'admin':
        messages.error(request, "Permission Denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.college = request.user.college
            user.save()
            messages.success(request, f"Student {user.username} provisioned successfully!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm(initial={'role': 'student', 'college': request.user.college})
        
    return render(request, 'dashboard/create_admin.html', {'form': form, 'title': 'Provision Student Account'})

@login_required
def admin_students(request):
    user = request.user
    if user.role != 'admin':
        messages.error(request, "Access denied. Admin portal only.")
        return redirect('dashboard')
        
    students = User.objects.filter(role='student', college=user.college)
    return render(request, 'dashboard/admin_students.html', {
        'students': students,
        'college': user.college
    })

@login_required
def admin_courses(request):
    user = request.user
    if user.role != 'admin':
        messages.error(request, "Access denied. Admin portal only.")
        return redirect('dashboard')
        
    courses = Course.objects.filter(branch__college=user.college)
    return render(request, 'dashboard/admin_courses.html', {
        'courses': courses,
        'college': user.college
    })

@login_required
def student_results(request):
    if request.user.role != 'student':
        messages.error(request, "Access restricted.")
        return redirect('dashboard')
    results = Result.objects.filter(student=request.user)
    return render(request, 'results/result_list.html', {'results': results})
