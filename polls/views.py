from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Question


# Create your views here.
# This index view is without the reder() shortcut
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template= loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list' : latest_question_list
#     }
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(template.render(context, request))

# This index view made using render function
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list' : latest_question_list}
    return render(request,'polls/index.html', context)


# This view is made using try... except ....
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404 ("Question does not exist")
#     return render(request, 'polls/detail.html', {'question' : question})

# This view is made by using get_object_or_404 shortcut

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question' : question})


def results(request, question_id):
    response = "You are looking at the results of the question"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You are voting on question %s" % question_id)
