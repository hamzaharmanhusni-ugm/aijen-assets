# Aijen Slide Kit - pembangun deck materi via Google Slides API (Composio).
# Layout L1-L10 menghasilkan list request batchUpdate per slide. Brand konsisten otomatis.
# Dipakai di sandbox Composio: exec(requests.get(RAW_KIT).text); build_deck(title, spec)
# Geometri 16:9 = 720 x 405 pt. ObjectId minimal 5 karakter.

# ---- brand ----
TEAL       = {'red':0.1098,'green':0.3294,'blue':0.2941}  # 1c544b
TEAL_LIGHT = {'red':0.4353,'green':0.6549,'blue':0.6157}  # 6fa79d
GREEN      = {'red':0.0863,'green':0.3412,'blue':0.1922}  # 165731
GREY       = {'red':0.3569,'green':0.4196,'blue':0.4314}  # 5B6B6E
WHITE      = {'red':1,'green':1,'blue':1}
CARD       = {'red':0.914,'green':0.945,'blue':0.937}     # e9f1ef
MUTED      = {'red':0.70,'green':0.74,'blue':0.73}
DOT_OFF    = {'red':0.83,'green':0.87,'blue':0.86}

HEAD = 'Poppins'
BODY = 'Roboto'

_RAW = 'https://raw.githubusercontent.com/hamzaharmanhusni-ugm/aijen-assets/main/logo/'
FULL_C = _RAW + 'aijen-logo-full.png'
FULL_W = _RAW + 'aijen-logo-full-white.png'
ICON_W = _RAW + 'aijen-icon-white.png'
WM     = _RAW + 'aijen-icon-white-faint.png'

DEFFOOT   = 'Kelas Implementasi AI & Automation   ·   Aijen'
HONESTFOOT = DEFFOOT + '   ·   contoh, bukan janji hasil'

# ---- primitif ----
def _box(o, pg, x, y, w, h, sh='TEXT_BOX'):
    return {'createShape': {'objectId': o, 'shapeType': sh, 'elementProperties': {'pageObjectId': pg,
        'size': {'width': {'magnitude': w, 'unit': 'PT'}, 'height': {'magnitude': h, 'unit': 'PT'}},
        'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': x, 'translateY': y, 'unit': 'PT'}}}}

def _img(o, pg, url, x, y, w, h):
    return {'createImage': {'objectId': o, 'url': url, 'elementProperties': {'pageObjectId': pg,
        'size': {'width': {'magnitude': w, 'unit': 'PT'}, 'height': {'magnitude': h, 'unit': 'PT'}},
        'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': x, 'translateY': y, 'unit': 'PT'}}}}

def _fill(o, c):
    return {'updateShapeProperties': {'objectId': o, 'shapeProperties': {
        'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': c}}}, 'outline': {'propertyState': 'NOT_RENDERED'}},
        'fields': 'shapeBackgroundFill.solidFill.color,outline.propertyState'}}

def _ins(o, t):
    return {'insertText': {'objectId': o, 'insertionIndex': 0, 'text': t}}

def _sty(o, sz, c, b=False, font=HEAD):
    return {'updateTextStyle': {'objectId': o, 'textRange': {'type': 'ALL'},
        'style': {'fontFamily': font, 'fontSize': {'magnitude': sz, 'unit': 'PT'}, 'bold': b,
                  'foregroundColor': {'opaqueColor': {'rgbColor': c}}},
        'fields': 'fontFamily,fontSize,bold,foregroundColor'}}

def _para(o, al='START', ls=None):
    st = {'alignment': al}; f = 'alignment'
    if ls: st['lineSpacing'] = ls; f += ',lineSpacing'
    return {'updateParagraphStyle': {'objectId': o, 'textRange': {'type': 'ALL'}, 'style': st, 'fields': f}}

def _vmid(o):
    return {'updateShapeProperties': {'objectId': o, 'shapeProperties': {'contentAlignment': 'MIDDLE'}, 'fields': 'contentAlignment'}}

def _bg(pg, c):
    return {'updatePageProperties': {'objectId': pg, 'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': c}}}}, 'fields': 'pageBackgroundFill.solidFill.color'}}

