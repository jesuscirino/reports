# -*- coding: utf-8 -*-
import pickle
import argparse
import os
import shutil
import datetime
import re
from os import walk, getcwd, path, scandir
import asyncio
#import steem
import time
#nodes = ['https://gtg.steem.house:8090','https://seed.bitcoiner.me']
#s = steem.Steem(nodes, keys=['PK_de_lince'])


TIMEFORMAT = '%Y-%m-%d-%H-%M-%S'

def get_list_files_with(pattern):
    p         = re.compile(pattern)
    route     = getcwd()
    return [f.name for f in scandir(route) if f.is_file() and p.match(f.name)]
def get_reason(text=''):
    """Return [str] key reason found it in a string parameter [text]"""
    p_tag_abuse          = re.compile(r'\*\*tag\s+abuse\s*', re.I)
    p_content_abuse      = re.compile(r'\*\*content\s+abuse\s*', re.I)
    p_plagio             = re.compile(r'\*\*plagiarism\s*', re.I)
    p_copy_paste         = re.compile(r'\*\*copy\s?\/?\s?paste\s*', re.I)
    p_photo              = re.compile(r'\*\*photoplagiarism\s*', re.I)
    p_spam               = re.compile(r'\*\*spam\s*', re.I)
    if p_tag_abuse.search(text):
        return 'Tag Abuse'
    elif p_content_abuse.search(text):
        return 'Content Abuse'
    elif p_plagio.search(text):
        return 'Plagiarism'
    elif p_copy_paste.search(text):
        return 'Copy Paste'
    elif p_photo.search(text):
        return 'Photoplagiarism'
    elif p_spam.search(text):
        return 'Spam'
    else:
        return 'None'
        
def dump_history(name_raw_file):
    """Use this function after of lince bot exec get_reports
    with discord bot load from id comment on any FILE"""
    now_file      = datetime.datetime.now()
    now_file      = str(now_file.strftime(TIMEFORMAT))+'.linc'
    pattern_linc  = r'^.*\.linc$'
    dic_b         = {}
    list_linc     = get_list_files_with(pattern_linc)
    print(list_linc)
    if list_linc:
        newest   = max(list_linc) 
        shutil.copy(newest, now_file)
        with open(now_file, 'rb') as f:
            dic_b = pickle.load(f) 
        print ('hay linces')
    with open(name_raw_file, 'r+') as f:
        p = re.compile(r'([\w\s]+\d+\/\d+\/\d+\s)?(\d+\))',re.I)
        for line in f:
            if p.match(line):
                lis   = line.split()
                date  = lis[-1]
                lince = lis[-2]
                lis   = [x for x in lis if 'http' in x]
                for x in lis:
                    x = x.strip('<')
                    x = x.strip('>')
                list_urls = [x for x in lis if 'http' in x]
                try:
                    post  = list_urls[0]
                except Exception as e:
                    print(e)
                    print('linea 76 alguien reportó mal')
                if post in dic_b.keys():
                    pass
                else:
                    dic_b[post] = {}
                    dic_b[post]['date']  = date
                    dic_b[post]['lince'] = lince
                    dic_b[post]['proof'] = list_urls[1:]
                    reason               = get_reason(line) 
                    dic_b[post]['reason']= reason
        with open(now_file,'wb') as f:
            pickle.dump(dic_b, f)

