from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from rest_framework import generics


from django.contrib.auth.models import User
from .serializers import QuestionSerializer, ChoiceSerializer, UserSerializer


from .models import Choice, Question

@login_required
def index(request):
    template_name = 'base.html'
    return render(request, template_name, {})



class QuestionList(generics.ListCreateAPIView):
    """
    Get / Create questions
    """
    queryset = Question.objects.all()
    
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveDestroyAPIView):

    """
    Get / Delete questions
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer




def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choices.get(pk=request.POST['choice'])
        print selected_choice
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))




class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'
