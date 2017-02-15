#-*- coding: utf-8 -*-

import xlrd, xlwt, os, uuid, shutil, sqlalchemy
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from ..models.mymodel import *

from pyramid.httpexceptions import HTTPFound
from pyramid.security import Allow, forget, remember
from datetime import *

@view_config(route_name='home', renderer='../templates/companies.jinja2')
def my_view(request):
    complist = []
    message = 'OK'
    log = 0
    s_waste = ''
    s_code = ''
    s_class = 0
    s_city = ''
    s_comp = ''
    try:
        s_waste = request.params['Warse']
        message = message + ' ' + s_waste
    except:
	k=0
    try:
        s_comp = request.params['Company'].capitalize()
        message = message + ' ' + s_waste
    except:
	k=0
    try:
        s_code = request.params['Code'].replace(' ', '')
        print(s_code)
        message = message + ' ' + s_code
    except:
	k=0
    try:
        s_class = request.params['Class']
        message = message + ' ' + s_class
    except:
	s_class = 0
    try:
        s_city = request.params['City'].capitalize()
        message = message + ' ' + s_city
    except:
	k=0
    l=1
    if l==0:
        return Response(str(log==None), content_type='text/plain', status=500)
    if ((s_waste == '') & (s_city == '') & (s_code == '')):
        return {'list': complist, 'project': 'Licenses', 'message': '', 'log': log}
    
    DBSession = Session(bind=engine)
    wastes = DBSession.query(Waste).filter(func.lower(Waste.name).like("%"+func.lower(s_waste)+"%"))
    wastes = wastes.filter(Waste.code.like("%"+s_code+"%"))
    if s_class == '':
	wastes = wastes.all()
    else:
        wastes = wastes.filter(Waste.danger == s_class).all()
    message = message+'wastes'+str(len(wastes))
    cities = DBSession.query(City).filter(City.name.like("%"+s_city+"%")).all()
    message = message+'wastes'+str(len(cities))
    companies = []	
    for c in cities:
        companis = DBSession.query(Company).filter(Company.city == c.id)
	companis = DBSession.query(Company).filter(Company.name.like("%"+s_comp+"%")).all()
        companies.extend(companis)
    comps = []
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0
    t5 = 0
    t6 = 0
    t7 = 0
    try:
        t1 = request.params['t1']
    except:
	t1 = 0
    try:
        t2 = request.params['t2']
    except:
	t2 = 0
    try:
        t3 = request.params['t3']
    except:
	t3 = 0
    try:
        t4 = request.params['t4']
    except:
	t4 = 0
    try:
        t5 = request.params['t5']
    except:
	t5 = 0
    try:
        t6 = request.params['t6']
    except:
	t6 = 0
    try:
        t7 = request.params['t7']
    except:
	t7 = 0
    for c in companies:
        for w in wastes:
            lic = DBSession.query(License).filter(License.waste == w.id)
            lic = lic.filter(License.company == c.id)
            if (t1=="1"):
                lic = lic.filter(License.collection != None)
            else:
                pp=0
            if (t2=="1"):
                lic = lic.filter(License.transportation != None)
            else:
                pp=0
            if (t3=="1"):
                lic = lic.filter(License.defusing != None)
            else:
                pp=0
            if (t4=="1"):
                lic = lic.filter(License.using != None)
            else:
                pp=0
            if (t5=="1"):
                lic = lic.filter(License.treatment != None)
            else:
                pp=0
            if (t6=="1"):
                lic = lic.filter(License.recovery != None)
            else:
                pp=0
            if (t7=="1"):
                lic = lic.filter(License.placement != None)
            else:
                pp=0
            lic = lic.first()
	    if lic is not None:
            	comps.append(lic)		 
    for comp in comps:
        company = DBSession.query(Company).filter(comp.company == Company.id).first()
        city = DBSession.query(City).filter(company.city == City.id).first()
        w = DBSession.query(Waste).filter(comp.waste == Waste.id).first()
        record = {'waste': w.name, 'code': w.code, 'class':w.danger, 'c1':comp.collection, 'c2':comp.transportation,'c3':comp.defusing, 'c4':comp.using, 'c5':comp.treatment, 'c6':comp.recovery, 'c7':comp.placement,
                  'c1f': comp.collectionf, 'c2f': comp.transportationf, 'c3f': comp.defusingf,
                  'c4f': comp.usingf, 'c5f': comp.treatmentf, 'c6f': comp.recoveryf, 'c7f': comp.placementf,
                  'company':company.name, 'city':city.name, 'other': comp.other, 'id': comp.id}
        complist.append(record)
    return {'list': complist, 'project': 'Licenses', 'log': log, 'message': '', 'b1':s_waste, 'b2':s_code, 'b3':s_class, 'b4':s_city, 'comp1':s_comp, 'tt1':t1, 'tt2':t2, 'tt3':t3, 'tt4':t4, 'tt5':t5, 'tt6':t6, 'tt7':t7}

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

