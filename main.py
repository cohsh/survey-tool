#!/usr/bin/env python3
# -*- coding: utf8 -*-
import tkinter
import os
from crossref.restful import Works

doi = ''

labels = {}
inputs = {}
words = {}
texts = {'title': 'Title', \
        'author': 'Authors', \
        'what': 'What is this?', \
        'excellent': 'Excellent points compared to previous studies', \
        'core': 'Core of Methods', \
        'validation': 'Validation', \
        'discussion': 'Discussion', \
        'next': 'Read next'}

font = 'Source Code Pro'

pt2px = 4.0 / 3.0

font_size_small = 12
font_size_big = 16

small_font = (font, font_size_small)
big_font = (font, font_size_big)

size = [400, 600]
space = int(font_size_big)

def main():
    global labels, inputs
    y0 = 0

    root = tkinter.Tk()
    root.title('Survey Tool')

    subtitle = tkinter.Label(text='Survey Tool', font=big_font)
    subtitle.place(x=0, y=y0)

    y0 += subtitle.winfo_reqheight()

    doi_label = tkinter.Label(text='DOI', font=small_font)
    doi_label.place(x=0, y=y0)

    y0 += doi_label.winfo_reqheight()

    doi_input = tkinter.Text(width=50, height=1, font=small_font)
    doi_input.place(x=0, y=y0)

    y0 += doi_input.winfo_reqheight()

    doi_btn = tkinter.Button(root, text='Get', command=lambda: get_paper(doi_input), font=small_font)
    doi_btn.place(x=0, y=y0)
    
    y0 += doi_btn.winfo_reqheight()

    for key in list(texts.keys()):
        labels[key] = tkinter.Label(text=texts[key], font=small_font)
        labels[key].place(x=0, y=y0)

        y0 += labels[key].winfo_reqheight()

        inputs[key] = tkinter.Text(width=50, height=3, font=small_font)
        inputs[key].place(x=0, y=y0)

        y0 += inputs[key].winfo_reqheight()

    btn_save = tkinter.Button(root, text='Save', command=lambda: save_text(words), font=small_font)
    btn_save.place(x=0, y=y0)
    
    y0 += btn_save.winfo_reqheight()

    root.geometry(str(doi_input.winfo_reqwidth())+'x'+str(int(y0)))

    root.state('normal')
    root.mainloop()

def get_paper(doi_input):
    global doi
    doi = doi_input.get(1.0, tkinter.END+'-1c')
    if (doi != ''):
        works = Works()
        paper = works.doi(doi)
        inputs['title'].insert(tkinter.END, paper['title'][0])
        doi = paper['DOI']

        for i in range(len(paper['author'])):
            inputs['author'].insert(tkinter.END, paper['author'][i]['given'])
            inputs['author'].insert(tkinter.END, ' ')
            inputs['author'].insert(tkinter.END, paper['author'][i]['family'])
            inputs['author'].insert(tkinter.END, ', ')
    else:
        pass


def save_text(info: dict):
    title = info.get('title', 'notitle')
    author = info.get('author', 'noname')
    what = info.get('what', 'nowhat')
    excellent = info.get('excellent', 'noexcellent')
    core = info.get('core', 'nocore')
    validation = info.get('validation', 'novalidation')
    discussion = info.get('discussion', 'nodiscussion')
    paper = info.get('next', 'nonext')

    nl = '\n\n'

    text = '# ' + title + nl + \
        '## ' + author + nl + \
        '### ' + texts['what'] + nl + \
        what + nl + \
        '### ' + texts['excellent'] + nl + \
        excellent + nl + \
        '### ' + texts['core'] + nl + \
        core + nl + \
        '### ' + texts['validation'] + nl + \
        validation + nl + \
        '### ' + texts['discussion'] + nl + \
        discussion + nl + \
        '### ' + texts['next'] + nl + \
        paper + nl

    md_file_name = doi + '.md'
    md_file_path = 'data/' + md_file_name
    file_path = os.path.dirname(md_file_path)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(md_file_path, 'w') as file:
        file.write(text)

if __name__ == '__main__':
    main()
