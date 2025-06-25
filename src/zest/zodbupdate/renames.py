iface = "zope.interface Interface"
rename_dict = {
    "App.interfaces IPersistentExtra": iface,
    "App.interfaces IUndoSupport": iface,
    "Products.ResourceRegistries.interfaces.settings IResourceRegistriesSettings": iface,
    "plone.restapi.behaviors ITiles": "plone.restapi.behaviors IBlocks",
    "collective.dexteritytextindexer.behavior IDexterityTextIndexer": "plone.app.dexterity.textindexer.behavior IDexterityTextIndexer",
}

try:
    # `Warning: Missing factory for plone.base.interfaces.controlpanel ITinyMCESpellCheckerSchema`
    from plone.base.interfaces.controlpanel import ITinyMCESpellCheckerSchema
except ImportError:
    # This interface was removed in Plone 6.1.
    rename_dict["plone.base.interfaces.controlpanel ITinyMCESpellCheckerSchema"] = iface

try:
    from plone.app.discussion.behavior import IAllowDiscussion
except ImportError:
    # The behavior module is only there in Plone 6.1,
    # and only if plone.app.discussion is actually included.
    pass
else:
    # So only here can we add the rename.
    allow_discussion = "plone.app.discussion.behavior IAllowDiscussion"
    rename_dict["plone.app.discussion.behaviors IAllowDiscussion"] = allow_discussion
    rename_dict["plone.app.dexterity.behaviors.discussion IAllowDiscussion"] = allow_discussion