'''def comment(init, top):
    """broadcast comments to post in lince reports"""
    if len(init) < 9:
        init          = '20' + init + '-00-00-00'
    if len(top) < 9:
        top           = '20' + top  + '-23-59-59'

    pattern_linc  = r'^.*\.linc$'
    list_linc     = get_list_files_with(pattern_linc)
    newest        = max(list_linc) 
    dic_b         = {}
    list_post     = []
    with open(newest, 'rb') as f:
        dic_b = pickle.load(f)
    for p in dic_b.keys():
        t = dic_b[p]['date']
        if t >= init  and t <= top:
            print(dic_b[p]['date'])
            print(p)
            if dic_b[p]['reason'] == 'Tag Abuse':
                body = """Recomendación, usa el tag spanish cuando el contenido sea escrito de manera parcial o total en español, el tag steem cuando tu publicación habla de la criptomoneda, el tag steemit cuando hables de la plataforma, el tag introduceyourself para tu primer publicación en la que te presentas y el tag photography cuando las fotografías sean de tu propiedad. Todo esto es para evitar publicar contenido clasificado como plagio o abuso en el futuro.
                
Steemit es una plataforma en la que se recompensa el trabajo original y propio. Si existe alguna duda sobre cómo puedes evitar el plagio y abuso favor de leer las publicaciones informativas de @lince.
                
Para cualquier aclaración los medios de comunicación son por correo a lince.steemit@gmail.com o en los chats de discord y steemit.chat"""
            elif dic_b[p]['reason'] == 'Photoplagiarism':
                try:
                    body = """Te sugerimos leer la siguiente publicación para evitar publicar contenido clasificado como plagio o abuso en el futuro: [Plagio de imágenes, ¿cómo evitarlo?](https://steemit.com/lince/@lince/por-que-debemos-incluir-las-fuentes-de-las-imagenes-que-tomamos-de-internet).

No tiene nada de malo apoyarse de contenido de internet, solo procura citar la fuente de donde se obtuvo la imagen o fotografía, que en este caso se encuentra [Aquí](""" +dic_b[p]['proof'][0]+""").

Esto no es una bandera, es una recomendación para que leas el post de @lince y en el futuro evites cometer algún tipo de abuso.
                    
Steemit es una plataforma en la que se recompensa el trabajo original y propio. Si existe alguna duda sobre cómo puedes evitar el plagio y abuso favor de leer las publicaciones informativas de @lince.
                    
Para cualquier aclaración los medios de comunicación son por correo a lince.steemit@gmail.com o en los chats de discord y steemit.chat"""
                except:
                    body = """Te sugerimos leer la siguiente publicación para evitar publicar contenido clasificado como plagio o abuso en el futuro: [Plagio textual, parcial o total de contenido ajeno](https://steemit.com/spanish/@lince/diferencia-entre-plagiar-y-usar-contenido-de-internet-aprende-la-diferencia).
                
No tiene nada de malo apoyarse de contenido de internet, solo procura citar la fuente de donde se obtuvo la información, que en este caso se encuentra [Aquí](""" +'google.com'+""").

Esto no es una bandera, es una recomendación para que leas el post de @lince y en el futuro evites cometer algún tipo de abuso.
                
Steemit es una plataforma en la que se recompensa el trabajo original y propio. Si existe alguna duda sobre cómo puedes evitar el plagio y abuso favor de leer las publicaciones informativas de @lince.

Para cualquier aclaración los medios de comunicación son por correo a lince.steemit@gmail.com o en los chats de discord y steemit.chat.
                """


            elif dic_b[p]["reason"] == "Plagiarism":
                try:
                    body = """Te sugerimos leer la siguiente publicación para evitar publicar contenido clasificado como plagio o abuso en el futuro: [Plagio textual, parcial o total de contenido ajeno](https://steemit.com/spanish/@lince/diferencia-entre-plagiar-y-usar-contenido-de-internet-aprende-la-diferencia).
                
No tiene nada de malo apoyarse de contenido de internet, solo procura citar la fuente de donde se obtuvo la información, que en este caso se encuentra [Aquí](""" +dic_b[p]["proof"][0]+""").

Esto no es una bandera, es una recomendación para que leas el post de @lince y en el futuro evites cometer algún tipo de abuso.
                
Steemit es una plataforma en la que se recompensa el trabajo original y propio. Si existe alguna duda sobre cómo puedes evitar el plagio y abuso favor de leer las publicaciones informativas de @lince.

Para cualquier aclaración los medios de comunicación son por correo a lince.steemit@gmail.com o en los chats de discord y steemit.chat.
                """
                except:
                     body = """Te sugerimos leer la siguiente publicación para evitar publicar contenido clasificado como plagio o abuso en el futuro: [Plagio textual, parcial o total de contenido ajeno](https://steemit.com/spanish/@lince/diferencia-entre-plagiar-y-usar-contenido-de-internet-aprende-la-diferencia).
                
No tiene nada de malo apoyarse de contenido de internet, solo procura citar la fuente de donde se obtuvo la información, que en este caso se encuentra [Aquí](""" +"google.com"+""").

Esto no es una bandera, es una recomendación para que leas el post de @lince y en el futuro evites cometer algún tipo de abuso.
                
Steemit es una plataforma en la que se recompensa el trabajo original y propio. Si existe alguna duda sobre cómo puedes evitar el plagio y abuso favor de leer las publicaciones informativas de @lince.

Para cualquier aclaración los medios de comunicación son por correo a lince.steemit@gmail.com o en los chats de discord y steemit.chat.
                """

            elif dic_b[p]['reason'] == 'Copy Paste':
                body = """El contenido de esta publicación puede estar relacionada con algún tipo de plagio o abuso relacionado con Plagio total o parcial de contenido ajeno. Te sugerimos leer la siguiente publicación para evitar publicar contenido clasificado como plagio o abuso en el futuro: [Plagio textual, parcial o total de contenido ajeno](https://steemit.com/spanish/@lince/diferencia-entre-plagiar-y-usar-contenido-de-internet-aprende-la-diferencia).
                
No tiene nada de malo apoyarse de contenido de internet, solo procura citar la fuente de donde se obtuvo la información, que en este caso se encuentra [Aquí](""" +dic_b[p]['proof'][0]+""").

Esto no es una bandera, es una recomendación para que leas el post de @lince y en el futuro evites cometer algún tipo de abuso.
                
Steemit es una plataforma en la que se recompensa el trabajo original y propio. Si existe alguna duda sobre cómo puedes evitar el plagio y abuso favor de leer las publicaciones informativas de @lince.

Para cualquier aclaración los medios de comunicación son por correo a lince.steemit@gmail.com o en los chats de discord y steemit.chat."""
            post = steem.post.Post(p, s)
            s.commit.post('',body,'lince', reply_identifier=post.identifier)
            print(body)
            print('xx'*10)
            time.sleep(30)
            '''
