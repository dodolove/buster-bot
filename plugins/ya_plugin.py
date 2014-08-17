#===istalismanplugin===
# -*- coding: utf-8 -*-

if not 'DIGIT_MENU' in globals().keys():
        DIGIT_MENU = {}

##########
def kk():
    db=eval(read_file('nww.txt'))
    dbb={}
    k = 0
    infected=0
    d = ''
    for x in db:
        k=0
        for c in x:
            if unicodedata.category(c) in ['Lo']:
                k=True
        if not k and not x.count('syria') and not x.count('arab'):
            dbb[x]=int(db[x]['user'])
        else:
            infected+=1
    #sorted(dbb.items())
    dbb = sorted(dbb.iteritems(), key=operator.itemgetter(1))
    dbb.reverse()
    zz = dbb
    rep = ''
    n = 0
    for x in dbb:
        n+=1
        rep+=str(n)+') '+h(x[0],x[0])+' ('+str(db[x[0]]['user'])+') ['+db[x[0]]['info']+']\n'
        if n>=100:
            break
    return u'Всего конференций: '+str(len(db))+u'<br />Отфильтровано в черный список: '+str(infected)+'<br />'+rep


WEATHER_CACHE = 'dynamic/weather_cache.txt'
db_file(WEATHER_CACHE, dict)

def yaw_getcity(jid, city=None):
    try: db=eval(read_file(WEATHER_CACHE))
    except: return None
    if city:
        db[jid]=city
        write_file(WEATHER_CACHE, str(db))
        return True
    else:
        if jid in db.keys():
            return db[jid]
    return None

def ya_week(t, s, p):
    if len(p)>35: return
    
    jid = get_true_jid(s)
    if not p:
        p = yaw_getcity(jid)
        if not p: return
    else:
        yaw_getcity(jid, p)
        
    p = urllib.quote(p.encode('utf8'))
    req = urllib2.Request('http://pogoda.yandex.ua/search/?request='+p)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
    page = urllib2.urlopen(req).read()
    gh = page
    
    try: city = re.findall('<title>(.*)</title>', page)[0]
    except: city = ''
    page = re.findall('клімат|докладно(.*?)Розіграш погоди', page, re.DOTALL | re.IGNORECASE)
    if not page:
        if not page:
            reply(t, s, u'Нет погоды для '+p)
            return
    page = page[0]
    m = re.findall('<tr>.*?</tr>',page, re.DOTALL | re.IGNORECASE)
    if not m:
        reply(t, s, u'Произошла ошибка!')
        return
    try:
        if len(m)>=14: m = m[10:]
    except: pass
    DICT = {}
    for x in m:
        l=x.split('</div>')
        if m.index(x)==0:
            l=x.split('</div></div>')
        DICT[m.index(x)]=l
    rep=city+u'\nДень | t° max - t° min\n'.encode('utf8')
    n=0
    try:
        for x in DICT[0]:
            k=htmlp(x)
            if k.isspace() or not re.findall('[0-9]+',k,re.DOTALL | re.IGNORECASE):
                continue
            rep+=k+' - '+htmlp(DICT[1][n])+' '+htmlp(DICT[2][n])+' '+htmlp(DICT[3][n])+'\n'
            n+=1
    except: pass
    rep = rep.replace('    ',' ')
    reply(t, s, unicode(rep,'UTF-8'))  
    

def htmlp(data):
    data=re.compile(r'<[^<>]*>').sub('', data)
    return data


import xml.etree.ElementTree as etree

def ya_word(p):
    import xml.etree.ElementTree
    p=p.replace(' ','+')
    r = re.compile(r"^\s+", re.MULTILINE)
    p = r.sub("", p) # "a\nb\nc"
    c = xml.etree.ElementTree.fromstring(urllib.urlopen('http://speller.yandex.net/services/spellservice/checkText?text='+p.encode('utf8','replace')).read())
    for x in c:
        if len(x)>1:
            try:
                word = x.find('word').text
                s = x.find('s').text
                pos = int(x.get('pos'))
                l = int(x.get('len'))
                p = p[:pos]+s+p[pos+l:]
            except:
                raise
    return p.replace('+',' ')


#SPELL = {}


#def ya_spell_msg(r,t,s,p):
#    if not 


def ya_gr(t, s, p):
    reply(t, s, ya_word(p))


register_command_handler(ya_gr, 'gr', ['все'], 0, 'Сервис проверки правописания Яндекс.Спеллер', 'gr <текст>', ['gr превед'])




def yanew_getid(city):
    list = []
    city = city.replace(' ','-')
    
    import xml.etree.ElementTree
    c = xml.etree.ElementTree.fromstring(urllib.urlopen('http://weather.yandex.ru/static/cities.xml').read())
    for i in c:
        for x in i:
            #print x
            if hasattr(x, 'text'):
                ct = x.text.lower()
                if ct==city.lower() or ct.count(city.lower()):#FIX#05.07 or ct.count(city.lower()):
                    #return x.get('id')
                    list.append((x.get('id'),x.get('part'),x.get('country'),x.text))
    return list

YA_TEMP = {}
YA_VAR = {}


