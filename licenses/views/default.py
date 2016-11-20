#-*- coding: utf-8 -*-

import xlrd, xlwt, os, uuid, shutil
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models.mymodel import *

from pyramid.httpexceptions import HTTPFound
from pyramid.security import Allow, forget, remember
from datetime import *

@view_config(route_name='home', renderer='../templates/companies.jinja2')
def my_view(request):
    try:
        if request.authenticated_userid == None:
            log = 'true'
        else:
            log = None
        DBSession = Session(bind=engine)
        comps = DBSession.query(License).all()
        complist = []
        for comp in comps:
            company = DBSession.query(Company).filter(comp.company == Company.id).first()
            city = DBSession.query(City).filter(company.city == City.id).first()
            w = DBSession.query(Waste).filter(comp.waste == Waste.id).first()
            record = {'waste': w.name, 'code': w.code, 'class':w.danger, 'c1':comp.collection, 'c2':comp.transportation,'c3':comp.defusing, 'c4':comp.using, 'c5':comp.treatment, 'c6':comp.recovery, 'c7':comp.placement,
                      'c1f': comp.collectionf, 'c2f': comp.transportationf, 'c3f': comp.defusingf,
                      'c4f': comp.usingf, 'c5f': comp.treatmentf, 'c6f': comp.recoveryf, 'c7f': comp.placementf,
                      'company':company.name, 'city':city.name, 'other': comp.other, 'id': comp.id}
            complist.append(record)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'list': complist, 'project': 'Licenses'}

@view_config(route_name='company', renderer='../templates/companies.jinja2')
def comp_view(request):
    try:
        DBSession = Session(bind=engine)
        comps = DBSession.query(Company).all()
        complist = []
        for comp in comps:
            city = DBSession.query(City).filter(comp.city == City.id).first()
            record = {'name': comp.name, 'city': city.name, 'id': comp.id}
            complist.append(record)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'list': complist, 'project': 'Licenses'}

@view_config(route_name='compadd', renderer='../templates/adding.jinja2')
def comp_view(request):
    try:

        DBSession = Session(bind=engine)
        comps = DBSession.query(Company).all()
        complist = []
        a = []
        cc = []
        aa = DBSession.query(Waste).all()
        for el in aa:
            a.append({'id': el.id, 'code': el.code, 'name': el.name})
        for comp in comps:
            city = DBSession.query(City).filter(comp.city == City.id).first()
            record = {'name': comp.name, 'city': city.name, 'id': comp.id}
            complist.append(record)
        if (request.params['id'] != '0'):
            lic = DBSession.query(License).filter(License.id == request.params['id']).first()
            ec = {'c1': lic.collection, 'c2': lic.transportation, 'c3': lic.defusing, 'c4': lic.using, 'c5': lic.treatment, 'c6': lic.recovery, 'c7': lic.placement,
                  'c1f': lic.collectionf, 'c2f': lic.transportationf, 'c3f': lic.defusingf, 'c4f': lic.usingf, 'c5f': lic.treatmentf, 'c6f': lic.recoveryf, 'c7f': lic.placementf}
            cc.append(ec)
        else:
            ec = {'c1': 0, 'c2': 0, 'c3': 0, 'c4': 0, 'c5': 0, 'c6': 0, 'c7': 0}
            cc.append(ec)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'list1': complist, 'list': a, 'project': 'Licenses', 'c':cc, 'id':request.params['id']}

@view_config(route_name='parse', request_method='POST')
def parse_view(request):
    try:
        DBSession = Session(bind=engine)
        with open("tempbook.xls", 'wb') as file:
            file.write(request.params["f"].value)
        rb = xlrd.open_workbook('tempbook.xls')
        sheet = rb.sheet_by_index(0)
        for rownum in range(sheet.nrows):
                row = sheet.row_values(rownum)
                ot = row[0]
                code = row[1]
                classe = row[2]
                c1d = row[3]
                c1f = row[4]
                c2d = row[5]
                c2f = row[6]
                c3d = row[7]
                c3f = row[8]
                c4d = row[9]
                c4f = row[10]
                c5d = row[11]
                c5f = row[12]
                c6d = row[13]
                c6f = row[14]
                c7d = row[15]
                c7f = row[16]
                org = row[17]
                city = row[18]
                other = row[19]
                if c1d == '':
                    c1d = None
                else:
                    k = '+'
                if c2d == '':
                    c2d = None
                else:
                    k = '++'
                if c3d == '':
                    c3d = None
                else:
                    k = '+++'
                if c4d == '':
                    c4d = None
                else:
                    k = '++++'
                if c5d == '':
                    c5d = None
                else:
                    k = '+++++'
                if c6d == '':
                    c6d = None
                else:
                    k = '++++++'
                if c7d == '':
                    c7d = None
                else:
                    k = '+++++++'
                if c1f == '':
                    c1f = None
                else:
                    k = '++++++++'
                if c2f == '':
                    c2f = None
                else:
                    k = '+++++++++'
                if c3f == '':
                    c3f = None
                else:
                    k = '++++++++++'
                if c4f == '':
                    c4f = None
                else:
                    k = '+++++++++++'
                if c5f == '':
                    c5f = None
                else:
                    k = '++++++++++++'
                if c6f == '':
                    c6f = None
                else:
                    k = '+++++++++++++'
                if c7f == '':
                    c7f = None
                else:
                    k = '++++++++++++++'
                w = DBSession.query(Waste).filter((Waste.name == ot or Waste.code == code) and Waste.danger == classe).first()
                k = '7'
                if w is None:
                    new_w = Waste(name=ot, code=code, danger=classe)
                    DBSession.add(new_w)
                    DBSession.commit()
                w = DBSession.query(Waste).filter(
                    (Waste.name == ot or Waste.code == code) and Waste.danger == classe).first()
                citi = DBSession.query(City).filter(City.name == city).first()
                k = '8'
                if citi is None:
                    new_city = City(name=city)
                    DBSession.add(new_city)
                    DBSession.commit()
                citi = DBSession.query(City).filter(City.name == city).first()
                compani = DBSession.query(Company).filter(Company.name == org and Company.city == citi.id).first()
                k = '9'
                if compani is None:
                    new_company = Company(name=org, city=citi.id)
                    DBSession.add(new_company)
                    DBSession.commit()
                compani = DBSession.query(Company).filter(Company.name == org).first()
                license = DBSession.query(License).filter(License.company == compani.id and License.waste == w.id).first()
                k='10'
                if license:
                    try:
                        DBSession.query(License).filter(License.company == compani.id and License.waste == w.id).first.delete()
                        DBSession.commit()
                    except:
                        k=' '
                new_license = License(company=compani.id, waste=w.id, collection=c1d, transportation=c2d,
                                      defusing=c3d, using=c4d, treatment=c5d, recovery=c6d, placement=c7d,
                                      collectionf=c1f, transportationf=c2f, defusingf=c3f, usingf=c4f,
                                      treatmentf=c5f, recoveryf=c6f, placementf=c7f, other=other)
                DBSession.add(new_license)
                DBSession.commit()
    except:
        return HTTPFound(location='/')
    return HTTPFound(location='/')


