from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from .models import Information
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'piazzapolls/main_page.html')

def main_page(request):
    try:
        information = Information(first_date='2018-04-15', last_CID=700, course_ID='LOLOLOLOLOL')
        information.save()
    except Information.DoesNotExist:
        raise Http404("Information does not exist")
    return render(request, 'piazzapolls/main_page.html', {'information': information})

def analyze(request, information_id):
    information = get_object_or_404(Information, pk=information_id)
    try:
        first_date = request.POST['answer1']
        last_CID = request.POST['answer2']
        course_ID = request.POST['answer3']
        keywords = request.POST['answer4']
    except:
        return render(request, 'piazzapolls/main_page.html', {
                                    'information': information,
                                    'error_message': "faulty input"
                                    })
    else:
        information.first_date = first_date
        information.last_CID = last_CID
        information.course_ID = course_ID
        information.keywords = keywords
        information.save()
        return HttpResponseRedirect(reverse('piazzapolls:results', args=(information.id,)))

def results(request, information_id):
    information = get_object_or_404(Information, pk=information_id)
    #THE "BACKEND" WORD HAPPENS HERE
    return render(request, 'piazzapolls/results.html', {
                                    'information': information,
                                    })



#Create your views here.
