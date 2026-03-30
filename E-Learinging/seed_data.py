import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from college.models import College, Branch, Year
from courses.models import Course, Enrollment
from videos.models import Video
from materials.models import Material
from quiz.models import Quiz, Question

User = get_user_model()

def seed():
    # 1. Create Colleges
    vignan, _ = College.objects.get_or_create(name="Vignan Institute", location="Hyderabad, India")
    tcs, _ = College.objects.get_or_create(name="TCS Academic Hub", location="Pune, India")

    # 2. Year & Branch
    year1, _ = Year.objects.get_or_create(year="1st Year")
    year2, _ = Year.objects.get_or_create(year="2nd Year")
    cs, _ = Branch.objects.get_or_create(name="Computer Science", college=vignan)
    it, _ = Branch.objects.get_or_create(name="Information Technology", college=tcs)

    # 3. Create Users
    # College Admin
    vignan_admin, created = User.objects.get_or_create(username="vignanadmin", defaults={'role': 'admin', 'college': vignan})
    if created: vignan_admin.set_password('vignan@123'); vignan_admin.save()

    # Faculty
    python_faculty, created = User.objects.get_or_create(username="pythonexpert", defaults={'role': 'faculty', 'college': vignan})
    if created: python_faculty.set_password('python@123'); python_faculty.save()

    java_faculty, created = User.objects.get_or_create(username="java_master", defaults={'role': 'faculty', 'college': tcs})
    if created: java_faculty.set_password('java@123'); java_faculty.save()

    # Student
    student1, created = User.objects.get_or_create(username="student1", defaults={'role': 'student', 'college': vignan})
    if created: student1.set_password('student@123'); student1.save()

    # 4. Create Courses
    python_course, _ = Course.objects.get_or_create(
        name="Python Programming Mastery",
        defaults={
            'description': "Complete Python for all levels chapter wise.",
            'branch': cs,
            'year': year1,
            'faculty': python_faculty
        }
    )

    java_course, _ = Course.objects.get_or_create(
        name="Java Full Stack Development",
        defaults={
            'description': "Build enterprise scale Java applications with Spring Boot.",
            'branch': it,
            'year': year2,
            'faculty': java_faculty
        }
    )

    # 5. Add Content (Chapter-wise)
    # Python Videos
    Video.objects.get_or_create(course=python_course, title="Chapter 1: Intro to Python", defaults={'video_file': "python_intro.mp4"})
    Video.objects.get_or_create(course=python_course, title="Chapter 2: Variables & Types", defaults={'video_file': "python_vars.mp4"})
    
    # Material
    Material.objects.get_or_create(course=python_course, title="Python Cheat Sheet PDF", defaults={'file': "python_notes.pdf"})

    # Java Videos
    Video.objects.get_or_create(course=java_course, title="Chapter 1: Core Java Intro", defaults={'video_file': "java_core.mp4"})
    
    # 6. Add 5 Quizzes (MCQ) for Python
    q1, _ = Quiz.objects.get_or_create(course=python_course, title="Python Basics Quiz")
    Question.objects.get_or_create(quiz=q1, question="Is Python case-sensitive?", option1="Yes", option2="No", option3="Maybe", option4="None", answer="Yes")
    Question.objects.get_or_create(quiz=q1, question="Which file extension is correct for Python?", option1=".py", option2=".pt", option3=".pyt", option4=".python", answer=".py")

    q2, _ = Quiz.objects.get_or_create(course=python_course, title="Data Types Mastery")
    Question.objects.get_or_create(quiz=q2, question="What is the type of [1, 2, 3]?", option1="tuple", option2="list", option3="set", option4="dict", answer="list")
    Question.objects.get_or_create(quiz=q2, question="Which one is immutable?", option1="list", option2="tuple", option3="dict", option4="set", answer="tuple")

    q3, _ = Quiz.objects.get_or_create(course=python_course, title="Control Flow Challenge")
    Question.objects.get_or_create(quiz=q3, question="Which keyword is used for 'otherwise' in if statements?", option1="else", option2="elif", option3="then", option4="otherwise", answer="else")
    Question.objects.get_or_create(quiz=q3, question="Which keyword is used to skip an iteration?", option1="break", option2="continue", option3="pass", option4="exit", answer="continue")

    q4, _ = Quiz.objects.get_or_create(course=python_course, title="Functions Deep Dive")
    Question.objects.get_or_create(quiz=q4, question="How do you return a value from a function?", option1="back", option2="send", option3="return", option4="yield", answer="return")
    Question.objects.get_or_create(quiz=q4, question="What keyword defines a function?", option1="func", option2="def", option3="function", option4="define", answer="def")

    q5, _ = Quiz.objects.get_or_create(course=python_course, title="Loops & Iteration")
    Question.objects.get_or_create(quiz=q5, question="Which loop iterates over a sequence?", option1="while", option2="for", option3="switch", option4="do", answer="for")
    Question.objects.get_or_create(quiz=q5, question="Which loop runs while a condition is true?", option1="for", option2="while", option3="repeat", option4="loop", answer="while")

    # 6. Add 5 Quizzes for Java
    jq1, _ = Quiz.objects.get_or_create(course=java_course, title="Java Fundamentals")
    Question.objects.get_or_create(quiz=jq1, question="Which data type is used to store fractional numbers?", option1="int", option2="long", option3="double", option4="float", answer="double")
    Question.objects.get_or_create(quiz=jq1, question="Which of these is used to exit a loop?", option1="exit", option2="break", option3="continue", option4="stop", answer="break")

    jq2, _ = Quiz.objects.get_or_create(course=java_course, title="OOP Principles")
    Question.objects.get_or_create(quiz=jq2, question="Which of these is not an OOP concept?", option1="Abstraction", option2="Compilation", option3="Inheritance", option4="Polymorphism", answer="Compilation")

    jq3, _ = Quiz.objects.get_or_create(course=java_course, title="Collections Framework")
    Question.objects.get_or_create(quiz=jq3, question="Which set allows null values?", option1="HashSet", option2="TreeSet", option3="LinkedHashSet", option4="Both A & C", answer="HashSet")

    jq4, _ = Quiz.objects.get_or_create(course=java_course, title="Multithreading Mastery")
    Question.objects.get_or_create(quiz=jq4, question="What method starts a thread?", option1="run()", option2="init()", option3="start()", option4="begin()", answer="start()")

    jq5, _ = Quiz.objects.get_or_create(course=java_course, title="Spring & Hibernate")
    Question.objects.get_or_create(quiz=jq5, question="Which annotation is used for mapping in Spring Boot?", option1="@GetMapping", option2="@Mapping", option3="@Route", option4="@Path", answer="@GetMapping")

    print("✅ Seed Data successfully expanded with final Java curriculum!")

    # 7. Add Java Materials
    Material.objects.get_or_create(course=java_course, title="Java Fundamentals Reference PDF", defaults={'file': "java_basics.pdf"})
    Material.objects.get_or_create(course=java_course, title="Spring Boot Microservices Architecture", defaults={'file': "spring_micro.pdf"})

    # 8. Enroll student in Java as well
    Enrollment.objects.get_or_create(student=student1, course=java_course)

if __name__ == "__main__":
    seed()