def get_body(init, top):
    """return a report with markdown format for steemit"""
    init          = '20' + init + '-00-00-00'
    top           = '20' + top  + '-23-59-59'
    pattern_linc  = r'^.*\.linc$'
    list_linc     = get_list_files_with(pattern_linc)
    newest        = max(list_linc) 
    dic_b         = {}
    body          = 'Autor/Author|Post|Acción/Action|Razón/Reason\n' + \
                    '--- | --- | --- | ---'
    with open(newest, 'rb') as f:
        dic_b = pickle.load(f)
    for p in dic_b.keys():
        t = dic_b[p]['date']
        if t >= init  and t <= top:
            #revisar links incompletos
            #print (p.split('/')[3]) 
            try:
                body = body + '\n' + '[Usuario](steemit.com/' + p.split('/')[4] + \
                        ')|[Post](' + p +')|Sugerencia|' + \
                        dic_b[p]['reason']
            #print(dic_b[p]['date'])
            except Exception as e:
                print(e)
    return body
def say(t):
    return t

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="set a file with discord messages from lincers", type=str)
    parser.add_argument("-b", "--body", help="show a body for a per dates init and top\
                            example: 17-12-30 -t 17-12-31", type=str)
    parser.add_argument("-t", "--top", help="set a top date \
                            example: -t 17-12-31", type=str)
    parser.add_argument("-c", "--commenter", help="broadcast steemit comments\
                            example: 17-12-30 -t 17-12-31", type=str)
    args   = parser.parse_args()
    FILE   = args.file
    BODY   = args.body
    TOP    = args.top
    COMM   = args.commenter
    if FILE:
        print("dumping lince history with {}...".format(FILE))
        dump_history(FILE)
        print("Done ok.")
    elif BODY:
        if TOP:
            print(get_body(BODY, TOP))
        else:
            print(get_body(BODY, BODY))
    elif COMM:
        if TOP:
            comment(COMM, TOP)
        else:
            comment(COMM, COMM)
