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

font_big = {'name': 'Source Code Pro', 'size': 24}
font_small = {'name': 'Source Code Pro', 'size': 12}
size = [400, 600]
space = int(size[0]*0.02)

y0 = 0

def main():
    global labels, inputs

    root = tkinter.Tk()
    root.geometry(str(size[0])+'x'+str(size[1]))
    root.title('Survey Tool')

    subtitle = tkinter.Label(text='Survey Tool', font=(font_big['name'], font_big['size']))
    subtitle.place(x=0, y=y0)

    add_spacing(2)

    doi_label = tkinter.Label(text='DOI', font=(font_small['name'], font_small['size']))
    doi_label.place(x=0, y=y0)

    add_spacing(1)

    doi_input = tkinter.Text(width=50, height=1, font=(font_small['name'], font_small['size']))
    doi_input.place(x=0, y=y0)

    add_spacing(1)

    doi_btn = tkinter.Button(root, text='Get', command=lambda: get_paper(doi_input), font=(font_small['name'], font_small['size']))
    doi_btn.place(x=0, y=y0)
    
    add_spacing(1)

    for key in list(texts.keys()):
        labels[key] = tkinter.Label(text=texts[key], font=(font_small['name'], font_small['size']))
        labels[key].place(x=0, y=y0)

        add_spacing(1)

        inputs[key] = tkinter.Text(width=50, height=3, font=(font_small['name'], font_small['size']))
        inputs[key].place(x=0, y=y0)

        add_spacing(3)

    btn_save = tkinter.Button(root, text='Save', command=lambda: save_text(words), font=(font_small['name'], font_small['size']))
    btn_save.place(x=0, y=y0)

    root.state('normal')
    root.mainloop()

def add_spacing(n):
    global y0
    for i in range(n):
        y0 += space

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
