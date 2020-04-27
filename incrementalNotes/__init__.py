from __future__ import absolute_import, division, print_function

from maya.cmds import promptDialog


def takeNote(incrementDirPath, newVersionString, sceneToMove):

    notes = incrementDirPath + 'note.md'

    res = promptDialog()

    if res == 'Confirm':

        text = promptDialog(q=True, text=True)
        if not text:
            return

        pendingVersion = '{:0>{}}'.format( int(newVersionString) + 1, len(newVersionString ))

        with open(notes, 'a') as fid:
            fid.write('\n\n# {}\n\n{}'.format(pendingVersion, text) )
