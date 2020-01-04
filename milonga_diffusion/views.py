from django.shortcuts import render
from .forms import AddForm
from django.http import HttpResponse
import json
from .gen_mesh import generate_mesh, generate_mil, generate_plot
import datetime, os
# def web_adder(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = AddForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             X = int(form.cleaned_data['xsize'])
#             Y = int(form.cleaned_data['ysize'])
#             return render(request, 'diffusion/grid.html', {'X': range(X), 'Y': range(Y)})

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = AddForm()

#     return render(request, 'diffusion/grid.html', {'form': form, })

# def button(request):
#     return render(request, 'diffusion/button.html')

def build_a_reactor(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            X = int(form.cleaned_data['x_size'])
            Y = int(form.cleaned_data['y_size'])
            return render(request, 'build_a_reactor/grid.html', {'form': form, 'X': range(X), 'Y': range(Y), 'maxX': X, 'maxY': Y})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddForm()
        return render(request, 'build_a_reactor/grid.html', {'form': form, 'X': range(10),  'Y': range(10), 'maxX': 10, 'maxY': 10})
        

def grab_geo(request):
    ts = str(datetime.datetime.now().timestamp()).replace(".","_")
    # response_data = {}
    test = request.POST.get("data", "")
    # print(type(test))
    generate_mesh(test, ts)
    generate_mil(ts)
    generate_plot(ts)
    # os.remove('static/'+ts+'_fast.png')
    return render(request, 'build_a_reactor/image.html', {'fast_plot_path': "plots/"+ts+"_fast.png", 
                                                            'thermal_plot_path': "plots/"+ts+"_thermal.png"})

