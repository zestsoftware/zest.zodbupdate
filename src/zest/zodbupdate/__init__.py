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
