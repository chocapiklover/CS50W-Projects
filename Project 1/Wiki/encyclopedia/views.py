from django.shortcuts import render, redirect, Http404

from . import util
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)

    if entry_content is None:
        raise Http404("Sorry not found")
    else:
        html_content = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    query = request.GET.get('q', '').strip()
    entries = util.list_entries()
    

    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

    if query in entries:
        return redirect('entry', title=query)
    

  
    elif  matching_entries:
        return render(request, 'encyclopedia/search.html', {
            'entries': matching_entries, 
            'content': query, 
        })

    else:
        return render(request, 'encyclopedia/index.html', {
            'query': query,
            # 'error_message': "couldn't find entry"
        })

def random_entry(request):
    allentry = util.list_entries()
    randomentry = random.choice(allentry)
    getentry = util.get_entry(randomentry)
    converted_content = markdown2.markdown(getentry)

    return render(request, 'encyclopedia/entry.html', {
        'title': randomentry,
        'content': converted_content, })

def newentry(request):
    if request.method == "GET":
        return render(request, 'encyclopedia/newentry.html')
    elif request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        entry_content = util.get_entry(title)

        # if entry_content is not None:
        if entry_content is not None:
            return render(request, 'encyclopedia/error.html', {
                'error_message': 'cant do this already exist '
            })
        else:
            util.save_entry(title, content)
            html_content = markdown2.markdown(content)
            return render(request, 'encyclopedia/entry.html', {
                'title': title, 
                'content': html_content
            })

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, 'encyclopedia/editpage.html', {
            'title': title,
            'content': content,
        })
    elif request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/index.html")


    


