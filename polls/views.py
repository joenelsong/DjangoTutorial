from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.urls import reverse

from .models import Choice, Question

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    context = {        'latest_question_list': latest_question_list    }
    return render(request, 'polls/index.html', context)
    #return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question' : question})

def vote(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=req.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(req, 'polls/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(req, 'polls/results.html', {'question' : question})

