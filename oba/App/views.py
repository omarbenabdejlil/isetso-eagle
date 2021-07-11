from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from os import walk
import os
from .models import Machine
from django.http import JsonResponse

# Create your views here.
def clearLines(l, nbr = 1):
    for i in range(0, nbr):
        l.pop(0)
    return l

def clearLinesByWord(l, txt):
    while (l[0].strip() != txt):
        l = clearLines(l)
    l = clearLines(l)
    return l

def getObject(Lines):
    l = []
    cp = 0
    for line in Lines:
        cp += 1
        if (line.strip()):
            l.append(line.strip())

    l = clearLines(l)
    hostName = l[0]

    l = clearLines(l)
    hostOs = l[0]

    l = clearLines(l, 3)
    disk = round(float(l[0][l[0].rfind('M') + 1: l[0].find('%')].strip()), 1)

    l = clearLines(l, 5)
    ram = l[0][l[0].find(':') + 1:].strip()
    ram = round(float(ram[: l[0].find(' ')]) / 1024, 2)

    l = clearLines(l, 2)
    if (l[0].strip().find('{ Bloc Interfaces }')):
        cpu = round(float(l[0].strip()), 2)
    else:
        cpu = round(float('0'), 2)

    l = clearLines(l, 2)
    interface = l[0]

    l = clearLinesByWord(l, '{ adresse ip }')
    ip = l[0]

    l = clearLinesByWord(l, '{ Graphic Card }')
    graphic = ''
    for i in l:
        graphic += i[i.find(':') + 1:].strip() + '\n'

    l=[hostName, hostOs, ip, disk, ram, cpu, interface, graphic.strip()]

    return l

def homePage(request):
    res=[]

    # dir = os.path.dirname(__file__)
    # file_path = os.path.join(dir, 'clients')
    dir = '/home/oba/Documents/oba/App/'
    file_path = os.path.join(dir, 'clients/')

    f = []
    for (dirpath, dirnames, filenames) in walk(file_path):
        f.extend(filenames)
        break

    for cp in range(0, len(f)):
        # path = file_path + '\\' + filenames[cp]
        path = file_path + '/' + filenames[cp]

        file = open(path, 'r')
        Lines = file.readlines()

        data = getObject(Lines)
        res.append(data)

if Machine.objects.filter(fileName=filenames[cp]).exists():
            obj = Machine.objects.get(fileName=filenames[cp])
            if(obj.hostName != data[0]):
                obj.hostName = data[0]
            if(obj.hostOs != data[1]):
                obj.hostOs = data[1]
            if(obj.ip != data[2]):
                obj.ip = data[2]
            if(obj.disk != data[3]):
                obj.disk = data[3]
            if(obj.ram != data[4]):
                obj.ram = data[4]
            if(obj.cpu != data[5]):
                obj.cpu = data[5]
            if(obj.interface != data[6]):
                obj.interface = data[6]
            if(obj.graphic != data[7]):
                obj.graphic = data[7]
            obj.save()
        else:
            m = Machine(
                hostName = data[0],
                hostOs = data[1],
                ip = data[2],
                disk = data[3],
                ram = data[4],
                cpu = data[5],
                interface = data[6],
                graphic = data[7],
                fileName = filenames[cp]
            )
            m.save()

    machineData = Machine.objects.all()

    context = {
        'res': res,
        'machineData': machineData,
    }
    return render(request, 'homePage.html', context)

def detailPage(request, id):
    if request.user.is_authenticated:
        item = Machine.objects.get(id=id)
        context = {
            'item': item,
        }
        return render(request, 'detailPage.html', context)
    else:
        return redirect('/')


@ login_required
def deleteMachine(request):
    pk = request.POST.get('pk', None)
    machine = get_object_or_404(Machine, pk=pk)
    fileName = machine.fileName
    machine.delete()

    # dir = os.path.dirname(__file__)
    # file_path = os.path.join(dir, 'clients')
    dir = '/home/oba/Documents/oba/App/'
    file_path = os.path.join(dir, 'clients/')
    # path = file_path + '\\' + fileName
    path = file_path + '/' + fileName
    os.remove(path)

    return JsonResponse({'msg': 'Success',})

@ login_required
def logout(request):
    auth_logout(request)
    return redirect('/')