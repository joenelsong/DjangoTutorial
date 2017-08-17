from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'


    def get_queryset(self):
        """Return the last 5 published questions if user is not an administrator."""

        if not self.request.user.is_staff:
            questions_queryset = Question.objects.\
                                        filter(pub_date__lte=timezone.now())
                                        #order_by('-pub_date')[:5] # remove this because it causes array splicin gof the query set, which means we can no longer filter it

            #Remove questions without choices
            temp = questions_queryset
            if temp:
                for question in temp:
                    choices = question.choice_set.all()
                    if not choices:
                        questions_queryset = questions_queryset.exclude(pk=question.pk)
                        return questions_queryset.order_by('-pub_date')[:5]

        # If Admin
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):  #DetailView expects the primary key value captured from the URL to be called "pk"
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        and excludes questions that have no answers
        """
        questions_queryset = Question.objects.\
            filter(pk=self.kwargs.get('pk')).\
            filter(pub_date__lte=timezone.now()) # do not get questions with future publish dates

        # Exclude questions without answers
        if questions_queryset:
            choices = questions_queryset[0].choice_set.all()
            if  choices:
                return questions_queryset
        return Question.objects.none() # return empty queryset


def vote(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=req.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(req, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet
        and excludes questions that have no answers
        """
        questions_queryset = Question.objects.\
            filter(pk=self.kwargs.get('pk')).\
            filter(pub_date__lte=timezone.now()) # do not get questions with future publish dates

        # Exclude questions without answers
        if questions_queryset:
            choices = questions_queryset[0].choice_set.all()
            if  choices:
                return questions_queryset
        return Question.objects.none() # return empty queryset