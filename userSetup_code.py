

try:
    import mayaHooks.override.incrementalSaveScene
    import incrementalNotes

    mayaHooks.override.incrementalSaveScene.callback_onSave.register(incrementalNotes.takeNote)

except Exception:
    import traceback
    from maya.cmds import warning
    print( traceback.format_exc() )
    warning('Error setting up incrementalNotes')