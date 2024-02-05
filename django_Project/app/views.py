from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from .models import Question, Choice
from django.views import generic
from django.shortcuts import render , get_object_or_404
from django.urls import reverse
from django.utils import timezone


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("app/index.html")
#     context = {
#         "latest_question_list":latest_question_list
#     }
    
#     return render(request,"app/index.html",context)

# def detail(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request,"app/detail.html",{"question":question})

# def results(request, question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,"app/results.html",{"question": question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice= question.choice_set.get(pk=request.POST["choice"])
#     except (KeyError, Choice.DoesNotExist):
#         return render(
#             request,"app/detail.html",{
#                 "question":question,
#                 "error_message":"You didn't select a choice."
#             }
#         )
        
#     else:
#         selected_choice.votes+=1
        
        
#         selected_choice.save()
#     return HttpResponseRedirect(reverse("app:results",args=(question_id,)))

class IndexView(generic.ListView):
    template_name = "app/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "app/detail.html"
    
    def get_queryset(self) :
        """exclude question that aren't published"""
        Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "app/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice= question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,"app/detail.html",{
                "question":question,
                "error_message":"You didn't select a choice."
            }
        )
        
    else:
        selected_choice.votes+=1
        
        
        selected_choice.save()
    return HttpResponseRedirect(reverse("app:results",args=(question_id,)))
    
    
def get_queryset(self):
    
    return Question.objects.filter(pub_date__lte = timezone.now()).order_by("pub_date")[:5]
