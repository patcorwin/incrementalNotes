from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import os
import re
import time

import maya.cmds

NOTE_MD = 'note.md'


def takeNote(incrementDirPath, newVersionString, sceneToMove):
    ''' Incremental save override to prompt for a note when saving.
    '''
    
    notesPath = incrementDirPath + NOTE_MD

    prevNotes = getOrderedNotes()

    msg = '\n\n'.join( [ver + '\n' + '\n'.join(data) for ver, data in prevNotes.items()[-3:]] ) if prevNotes else None

    res = maya.cmds.promptDialog(m=msg)

    if res == 'Confirm':

        text = maya.cmds.promptDialog(q=True, text=True)
        if not text:
            return

        pendingVersion = '{:0>{}}'.format( int(newVersionString) + 1, len(newVersionString ))

        with open(notesPath, 'a') as fid:
            fid.write('\n\n# {}\n\n{}'.format(pendingVersion, text) )


def incrementalSaveDir():
    path = maya.cmds.file(q=True, sn=True)
    
    if not path:
        return ''
    
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    
    return dirname + '/incrementalSave/' + basename


def formatModfiedTime(path):
    return time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(os.path.getmtime(path)))


incNumberRE = re.compile(r'\.(\d+)\.m(a|b)$')

def getIncrementTimestamps():
    path = maya.cmds.file(q=True, sn=True)
    
    if not path:
        return {}
    
    basename = os.path.splitext(os.path.basename(path))[0]
    
    folder = incrementalSaveDir()
    
    if not os.path.exists(folder):
        return {}
    
    return {   int(incNumberRE.search(f).group(1)): formatModfiedTime(folder + '/' + f)
        for f in os.listdir(folder) if f.startswith(basename) }


def getNotePath():
    ''' From the scene name, return the full path to `note.md`.
    '''

    path = maya.cmds.file(q=True, sn=True)
    
    if not path:
        return ''
    
    fullpath = incrementalSaveDir() + '/' + NOTE_MD
    
    if os.path.exists(fullpath):
        return fullpath
    
    return ''


def getOrderedNotes(start=None, end=None):
    ''' Returns an ordered dict of { <version #>: <note> }, optionally specifying start and end indices.
    '''
    path = getNotePath()
    
    notes = OrderedDict()
    if not path:
        return notes
    
    key = None
        
    with open(path, 'r') as fid:
        for line in fid:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('#'):
                notes[line] = []
                key = line
            elif key:
                notes[key].append(line)
    
    if start or end:
        return OrderedDict( notes.items()[start:end] )
    else:
        return notes
        

def printRecentNotes(oldest=-3):
    ''' Shows the last three notes in the script editor.
    '''
    
    timestamps = getIncrementTimestamps()
    notes = getOrderedNotes(oldest)
    
    if not notes:
        print('No incremental notes have been made for this file')
        return
    
    for key, val in notes.items():
        print(key, ' ', timestamps.get(int(key.split(' ')[-1]), '') )
        print( '\n'.join(val) )
        print('')
    
    print('Last: ', formatModfiedTime(maya.cmds.file(q=True, sn=True)))