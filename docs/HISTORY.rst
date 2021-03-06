Changelog
=========

0.4.4 (unreleased)
------------------

- Add basic translations for optout save for ES, GR, PL. [fredvd]

- Translate portal message after submitting opt_out dashboard. [fredvd]

- Shortcut registry settings request in init_cookis because the upgrade step for 'enable' cannot execute. 
  [fredvd]
  
- Update uninstall profile to remove resources and controlpanel
  [fredvd]

- Add upgrade step for new main 'enable' switch in control panel.
  [fredvd]
  
- Fix relative path to privacy statement in multilingual sites.
  [fredvd]

- Add came_from variable and redirect back after saving optout-dashboard.
  [jladage]

- Support url parameters like utm_campaign in redirect after accepting cookies.
  [jladage]

- Added main on/off switch to control panel. Requires a reinstall of the addon.
  [jladage]


0.4.3 (2020-12-14)
------------------

- Fix python2 compatiblity.
  [cekk]


0.4.2 (2020-08-05)
------------------

- Fix bundle configuration.
  [cekk]


0.4.1 (2020-05-11)
------------------

- Add validate_invariants attribute in persistent controlpanel object.
  [cekk]


0.4.0 (2020-03-06)
------------------

- Python 3 compatibility.
  [cekk]


0.3.0 (2018-04-12)
------------------

- German translations
  [tomgross]
- Add uninstall profile
  [tomgross]


0.2.0 (2017/12/21)
------------------

- Move resources to bundle
  [cekk]
- Fix code-quality
  [cekk]
- Add travis config
  [cekk]


0.1.3 (2017-07-03)
------------------

- plone5 compatibility [mamico]
- corrected typo in LC_MESSAGES for the italian language [arsenico13]


0.1.2 (2015-10-16)
------------------

- cookieconsent cookie now expires in 10 years
  [cekk]


0.1.1 (2015-10-14)
------------------

- Add safe_html filter for text configuration
  [cekk]


0.1.0 (2015-09-16)
------------------

- Initial release
