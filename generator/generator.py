#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# By: André Costa, Wikimedia Sverige
# License: MIT
# 2015
#
# From a json of data and a json of str to qLabel matches generate one
# html+css per restaurant using the style developed by Midas N at
# https://github.com/MidasN/WikimediaTastydata
#
# TODO: Add support for dish-categories
#
import os
import sys
import codecs
import json

qMatches = {}
block = '  '
# keep track of matched and unmatched words to identify any missed connections
unmatched = []
matched = []


def run(data_file, matches_file, directory=u'.'):
    '''
    Given a data file and an output directory generate one html+css per
    restaurant to said directory. Also generates an index page.
    '''
    global qMatches
    # load datafile
    with codecs.open(data_file, 'r', 'utf8') as f:
        data = json.load(f)

    # load qMatches
    with codecs.open(matches_file, 'r', 'utf8') as f:
        qMatches = json.load(f)

    i = 0
    index = []
    for restaurantData in data:
        i += 1
        index.append(makeRestaurant(i, restaurantData, directory))

    # make html from index
    with codecs.open(u'%s/index.html' % directory, 'w', 'utf8') as f:
        f.write(makeIndex(index))

    # output matched and unmatched
    global matched, unmatched
    matched = list(set(matched))
    unmatched = list(set(unmatched))
    with codecs.open(os.path.join(directory, u'matchinfo.csv'), 'w', 'utf8') as f:
        f.write(u'%s\n' % '|'.join(matched))
        f.write(u'%s' % '|'.join(unmatched))


def makeRestaurant(no, restaurantData, directory):
    '''
    Given a restaurantData object and an id-no create the required
    html and css files.
    @return restaurantData['name']
    '''
    dishes = []
    for dishData in restaurantData['dishes']:
        dishes.append(makeDish(dishData))

    # make intro
    txt = intro(restaurantData['name'], no)

    # add title
    txt += u'''
%s<p class="restaurant-name"><mark>%s</mark></p>
%s<ul class="menu flow-text">''' % (4*block, restaurantData['name'], 4*block)
    # add dishes
    txt += ''.join(dishes)

    # footer
    txt += u'''
%s</ul>
%s</div>
%s</div>
%s<div class="row footer">
%sAdapted by <a href="http://wikimedia.se">Wikimedia Sverige</a> based on work by <a href="http://denny.vrandecic.de">Denny Vrandecic</a>. Funded by <a href="http://vinnova.se">Vinnova</a>. <a href="https://github.com/Wikimedia-Sverige/tastydata">Source on Github</a>.
%s<br />''' % (4*block, 3*block, 2*block, 2*block, 3*block, 3*block)

    # add imageref
    txt += u'''
%sImage: <a href="https://commons.wikimedia.org/wiki/File:%s">%s</a> by %s, license: %s''' % (3*block, restaurantData['bg_img'].replace(' ', '_'), restaurantData['bg_img'], restaurantData['bg_credit'], restaurantData['bg_license'])

    # add outro
    txt += outro()

    # output
    with codecs.open(u'%s/%r.html' % (directory, no), 'w', 'utf8') as f:
        f.write(txt)

    # make css
    css = makeCss(restaurantData['colour'],
                  restaurantData['active_colour'],
                  restaurantData['bg_img'])
    with codecs.open(u'%s/%r.css' % (directory, no), 'w', 'utf8') as f:
        f.write(css)

    # return name for index
    return restaurantData['name']


def makeDish(dishData):
    '''
    Given a dish object return a formated string
    '''
    indent = 6
    ingredients = []
    for ingredientData in dishData['ingredients']:
        ingredients.append(makeIngredient(ingredientData, indent+1))

    # add title (and possibly coment)
    txt = u'\n%s<li>' % ((indent-1)*block)
    txt += u'\n%s<p class="dish">' % (indent*block)
    txt += addQlabel(dishData['name'], indent+1)
    if 'cmt' in dishData.keys():
        txt += addComment(dishData['cmt'], indent+2)

    # add price
    txt += u'\n%s<span class="price">%s</span>' % ((indent+1)*block, dishData['price'])
    txt += u'\n%s</p>' % (indent*block)

    # ingredients with wrapper
    txt += u'''
%s<p class="ingredient">%s
%s</p>''' % ((indent*block), ', '.join(ingredients), (indent*block))
    # close
    txt += '\n%s</li>' % ((indent-1)*block)

    return txt


def makeIngredient(ingredientData, indent):
    '''
    Given an ingredient object return a formated string
    '''
    txt = addQlabel(ingredientData['name'], indent)
    if 'cmt' in ingredientData.keys():
        txt += addComment(ingredientData['cmt'], indent+1)
    return txt


def addComment(cmt, indent):
    '''
    Given a cmt string add it inside brackets
    '''
    txt = addQlabel(cmt, indent)
    # If brackets are not wrapped tightly then spaces sneak in
    txt = txt.replace('<span', '(<span').replace('</span>', '</span>)')
    return txt.replace('class="qlabel"', 'class="qlabel cmt"')


