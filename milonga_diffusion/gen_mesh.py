import sys, os
import gmsh_api
import gmsh_api.gmsh as gmsh
import numpy as np
import pandas
import math
import json
import re
import subprocess

root_dir = "/home/kevin/reactor_sim/milonga_diffusion/"

def generate_mesh(cells_string, post_timestamp):
    # print(cells_string)
    # raise Exception(str(cells_string))
    # print(cells_string)
    cells = json.loads(cells_string)
    gmsh.initialize(sys.argv)
    gmsh.model.add(post_timestamp)

    u = 5
    lc = 1.25

    # cells = {'0,0': 'fuel', '1,0': 'fuel', '2,0': 'water', '0,1': 'water', '1,1': 'fuel', '2,1': 'fuel', '0,2': 'water', '1,2': 'fuel', '2,2': 'fuel'}
    max_x = 0
    max_y = 0
    for cell in cells:
        coords = cell.split(',')
        x = int(coords[0])
        y = int(coords[1])
        # print(x)
        # print(y)
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    #make points
    #pointDict {"x,y": id}
    pointDict = {}
    for j in range(max_y+2):
        for i in range(max_x+2):
            x = i*u
            y = j*u
            id = gmsh.model.geo.addPoint(x, y, 0, lc)
            pointDict.update({str(i)+','+str(j): id})


    # print(str(pointDict))
    innerlines = 0
    matDict = {}
    # lineDict {"x1,y1,x2,y2":id}
    lineDict = {}
    for cell in cells:
        coords = cell.split(',')
        x = int(coords[0])
        y = int(coords[1])

        p1 = pointDict[str(x)+','+str(y)]
        p2 = pointDict[str(x+1)+','+str(y)]
        p3 = pointDict[str(x)+','+str(y+1)]
        p4 = pointDict[str(x+1)+','+str(y+1)]
        # print(p1)
        
        #make or get line 1
        l1v = str(x)+","+str(y)+","+str(x+1)+","+str(y)
        if l1v not in lineDict.keys():
            l1 = gmsh.model.geo.addLine(p1, p2)
            lineDict.update({l1v: l1})
        else:
            innerlines += 1
            l1 = lineDict[l1v]

        #make or get line 2
        l2v = str(x)+","+str(y+1)+","+str(x+1)+","+str(y+1)
        if l2v not in lineDict.keys():
            l2 = gmsh.model.geo.addLine(p3, p4)
            lineDict.update({l2v: l2})
        else:
            innerlines += 1
            l2 = lineDict[l2v]


        #make or get line 3
        l3v = str(x)+","+str(y)+","+str(x)+","+str(y+1)
        if l3v not in lineDict.keys():
            l3 = gmsh.model.geo.addLine(p1, p3)
            lineDict.update({l3v: l3})
        else:
            innerlines += 1
            l3 = lineDict[l3v]

        #make or get line 4
        l4v = str(x+1)+","+str(y)+","+str(x+1)+","+str(y+1)
        if l4v not in lineDict.keys():
            l4 = gmsh.model.geo.addLine(p2, p4)
            lineDict.update({l4v: l4})
        else:
            innerlines += 1
            l4 = lineDict[l4v]


        curveid = gmsh.model.geo.addCurveLoop([-l4, l1, l2, l3])
        curveid = gmsh.model.geo.addCurveLoop([l1, l4, -l2, -l3])
        cellid = gmsh.model.geo.addPlaneSurface([curveid])

        mat = cells[cell]
        if mat in matDict.keys():
            matDict[mat].append(cellid)
        else:
            matDict.update({mat: [cellid]})



    # print(str(innerlines))

    j = 1
    for mat in matDict:
        gmsh.model.addPhysicalGroup(2, matDict[mat], j) #2d, surf 1, tag 1
        gmsh.model.setPhysicalName(2, j, mat) # 2d, surf 1, name
        j += 1


    top = str(max_y+1)
    right = str(max_x+1)

    #get boundary lines
    bottom_boundary = []
    top_boundary = []
    for i in range(max_x+1):
        bottom_boundary.append(lineDict[str(i)+",0,"+str(i+1)+",0"])
        top_boundary.append(lineDict[str(i)+","+top+","+str(i+1)+","+top])

    right_boundary = []
    left_boundary = []
    for j in range(max_y+1):
        right_boundary.append(lineDict[right+','+str(j)+','+right+','+str(j+1)])
        left_boundary.append(lineDict["0,"+str(j)+",0,"+str(j+1)])


    # print(list(map(lambda x: "-"+str(x), top_boundary)))

    boundary_loop = bottom_boundary + right_boundary + list(map(lambda x: "-"+str(x), top_boundary)) + list(map(lambda x: "-"+str(x), left_boundary))

    # print(str(boundary_loop))

    p = gmsh.model.addPhysicalGroup(1, boundary_loop) #2d, surf 1, tag 1
    # print(p)
    gmsh.model.setPhysicalName(1, p, 'boundary') # 2d, surf 1, name

    gmsh.model.occ.synchronize()

    gmsh.model.mesh.generate(2) # 2d

    gmsh.write(root_dir + 'static/' + post_timestamp + ".msh")

    gmsh.finalize()


