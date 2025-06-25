from importlib.metadata import distribution
from importlib.metadata import PackageNotFoundError


try:
    distribution("plone.dexterity")
except PackageNotFoundError:
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
