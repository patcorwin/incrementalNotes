

try:
    import mayaHooks.override.incrementalSaveScene
    import incrementalNotes

    mayaHooks.override.incrementalSaveScene.enable()

    mayaHooks.override.incrementalSaveScene.registerOnSave(incrementalNotes.takeNote)

except Exception:
    import traceback
    from maya.cmds import warning
    print( traceback.format_exc() )
    warning('Error setting up incrementalNotes')