def msg_yanew_more(r, t, s, p):
    jid = get_true_jid(s)
    if jid in YA_TEMP.keys() and p=='+':
        if time.time()-YA_TEMP[jid]<300:
            yanew_getweath(t, s, '', more=1)
        del YA_TEMP[jid]

register_message_handler(msg_yanew_more)


def yanew_getweath(t, s, p, more=0):
    global YA_VAR
    global DIGIT_MENU
    
    jid = get_true_jid(s)
    fn = inspect.stack()[0][3]
    mem = False

    if jid in YA_VAR.keys() and p in YA_VAR[jid].keys():
        p = YA_VAR[jid][p]
        try:
            del YA_VAR[jid]
            del DIGIT_MENU[jid]
        except: pass
        
    from datetime import date
    if not p:
        p = yaw_getcity(jid)
        if not p:
            reply(t, s, u'И какой город мне показывать?')
            return
    else:
        yaw_getcity(jid, p)
        mem = True
        #reply(t, s, u'Запомнил!')
        #time.sleep(2)
    
    
    def fdd(x, key):
        res = 'None'
        if hasattr(x, 'find'):
            res = x.find(key)
            if hasattr(res, 'text'):
                return res.text
        return res
    wind = {'n':u'с','e':u'в','w':u'з','s':u'ю','c':u'затишье'}
    R = [None,u'Пн.',u'Вт.',u'Ср.',u'Чт.',u'Пт.',u'Сб.',u'Вс.']
    a = '{http://weather.yandex.ru/forecast}'
    d = {0:a+'forecast',1:a+'day',2:a+'fact',3:a+'day_part',4:a+'temperature_from',5:a+'temperature_to',6:a+'weather_type',7:a+'weather_type_short',8:a+'wind_speed',9:a+'humidity',10:a+'temperature',11:a+'sunrise',12:a+'sunset'}
    word = {d[11]:u'Рассвет',d[12]:u'Закат',d[4]:u'от',d[5]:u'до',u'morning':u'Утром',u'day':u'Днем',u'evening':u'Вечером',u'night':u'Ночью'}
    id = (p if p.isdigit() else yanew_getid(p))
    if not id:
        reply(t, s, u'Город не найден!')
        return
    r = u'Выберите Bаш населенный пункт, например 1:\n'
    np = 0
    if len(id)>1 and not isinstance(id, basestring):
        for k in id:
            np+=1
            
            try:
                r+=str(np)+') '+k[1]+' '+k[2]+' - '+k[3]+'\n'
                if not jid in YA_VAR:
                    YA_VAR[jid] = {}
                YA_VAR[jid][str(np)] = k[0]
            except: pass
        DIGIT_MENU[jid]=fn
        reply(t, s, r)
        return
    if isinstance(id, list):
        id=id[0][0]
    #print id
    c = etree.parse(urllib.urlopen('http://export.yandex.ru/weather-ng/forecasts/'+id+'.xml')).getroot()
    listday = [x for x in c._children if x.tag == d[1]]
    if not more and len(listday)>2:
        listday = listday[:2]
    else: listday = listday[2:]
    fact = [x for x in c._children if x.tag == d[2]]
    if fact: fact = fact[0]
    rep = u'Погодa для '+c.get('city')+', '+c.get('country')+'\n'
    rep+= u'Сейчас: '+fdd(fact, d[10])+u'°C, '+fdd(fact, d[7])+', '+fdd(fact, d[8])+u'м/с\n'
    l = ''
    dw = ''
    for x in listday:
        date = x.attrib.get('date','0')
        try:
            sp = [int(g) for g in date.split('-')]
            dw = R[datetime.date(sp[0], sp[1], sp[2]).isoweekday()]
        except: pass
        rep+='\n   '+date+','+dw+'\n'
        l = u'  Свет. день: '+x.find(d[11]).text+u'-'+x.find(d[12]).text+'\n'
        #try: x.iter('{http://weather.yandex.ru/forecast}day_part')
        #except: continue
        for i in [m for m in x.findall('{http://weather.yandex.ru/forecast}day_part')]:
            if not i.attrib['type'] in word:
                continue
            
            rep+=word[i.attrib['type']]+':\n'
            
            try: rep+=i.find(d[4]).text+' ... '+i.find(d[5]).text+', '+i.find(d[7]).text+'\n'
            except: rep+=i.find(d[10]).text+', '+i.find(d[7]).text+'\n'
            finally: pass
        rep+=l
    if not more:
        rep+=u'\n+ чтобы читать дальше'
        YA_TEMP[get_true_jid(s)]=time.time()
    
    reply(t, s, ('' if not mem else u'Город сохранен, в следующий раз можете использовать команду без параметров!\n')+rep)
    

    
#register_command_handler(ya_week, 'week', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ru ', 'week <city>', ['week киев'])
register_command_handler(yanew_getweath, 'ya', ['все'], 0, 'Погода предоставлена сайтом http://yandex.ru \nАвтоматически запоминает последний указанный город, в дальнейшем можно использовать без параметров.', 'ya <city>', ['ya киев'])