# ---- potongan brand ----
def _accent(pg, k, x=46, y=84, w=56, h=5):
    return [_box(k+'_ac', pg, x, y, w, h, 'RECTANGLE'), _fill(k+'_ac', TEAL_LIGHT)]

def _topband(pg, k, label):
    return [_box(k+'_bd', pg, 0, 0, 720, 52, 'RECTANGLE'), _fill(k+'_bd', TEAL),
            _img(k+'_ic', pg, ICON_W, 24, 14, 24, 24),
            _box(k+'_lb', pg, 58, 15, 600, 24), _ins(k+'_lb', label), _sty(k+'_lb', 13, WHITE, True, HEAD)]

def _footer(pg, k, text, on_dark=False):
    col = TEAL_LIGHT if on_dark else GREY
    return [_box(k+'_ft', pg, 46, 384, 640, 20), _ins(k+'_ft', text), _sty(k+'_ft', 10, col, False, BODY)]

# ---- L1 Cover ----
def cover(pg, k, title, subtitle='', mode='teal', footer='aijen.id   ·   Kelas Recording'):
    r = []
    if mode == 'teal':
        r += [_bg(pg, TEAL), _img(k+'_wm', pg, WM, 452, 150, 330, 330), _img(k+'_lo', pg, FULL_W, 52, 34, 118, 118)]
        tc, sc = WHITE, TEAL_LIGHT
    else:
        r += [_img(k+'_lo', pg, FULL_C, 52, 34, 118, 118)]
        tc, sc = TEAL, GREY
    r += _accent(pg, k, 60, 206, 66, 6)
    r += [_box(k+'_ti', pg, 58, 222, 600, 110), _ins(k+'_ti', title), _sty(k+'_ti', 38, tc, True, HEAD)]
    if subtitle:
        r += [_box(k+'_su', pg, 60, 316, 560, 30), _ins(k+'_su', subtitle), _sty(k+'_su', 16, sc, False, HEAD)]
    if mode == 'teal':
        r += [_box(k+'_ft', pg, 60, 378, 600, 22), _ins(k+'_ft', footer), _sty(k+'_ft', 10.5, TEAL_LIGHT, False, BODY)]
    else:
        r += [_box(k+'_fb', pg, 0, 386, 720, 19, 'RECTANGLE'), _fill(k+'_fb', TEAL),
              _box(k+'_ft', pg, 60, 388, 600, 15), _ins(k+'_ft', footer), _sty(k+'_ft', 9, WHITE, False, BODY)]
    return r

# ---- L2 Pembatas Bagian ----
def divider(pg, k, kicker, title, mode='teal'):
    r = [_bg(pg, TEAL), _img(k+'_wm', pg, WM, 470, 130, 360, 360)]
    r += [_box(k+'_ki', pg, 60, 150, 460, 24), _ins(k+'_ki', kicker), _sty(k+'_ki', 15, TEAL_LIGHT, True, HEAD)]
    r += _accent(pg, k, 60, 182, 66, 6)
    r += [_box(k+'_ti', pg, 58, 196, 560, 130), _ins(k+'_ti', title), _sty(k+'_ti', 40, WHITE, True, HEAD)]
    return r

# ---- L3 Gagasan ----
def idea(pg, k, text, kicker='', footer=DEFFOOT):
    r = []
    if kicker:
        r += [_box(k+'_ki', pg, 60, 70, 560, 24), _ins(k+'_ki', kicker), _sty(k+'_ki', 13, TEAL_LIGHT, True, HEAD)]
    r += _accent(pg, k, 60, 108, 66, 6)
    r += [_box(k+'_tx', pg, 58, 128, 600, 210), _ins(k+'_tx', text), _sty(k+'_tx', 30, TEAL, True, HEAD), _para(k+'_tx', 'START', 130)]
    r += _footer(pg, k, footer)
    return r

# ---- L4 Daftar ----
def listing(pg, k, title, items, kicker='MODUL', footer=DEFFOOT):
    r = _topband(pg, k, kicker) + _accent(pg, k)
    r += [_box(k+'_ti', pg, 44, 94, 640, 44), _ins(k+'_ti', title), _sty(k+'_ti', 26, TEAL, True, HEAD)]
    body = '\n'.join('•  ' + it for it in items)
    r += [_box(k+'_bo', pg, 46, 158, 624, 200), _ins(k+'_bo', body), _sty(k+'_bo', 16, GREY, False, BODY), _para(k+'_bo', 'START', 200)]
    r += _footer(pg, k, footer)
    return r