def generate_mil(ts):
    
    with open(root_dir + 'diffusion_template.mil', 'r') as template:
        t_string = template.read()
    t_string = t_string.replace('replace_this', ts)

    with open(root_dir + 'static/' + ts+'_diffusion.mil', 'w+') as f:
        f.write(t_string)
    #     # print('wrote mil')
    # with open('/var/www/'+ts+'_diffusion.mil', 'w') as f:
    #     f.write(t_string)

    # subprocess.call(['milonga', root_dir + 'static/' + ts +'_diffusion.mil > '+root_dir + 'static/' + ts+'.keff')
    out = subprocess.check_output(['milonga', root_dir + 'static/' + ts +'_diffusion.mil'])

    # with open(root_dir + 'static/' +ts+'.keff', 'r') as f:
    #     try:
    #         keff = float(re.findall("k:\t(\d\.\d*)", f.read())[0])
    #     except:
    #         keff = 0
    #         print('k is zero')

    # print(out.decode())

    try:
        keff = float(re.findall("k:\t(\d\.\d*)", out.decode())[0])
    except:
        keff = 0
        print('k is zero')
    
    os.remove(root_dir + 'static/' +ts+'_diffusion.mil')
    os.remove(root_dir + 'static/' +ts+'.msh')
    # os.remove(root_dir + 'static/' +ts+'.keff')

    return keff

def generate_plot(ts):
    with open(root_dir + 'static/' +ts+'_diffusion.gp', 'w+') as f2:
        f2.write('''
        load "/home/kevin/reactor_sim/milonga_diffusion/gnuplot-palettes/gnbu.pal"
        set term png
        set output "'''+root_dir + '''static/plots/'''+ts+'''_fast.png"
        set view map
        set size ratio -1
        set title "Fast Neutron Flux"
        set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"#FFFFFF" behind
        set pm3d interpolate 8,8
        set dgrid3d
        unset border
        set lmargin at screen 0.05;
        set rmargin at screen 0.9;
        set bmargin at screen 0.1;
        set tmargin at screen 0.87;
        splot "''' + root_dir + 'static/' + ts + '''.dat" using 1:2:3 with pm3d notitle

        set term png
        set output "'''+root_dir + '''static/plots/'''+ts+'''_thermal.png"
        set view map
        set size ratio -1
        set title "Thermal Neutron Flux"
        set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"#FFFFFF" behind
        set dgrid3d
        unset border
        set lmargin at screen 0.0;
        set rmargin at screen 1;
        set bmargin at screen 0.1;
        set tmargin at screen 0.87;
        splot "''' + root_dir + 'static/' + ts + '''.dat" using 1:2:4 with pm3d notitle'''
        )

    os.system('chmod 775 '+root_dir + 'static/' +ts+'_diffusion.gp')
    os.system('gnuplot '+root_dir + 'static/' +ts+'_diffusion.gp')
    os.remove(root_dir + 'static/' +ts+'_diffusion.gp')
    os.remove(root_dir + 'static/' +ts+'.dat')