def addQlabel(entity, indent):
    '''
    Given a text string look for the equivalent Qno.
    If one is found then return ahref + encoded span otherwise just
    span.
    '''
    global matched, unmatched
    i = '' + indent * block
    if entity in qMatches.keys():
        matched.append(qMatches[entity])
        return u'''
%s<a href="#" title="%s" data-toggle="popover" data-trigger="manual" data-placement="auto" data-content="Data not loaded yet :/" data-html="true">
%s<span class="qlabel" its-ta-ident-ref="http://www.wikidata.org/entity/%s">%s</span></a>''' % (i, entity, (indent+1)*block, qMatches[entity], entity)
    else:
        unmatched.append(entity)
        return u'''
%s<span>%s</span>''' % (i, entity)


def intro(name, no):
    return u'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>%s</title>
    <!-- Universal Language Selector CSS -->
    <link href="lib/jquery.uls/css/jquery.uls.css" rel="stylesheet" type="text/css"/>
    <link href="lib/jquery.uls/css/jquery.uls.grid.css" rel="stylesheet" type="text/css"/>
    <link href="lib/jquery.uls/css/jquery.uls.lcd.css" rel="stylesheet" type="text/css"/>
    <!-- Bootstrap and Main CSS files -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="main.css" rel="stylesheet" type="text/css"/>
    <!-- Menu-specific CSS that overrides Bootstrap and Main -->
    <link href="%r.css" rel="stylesheet" type="text/css">
    <!-- Custom fonts -->
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Droid+Serif:400,700,400italic,700italic" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700" rel="stylesheet" type="text/css">
    <!-- Scripts -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" type="text/javascript"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js" type="text/javascript"></script>
    <!-- Qlabel libraries -->
    <script src="lib/jquery.qlabel.js" type="text/javascript"></script>
    <!-- Universal Language Selector libraries -->
    <script src="lib/jquery.uls/src/jquery.uls.data.js" type="text/javascript"></script>
    <script src="lib/jquery.uls/src/jquery.uls.data.utils.js" type="text/javascript"></script>
    <script src="lib/jquery.uls/src/jquery.uls.lcd.js" type="text/javascript"></script>
    <script src="lib/jquery.uls/src/jquery.uls.languagefilter.js" type="text/javascript"></script>
    <script src="lib/jquery.uls/src/jquery.uls.regionfilter.js" type="text/javascript"></script>
    <script src="lib/jquery.uls/src/jquery.uls.core.js" type="text/javascript"></script>
    <script src="menu.js" type="text/javascript"></script>
  </head>
  <body>
    <div class="container-fluid">
      <div class="row header">
        <button type="button" class="btn btn-primary uls-trigger">Select language</button>
        <button type="button" class="btn btn-primary" style="float:right" onclick="window.location.href='./index.html'">Home</button>
      </div>
      <div class="row">''' % (name, no)


def outro():
    return u'''
    </div>
  </body>
</html>'''


def makeCss(colour, active_colour, img):
    img_url = u'https://commons.wikimedia.org/wiki/Special:Redirect/file?wptype=file&wpvalue=%s' % img.replace(' ', '+')
    return u'''body{
    background-image: url("%s");
}

mark,
.menu,
.footer,
.btn-primary {
    border-color: %s;
    background-color: %s;
}

.btn-primary:hover,
.btn-primary:focus,
.btn-primary:active,
.btn-primary.active {
    border-color: %s;
    background-color: %s;
}
''' % (img_url, colour, colour, active_colour, active_colour)


def makeIndex(index):
    txt = u'''<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>Tastydata restaurant index</title>
    <!-- Bootstrap and Main CSS files -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="main.css" rel="stylesheet" type="text/css"/>
    <!-- Menu-specific CSS that overrides Bootstrap and Main -->
    <link href="index.css" rel="stylesheet" type="text/css">
    <!-- Custom fonts -->
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Droid+Serif:400,700,400italic,700italic" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700" rel="stylesheet" type="text/css">
    <!-- Scripts -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js" type="text/javascript"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js" type="text/javascript"></script>
  </head>
  <body>
    <div class="container-fluid">
      <div class="row">
        <p class="restaurant-name"><mark>Restaurant index</mark></p>
        <ul class="menu flow-text">'''

    for i in range(0, len(index)):
        txt += u'''
          <li>
            <p class="dish"><a href="%r.html">%r. %s</a></p>
          </li>''' % (i+1, i+1, index[i])

    txt += u'''
        </ul>
      </div>
    </div>
    <div class="row footer">
      A project by <a href="http://wikimedia.se">Wikimedia Sverige</a>. Funded by <a href="http://vinnova.se">Vinnova</a>.
      <br />
      Image: <a href="https://commons.wikimedia.org/wiki/File:Wikidata_tastydata.svg">Wikidata tastydata</a> by <a href="https://commons.wikimedia.org/wiki/User:ArildV">Offnfopt</a>, license: <a href="https://creativecommons.org/publicdomain/zero/1.0/deed.sv" rel="license">CC0</a>
    </div>
  </body>
</html>'''
    return txt


if __name__ == "__main__":
    try:
        data_file, matches_file, dest = sys.argv[1:]
    except ValueError:
        print("Usage: {0} data_file matches_file destination".format(sys.argv[0]))
        exit(1)
    run(data_file, matches_file, dest)
