=========
Changelog
=========

Version 1.0.3
==================

- Adjust parameters for A321 use-case by @florentLutz

Version 1.0.2
==================

- Froze version of FAST-OAD-core by @florentLutz

Version 1.0.1
==================

- Updated FAST-OAD CS25 plugin to last version (was causing errors on plots that used wrong parameters names) by @Mokyoslurp
- Tutorial layout adjustements for smaller screens by @Mokyoslurp
- Spaces in the inputted aircraft name are remplaced by underscores rather than being erased by @aeomath
- Removed dark overlay appearing on small screens when starting the app by @Mokyoslurp
- Minor code refactors by @Mokyoslurp 

Version 1.0.0
==================

- Update of the GUI by the use of ipyvuetify instead of ipywidgets by @Mokyoslurp
- Interface more intuitive and practical (more ways to set inputs, easier selection of output aircraft)  by @Mokyoslurp
- Code architecture refactor by seperating GUI code and process code. Future tests will be easier to implement  by @Mokyoslurp
- Process figure (residuals or objectives) are now plotted while the process is still computing (in a different thread)  by @Mokyoslurp
- Addition of some figures and a structure to add/delete figures easily  by @Mokyoslurp
- Addition of a tutorial to explain the user how the app works  by @Mokyoslurp

Version 0.2.0
==================

- Choose reference data used by @florentLutz #2

Version 0.1.0
==================

- First release of the code
- Can run MDA and MDO with a limited number of parameters

