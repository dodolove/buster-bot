# -*- coding: utf-8 -*-

USER_PING_FILE = 'dynamic/user_ping.txt'

initialize_file(USER_PING_FILE, '{}')

TURBO_PING = {}

def hnd_turboping(t, s, p):
    global TURBO_PING
    
    if s[0].isdigit():
        reply(t, s, u'Only for Jabber protocol!')
        return
    jid = s[1]+'/'+s[2]
    if p:
        if s[1] in GROUPCHATS and p in GROUPCHATS[s[1]]:
            jid = s[1]+'/'+p
        else:
            jid = p

    TURBO_PING[jid]=[]
    reply(t, s, u'Тестирование начато..')
    for x in range(10):
        packet = IQ(CLIENTS[s[3]], 'get')
        packet.addElement('query', 'jabber:iq:version')
        packet.addCallback(turboping_handler, jid, time.time())
        reactor.callFromThread(packet.send, jid)
        time.sleep(6)
    tt=time.time()
    while not len(TURBO_PING[jid])!=9:
        if time.time()-tt<160:
            time.sleep(1)
            pass
        break
    if len(TURBO_PING[jid])<3:
        reply(t, s, u'Понг хреновый, либо адрес указан неверно!Часть пакетов утеряна!')
        return
    l = getMedian(TURBO_PING[jid])
    reply(t, s, u'Минимальное время '+str(min(TURBO_PING[jid]))+u' секунд, макс. '+str(max(TURBO_PING[jid]))+u' секунд.\nВ среднем, из '+str(len(TURBO_PING[jid]))+u' отправленных пакетов понг составляет '+str(l)+u' секунд.')

register_command_handler(hnd_turboping, 'турбопинг', ['все'], 0, 'Проверяет пинг указаного адреса в течении минуты, выводит медиану, максимальное и минимально значение.', 'турбопинг', ['турбопинг'])

def turboping_handler(jid, i, x):
    if x['type'] == 'result':
        t = time.time()
        TURBO_PING[jid].append(round(t-i, 3))


def getMedian(numericValues):
    theValues = sorted(numericValues)
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        lower = theValues[len(theValues)/2-1]
        upper = theValues[len(theValues)/2]
    return (float(lower + upper)) / 2
    
        

def ping_handler(t, s, p):
    if s[0].isdigit():
        reply(t, s, u'Понг')
        return
    jid = s[1]+'/'+s[2]
    if p:
        if s[1] in GROUPCHATS and p in GROUPCHATS[s[1]]:
            jid = s[1]+'/'+p
        else:
            jid = p
    packet = IQ(CLIENTS[s[3]], 'get')
    packet.addElement('query', 'jabber:iq:version')
    packet.addCallback(ping_result_handler, t, s, p, time.time())
    reactor.callFromThread(packet.send, jid)

def ping_result_handler(type, s, p, i, x):
    add=''
    ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
    if x['type'] == 'error':
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: code = []
        if ' '.join(code) in ERROR: add=ERROR[' '.join(code)]
        reply(type, s, u'Не пингуется. '+' '.join(code)+' '+add)
        return
    elif x['type'] == 'result':
        t = time.time()
        rep = u'понг от '
	if p:
            rep += p
	else:
            rep += u'тебя'
	rep+=u' '+str(round(t-i, 3))+u' секунд'
        reply(type, s, rep)


def time_handler(t, s, p):
    jid = s[1]+'/'+s[2]
    if p: jid = p
    if s[1] in GROUPCHATS and p:
        if p in GROUPCHATS[s[1]]:
            jid=s[1]+'/'+p
        else:
            jid=p
    packet = IQ(CLIENTS[s[3]], 'get')
    packet.addElement('query', 'jabber:iq:time')
    packet.addCallback(time_result_handler, t, s, p)
    reactor.callFromThread(packet.send, jid)

def time_result_handler(t, s, p, x):
    try:
        query = element2dict(x)['query']
        display = element2dict(query)['display']
        reply(t, s, display.children[0])
    except:
        urnxmpptime(t, s, p)


