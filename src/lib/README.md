# Starcraft 2 Reader

Current sc2reader taken from lib used by ggtracker:
https://github.com/ggtracker/sc2reader/tree/upstream

Disabled "CreepTracker" plugin in sc2reader.engine.plugins.__init__ because it throws error due to dependency on PIL
and is not actually used by us for anything.
