import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.timezone import utc
from stories.models import Story
from django.template import loader, Context
from django.shortcuts import render_to_response
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required

from stories.forms import StoryForm
def top_stories(top=2,consider=10):
  lastest_stories = Story.objects.all().order_by('-created_at')[:consider]
  ranked_stories = sorted([(score(story),story) for story in lastest_stories],reverse=True)
  return [story for _, story in ranked_stories][:top]

def score(story, gravity=1.8, timebase=120):
  points = (story.points + 1)**0.8
  now = datetime.datetime.utcnow().replace(tzinfo=utc)
  age = int((now - story.created_at).total_seconds())/60
  return points/(age+timebase)**1.8


def index(request):
  stories = top_stories(top=5)

  if request.user.is_authenticated():
    liked_stories = request.user.liked_stories.filter(id__in=[story.id for story in stories])
  else:
    liked_stories=[]

  # context = RequestContext(request,{
  #   'stories': stories
  #   })
  # template = loader.get_template('stories/index.html')
  # context  = Context({'stories':stories})
  # response = template.render(context)
  # return HttpResponse(response)
  return render(request, 'stories/index.html',{
    'stories':stories,
    'user':request.user,
    'liked_stories':liked_stories
    })
  #return render_to_response('stories/index.html',{'stories':stories})

@login_required
def story(request):
  if request.method == 'POST':
      form = StoryForm(request.POST)
      if form.is_valid():
        story = form.save(commit=False)
        story.moderator = request.user
        story.save()
        return HttpResponseRedirect('/')
  else:
    form = StoryForm()
  return render(request,'stories/story.html',{'form':form})


@login_required
def vote(request):
  print request.POST
  print request.POST.get('story')

  story = get_object_or_404(Story, pk=request.POST.get('story'))
  story.points +=1
  story.save()

  user = request.user
  user.liked_stories.add(story)
  user.save()

  return HttpResponse()
