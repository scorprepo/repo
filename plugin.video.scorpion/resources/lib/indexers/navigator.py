# -*- coding: utf-8 -*-


import os, sys
import xbmc, xbmcaddon, xbmcgui

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import views

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

artPath = control.artPath()
addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
    HOMEPATH = xbmc.translatePath('special://home/')
    ADDONSPATH = os.path.join(HOMEPATH, 'addons')
    THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
    LOCALNEWS = os.path.join(THISADDONPATH, 'changelog.txt')

    def root(self):
        self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32015, 'favs', 'favourites.png', 'DefaultTVShows.png')

        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        # self.addDirectoryItem('Live Tv (IPTV)', 'livetvNavigator', 'iptv.png', 'DefaultTVShows.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads is True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')

        if control.setting('dev') == 'true':
            self.addDirectoryItem('Testing', 'testing', 'channels.png', 'DefaultTVShows.png')

        self.endDirectory()

    def movies(self, lite=False):
        self.addDirectoryItem(32005, 'movies&url=premiere', 'trending.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32035, 'movies&url=featured', 'featuredmovies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32017, 'movies&url=trending', 'trending.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        self.addDirectoryItem(32019, 'movies&url=votes', 'most-voted.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
        self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.endDirectory()

    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials is True and imdbCredentials is True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials is True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials is True:
            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktCredentials is True:
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials is True:
            self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators is True:
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem('Trakt OnDeck (Movies)', 'movies&url=onDeckMovies', 'trakt.png', 'DefaultTVShows.png')

        self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

        if lite is False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()

    def tvshows(self, lite=False):
        self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32017, 'tvshows&url=trending', 'trending.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32035, 'tvshows&url=featured', 'featuredtv.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32019, 'tvshows&url=votes', 'most-voted.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.endDirectory()

    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials is True and imdbCredentials is True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

        elif traktCredentials is True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials is True:
            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')

        if traktCredentials is True:
            self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        elif imdbCredentials is True:
            self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators is True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem('Trakt OnDeck', 'tvshows&url=onDeckTV', 'trakt.png', 'DefaultTVShows.png')

        self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

        if traktCredentials is True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

        if lite is False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()

    def settings(self):
        self.addDirectoryItem(32540, 'urlResolverRDTorrent', 'resolveurl.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32051, 'clearMetaCache', 'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'settings.png', 'DefaultAddonProgram.png')

        self.endDirectory()
        
    def livetvNavigator(self):
        self.addDirectoryItem('Entertainment', 'entertainment', 'channels.png', 'DefaultTvshows.png')
        self.addDirectoryItem('Movies', 'movies', 'channels.png', 'DefaultTvshows.png')
        self.addDirectoryItem('Kids', 'kids', 'channels.png', 'DefaultTvshows.png')
        self.addDirectoryItem('Sports', 'sports', 'channels.png', 'DefaultTvshows.png')
        self.addDirectoryItem('News', 'news', 'channels.png', 'DefaultTvshows.png')
        self.addDirectoryItem('Music', 'music', 'channels.png', 'DefaultTvshows.png')
        self.addDirectoryItem('Radio', 'radioNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('ArconaiTV 24/7', 'arconaitv_menu', 'channels.png', 'DefaultTvshows.png')
        self.addDirectoryItem('Imkmedia', 'imkmediaNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('ZyneTV', 'zynetvNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('StreamLive', 'streamliveNavigator', 'channels.png', 'DefaultTVShows.png')
        #self.addDirectoryItem('UsaTv Go', 'ustvgoNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Sports24', 'sports24Navigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Ustreamix', 'ustreamixNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('123Tvnow', '123tvnowNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('YourSports', 'yoursportsliveNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Pluto TV', 'pluto', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Wrestling', 'wrestlingNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Foreign Channels', 'foreignNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('[COLOR black]Adult\'s Only[/COLOR]', 'navXXX', 'highly-rated.png', 'DefaultTVShows.png')
        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=7.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()

    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')

        self.endDirectory()

    def views(self):
        try:
            control.idle()

            items = [(control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes')]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1:
                return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels={'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials is False and imdbCredentials is False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()

    def infoCheck(self, version):
        try:
            control.infoDialog('', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'

    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def clearCacheSearch(self):
        control.idle()
        if control.yesnoDialog(control.lang(32056).encode('utf-8'), '', ''):
            control.setSetting('tvsearch', '')
            control.setSetting('moviesearch', '')
            control.refresh()
            control.idle()

    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []
        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('addons', {'skin.scorpion': 500, 'skin.confluence': 500})
