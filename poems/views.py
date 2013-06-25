# Create your views here.

from django.http import HttpResponse

from poems.models import Poem, Source


def index(request):
    latest_poems_list = Poem.objects.order_by('-gen_date')[:5]
    best_poems_list = Poem.objects.order_by('-votes')[:5]
    #TODO display source titles
    context = RequestContext(request, {
        'latest_poems_list': latest_poems_list,
        'best_poems_list': best_poems_list,
    })
    return render(request, 'poems/index.html', context)

def detail(request, poem_id):
    poem = get_object_or_404(Poem, pk=poem_id)
    return render(request, 'poems/detail.html', {'poem': poem})

def new(request):
    return render(request, 'poems/new.html')

def snap(request, poem_id): #or roll eyes / sigh loudly
    poem = get_object_or_404(Poem, pk=poem_id)
    vote_polarity = pk=request.POST['polarity']
    if vote_polarity == "snap":
      poem.up_votes += 1
    elif vote_polarity == "sigh":
      poem.down_votes -= 1
    else:
      #TODO: make this not happen
      raise Http404
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('poems:detail', args=(poem.id,)))

def create(request, poll_id):
    poem = get_object_or_404(Poem, pk=poem_id)
    try:
        source_url = request.POST['source_url']
        format_name = request.POST['format_name']
        source_text = "asdfasdf #TODO"
        #eventually test this for stuff
    except (KeyError):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        # UI: 
        #  1. give boxes to choose source, format
        #  2. "approval page" with button to "show it, poet" or not
        #  3. share page
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        linetexts = sent_detector.tokenize(source_text)

        p = Poemifier(format_name.capitalize())
        #this can't be a do... while, because we have to add all the lines, then do various processing steps.
        for linetext in linetexts:
          line = Line(linetext, p.rhyme_checker)
          if line.should_be_skipped():
            continue
          #p.try_line(line) #too slow
          p.add_line(line)
        poem_text = poem.format_poem( p.create_poem(True) )

        #TODO

          # Always return an HttpResponseRedirect after successfully dealing
          # with POST data. This prevents data from being posted twice if a
          # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

