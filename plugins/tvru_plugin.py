#===istalismanplugin===# -*- coding: utf-8 -*-from fake_useragent import UserAgentimport HTMLParserimport cookielibTVC = cookielib.CookieJar()TV = urllib2.build_opener(urllib2.HTTPCookieProcessor(TVC))TV.addheaders = [('User-agent',(UserAgent().random))]URLTV = base64.b64decode('aHR0cDovL20udHYueWFuZGV4LnJ1Lw==')TVREDIR = str()TV_LAST_FILE = 'dynamic/tv_cache_file.txt'db_file(TV_LAST_FILE, dict)def prog_grabru(code, n='1', uk=0):        import urllib2        import re        import time        kod=code.lower()        kod=kod.strip()        if kod == '' or not kod.isdecimal():                program = u'И какой канал мне показывать? Номер канала можно узнать, дав команду боту "тв_лист"'                return program                zone = '1'        if uk: zone+='87'                url = URLTV+zone+'/channels/'+kod        if n == '2': url = URLTV+zone+'?channel='+kod+'&when='+n+'&day='+prog_listru()[0]        r = TV.open(url).read()#urllib2.urlopen(req).read()        r = re.findall('<th class="channel">(.*?)Выбор каналов', r, re.DOTALL | re.IGNORECASE)        if not r:                if not uk:                        return prog_grabru(code, n, uk=1)                else:                        program = u'Нет программы на сегодня.'        else:                r = r[0]                r = r.replace('</tr>','\n').replace('</a>',' ')                r = re.compile(r'<[^<>]*>').sub('', r)                try: r = re.sub(r'\n\s{0,3}[^0-9]{1,2}[^:].*?$','',r)##16.08.13                except: pass                program = r        return programdef prog_grabru2(code):    return prog_grabru(code, n='2')RZ=''def tv_finder_by_name(t, s, p, full=0, tw=0, var=0, nextday=0):        a = prog_listru()                day = a[0]        if nextday:                day = str(int(day)+1)        channel = '%2C'.join(a[2])        reg = ('213' if not tw else '187')        #print reg, day, channel        url = URLTV+reg+'/?day='+day+'&when=1&channel='+channel        if not day.isdigit():                reply(t, s, u'Парсер накрылся!')                return        r = TV.open(url).read()                r = r.decode('utf8','ignore')        try: r = r.split('Все настроенные')[1]        except: pass        #r = re.findall('<option value="(.*?)">(.*?)</option>', r, re.DOTALL | re.IGNORECASE)        #r = filter(lambda x : x[0].isdigit(), r)                r = re.findall('<a href="/\d{1,4}/channels/(\d{1,4})">(.*?)</a>', r, re.DOTALL | re.IGNORECASE)                #r = [x for x in r if not [c[0] for c in r].count(x[0])>1 and not x[0] in ['2']]                rep = str()        list = [x for x in r if x[1].strip().lower().count(p.lower()) or x[0]==p]        gu = list        if not list:                if tw:                        rep = u'Канал по запросу < '+p+u' > не найден!'                        if not var: reply(t, s, rep)                        else: return rep                        return                else:                        a = tv_finder_by_name(t, s, p, full, 1, var)                        if var: return a                return        #x = list[0]        when = '1'                try:                if full: when = '2'                url = URLTV+reg+'?day='+day+'&channel='+list[0][0]+'&flag=&when='+when                                #req = urllib2.Request(URLTV+reg+'?day='+day+'&channel='+list[0][0]+'&flag=&when='+when)                r = TV.open(url).read().decode('utf8','ignore')#urllib2.urlopen(req).read().decode('utf8','ignore')                                title = re.findall('<title>(.*?)</title>', r, re.DOTALL | re.IGNORECASE)[0]                #r = re.findall('<.*?>'+list[0][1]+'(.*?)</table>', r, re.DOTALL|re.IGNORECASE)                r = re.findall('(\d{1,2}:\d{1,2}.*?)</tr>',r,re.DOTALL|re.IGNORECASE)                r = ''.join(r)                #try: r = r[0]                #except: pass                r = r.replace('<trr>','\n').replace('</a>',' ')                r = re.compile(r'<[^<>]*>').sub('', r)                r = title+r                r = re.compile(r'(\d{1,2}:\d{1,2})').sub(r'\n\1',r)        except:                r = u'Упс, разметка видимо сменилась'        if len(list)>1 and not var:                handler_TVru_search(t, s, p)                return                rep = r        if var:                return rep        reply(t, s, r)        #rep = ('Найдено возможных совпадений по каналам: '+str(len(list))+' см. тв_лист\n' if len(list)>1 anc+(prog_grabru(x[0]) if full==0 else prog_grabru(x[0],n='2'))        #if var: return rep        #else: reply(t, s, rep)PROGL_LAST = {'last':0, 'day':0, 'program':str(), 'channels':list(), 'rep':str()}def prog_listru(nn=0,k=0):        global URLTV        global TVREDIR        from fake_useragent import UserAgent        f = PROGL_LAST        if time.time()-PROGL_LAST['last']<300:                return f['day'], (f['rep'] if not nn else f['program']), f['channels']        url, nurl = URLTV+('87' if k else '213'), str()        rr = TV.open(url).read()        try:                if rr.count('window.location.replace'):                        ###'Redirect'                        nurl = re.findall(r'href=[\'"]?([^\'" >]+)', rr)[0]                        h = HTMLParser.HTMLParser()                        nurl = h.unescape(nurl)                        if nurl.count('ua'):                                URLTV = base64.b64decode('aHR0cDovL20udHYueWFuZGV4LnVhLw==')                        rr = TV.open(nurl).read()        except: pass                day = re.findall('<input type="hidden" name="day" value="(.*?)"', rr, re.DOTALL | re.IGNORECASE)        if day: day = day[0]        try: rr = rr.split('Все настроенные')[1]        except: pass        r = re.findall('<option value="(.*?)">(.*?)</option>', rr, re.DOTALL | re.IGNORECASE)                channels = re.findall('<option value="(\d{1,4})">.*?</option>', rr, re.DOTALL | re.IGNORECASE)        program=''        if not channels:                return u'Несмог получить список каналов!'        r = filter(lambda x : x[0].isdigit(), r)        r = [x for x in r if not [c[0] for c in r].count(x[0])>1 and not x[0] in ['2']]        r = sorted(r, key=lambda x: int(x[0]))        rep=''        n=0        for x in r:                s=', '                if r.index(x)==(len(r)-1): s=''                n+=1                if n == 3:                        n = 0                        s = '\n'                rep+=x[0]+' -'+x[1]+s        program = ', '.join([x[0]+' -'+x[1] for x in r])        PROGL_LAST['day'] = day        PROGL_LAST['rep'] = rep        PROGL_LAST['channels'] = channels        PROGL_LAST['program'] = program        PROGL_LAST['last'] = time.time()        return day, (rep if not nn else program), channelsdef handler_TVru_now(type, source, p):        nd = 0        l = TVru_stat(source, p)                if p:                                tv_finder_by_name(type, source, p, nextday=nd)                        else:                list = l                if not list:                        reply(type, source, u'История не найдена..Укажите название канала!')                        return                rep = str()                i = []                a = ''                for x in list:                        a = tv_finder_by_name(type, source, x, var=1)                        time.sleep(1)                        if not a in i and isinstance(a, basestring):                                i.append(a)                                reply(type, source, '\n'.join(i))def TVru_stat(source, p):        jid = get_true_jid(source)        db = eval(read_file(TV_LAST_FILE))        if not jid in db.keys():                db[jid] = []        if not isinstance(db[jid],list):                db[jid] = []        if not p.isspace() and len(p)>0:                if not p in db[jid]:                        db[jid].append(p)                        if len(db[jid])>5:                                db[jid].pop(0)                else:                        db[jid].remove(p)                        db[jid].insert(len(db[jid])-1,p)        write_file(TV_LAST_FILE, str(db))        return db[jid]def handler_TVru_full(type, source, p):        ss = p.split()        nd = 0        if len(ss)>1 and ss[0].lower()==u'завтра':                p = ' '.join(ss[1:])                nd = 1        l = TVru_stat(source, p)                if not p:                if l:                        p = l[len(l)-1]                else:                        reply(type, source, u'История не найдена..Уточните канал!')                        return        if type == 'public':                type == 'private'                reply(type,source,u'смотри приват!')                tv_finder_by_name(type, source, p, full=1, nextday=nd)def handler_TVru_list(type, source, parameters):        if type == 'public':                reply(type,source,u'смотри приват!')        rep=''        f=prog_listru()[1]        reply('private',source, f)def handler_TVru_search(type, source, parameters):        if not parameters or parameters.isspace():                return        parameters=parameters.lower()        b = str()        if type == 'public':                reply(type,source,u'смотри приват!')        rep=''        f=prog_listru(nn=1)[1].split(',')        f2=prog_listru(nn=1,k=1)[1].split(',')        f.extend([ x for x in f2 if not x in f])        for x in f:                x=x.decode('utf-8','replace')                b=x.lower()                if b.count('-'):                        c=b.split('-')[1]                        if c.count(parameters):                                rep+=x+'\n'        if not rep or rep.isspace():                reply('private', source, u'Ничего не найдено!')                return        reply('private',source, rep+u'\nКомандуйте тв и номер канала, напр. тв 4')register_command_handler(handler_TVru_search, 'тв_найти', ['фан','все'], 0, 'Ищет код по названию канала или по совпадению', 'тв_найти канал', ['тв_найти Discovery'])  register_command_handler(handler_TVru_full, 'тв+', ['фан','все'], 0, 'Показать телепрограму для определенного канала полностью. Каналы можно просмотреть в команде "тв_лист". \nКоманда без параметров выводит телепрограмму на последний запрошенный канал из истроии.', 'тв+ [номер канала/название]', ['тв+ завтра 2x2','тв 144'])register_command_handler(handler_TVru_now, 'тв', ['фан','все'], 0, 'Показать телепрограму для определенного канала. Каналы можно просмотреть в команде "тв_лист".\n Команда без параметров выводит телепрограмму на последних 5 каналов из истории. \nСервис предоставлен сайтом '+URLTV, 'тв [номер канала/название канала]', ['тв 144','тв discovery'])register_command_handler(handler_TVru_list, 'тв_лист', ['фан','все'], 0, 'Просмотреть номера каналов чтобы потом узнать телепрограму', 'тв_лист', ['тв_лист'])TVP_HIST = {}def tv_search(t, s, p, kk=None):        global URLTV                jid = get_true_jid(s)                if not p: return        c = str()                if len(p)==1 and p.isdigit():                if jid in TVP_HIST.keys():                        c='&p='+p                        p=TVP_HIST[jid]        else:                TVP_HIST[jid]=p        pp = p        nurl = str()        h = None        p = urllib.urlencode({'text':p.encode('utf8')})                url = URLTV+('213' if not kk else '187')+'/search?'+p+c        #req = urllib2.Request(url)        #req.add_header('User-Agent', UserAgent().random)        r = TV.open(url, p).read()#urllib2.urlopen(req).read()        try:                if r.count('window.location.replace'):                        ###'Redirect'                        nurl = re.findall(r'href=[\'"]?([^\'" >]+)', r)[0]                        h = HTMLParser.HTMLParser()                        nurl = h.unescape(nurl)                        if nurl.count('ua'):                                URLTV = base64.b64decode('aHR0cDovL20udHYueWFuZGV4LnVhLw==')                        r = TV.open(nurl).read()        except: pass                r = r.replace('</div>','\n')                #r = re.findall('по телепрограмме</[a-zA-Z0-9_]{2,}>(.*?)Все сервисы', r, re.DOTALL | re.IGNORECASE)        #if r:        #        r=r[0]        #else:        #        reply(t, s, u'По запросу результатов нету!')        #        return        i = r.split('Все сервисы')        if i:                r = i[0]                        if r.count('предыдущая</i>'):                r = re.compile(r'предыдущая.*?$',re.DOTALL | re.IGNORECASE).sub(('--> твп 2 чтобы читать дальше' if not c else ''), r)                r = r.replace('</a>','\n')        d = universal_html_parser(r)        reply(t, s, (d if d else u'Поиск недал результатов'))register_command_handler(tv_search, 'твп', ['фан','все'], 0, 'Поиск фильмов и предач в телепрограмме (by '+URLTV+')', 'твп <передача>', ['твп хобости','твп новости 2'])