@view_config(route_name='adding')
def adding_view(request):
    try:
        DBSession = Session(bind=engine)
        ot = request.params['waste']
        c1d = request.params['c1']
        c1f = request.params['c11']
        c2d = request.params['c2']
        c2f = request.params['c21']
        c3d = request.params['c3']
        c3f = request.params['c31']
        c4d = request.params['c4']
        c4f = request.params['c41']
        c5d = request.params['c5']
        c5f = request.params['c51']
        c6d = request.params['c6']
        c6f = request.params['c61']
        c7d = request.params['c7']
        c7f = request.params['c71']
        org = request.params['company']
        other = request.params['other']
        if c1d == '':
            c1d = None
        else:
            k = '+'
        if c2d == '':
            c2d = None
        else:
            k = '++'
        if c3d == '':
            c3d = None
        else:
            k = '+++'
        if c4d == '':
            c4d = None
        else:
            k = '++++'
        if c5d == '':
            c5d = None
        else:
            k = '+++++'
        if c6d == '':
            c6d = None
        else:
            k = '++++++'
        if c7d == '':
            c7d = None
        else:
            k = '+++++++'
        if c1f == '':
            c1f = None
        else:
            k = '++++++++'
        if c2f == '':
            c2f = None
        else:
            k = '+++++++++'
        if c3f == '':
            c3f = None
        else:
            k = '++++++++++'
        if c4f == '':
            c4f = None
        else:
            k = '+++++++++++'
        if c5f == '':
            c5f = None
        else:
            k = '++++++++++++'
        if c6f == '':
            c6f = None
        else:
            k = '+++++++++++++'
        if c7f == '':
            c7f = None
        else:
            k = '++++++++++++++'
        w = DBSession.query(Waste).filter(Waste.id == ot).first()
        compani = DBSession.query(Company).filter(Company.id == org).first()
        new_license = License(company=compani.id, waste=w.id, collection=c1d, transportation=c2d,
                              defusing=c3d, using=c4d, treatment=c5d, recovery=c6d, placement=c7d,
                              collectionf=c1f, transportationf=c2f, defusingf=c3f, usingf=c4f,
                              treatmentf=c5f, recoveryf=c6f, placementf=c7f, other=other)
        DBSession.add(new_license)
        DBSession.commit()
        try:
            DBSession.query(License).filter(License.id==request.params['id']).delete()
        except:
            p=''
        DBSession.commit()
    except:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return HTTPFound('/')

view_config(route_name='deleting', request_method='GET')
def del_view(request):
    try:
        DBSession = Session(bind=engine)
        DBSession.query(License).filter(License.id == request.params['id'])
        DBSession.commit()
    except DBAPIError:
        return HTTPFound('/')
    return HTTPFound('/')

# главная страница
@view_config(route_name='login', renderer='../templates/signin.jinja2')
def signin(request):
    if request.authenticated_userid == None:
        headers = forget(request)
    else: return HTTPFound(location='../', headers = None)
    return {'project': 'kek', 'users' :['1', '2', '3']}

# обработка логина
@view_config(route_name='logged', renderer='../templates/logged.jinja2', request_method='POST')
def login(request):
    DBSession = Session(bind=engine)
    result = DBSession.query(User).filter(User.email == request.params['username'], User.password == request.params['password']).first()
    if result != None:
        headers = remember(request, request.params['username'])
        return HTTPFound(location='/', headers = headers)
    return HTTPFound(location='/login')

@view_config(route_name='logouted', renderer='../templates/logouted.jinja2')
def logout(request):
    headers = forget(request)
    return HTTPFound('/', headers=headers)

db_err_msg = """\
При подключении к базе данных возникла ошибка.
Возможно, база данных не инициализирована, либо отсутствует файл БД.
Обртитесь к администратору для устранения проблем
"""
