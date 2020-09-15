from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Comments

def index(request): 
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions. (not including those set to be
        published in the future)."""
        return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]


class CommentsView(generic.ListView):
    template_name='polls/comments.html'
    model=Comments
    def get_queryset(self):
      return Comments.objects.all

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def comments_list(request):
    com_list = Comments.objects.all()
    context = {'com_list': com_list}
    return render(request, 'polls/comments.html', context)

def postcomment(request):  
    if (request.method=="POST"):
        name=request.POST.get('comname')
        body=request.POST.get('combod')
        if (name and body ):
            new_comment=Comments.objects.create(name=name, body=body)
            new_comment.save()
        return HttpResponseRedirect('comments/list')
    else: 
        return render(request, 'polls/postcomment.html')