def urnxmpptime(t, s, p):
    jid = s[1]+'/'+s[2]
    if p: jid = p
    if s[1] in GROUPCHATS and p:
        if p in GROUPCHATS[s[1]]:
            jid=s[1]+'/'+p
        else:
            jid=p
    packet = IQ(CLIENTS[s[3]], 'get')
    packet.addElement('time', 'urn:xmpp:time')
    packet.addCallback(timenew_result, t, s, p)
    reactor.callFromThread(packet.send, jid)


def getTag(element,name,xmlns = None):
	for el in element.elements():
		if not isinstance(el,basestring) and el.name == name:
			if xmlns and el.uri == xmlns:
				return el
			return el
	return None

def getTags(element,name,xmlns=None):
	if xmlns is None:
		filtAlg = lambda el : not isinstance(el,basestring) and el.name == name
	else:
		filtAlg = lambda el : not isinstance(el,basestring) and el.name == name and el.uri == xmlns
	result = filter(filtAlg,element.elements())
	return (result if result else None)

def timenew_result(t, s, p, x):
    try:
        tzo, utc, dt2 = '','',0

        
        if x['type']=='error':
            reply(t, s, u'На urn:xmpp:time сервис ответил ошибкой!')
            return
        
        fmt = '%Y-%m-%d %H:%M:%S'

        try:
            tzo = getTag(x.children[0],'tzo')
            utc = getTag(x.children[0],'utc')
        except:
            query = element2dict(x)['time']
            tzo = element2dict(query)['tzo']
            utc = element2dict(query)['utc']

        tzo, utc = tzo.children[0], utc.children[0]

        utc = utc.replace('T',' ').replace('Z','')
        if utc.count('.'): utc = utc.split('.')[0]

        ss = tzo[1:].split(':')
        h = int(ss[0])
        m = int(ss[1])
        import datetime
        if tzo[:1] in ['-']:
            try: dt2 = datetime.datetime(*time.strptime(utc, fmt)[:6])-datetime.timedelta(hours=h, minutes=m)
            except: dt2 = 0
        if tzo[:1] in ['+']:
            try: dt2 = datetime.datetime(*time.strptime(utc, fmt)[:6])+datetime.timedelta(hours=h, minutes=m)
            except: dt2 = 0
        reply(t, s, u'Часовой пояс '+tzo+u' Время по Гринвичу '+utc+u' На экране '+str(dt2))
    except:
        reply(t, s, u'Невозможно определить время!')


def disco_handler(t, s, p):
    if p:
        if p.count(' '):
            n = p.split()
            p, grep = n[0], n[1]
        else:
            p, grep = p, ' '
        if not p.count('.'):
            p=p+'@conference.jabber.ru'
        packet = IQ(CLIENTS[s[3]], 'get')
        packet.addElement('query', 'http://jabber.org/protocol/disco#items')
        packet.addCallback(disco_result_handler_a, t, s, p, grep)
        reactor.callFromThread(packet.send, p)
    else: reply(t, s, u'и?')

def disco_result_handler_a(t, s, p, grep, x):
    if x['type'] == 'result':
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        if p.count('conference.') or p.count('chat.') or p.count('muc.'):
            if p.count('@'):
                r = [i.get('name') for i in query]
                r.sort()
            else:
                r = []
                for i in query:
                    try: g = re.search('^(.+)\(([0-9]+)\)$', i['name']).groups()
                    except: g = (i['name'], '0')
                    if int(g[1]) < 99: r.append((g[0], i['jid'], g[1]))
                r.sort(lambda x, y: cmp(int(y[2]), int(x[2])))
                r = ['%s - %s (%s)' % i for i in r]
        else:
            r = [i['jid'] for i in query]
            r.sort()
        if r: reply(t, s, u'Надискаверил:\n'+show_list(r, grep))
        else: reply(t, s, u'Пустое диско!')
    elif x['type'] == 'error':
        code, add = [], ''
        ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: pass
        if ''.join(code) in ERROR: add=ERROR[' '.join(code)]
        reply(t, s, u'Не дискаверится. '+' '.join(code)+' '+add)
        return

def show_list(seq, grep=None, empty='[empty list]'):
 if len(seq) == 1: return seq[0]
 else:
  r = ''
  for i in range(len(seq)):
   r += '%s) %s\n' % (i+1, seq[i])
  if grep: r = '\n'.join([i for i in r.split('\n') if i.lower().count(grep.lower())])
  if not r: r = empty
  return r

USER_PING = {}

