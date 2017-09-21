# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect

import json
from django.http import HttpResponse
from sdin.models import *

from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

'''
All response contains a status in json
'status' : xxx
1 for success
0 for failed
'''

@login_required
def design(request):
    return render(request, 'design.html')

def search_parts(request):
    '''
    GET method with param:
        name=xxx
    return json:
        'parts': [{
            'id': xxx,
            'Name': xxx,
            'Description': xxx,
            'Type': xxx,
        }]
    '''
    query_name = request.GET.get('name')
    # Params empty
    if query_name is None or len(query_name) == 0:
        return HttpResponse(json.dumps({
            'status': 0}))

    query_set = Parts.objects.filter(Name__contains = query_name)
    parts = [x.__dict__ for x in query_set]
    return HttpResponse(json.dumps({
            'status': 1,
            'parts': parts}))

@login_required
def get_favorite(request):
    '''
    GET method with no param
    return json:
        'circuits': [{
            'id': xxx,
            'Name': xxx,
            'Description': xxx
        }]
    '''
    query_set = UserFavorite.objects.filter(user = request.user)
    favorites = [x.circuit.__dict__ for x in query_set]
    return HttpResponse(json.dumps({
            'status': 1,
            'circuits': favorites}))

def get_part(request):
    '''
    GET method with param:
        id=xxx
    return json:
        part: {
            'id': xxx,
            'Name': xxx,
            'Description': xxx,
            'Type': xxx,
            'Subparts': [1, 2, 3] # ids of subparts
        }
    '''
    query_id = request.GET.get('id')
    try:
        part = Parts.objects.get(pk = query_id)
        part_dict = part.__dict__
        part_dict['Subparts'] = [x.id for x in part.Subparts.all()]
        return HttpResponse(json.dumps({
            'status': 1,
            'part': part_dict}))
    except:
        return HttpResponse(json.dumps({
            'status': 0}))

def get_circuit(request):
    '''
    GET method with param:
        id=xxx
    return json:
        parts: [{
            'id': xxx, # id of part on Parts table
            'cid': xxx, # id for circuit, used in lines
            'Name': xxx,
            'Description': xxx,
            'Type': xxx,
            'X': xxx, # position in canvas
            'Y': xxx,}
        ]
        lines: [{
            'Start': xxx,    # part cid
            'End': xxx,  # part cid
            'Type': xxx, # connection type}
        ]
    '''
    query_id = request.GET.get('id')
    try:
        parts_query = CircuitParts.object.filter(Circuit = query_id)
        parts = [{'id': x.Part.id, 'cid': x.id, 'Name': x.Part.Name,
            'Description': x.Part.Description, 'Type': x.Part.Type,
            'X': x.X, 'Y': x.Y} for x in parts_query]
        line_query = CircuitLines.objects.filter(Start__Circuit = query_id, \
                End_Circuit = query_id)
        lines = [{'Start': x.Start.id, 'End': x.End.id, 'Type': x.Type} \
                for x in line_query]
        return HttpResponse(json.dumps({
            'status': 1,
            'parts': parts,
            'lines': lines}))
    except:
        return HttpResponse(json.dumps({
            'status': 0}))

def save_query(request):
    '''
    POST method with json:
    {
        parts: [{
            'id': xxx,
            'cid': xxx, # cid generated by yourself
            'X': xxx,
            'Y': xxx
        }],
        lines: [{
            'Start': xxx, # cid defined by yourself
            'End': xxx,
            'Type': xxx
        }],
        circuit: {
            'id': xxx, # circuit id if it's already existing, -1 else
            'Name': xxx,
            'Description': xxx
        }
    }
    response with json:
    {
        status: 0 for error, 1 for success.
    }
    '''
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if data['circuit']['id'] == -1:
                # new circuit
                circuit = Circuit.objects.create(
                        Name = data['circuit']['Name'],
                        Description = data['circuit']['Description'])
            else:
                # existing circuit
                circuit = Circuit.objects.get(pk = data['circuit']['id'])
                circuit.Name = data['circuit']['Name']
                circuit.Description = data['circuit']['Description']
                circuit.save()
                # delete existing circuit part
                for x in CircuitParts.objects.filter(Circuit = circuit):
                    x.delete()
            
            cids = {}
            for x in data['parts']:
                circuit_part = CircuitParts.objects.create(
                        Part = x['id'],
                        Circuit = circuit,
                        X = x['X'],
                        Y = x['Y'])
                cids[x['cid']] = circuit_part.id
            for x in data['lines']:
                CircuitLines.objects.create(
                        Start = cids[x['Start']],
                        End = cids[x['End']],
                        Type = x['Type'])
            return HttpResponse(json.dumps({
                    'status': 1}))
        except:
            return HttpResponse(json.dumps({
                'status': 0}))
    else:
        return HttpResponse(json.dumps({
            'status': 0}))