@view_config(route_name='updating', renderer='../templates/updating.jinja2', permission='view')
def upd_view(request):
    try:

        DBSession = Session(bind=engine)
        lic = DBSession.query(License).filter(License.id == request.params['id']).first()
        comp = DBSession.query(Company).filter(Company.id == lic.company).first()
        city = DBSession.query(City).filter(City.id == comp.city).first()
        waste = DBSession.query(Waste).filter(Waste.id == lic.waste).first()
        other = lic.other
        ec = {'c1': lic.collection, 'c2': lic.transportation, 'c3': lic.defusing, 'c4': lic.using, 'c5': lic.treatment, 'c6': lic.recovery, 'c7': lic.placement,
                  'c1f': lic.collectionf, 'c2f': lic.transportationf, 'c3f': lic.defusingf, 'c4f': lic.usingf, 'c5f': lic.treatmentf, 'c6f': lic.recoveryf, 'c7f': lic.placementf}
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'c': ec, 'company': comp, 'project': 'Licenses', 'city':city, 'waste': waste, 'other': other, 'id':request.params['id']}

@view_config(route_name='update', renderer='../templates/updating.jinja2', permission='view')
def update_view(request):
    try:
        DBSession = Session(bind=engine)
        DBSession.query(License).filter(License.id == request.params['id']).delete()
        ot = request.params['w']
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
        org = request.params['comp']
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

    except DBAPIError:
        return Response(k, content_type='text/plain', status=500)
    return HTTPFound('/')


@view_config(route_name='compadd', renderer='../templates/adding.jinja2', permission='view')
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
            try:
                row = sheet.row_values(rownum)
                ot = row[0]
                code = str(row[1]).replace('.0', '')
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
                w = DBSession.query(Waste).filter(((Waste.name == ot) or (Waste.code == code)))
                w = w.filter((Waste.danger == classe)).first()
                k = '7'
                if w is None:
                    new_w = Waste(name=ot, code=code, danger=classe)
                    DBSession.add(new_w)
                    DBSession.commit()
                w = DBSession.query(Waste).filter(((Waste.name == ot) or (Waste.code == code)))
                w = w.filter((Waste.danger == classe)).first()
                citi = DBSession.query(City).filter(City.name == city).first()
                k = '8'
                if citi is None:
                    new_city = City(name=city)
                    DBSession.add(new_city)
                    DBSession.commit()
                citi = DBSession.query(City).filter(City.name == city).first()
                compani = DBSession.query(Company).filter((Company.name == org))
                compani = compani.filter((Company.city == citi.id)).first()
                k = '9'
                if compani is None:
                    new_company = Company(name=org, city=citi.id)
                    DBSession.add(new_company)
                    DBSession.commit()
                compani = DBSession.query(Company).filter(Company.name == org).first()
                try:
                    li = DBSession.query(License).filter(License.company == compani.id)
                    li = li.filter(License.waste == w.id).first()#and (License.waste == w.id)).first()
                    #for li in deletinglic:
                    DBSession.query(License).filter(License.id == li.id).delete()
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
                k=''
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

@view_config(route_name='delete', request_method='GET')
def deleting_view(request):
    try:
        DBSession = Session(bind=engine)
        DBSession.query(License).filter(License.id == request.params['id']).delete()
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

@view_config(route_name='upp', renderer='../templates/upd.jinja2')
def upp(request):
    return {'id': request.params['id']}

@view_config(route_name='upp1', renderer='../templates/add.jinja2')
def upp1(request):
    return {'id': request.params['id']}

@view_config(route_name='upp2', renderer='../templates/del.jinja2')
def upp2(request):
    return {'id': request.params['id']}

# обработка логина
@view_config(route_name='logged', request_method='POST')
def login(request):
    DBSession = Session(bind=engine)
    result = DBSession.query(User).filter(User.email == request.params['username'])
    result = result.filter(User.password == request.params['password']).first()
    if result:
        headers = remember(request, 'admin')
        return HTTPFound(location='/', headers = headers)
    headers = remember(request, 'admin')
    return HTTPFound(location='/', headers = headres)

@view_config(route_name='logouted')
def logout(request):
    headers = forget(request)
    return HTTPFound('/', headers=headers)

db_err_msg = """\
При подключении к базе данных возникла ошибка.
Возможно, база данных не инициализирована, либо отсутствует файл БД.
Обртитесь к администратору для устранения проблем
"""
