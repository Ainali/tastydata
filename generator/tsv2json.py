#!/usr/bin/env python
# -*- coding: utf-8  -*-
#
# By: André Costa, Wikimedia Sverige
# License: MIT
# 2015
#
# Convert the menudata tsv to a json
# each field is either a string (wihtout a comma) or a
# quoted string, with a comma
#

import os
import sys
import codecs
import json


def run(data_file, matches_file, directory=u'.'):
    '''
    Given a data file and an output directory generate one html+css per
    restaurant to said directory. Also generates an index page.
    '''
    # load datafile
    with codecs.open(data_file, 'r', 'utf8') as f:
        lines = f.read().split('\n')

    # do restaurant data
    rId = -1
    dId = -1
    data = []
    for l in lines:
        if len(l) == 0:
            continue
        p = l.split('\t')

        if p[0] != '':
            # restaurant line
            rId += 1
            dId = -1
            data.append({
                'name': '%s' % p[0],
                'bg_img': '%s' % p[1],
                'colour': '%s' % p[2],
                'active_colour': '%s' % p[3],
                'bg_credit': '%s' % p[4],
                'bg_license': '%s' % p[5],
                'dishes': []
            })
        elif p[1] != '':
            # dish line
            dId += 1
            dData = {
                'name': '%s' % p[1],
                'price': '%s' % p[2],
                'ingredients': []
            }
            if len(p[3]) > 0:
                dData['cmt'] = '%s' % p[3]
            data[rId]['dishes'].append(dData.copy())
        elif p[2] != '':
            # ingredients line
            iData = {
                'name': '%s' % p[2]
            }
            if len(p[3]) > 0:
                iData['cmt'] = '%s' % p[3]
            data[rId]['dishes'][dId]['ingredients'].append(iData.copy())
        else:
            print('shit!')

    output_file = os.path.join(directory, u'%s.json' % data_file[:-len('.tsv')])
    with codecs.open(output_file, 'w', 'utf8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

    # do matches
    with codecs.open(matches_file, 'r', 'utf8') as f:
        lines = f.read().split('\n')

    matches = {}
    for l in lines:
        if len(l) == 0:
            continue
        p = l.split('\t')
        if p[0] in matches.keys():
            print('duplicate word: %s' % p[0])
        else:
            matches[p[0]] = p[1]

    output_file = os.path.join(directory, u'%s.json' % matches_file[:-len('.tsv')])
    with codecs.open(output_file, 'w', 'utf8') as f:
        f.write(json.dumps(matches, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    try:
        data_file, matches_file, dest = sys.argv[1:]
    except ValueError:
        print("Usage: {0} data_file matches_file destination".format(sys.argv[0]))
        exit(1)
    run(data_file, matches_file, dest)
