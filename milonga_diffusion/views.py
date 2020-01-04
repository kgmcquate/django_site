from django.shortcuts import render
from .forms import AddForm
from django.http import HttpResponse
import json
from .gen_mesh import generate_mesh, generate_mil, generate_plot
import datetime, os

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
            if X > 25:
                X = 25
            elif X < 5:
                X = 5
            
            if Y > 25:
                Y = 25
            elif Y < 5:
                Y = 5
            
            return render(request, 'build_a_reactor/grid.html', {'form': form, 'X': range(X), 'Y': range(Y), 'maxX': X, 'maxY': Y})
        # else:
        #     # warning = 'Dimensions must be between 5 and 25'
        #     return render(request, 'build_a_reactor/grid.html', {'form': form, 'X': range(10), 'Y': range(10), 'maxX': 10, 'maxY': 10})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AddForm()
        return render(request, 'build_a_reactor/grid.html', {'form': form, 'X': range(10),  'Y': range(10), 'maxX': 10, 'maxY': 10})
        

def grab_geo(request):
    ts = 'temp_' + str(datetime.datetime.now().timestamp()).replace(".","_")
    # response_data = {}
    test = request.POST.get("data", "")
    # print(type(test))
    generate_mesh(test, ts)
    keff = generate_mil(ts)

    if keff > 0:
        generate_plot(ts)
    # os.remove('static/'+ts+'_fast.png')

    keff = float(keff)
    if keff == 0:
        msg = 'Can\'t Solve'
    elif keff < 0.99:
        msg = "Reactor is Subcritical: k = "+str(keff)
    elif keff > 1.01:
        msg = "Reactor is Supercritical: k = "+str(keff)
    elif (keff > 1.001) or (keff < 0.999):
        msg = "Reactor is Approximately Critical: k = "+str(keff)
    elif (keff > 1.0002) or (keff < 0.9998):
        msg = "Reactor is Nearly Critical: k = "+str(keff)
    else:
        msg = "Congratulations, Reactor is Critical: k = "+str(keff)
    

    return render(request, 'build_a_reactor/plots.html', {'fast_plot_path': "plots/"+ts+"_fast.png", 
                                                            'thermal_plot_path': "plots/"+ts+"_thermal.png",
                                                            'k_msg': msg})