# ---- L5 Kerangka 7 poin ----
def framework(pg, k, title, labels, active, kicker='KERANGKA USE CASE', footer=DEFFOOT):
    r = _topband(pg, k, kicker) + _accent(pg, k)
    r += [_box(k+'_ti', pg, 44, 94, 640, 40), _ins(k+'_ti', title), _sty(k+'_ti', 23, TEAL, True, HEAD)]
    y = 150
    for i, lb in enumerate(labels):
        o = k + '_p%d' % i
        on = (i == active)
        r += [_box(o+'d', pg, 46, y+5, 10, 10, 'RECTANGLE'), _fill(o+'d', TEAL_LIGHT if on else DOT_OFF)]
        r += [_box(o, pg, 66, y, 580, 24), _ins(o, ('%d. ' % (i+1)) + lb), _sty(o, 15, TEAL if on else MUTED, on, HEAD)]
        y += 33
    r += _footer(pg, k, footer)
    return r

# ---- L6 Angka / ROI ----
def number(pg, k, title, items, number, numlabel, kicker='MODUL', footer=HONESTFOOT):
    r = _topband(pg, k, kicker) + _accent(pg, k)
    r += [_box(k+'_ti', pg, 44, 94, 640, 44), _ins(k+'_ti', title), _sty(k+'_ti', 26, TEAL, True, HEAD)]
    body = '\n'.join('•  ' + it for it in items)
    r += [_box(k+'_bo', pg, 46, 160, 380, 200), _ins(k+'_bo', body), _sty(k+'_bo', 15, GREY, False, BODY), _para(k+'_bo', 'START', 180)]
    r += [_box(k+'_cd', pg, 452, 150, 232, 150, 'ROUND_RECTANGLE'), _fill(k+'_cd', CARD)]
    r += [_box(k+'_ca', pg, 474, 170, 40, 4, 'RECTANGLE'), _fill(k+'_ca', TEAL_LIGHT)]
    r += [_box(k+'_nu', pg, 470, 182, 200, 46), _ins(k+'_nu', number), _sty(k+'_nu', 34, GREEN, True, HEAD)]
    r += [_box(k+'_nl', pg, 472, 236, 200, 24), _ins(k+'_nl', numlabel), _sty(k+'_nl', 12, GREY, False, BODY)]
    r += _footer(pg, k, footer)
    return r

# ---- L7 Pagar / Risiko ----
def risk(pg, k, title, items, kicker='PAGAR & RISIKO', footer=DEFFOOT):
    r = _topband(pg, k, kicker)
    r += [_box(k+'_cd', pg, 46, 80, 628, 252, 'ROUND_RECTANGLE'), _fill(k+'_cd', TEAL)]
    r += [_box(k+'_bg', pg, 70, 104, 40, 40, 'ROUND_RECTANGLE'), _fill(k+'_bg', TEAL_LIGHT)]
    r += [_box(k+'_bx', pg, 70, 104, 40, 40), _ins(k+'_bx', '!'), _sty(k+'_bx', 22, TEAL, True, HEAD), _para(k+'_bx', 'CENTER'), _vmid(k+'_bx')]
    r += [_box(k+'_ti', pg, 124, 104, 528, 40), _ins(k+'_ti', title), _sty(k+'_ti', 23, WHITE, True, HEAD), _vmid(k+'_ti')]
    body = '\n'.join('•  ' + it for it in items)
    r += [_box(k+'_bo', pg, 72, 158, 560, 156), _ins(k+'_bo', body), _sty(k+'_bo', 15, WHITE, False, BODY), _para(k+'_bo', 'START', 180)]
    r += _footer(pg, k, footer)
    return r

