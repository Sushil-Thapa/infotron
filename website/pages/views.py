from django.shortcuts import render
from django.contrib import messages
import os

from mind.mapper import Mapper


def home(request):
    '''
    This is the homepage of the website.
    '''

    output = "no output"

    if request.method == 'POST':
        command = request.POST.get('command')
        selectedFile = request.POST.get('selectedFile')

        if command is not '' and selectedFile is not '':
            mapper = Mapper()
            output = mapper.mapRE("Cluster", "mind/datasets/" + selectedFile, command)

            messages.success(request, "Please wait! \"%s\" is being executed on %s." % (command, selectedFile))
        else:
            messages.error(request, "Please select a file and type in a valid command.")

    datasets = []
    for file_name in os.listdir("mind/datasets/"):
        if file_name.endswith(".csv"):
            datasets.append(file_name)

    args = {
        'title': "InfoTron : HOME",
        'command': request.POST.get('command'),
        'selectedFile': request.POST.get('selectedFile'),
        'output': output,
        'datasets': datasets,
    }

    return render(request, 'pages/index.html', args)
