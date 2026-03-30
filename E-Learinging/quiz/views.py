from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question
from results.models import Result
from django.contrib import messages

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        score = 0
        total = questions.count()
        
        for q in questions:
            user_answer = request.POST.get(f'question_{q.id}')
            if user_answer == q.answer:
                score += 1
        
        final_score = int((score / total) * 100) if total > 0 else 0
        Result.objects.create(student=request.user, quiz=quiz, score=final_score)
        
        messages.success(request, f"Quiz submitted! Your score: {final_score}%")
        return redirect('dashboard')
    
    return redirect('dashboard')