# ---- L8 Diagram alur ----
def diagram(pg, k, title, steps, kicker='ALUR', footer=DEFFOOT):
    r = _topband(pg, k, kicker) + _accent(pg, k)
    r += [_box(k+'_ti', pg, 44, 94, 640, 44), _ins(k+'_ti', title), _sty(k+'_ti', 26, TEAL, True, HEAD)]
    n = len(steps); bw = 170
    gap = (720 - 2*46 - n*bw) / (n-1) if n > 1 else 0
    x = 46; y = 188
    for i, st in enumerate(steps):
        o = k + '_s%d' % i
        last = (i == n-1)
        r += [_box(o, pg, x, y, bw, 92, 'ROUND_RECTANGLE'), _fill(o, TEAL if last else CARD)]
        r += [_box(o+'t', pg, x+12, y, bw-24, 92), _ins(o+'t', st), _sty(o+'t', 16, WHITE if last else TEAL, True, HEAD), _para(o+'t', 'CENTER'), _vmid(o+'t')]
        if i < n-1:
            ax = x + bw + gap/2 - 11
            r += [_box(o+'a', pg, ax, y, 22, 92), _ins(o+'a', '→'), _sty(o+'a', 26, TEAL_LIGHT, True, HEAD), _para(o+'a', 'CENTER'), _vmid(o+'a')]
        x += bw + gap
    r += _footer(pg, k, footer)
    return r

# ---- L9 Rangkuman ----
def summary(pg, k, title, items, kicker='RANGKUMAN', footer=DEFFOOT):
    r = _topband(pg, k, kicker) + _accent(pg, k)
    r += [_box(k+'_ti', pg, 44, 94, 640, 44), _ins(k+'_ti', title), _sty(k+'_ti', 26, TEAL, True, HEAD)]
    y = 156
    for i, it in enumerate(items):
        o = k + '_n%d' % i
        r += [_box(o+'c', pg, 46, y, 30, 30, 'ROUND_RECTANGLE'), _fill(o+'c', CARD)]
        r += [_box(o+'cn', pg, 46, y, 30, 30), _ins(o+'cn', str(i+1)), _sty(o+'cn', 14, TEAL, True, HEAD), _para(o+'cn', 'CENTER'), _vmid(o+'cn')]
        r += [_box(o, pg, 88, y, 580, 30), _ins(o, it), _sty(o, 15, GREY, False, BODY), _vmid(o)]
        y += 44
    r += _footer(pg, k, footer)
    return r

# ---- L10 Langkah lanjut / Penutup (tawaran halus) ----
def closing(pg, k, title, sub='', cta='', mode='teal', footer=DEFFOOT):
    r = [_bg(pg, TEAL), _img(k+'_wm', pg, WM, 470, 130, 360, 360), _img(k+'_lo', pg, FULL_W, 52, 34, 110, 110)]
    r += _accent(pg, k, 60, 196, 66, 6)
    r += [_box(k+'_ti', pg, 58, 212, 600, 90), _ins(k+'_ti', title), _sty(k+'_ti', 34, WHITE, True, HEAD)]
    if sub:
        r += [_box(k+'_su', pg, 60, 300, 580, 40), _ins(k+'_su', sub), _sty(k+'_su', 16, TEAL_LIGHT, False, HEAD)]
    if cta:
        r += [_box(k+'_cb', pg, 60, 346, 320, 30, 'ROUND_RECTANGLE'), _fill(k+'_cb', TEAL_LIGHT)]
        r += [_box(k+'_ct', pg, 60, 346, 320, 30), _ins(k+'_ct', cta), _sty(k+'_ct', 13, TEAL, True, HEAD), _para(k+'_ct', 'CENTER'), _vmid(k+'_ct')]
    return r

# ---- placeholder gambar (diganti screenshot saat rekam) ----
def _ph(o, pg, x, y, w, h, label):
    r = [_box(o, pg, x, y, w, h, 'ROUND_RECTANGLE')]
    r += [{'updateShapeProperties': {'objectId': o, 'shapeProperties': {
        'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': {'red': 0.93, 'green': 0.95, 'blue': 0.95}}}},
        'outline': {'dashStyle': 'DASH', 'weight': {'magnitude': 1.5, 'unit': 'PT'},
                    'outlineFill': {'solidFill': {'color': {'rgbColor': TEAL_LIGHT}}}, 'propertyState': 'RENDERED'}},
        'fields': 'shapeBackgroundFill.solidFill.color,outline'}}]
    r += [_box(o+'t', pg, x+10, y, w-20, h), _ins(o+'t', '[ ganti dengan gambar ]\n' + label),
          _sty(o+'t', 12, GREY, False, BODY), _para(o+'t', 'CENTER'), _vmid(o+'t')]
    return r

