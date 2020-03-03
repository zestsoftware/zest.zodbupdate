# -*- coding: utf-8 -*-
import pkg_resources

try:
    pkg_resources.get_distribution("plone.dexterity")
except pkg_resources.DistributionNotFound:
    # No plone.dexterity available.
    pass
else:
    # plone.dexterity is there and we need to register its utility.
    from plone.dexterity.schema import SchemaModuleFactory
    from zope.component.hooks import getSiteManager

    sm = getSiteManager()
    sm.registerUtility(
        factory=SchemaModuleFactory, name="plone.dexterity.schema.generated"
    )


# The zodbupdate rename dictionary, read by an entrypoint:
rename_dict = {
    "App.interfaces IPersistentExtra": "zope.interface Interface",
    "App.interfaces IUndoSupport": "zope.interface Interface",
    "Products.ResourceRegistries.interfaces.settings IResourceRegistriesSettings": "zope.interface Interface",
}
