from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from videos.models import Video
from materials.models import Material
from quiz.models import Quiz
from progress.models import Progress
from django.contrib import messages

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return render(request, 'courses/detail.html', {'course': course, 'is_enrolled': is_enrolled})

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role != 'student':
        messages.error(request, "Only students can enroll in courses.")
        return redirect('course_detail', pk=pk)
    
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        # Create initial progress
        Progress.objects.get_or_create(student=request.user, course=course, defaults={'completion': 0})
        messages.success(request, f"Successfully enrolled in {course.name}!")
    else:
        messages.info(request, f"You are already enrolled in {course.name}.")
    
    return redirect('dashboard')

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    course = video.course
    # Check if student is enrolled
    if request.user.role == 'student':
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.error(request, "You must enroll in this course to watch videos.")
            return redirect('course_detail', pk=course.pk)
            
    all_videos = course.videos.all()
    all_materials = course.materials.all()
    all_quizzes = course.quizzes.all()
    
    return render(request, 'courses/video.html', {
        'video': video,
        'course': course,
        'all_videos': all_videos,
        'all_materials': all_materials,
        'all_quizzes': all_quizzes
    })