def join_user_ping(g, n, r, a, cljid):
    global USER_PING
    if not g in USER_PING or not g in GROUPCHATS or get_bot_nick(g)==n:
        return
    if 'timel' in USER_PING[g] and 'limit' in USER_PING[g] and 'now' in USER_PING[g]:
        if time.time() - USER_PING[g]['timel']<60:
            USER_PING[g]['now']+=1
            USER_PING[g]['timel'] = time.time()
            if USER_PING[g]['now']>USER_PING[g]['limit']:
                if a in ['participant']:
                    room_access(cljid, g, 'role', 'visitor', 'nick', n)
                return
        USER_PING[g]['timel'] = time.time()
        if USER_PING[g]['now']!=0: USER_PING[g]['now'] = 0
    jid=g+'/'+n
    if a in ['participant','visitor']:
        if a==u'participant':
            room_access(cljid, g, 'role', 'visitor', 'nick', n)
        packet = IQ(CLIENTS[cljid], 'get')
        packet.addElement('query', 'jabber:iq:version')
        packet.addCallback(user_ping_result, g, n, cljid)
        reactor.callFromThread(packet.send, jid)

def user_ping_result(g, n, cljid, x):
    if x['type'] == 'result':
        if g in USER_PING:
            t = USER_PING[g].get('timer',3)
            time.sleep(t)
        room_access(cljid, g, 'role', 'participant', 'nick', n)

def user_ping_init(cljid):
    try: db = eval(read_file(USER_PING_FILE))
    except:
        write_file(USER_PING_FILE, '{}')
        db = {}
    global USER_PING
    USER_PING = db.copy()

def hnd_user_ping(t, s, p):
    if not s[1] in GROUPCHATS: return
    if not p:
        reply(t, s, u'Читай помощь по команде!')
        return
    if p=='0':
        if not s[1] in USER_PING:
            reply(t, s, u'уже отключено!')
            return
        del USER_PING[s[1]]
        write_file(USER_PING_FILE, str(USER_PING))
        reply(t, s, u'Отключил!')
        return
    if p=='1':
        if s[1] in USER_PING:
            reply(t, s, u'уже работает!')
            return
        USER_PING[s[1]]={'limit':0,'now':0,'timel':time.time()}
        write_file(USER_PING_FILE, str(USER_PING))
        reply(t, s, u'Теперь включено!')
        return
    if p.split() and p.split()[0] == u'лимит' and p.split()[1].isdigit():
        USER_PING[s[1]]={'limit':int(p.split()[1]),'now':0,'timel':time.time()}
        write_file(USER_PING_FILE, str(USER_PING))
        reply(t, s, u'Установлен лимит на выдачу войса '+p.split()[1]+u' юзеров в минуту!')
    if p.split() and p.split()[0] == u'таймер' and p.split()[1].isdigit():
        if not s[1] in USER_PING:
            USER_PING[s[1]]={}
        USER_PING[s[1]]['timer']=int(p.split()[1])
        write_file(USER_PING_FILE, str(USER_PING))
        reply(t, s, u'ok!')

register_join_handler(join_user_ping)
register_stage0_init(user_ping_init)
register_command_handler(urnxmpptime, 'time', ['все'], 0, 'Показывает время юзая XEP-0202 (urn:xmpp:time)', 'time ник', ['time вася'])
register_command_handler(hnd_user_ping, 'юзер_пинг', ['все'], 20, 'Пингует вошедшего юзера, и только после ответа клиента выдает голос. Команда может использоваться против примитивных спам-ботов. Для установки лимита на количество выдачи голосов за минут используем ключ команды <лимит> <число>; Для установки таймера выдачи голоса вошедшим после ответа их клиента используем ключ <таймер> <секунды>', 'юзер_пинг <0|1|лимит>', ['юзер_пинг 1','юзер_пинг лимит 1'])
register_command_handler(disco_handler, 'диско', ['все'], 0, 'Дискаверит конференцию или сервер.', 'диско чат', ['диско cool@conference.talkonaut.com'])
register_command_handler(time_handler, 'часики', ['все'], 0, 'часики', 'часики ник', ['часики вася'])
register_command_handler(ping_handler, 'пинг', ['все'], 0, 'пинг', 'пинг', ['пинг'])
