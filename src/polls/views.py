from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Choice
from .models import Question

# def index(request):
#     latest_question_list = Question.objects.all()

#     return render(request, "polls/index.html", { 'latest_question_list': latest_question_list })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
    

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)

#     return render(request, "polls/detail.html", { 'question': question })
class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)

#     return render(request, "polls/results.html", { 'question': question })
class ResultDetailView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": 'No elegiste una respuesta válida'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

