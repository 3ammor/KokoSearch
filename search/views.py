from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import subprocess
from search.utils import valid_image_mimetype
import json
from Ranker.ranker import Ranker
import time


def index(request):
    return render(request, 'index.html',
                  {
                      'github_repo': ""
                  })


def process_query(request):
    if request.method == 'POST' and request.POST['query']:
        start = time.time()
        print('searching')
        id2word_file = "Ranker/results/results_wordids.txt.bz2"
        corpus = "Ranker/results/results_tfidf.mm"
        model = "Ranker/lda_model/lda.model"
        rank = Ranker(_id2word_path=id2word_file, corpus_path=corpus, model_path=model)
        obj = rank.search(request.POST['query'])
        num_res = len(obj)
        req_time = (start - time.time()) / 1000
        print('search finished')
        return redirect(results, obj=obj, num_res=num_res, req_time=req_time, query=request.POST['query'])
    return redirect(index)


def process_image(request):
    if request.method == 'POST' and request.FILES['image']:
        img = request.FILES['image']

        if not valid_image_mimetype(img):
            return redirect(index)

        fs = FileSystemStorage()
        filename = fs.save(img.name, img)

        uploaded_file_url = fs.url(filename)

        # cmd = ['gedit']
        # subprocess.Popen(cmd).wait()

        fs.delete(filename)

        with open('ImageToTopic/vis/vis.json') as data_file:
            data = json.load(data_file)

        return HttpResponse("Search by image\n" + str(uploaded_file_url) + "\n" + str(data[0]['caption']))

    return redirect(index)


def results(request, obj, num_res, req_time, query):
    return render(request, 'search_results.html',
                  {
                      'num_res': num_res,
                      'req_time': req_time,
                      'query': query,
                      'links': obj
                  })
