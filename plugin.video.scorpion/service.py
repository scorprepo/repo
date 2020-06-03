# -*- coding: utf-8 -*-

from resources.lib.modules import log_utils
from resources.lib.modules import control

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

try:
    AddonVersion = control.addon('plugin.video.scorpion').getAddonInfo('version')
    RepoVersion = control.addon('repository.scorpion').getAddonInfo('version')

    log_utils.log(' Scorpion PLUGIN VERSION: %s ' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log(' Scorpion REPOSITORY VERSION: %s ' % str(RepoVersion), log_utils.LOGNOTICE)
except:
    log_utils.log('CURRENT Scorpion VERSIONS REPORT ', log_utils.LOGNOTICE)
    log_utils.log('### ERROR GETTING Scorpion VERSIONS - NO HELP WILL BE GIVEN AS THIS IS NOT AN OFFICIAL Scorpion INSTALL. ', log_utils.LOGNOTICE)