#!/usr/bin/env python3
# -*- coding: utf8 -*-
import tkinter
import os
from crossref.restful import Works

texts = {'title': 'Title', \
        'author': 'Authors', \
        'what': 'What is this?', \
        'excellent': 'Excellent points compared to previous studies', \
        'core': 'Core of Methods', \
        'validation': 'Validation', \
        'discussion': 'Discussion', \
        'next': 'Read next'}

inputs = {}

font = 'Source Code Pro'

font_size_small = 12
font_size_big = 16

small_font = (font, font_size_small)
big_font = (font, font_size_big)

def main():
    global inputs
    labels ={}
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

    btn_save = tkinter.Button(root, text='Save', command=lambda: save_text(inputs), font=small_font)
    btn_save.place(x=0, y=y0)
    
    y0 += btn_save.winfo_reqheight()

    root.geometry(str(doi_input.winfo_reqwidth())+'x'+str(int(y0)))

    root.state('normal')
    root.mainloop()

def get_paper(doi_input: tkinter.Text):
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


def save_text(inputs: dict[tkinter.Text]):
    nl = '\n\n'

    output_text = ''

    for key in list(texts.keys()):
        output_text += '### ' + texts[key] + nl
        output_text += inputs[key].get(1.0, tkinter.END+'-1c') + nl

    md_file_name = doi + '.md'
    md_file_path = 'data/' + md_file_name
    file_path = os.path.dirname(md_file_path)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(md_file_path, 'w') as file:
        file.write(output_text)

if __name__ == '__main__':
    main()