# ---- L11 Layar penuh (screenshot) ----
def shot(pg, k, title, desc, kicker='MODUL', caption='', footer=DEFFOOT):
    r = _topband(pg, k, kicker) + _accent(pg, k)
    r += [_box(k+'_ti', pg, 44, 94, 640, 40), _ins(k+'_ti', title), _sty(k+'_ti', 24, TEAL, True, HEAD)]
    r += _ph(k+'_ph', pg, 46, 150, 628, 182, desc)
    if caption:
        r += [_box(k+'_cp', pg, 46, 338, 628, 22), _ins(k+'_cp', caption), _sty(k+'_cp', 12, GREY, False, BODY)]
    r += _footer(pg, k, footer)
    return r

# ---- L12 Split: teks + screenshot ----
def split(pg, k, title, items, desc, kicker='MODUL', footer=DEFFOOT):
    r = _topband(pg, k, kicker) + _accent(pg, k)
    r += [_box(k+'_ti', pg, 44, 94, 640, 40), _ins(k+'_ti', title), _sty(k+'_ti', 24, TEAL, True, HEAD)]
    body = '\n'.join('•  ' + it for it in items)
    r += [_box(k+'_bo', pg, 46, 158, 300, 188), _ins(k+'_bo', body), _sty(k+'_bo', 15, GREY, False, BODY), _para(k+'_bo', 'START', 180)]
    r += _ph(k+'_ph', pg, 366, 152, 308, 188, desc)
    r += _footer(pg, k, footer)
    return r

LAYOUTS = {'cover': cover, 'divider': divider, 'idea': idea, 'list': listing, 'framework': framework,
           'number': number, 'risk': risk, 'diagram': diagram, 'summary': summary, 'closing': closing,
           'shot': shot, 'split': split}

# ---- driver (perlu run_composio_tool dari sandbox) ----
def build_deck(title, spec):
    c, _ = run_composio_tool(tool_slug='GOOGLESLIDES_CREATE_PRESENTATION', arguments={'title': title,
        'pageSize': {'width': {'unit': 'EMU', 'magnitude': 9144000}, 'height': {'unit': 'EMU', 'magnitude': 5143500}}})
    d = c.get('data', {}); d = d.get('data', d); pid = d.get('presentationId')
    g, _ = run_composio_tool(tool_slug='GOOGLESLIDES_PRESENTATIONS_GET', arguments={'presentationId': pid, 'fields': 'slides(objectId,pageElements(objectId))'})
    gd = g.get('data', {}); gd = gd.get('data', gd); s0 = gd['slides'][0]; page1 = s0['objectId']
    reqs = [{'deleteObject': {'objectId': e['objectId']}} for e in s0.get('pageElements', [])]
    pages = []
    for i, sp in enumerate(spec):
        if i == 0:
            pg = page1
        else:
            pg = 'sld%02dp' % (i+1)
            reqs += [{'createSlide': {'objectId': pg, 'insertionIndex': i, 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}}]
        pages.append(pg)
        args = dict(sp.get('args', {}))
        if 'mode' in sp:
            args['mode'] = sp['mode']
        reqs += LAYOUTS[sp['layout']](pg, 's%02d' % (i+1), **args)
    res, err = run_composio_tool(tool_slug='GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE', arguments={'presentationId': pid, 'requests': reqs})
    return {'presentationId': pid, 'pages': pages, 'n': len(reqs), 'error': err}

def thumbs(pid, pages):
    out = []
    for p in pages:
        t, _ = run_composio_tool(tool_slug='GOOGLESLIDES_GET_PAGE_THUMBNAIL2', arguments={'presentationId': pid, 'pageObjectId': p, 'thumbnailProperties': {'mimeType': 'PNG', 'thumbnailSize': 'LARGE'}})
        dd = t.get('data', {}); dd = dd.get('data', dd)
        out.append(dd.get('contentUrl'))
    return out
