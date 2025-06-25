iface = "zope.interface Interface"
rename_dict = {
    "App.interfaces IPersistentExtra": iface,
    "App.interfaces IUndoSupport": iface,
    "Products.ResourceRegistries.interfaces.settings IResourceRegistriesSettings": iface,
    "plone.restapi.behaviors ITiles": "plone.restapi.behaviors IBlocks",
    "collective.dexteritytextindexer.behavior IDexterityTextIndexer": "plone.app.dexterity.textindexer.behavior IDexterityTextIndexer",
    "plone.app.discussion.behaviors IAllowDiscussion": "plone.app.discussion.behavior IAllowDiscussion",
    "plone.app.dexterity.behaviors.discussion IAllowDiscussion": "plone.app.discussion.behavior IAllowDiscussion",
}

try:
    # `Warning: Missing factory for plone.base.interfaces.controlpanel ITinyMCESpellCheckerSchema`
    from plone.base.interfaces.controlpanel import ITinyMCESpellCheckerSchema
except ImportError:
    # This interface was removed in Plone 6.1.
    rename_dict["plone.base.interfaces.controlpanel ITinyMCESpellCheckerSchema"] = iface
