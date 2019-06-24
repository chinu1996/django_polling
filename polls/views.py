from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from .models import Question,Choice
from django.utils import timezone

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


"""The following is not made using generic views"""
# # This view is made by using get_object_or_404 shortcut which is same as try... except.... but less code :)
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question' : question})
#
#
# def results(request, question_id):
#     response = "You are looking at the results of the question"
#     return HttpResponse(response % question_id)


"""  The following is made using generic views which helps us delete the
     redundant code(see above detail and results view
     To do this first amend the URLconf then amend views"""


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    """
        Return the last five published questions (not including those set to be
        published in the future).
        """
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detaul.html',{
            'question' : question,
            'error_message' : "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.


def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/results.html', {'question': question})



