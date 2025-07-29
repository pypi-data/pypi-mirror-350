# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0a5 (2025-05-23)


### New features:

- Added c.person as dependency, move person related things from k.intranet. @sneridagh [#13](https://github.com/kitconcept/kitconcept-core/issues/13)


### Internal:

- Update to VLT 6.1.0. @sneridagh 

## 1.0.0a4 (2025-05-16)


### Bug fixes:

- Fix migration tool exception access without a site hook being set. @ericof [#11](https://github.com/kitconcept/kitconcept-core/issues/11)

## 1.0.0a3 (2025-05-15)


### Internal:

- Explicitly add all content types to our generic setup profile. @sneridagh 
- Refactor site creation function to use three distinct profiles: base, cmfdependencies and dependencies. The later one is responsible for installing, on first run, the add-on dependencies for kitconcept.core. @ericof 
- Upgrade kitconcept.voltolighttheme to version 6.0.1 @sneridagh 
- Upgrade plone.volto to version 5.1.0 @ericof 


### Tests

- Add FTI tests for all content types. @ericof 
- Create a testing distribution to be used in internal tests. @ericof 

## 1.0.0a2 (2025-05-13)


### New features:

- Upgrade plone.restapi to version 9.14.0 @ericof [#6](https://github.com/kitconcept/kitconcept-core/issues/6)


### Internal:

- Remove old portlets registration -- but keep portlet managers (as they are required by other packages). @ericof [#3](https://github.com/kitconcept/kitconcept-core/issues/3)
- Pin Python to version 3.12 in pyproject.toml. @ericof [#4](https://github.com/kitconcept/kitconcept-core/issues/4)

## 1.0.0a1 (2025-05-09)


### New features:

- Add collective.volto.formsupport / collective.honeypot as dependencies. @ericof 
- Add kitconcept.voltolighttheme as dependency. @ericof 
- Add plonegovbr.socialmedia as dependency. @ericof
