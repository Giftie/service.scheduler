import os, traceback, socket, time, sys, datetime
from threading import Timer
import xbmcaddon, xbmc, xbmcgui, xbmcvfs


__addon__                = xbmcaddon.Addon( "service.scheduler" )
__language__             = __addon__.getLocalizedString
__scriptname__           = __addon__.getAddonInfo('name')
__scriptID__             = __addon__.getAddonInfo('id')
__author__               = __addon__.getAddonInfo('author')
__version__              = __addon__.getAddonInfo('version')
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ).decode('utf-8'), os.path.basename( __addon__.getAddonInfo('path') ) )
BASE_RESOURCE_PATH       = xbmc.translatePath( os.path.join( __addon__.getAddonInfo('path').decode('utf-8'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
addon_work_folder                = xbmc.translatePath( __addon__.getAddonInfo('profile') ).decode('utf-8')
log_file_path                    = os.path.join( addon_work_folder, "scheduler.log" )
true = True
false = False
null = None

cdart_script                     = "RunScript(script.cdartmanager,%s)"
video_library_script             = "UpdateLibrary(video)"
music_library_script             = "UpdateLibrary(music)"

setting_interval                = 86400 # interval to reload settings.  86400 seconds = 24 hours

class Scheduler():
    def __init__( self, *args, **kwargs ):
        self.setup()
        
    def onInit( self ):
        self.start()
    
    def setup( self ):
        self.load_settings()
        self.set_trigger_variables()
        
    def load_settings( self ):
        xbmc.log( "[service.scheduler] - Loading Setting", xbmc.LOGNOTICE )
        self.enable_logging                   = eval( __addon__.getSetting( "enable_logging" ) )
        self.cdart                            = { "enabled": eval( __addon__.getSetting( "cdartmanager" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "cdart_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "cdart_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "cdart_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                     "mode": int( __addon__.getSetting( "cdart_mode" ) ), # available modes autoall(0), autocdart(1), autocover(2), autofanart(3), autologo(4), autothumb(5), autobanner(6)
                                                      "day": int( __addon__.getSetting( "cdart_day" ) ),
                                                     "time": __addon__.getSetting( "cdart_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "cdart_interval" ) ) ]
                                                }
        self.cdart_update                     = { "enabled": eval( __addon__.getSetting( "cdart_update" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "cdart_update_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "cdart_update_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "cdart_update_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                      "day": int( __addon__.getSetting( "cdart_update_day" ) ),
                                                     "time": __addon__.getSetting( "cdart_update_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "cdart_update_interval" ) ) ]
                                                }
        self.video_library                    = { "enabled": eval( __addon__.getSetting( "video_library" ) ),
                                                    "cycle": int( __addon__.getSetting( "video_library_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                      "day": int( __addon__.getSetting( "video_library_day" ) ),
                                                     "time": __addon__.getSetting( "video_library_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "video_library_interval" ) ) ]
                                                }      
        self.music_library                    = { "enabled": eval( __addon__.getSetting( "music_library" ) ),
                                                    "cycle": int( __addon__.getSetting( "music_library_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                      "day": int( __addon__.getSetting( "music_library_day" ) ),
                                                     "time": __addon__.getSetting( "music_library_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "music_library_interval" ) ) ]
                                                }                  
        self.custom1                          = { "enabled": eval( __addon__.getSetting( "custom1" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom1_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom1_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom1_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom1_script" ),
                                                      "day": int( __addon__.getSetting( "custom1_day" ) ),
                                                     "time": __addon__.getSetting( "custom1_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom1_interval" ) ) ]
                                                }
        self.custom2                          = { "enabled": eval( __addon__.getSetting( "custom2" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom2_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom2_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom2_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom2_script" ),
                                                      "day": int( __addon__.getSetting( "custom2_day" ) ),
                                                     "time": __addon__.getSetting( "custom2_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom2_interval" ) ) ]
                                                }
        self.custom3                          = { "enabled": eval( __addon__.getSetting( "custom3" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom3_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom3_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom3_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom3_script" ),
                                                      "day": int( __addon__.getSetting( "custom3_day" ) ),
                                                     "time": __addon__.getSetting( "custom3_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom3_interval" ) ) ]
                                                }
        self.custom4                          = { "enabled": eval( __addon__.getSetting( "custom4" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom4_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom4_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom4_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom4_script" ),
                                                      "day": int( __addon__.getSetting( "custom4_day" ) ),
                                                     "time": __addon__.getSetting( "custom4_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom4_interval" ) ) ]
                                                }
        self.custom5                          = { "enabled": eval( __addon__.getSetting( "custom5" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom5_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom5_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom5_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom5_script" ),
                                                      "day": int( __addon__.getSetting( "custom5_day" ) ),
                                                     "time": __addon__.getSetting( "custom5_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom5_interval" ) ) ]
                                                }
        self.custom6                          = { "enabled": eval( __addon__.getSetting( "custom6" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom6_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom6_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom6_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom6_script" ),
                                                      "day": int( __addon__.getSetting( "custom6_day" ) ),
                                                     "time": __addon__.getSetting( "custom6_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom6_interval" ) ) ]
                                                }
        self.custom7                          = { "enabled": eval( __addon__.getSetting( "custom7" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom7_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom7_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom7_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom7_script" ),
                                                      "day": int( __addon__.getSetting( "custom7_day" ) ),
                                                     "time": __addon__.getSetting( "custom7_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom7_interval" ) ) ]
                                                }
        self.custom8                          = { "enabled": eval( __addon__.getSetting( "custom8" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom8_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom8_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom8_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom8_script" ),
                                                      "day": int( __addon__.getSetting( "custom8_day" ) ),
                                                     "time": __addon__.getSetting( "custom8_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom8_interval" ) ) ]
                                                }
        self.custom9                          = { "enabled": eval( __addon__.getSetting( "custom9" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom9_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom9_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom9_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom9_script" ),
                                                      "day": int( __addon__.getSetting( "custom9_day" ) ),
                                                     "time": __addon__.getSetting( "custom9_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom9_interval" ) ) ]
                                                }
        self.custom10                         = { "enabled": eval( __addon__.getSetting( "custom10" ) ),
                                    "disabled_on_videoscan": eval( __addon__.getSetting( "custom10_disable_video" ) ),
                                    "disabled_on_musicscan": eval( __addon__.getSetting( "custom10_disable_music" ) ),
                                                    "cycle": int( __addon__.getSetting( "custom10_cycle" ) ), # intervals - Weekly(0), Daily(1), Hourly(2)
                                                   "script":  __addon__.getSetting( "custom10_script" ),
                                                      "day": int( __addon__.getSetting( "custom10_day" ) ),
                                                     "time": __addon__.getSetting( "custom10_time" ),
                                                 "interval": ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom10_interval" ) ) ]
                                                }
        if __addon__.getSetting( "default_interval" ) == "true":
            self.sleep_interval               = 900  # 15 Minutes
            self.test_interval                = 15
        else:
            self.test_interval                = int( float( __addon__.getSetting( "sleep_interval" ) ) )
            self.sleep_interval               = self.test_interval * 60
        self.default_cdart_time_delay         = self.test_interval
        self.default_cdart_update_time_delay  = 15    # In minutes
        self.music_time_delay                 = 60    # In minutes
        self.video_time_delay                 = 60    # In minutes
        self.general_time_delay               = 60    # In minutes
    
    def triggered_settings( self ):
        load_settings()
        self.setup()
        self.store_log_file( "Reloading Settings", "Settings" )
        self.settings_timer.cancel()
        self._triggered_settings = False
    
    def set_trigger_variables( self ):
        self.music_scan                       = False
        self.video_scan                       = False
        self.interval                         = False
        self._triggered_settings              = False
        self.video_library_day_triggerd       = False
        self.music_library_day_triggerd       = False
        self.cdart_day_triggerd               = False
        self.cdart_update_day_triggerd        = False
        self.custom1_day_triggerd             = False
        self.custom2_day_triggerd             = False
        self.custom3_day_triggerd             = False
        self.custom4_day_triggerd             = False
        self.custom5_day_triggerd             = False
        self.custom6_day_triggerd             = False
        self.custom7_day_triggerd             = False
        self.custom8_day_triggerd             = False
        self.custom9_day_triggerd             = False
        self.custom10_day_triggerd            = False
        self.video_library_time_trigger       = False
        self.music_library_time_trigger       = False
        self.cdart_time_trigger               = False
        self.cdart_update_time_trigger        = False
        self.custom1_time_trigger             = False
        self.custom2_time_trigger             = False
        self.custom3_time_trigger             = False
        self.custom4_time_trigger             = False
        self.custom5_time_trigger             = False
        self.custom6_time_trigger             = False
        self.custom7_time_trigger             = False
        self.custom8_time_trigger             = False
        self.custom9_time_trigger             = False
        self.custom10_time_trigger            = False
        self.video_library_triggered          = False
        self.music_library_triggered          = False
        self.cdart_triggered                  = False
        self.cdartmanager_update              = False
        self.cdartmanager_running             = False
        self.cdart_update_triggered           = False
        self.custom1_triggered                = False
        self.custom2_triggered                = False
        self.custom3_triggered                = False
        self.custom4_triggered                = False
        self.custom5_triggered                = False
        self.custom6_triggered                = False
        self.custom7_triggered                = False
        self.custom8_triggered                = False
        self.custom9_triggered                = False
        self.custom10_triggered               = False
        self.previous_day                     = ""
        self.sleep_timer                      = None
        self.cdart_timer_set                  = False
        self.video_library_timer_set          = False
        self.music_library_timer_set          = False
        self.custom1_timer_set                = False
        self.custom2_timer_set                = False
        self.custom3_timer_set                = False
        self.custom4_timer_set                = False
        self.custom5_timer_set                = False
        self.custom6_timer_set                = False
        self.custom7_timer_set                = False
        self.custom8_timer_set                = False
        self.custom9_timer_set                = False
        self.custom10_timer_set               = False
        self.music_delay                      = 0
        self.video_delay                      = 0
        self.cdart_delay                      = 0
        self.cdart_update_delay               = 0
        self.custom1_delay                    = 0
        self.custom2_delay                    = 0
        self.custom3_delay                    = 0
        self.custom4_delay                    = 0
        self.custom5_delay                    = 0
        self.custom6_delay                    = 0
        self.custom7_delay                    = 0
        self.custom8_delay                    = 0
        self.custom9_delay                    = 0
        self.custom10_delay                   = 0

    def trigger_builtin( self, builtin_func, mode ):
        xbmc.log( "[service.scheduler] - Mode triggered: %s" % mode, xbmc.LOGNOTICE )
        xbmc.log( "[service.scheduler] - Built-in Function: %s" % builtin_func, xbmc.LOGNOTICE )
        xbmc.executebuiltin( "%s" % builtin_func )
        self.store_log_file( builtin_func, mode )
        if mode == "video":
            self.video_library_triggered      = False
            self.video_delay                  = 0
            self.video_scan                   = True
            if self.video_library_timer_set:
                self.video_library_timer.cancel()
                self.video_library_timer_set = False
        if mode == "music":
            self.music_library_triggered      = False
            self.music_delay                  = 0
            self.music_scan                   = True
            if self.music_library_timer_set:
                self.music_library_timer.cancel()
                self.music_library_timer_set = False
        if mode == "cdart":
            self.cdart_triggered              = False
            self.cdart_delay                  = 0
            if self.cdart_timer_set:
                self.cdart_timer.cancel()
                self.cdart_timer_set = False
        if mode == "cdart_update":
            self.cdart_update_triggered       = False
            self.cdart_update_delay           = 0
            if self.cdart_timer_set:
                self.cdart_update_timer.cancel()
                self.cdart_update_timer_set = False
        if mode == "custom1":
            self.custom1_triggered            = False
            self.custom1_delay                = 0
            if self.custom1_timer_set:
                self.custom1_timer.cancel()
                self.custom1_timer_set = False
        if mode == "custom2":
            self.custom2_triggered            = False
            self.custom2_delay                = 0
            if self.custom2_timer_set:
                self.custom2_timer.cancel()
                self.custom2_timer_set = False
        if mode == "custom3":
            self.custom3_triggered            = False
            self.custom3_delay                = 0
            if self.custom3_timer_set:
                self.custom3_timer.cancel()
                self.custom3_timer_set = False
        if mode == "custom4":
            self.custom4_triggered            = False
            self.custom4_delay                = 0
            if self.custom4_timer_set:
                self.custom4_timer.cancel()
                self.custom4_timer_set = False
        if mode == "custom5":
            self.custom5_triggered            = False
            self.custom5_delay                = 0
            if self.custom5_timer_set:
                self.custom5_timer.cancel()
                self.custom5_timer_set = False
        if mode == "custom6":
            self.custom6_triggered            = False
            self.custom6_delay                = 0
            if self.custom6_timer_set:
                self.custom6_timer.cancel()
                self.custom6_timer_set = False
        if mode == "custom7":
            self.custom7_triggered            = False
            self.custom7_delay                = 0
            if self.custom7_timer_set:
                self.custom7_timer.cancel()
                self.custom7_timer_set = False
        if mode == "custom8":
            self.custom8_triggered            = False
            self.custom8_delay                = 0
            if self.custom8_timer_set:
                self.custom8_timer.cancel()
                self.custom8_timer_set = False
        if mode == "custom9":
            self.custom9_triggered            = False
            self.custom9_delay                = 0
            if self.custom9_timer_set:
                self.custom9_timer.cancel()
                self.custom9_timer_set = False
        if mode == "custom10":
            self.custom10_triggered            = False
            self.custom10_delay                = 0
            if self.custom10_timer_set:
                self.custom10_timer.cancel()
                self.custom10_timer_set = False

    def store_log_file( self, builtin_func, mode ):
        if self.enable_logging:
            line = "%s - %s - %s mode Tiggered - Built-in function call - %s\r\n" % ( (  "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")[ self.current_day ], self.current_time, mode, builtin_func )
            if not xbmcvfs.exists( log_file_path):
                log_file = open( log_file_path, "wb" )
            else:
                log_file = open( log_file_path, "a" )
            try:
                log_file.write( line.encode("utf8") )
            except:
                log_file.write( repr(line) )
            log_file.close()

    def clear_interval( self ):
        xbmc.log( "[service.scheduler] - Clearing Sleep Interval", xbmc.LOGDEBUG )
        self.interval = False
        self.sleep_timer.cancel()

    def set_settings_timer( self ):
        xbmc.log( "[service.scheduler] - Setting Settings Load Interval: %s seconds" % setting_interval, xbmc.LOGDEBUG )
        self.settings_timer = Timer( setting_interval, self.load_settings,() )
        self.settings_timer.daemon = True
        self.settings_timer.start()
        self._triggered_settings = True
        
    def set_interval_timer( self ):
        xbmc.log( "[service.scheduler] - Setting Sleep Interval: %s seconds" % self.sleep_interval, xbmc.LOGDEBUG )
        self.sleep_timer = Timer( self.sleep_interval, self.clear_interval,() )
        self.sleep_timer.daemon = True
        self.sleep_timer.start()
        self.interval = True
        
    def test_time( self, value, interval ):
        xbmc.log( "[service.scheduler] - Adjusting Testing time", xbmc.LOGDEBUG )
        xbmc.log( "[service.scheduler] - Current Value: %s " % value, xbmc.LOGDEBUG )
        xbmc.log( "[service.scheduler] - Current Interval: %s" % interval, xbmc.LOGDEBUG )
        value_hour = int( value.split( ":" )[ 0 ] )
        value_min  = int( value.split( ":" )[ 1 ] )
        new_value_min = value_min + interval
        new_value_hour = value_hour
        while( 1 ):
            if new_value_min > 59:
                new_value_hour += 1
                new_value_min -= 60
            else:
                break
                
        xbmc.log( "[service.scheduler] - Test time: %02d:%02d" % ( new_value_hour, new_value_min ), xbmc.LOGDEBUG )
        return "%02d:%02d" % ( new_value_hour, new_value_min )
        
    def schedule_check( self ):
        # Check and set required delays
        if self.cdart_update[ "enabled" ]:
            if ( ( self.cdart_update[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.cdart_update[ "disabled_on_videoscan" ] and self.video_scan ) ) or ( ( self.cdartmanager_running ) and self.cdart_update_delay < 1 ) and not self.cdartmanager_update:
                if self.cdart_update[ "disabled_on_musicscan" ] and self.music_scan:
                    self.cdart_update_delay = self.default_cdart_update_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.cdart_update_delay, xbmc.LOGNOTICE )
                elif self.cdart_update[ "disabled_on_videoscan" ] and self.video_scan:
                    self.cdart_update_delay = self.default_cdart_update_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.cdart_update_delay, xbmc.LOGNOTICE )
                elif self.cdartmanager_running:
                    self.cdart_update_delay = self.default_cdart_update_time_delay
                    xbmc.log( "[service.scheduler] - cdART Manager already running, delaying %s Minutes " % self.cdart_update_delay, xbmc.LOGNOTICE )
        if self.cdart[ "enabled" ]:
            if ( ( self.cdart[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.cdart[ "disabled_on_videoscan" ] and self.video_scan ) ) or ( ( self.cdartmanager_update ) and self.cdart_delay < 1 ):
                if self.cdart[ "disabled_on_musicscan" ] and self.music_scan:
                    self.cdart_delay = self.default_cdart_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.cdart_delay, xbmc.LOGNOTICE )
                elif self.cdart[ "disabled_on_videoscan" ] and self.video_scan:
                    self.cdart_delay = self.default_cdart_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.cdart_delay, xbmc.LOGNOTICE )
                elif ( self.cdartmanager_update or self.cdartmanager_running ):
                    self.cdart_delay = self.default_cdart_time_delay
                    if self.cdartmanager_update:
                        xbmc.log( "[service.scheduler] - cdART Manager already running in mode: Update, delaying %s Minutes " % self.cdart_delay, xbmc.LOGNOTICE )
                    if self.cdartmanager_running:
                        xbmc.log( "[service.scheduler] - cdART Manager already running in mode: Running, delaying %s Minutes " % self.cdart_delay, xbmc.LOGNOTICE )
        if self.music_library[ "enabled" ]:
            if ( self.cdartmanager_update or self.cdartmanager_running ) and self.music_delay < 1: # Just to delay music library build if cdART Manager is running
                self.music_delay = self.music_time_delay
        if self.custom1[ "enabled" ]:
            if ( ( self.custom1[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom1[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom1_delay < 1:
                if self.custom1[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom1_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom1_delay, xbmc.LOGNOTICE )
                elif self.custom1[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom1_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom1_delay, xbmc.LOGNOTICE )
        if self.custom2[ "enabled" ]:
            if ( ( self.custom2[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom2[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom2_delay < 1:
                if self.custom2[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom2_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom2_delay, xbmc.LOGNOTICE )
                elif self.custom2[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom2_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom2_delay, xbmc.LOGNOTICE )
        if self.custom3[ "enabled" ]:
            if ( ( self.custom3[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom3[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom3_delay < 1:
                if self.custom3[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom3_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom3_delay, xbmc.LOGNOTICE )
                elif self.custom3[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom3_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom3_delay, xbmc.LOGNOTICE )
        if self.custom4[ "enabled" ]:
            if ( ( self.custom4[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom4[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom4_delay < 1:
                if self.custom4[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom4_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom4_delay, xbmc.LOGNOTICE )
                elif self.custom4[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom4_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom4_delay, xbmc.LOGNOTICE )
        if self.custom5[ "enabled" ]:
            if ( ( self.custom5[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom5[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom5_delay < 1:
                if self.custom5[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom5_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom5_delay, xbmc.LOGNOTICE )
                elif self.custom5[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom5_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom5_delay, xbmc.LOGNOTICE )
        if self.custom6[ "enabled" ]:
            if ( ( self.custom6[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom6[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom6_delay < 1:
                if self.custom6[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom6_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom6_delay, xbmc.LOGNOTICE )
                elif self.custom6[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom6_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Library Library Scan in Progress, delaying %s Minutes " % self.custom6_delay, xbmc.LOGNOTICE )
        if self.custom7[ "enabled" ]:
            if ( ( self.custom7[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom7[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom7_delay < 1:
                if self.custom7[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom7_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom7_delay, xbmc.LOGNOTICE )
                elif self.custom7[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom7_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Library Library Scan in Progress, delaying %s Minutes " % self.custom7_delay, xbmc.LOGNOTICE )
        if self.custom8[ "enabled" ]:
            if ( ( self.custom8[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom8[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom8_delay < 1:
                if self.custom8[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom8_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom8_delay, xbmc.LOGNOTICE )
                elif self.custom8[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom8_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom8_delay, xbmc.LOGNOTICE )
        if self.custom9[ "enabled" ]:
            if ( ( self.custom9[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom9[ "disabled_on_videoscan" ] and self.video_scan ) )  and self.custom9_delay < 1:
                if self.custom9[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom9_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom9_delay, xbmc.LOGNOTICE )
                elif self.custom9[ "disabled_on_videoscan" ] and self.video_scan:
                    self.custom9_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom9_delay, xbmc.LOGNOTICE )
        if self.custom10[ "enabled" ]:
            if ( ( self.custom10[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom10[ "disabled_on_videoscan" ] and self.video_scan ) ) and self.custom10_delay < 1:
                if self.custom10[ "disabled_on_musicscan" ] and self.music_scan:
                    self.custom10_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom10_delay, xbmc.LOGNOTICE )
                elif ( self.custom10[ "disabled_on_videoscan" ] and self.video_scan ):
                    self.custom10_delay = self.general_time_delay
                    xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom10_delay, xbmc.LOGNOTICE )
        # Check schedule
        if self.cdart[ "enabled" ] and not ( ( self.cdart[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.cdart[ "disabled_on_videoscan" ] and self.video_scan ) ) and not self.cdartmanager_update and not self.cdartmanager_running:
            self.builtin_function = cdart_script % ( "autoall", "autocdart", "autocover", "autofanart", "autologo", "autothumb", "autobanner" )[ self.cdart[ "mode" ] ]
            if self.cdart[ "cycle" ] == 0 and self.current_day == self.cdart[ "day" ] and not self.cdart_day_triggerd:
                if ( self.current_time == self.cdart[ "time" ] or ( self.current_time > self.cdart[ "time" ] and self.current_time < ( self.test_time( self.cdart[ "time" ], self.test_interval + self.cdart_delay ) ) ) ) and not self.cdart_time_trigger:
                    self.trigger_builtin( self.builtin_function, "cdart" )
                    self.cdart_time_trigger = True
            elif self.cdart[ "cycle" ] == 0 and not self.current_day == self.cdart[ "day" ]:
                self.cdart_day_triggerd = False
                self.cdart_time_trigger = False
            elif self.cdart[ "cycle" ] == 1 and ( self.current_time == self.cdart[ "time" ] or ( self.current_time > self.cdart[ "time" ] and self.current_time < ( self.test_time( self.cdart[ "time" ], self.test_interval + self.cdart_delay ) ) ) ) and not self.cdart_time_trigger:
                self.trigger_builtin( self.builtin_function, "cdart" )
                self.cdart_time_trigger = True
            elif self.cdart[ "cycle" ] == 1 and self.current_time > self.test_time( self.cdart[ "time" ], self.test_interval + 1 ):
                self.cdart_time_trigger = False
            elif self.cdart[ "cycle" ] == 2 and not self.cdart_triggered:
                xbmc.log( "[service.scheduler] - Starting cdART Manager Hourly Schedule, every %s Hours" % self.cdart_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.cdart_triggered = True
                self.cdart_timer_set = True
                self.cdart_timer = Timer( self.cdart[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.builtin_function, "cdart" ] )
                self.cdart_timer.setName('cdART_Timer')
                self.cdart_timer.start()
        if self.cdart_update[ "enabled" ] and not ( ( self.cdart_update[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.cdart_update[ "disabled_on_videoscan" ] and self.video_scan ) ) and not self.cdartmanager_update and not self.cdartmanager_running:
            self.builtin_function = cdart_script % "update"
            if self.cdart_update[ "cycle" ] == 0 and self.current_day == self.cdart_update[ "day" ] and not self.cdart_update_day_triggerd:
                if ( self.current_time == self.cdart_update[ "time" ] or ( self.current_time > self.cdart_update[ "time" ] and self.current_time < ( self.test_time( self.cdart_update[ "time" ], self.test_interval + self.cdart_update_delay ) ) ) ) and self.cdart_update_time_trigger:
                    self.trigger_builtin( self.builtin_function, "cdart_update" )
                    self.cdart_update_time_trigger = True
            elif self.cdart_update[ "cycle" ] == 0 and not self.current_day == self.cdart_update[ "day" ]:
                self.cdart_update_day_triggerd = False
                self.cdart_update_time_trigger = False
            elif self.cdart_update[ "cycle" ] == 1 and ( self.current_time == self.cdart_update[ "time" ] or ( self.current_time > self.cdart_update[ "time" ] and self.current_time < ( self.test_time( self.cdart_update[ "time" ], self.test_interval + self.cdart_update_delay ) ) ) ) and not self.cdart_update_time_trigger:
                self.trigger_builtin( self.builtin_function, "cdart_update" )
                self.cdart_update_time_trigger = True
            elif self.cdart_update[ "cycle" ] == 1 and self.current_time > self.test_time( self.cdart_update[ "time" ], self.test_interval + 1 ):
                self.cdart_update_time_trigger = False
            elif self.cdart_update[ "cycle" ] == 2 and not self.cdart_update_triggered:
                xbmc.log( "[service.scheduler] - Starting cdART Manager Update Hourly Schedule, every %s Hours" % self.cdart_update_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.cdart_update_triggered = True
                self.cdart_update_timer_set = True
                self.cdart_update_timer = Timer( self.cdart_update[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.builtin_function, "cdart_update" ] )
                self.cdart_update_timer.setName('cdART_Update_Timer')
                self.cdart_update_timer.start()
        if self.custom1[ "enabled"] and not ( ( self.custom1[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom1[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom1[ "cycle" ] == 0 and self.current_day == self.custom1[ "day" ] and not self.custom1_day_triggerd:
                if ( self.current_time == self.custom1[ "time" ] or ( self.current_time > self.custom1[ "time" ] and self.current_time < ( self.test_time( self.custom1[ "time" ], self.test_interval + self.custom1_delay ) ) ) ) and not self.custom1_time_trigger:
                    self.trigger_builtin( self.custom1[ "script" ], "custom1" )
                    self.custom1_time_trigger = True
            elif self.custom1[ "cycle" ] == 0 and not self.current_day == self.custom1[ "day" ]:
                self.custom1_day_triggerd = False
                self.custom1_time_trigger = False
            elif self.custom1[ "cycle" ] == 1 and ( self.current_time == self.custom1[ "time" ] or ( self.current_time > self.custom1[ "time" ] and self.current_time < ( self.test_time( self.custom1[ "time" ], self.test_interval + self.custom1_delay ) ) ) ) and not self.custom1_time_trigger:
                self.trigger_builtin( self.custom1[ "script" ], "custom1" )
                self.custom1_time_trigger = True
            elif self.custom1[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom1[ "time" ], self.test_interval + 1):
                self.custom1_time_trigger = False
            elif self.custom1[ "cycle" ] == 2 and not self.custom1_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom1_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom1_triggered = True
                self.custom1_timer_set = True
                self.custom1_timer = Timer( self.custom1[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom1[ "script" ], "custom1" ] )
                self.custom1_timer.setName('Custom1_Timer')
                self.custom1_timer.start()
        if self.custom2[ "enabled"] and not ( ( self.custom2[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom2[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom2[ "cycle" ] == 0 and self.current_day == self.custom2[ "day" ] and not self.custom2_day_triggerd:
                if ( self.current_time == self.custom2[ "time" ] or ( self.current_time > self.custom2[ "time" ] and self.current_time < ( self.test_time( self.custom2[ "time" ], self.test_interval + self.custom2_delay ) ) ) ) and not self.custom2_time_trigger:
                    self.trigger_builtin( self.custom2[ "script" ], "custom2" )
                    self.custom2_time_trigger = True
            elif self.custom2[ "cycle" ] == 0 and not self.current_day == self.custom2[ "day" ]:
                self.custom2_day_triggerd = False
                self.custom2_time_trigger = False
            elif self.custom2[ "cycle" ] == 1 and ( self.current_time == self.custom2[ "time" ] or ( self.current_time > self.custom2[ "time" ] and self.current_time < ( self.test_time( self.custom2[ "time" ], self.test_interval + self.custom2_delay ) ) ) ) and not self.custom2_time_trigger:
                self.trigger_builtin( self.custom2[ "script" ], "custom2" )
                self.custom2_time_trigger = True
            elif self.custom2[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom2[ "time" ], self.test_interval + 1):
                self.custom2_time_trigger = False
            elif self.custom2[ "cycle" ] == 2 and not self.custom2_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 2 Hourly Schedule, every %s Hours" % self.custom2_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom2_triggered = True
                self.custom2_timer_set = True
                self.custom2_timer = Timer( self.custom2[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom2[ "script" ], "custom2" ] )
                self.custom2_timer.setName('Custom2_Timer')
                self.custom2_timer.start()
        if self.custom3[ "enabled" ] and not ( ( self.custom3[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom3[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom3[ "cycle" ] == 0 and self.current_day == self.custom3[ "day" ] and not self.custom3_day_triggerd:
                if ( self.current_time == self.custom3[ "time" ] or ( self.current_time > self.custom3[ "time" ] and self.current_time < ( self.test_time( self.custom3[ "time" ], self.test_interval + self.custom3_delay ) ) ) ) and not self.custom3_time_trigger:
                    self.trigger_builtin( self.custom3[ "script" ], "custom3" )
                    self.custom3_time_trigger = True
            elif self.custom3[ "cycle" ] == 0 and not self.current_day == self.custom3[ "day" ]:
                self.custom3_day_triggerd = False
                self.custom3_time_trigger = False
            elif self.custom3[ "cycle" ] == 1 and ( self.current_time == self.custom3[ "time" ] or ( self.current_time > self.custom3[ "time" ] and self.current_time < ( self.test_time( self.custom3[ "time" ], self.test_interval + self.custom3_delay ) ) ) ) and not self.custom3_time_trigger:
                self.trigger_builtin( self.custom3[ "script" ], "custom3" )
                self.custom3_time_trigger = True
            elif self.custom3[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom3[ "time" ], self.test_interval + 1 ):
                self.custom3_time_trigger = False
            elif self.custom3[ "cycle" ] == 2 and not self.custom3_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 3 Hourly Schedule, every %s Hours" % self.custom3_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom3_triggered = True
                self.custom3_timer_set = True
                self.custom3_timer = Timer( self.custom3[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom3[ "script" ], "custom3" ] )
                self.custom3_timer.setName('Custom3_Timer')
                self.custom3_timer.start()
        if self.custom4[ "enabled" ] and not ( ( self.custom4[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom4[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom4[ "cycle" ] == 0 and self.current_day == self.custom4[ "day" ] and not self.custom4_day_triggerd:
                if ( self.current_time == self.custom4[ "time" ] or ( self.current_time > self.custom4[ "time" ] and self.current_time < ( self.test_time( self.custom4[ "time" ], self.test_interval + self.custom4_delay ) ) ) ) and not self.custom4_time_trigger:
                    self.trigger_builtin( self.custom4[ "script" ], "custom4" )
                    self.custom4_time_trigger = True
            elif self.custom4[ "cycle" ] == 0 and not self.current_day == self.custom4[ "day" ]:
                self.custom4_day_triggerd = False
                self.custom4_time_trigger = False
            elif self.custom4[ "cycle" ] == 1 and ( self.current_time == self.custom4[ "time" ] or ( self.current_time > self.custom4[ "time" ] and self.current_time < ( self.test_time( self.custom4[ "time" ], self.test_interval + self.custom4_delay ) ) ) ) and not self.custom4_time_trigger:
                self.trigger_builtin( self.custom4[ "script" ], "custom4" )
                self.custom4_time_trigger = True
            elif self.custom4[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom4[ "time" ], self.test_interval + 1 ):
                self.custom4_time_trigger = False
            elif self.custom4[ "cycle" ] == 2 and not self.custom4_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 4 Hourly Schedule, every %s Hours" % self.custom4_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom4_triggered = True
                self.custom4_timer_set = True
                self.custom4_timer = Timer( self.custom4[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom4[ "script" ], "custom4" ] )
                self.custom4_timer.setName('Custom4_Timer')
                self.custom4_timer.start()
        if self.custom5[ "enabled"] and not ( ( self.custom5[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom5[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom5[ "cycle" ] == 0 and self.current_day == self.custom5[ "day" ] and not self.custom5_day_triggerd:
                if ( self.current_time == self.custom5[ "time" ] or ( self.current_time > self.custom5[ "time" ] and self.current_time < ( self.test_time( self.custom5[ "time" ], self.test_interval + self.custom5_delay ) ) ) ) and not self.custom5_time_trigger:
                    self.trigger_builtin( self.custom5[ "script" ], "custom5" )
                    self.custom5_time_trigger = True
            elif self.custom5[ "cycle" ] == 0 and not self.current_day == self.custom5[ "day" ]:
                self.custom5_day_triggerd = False
                self.custom5_time_trigger = False
            elif self.custom5[ "cycle" ] == 1 and ( self.current_time == self.custom5[ "time" ] or ( self.current_time > self.custom5[ "time" ] and self.current_time < ( self.test_time( self.custom5[ "time" ], self.test_interval + self.custom5_delay ) ) ) ) and not self.custom5_time_trigger:
                self.trigger_builtin( self.custom5[ "script" ], "custom5" )
                self.custom5_time_trigger = True
            elif self.custom5[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom5[ "time" ], self.test_interval + 1 ):
                self.custom5_time_trigger = False
            elif self.custom5[ "cycle" ] == 2 and not self.custom5_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 5 Hourly Schedule, every %s Hours" % self.custom5_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom5_triggered = True
                self.custom5_timer_set = True
                self.custom5_timer = Timer( self.custom5[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom5[ "script" ], "custom5" ] )
                self.custom5_timer.setName('Custom5_Timer')
                self.custom5_timer.start()
        if self.custom6[ "enabled"] and not ( ( self.custom6[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom6[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom6[ "cycle" ] == 0 and self.current_day == self.custom6[ "day" ] and not self.custom6_day_triggerd:
                if ( self.current_time == self.custom6[ "time" ] or ( self.current_time > self.custom6[ "time" ] and self.current_time < ( self.test_time( self.custom6[ "time" ], self.test_interval + self.custom6_delay ) ) ) ) and not self.custom6_time_trigger:
                    self.trigger_builtin( self.custom6[ "script" ], "custom6" )
                    self.custom6_time_trigger = True
            elif self.custom6[ "cycle" ] == 0 and not self.current_day == self.custom6[ "day" ]:
                self.custom6_day_triggerd = False
                self.custom6_time_trigger = False
            elif self.custom6[ "cycle" ] == 1 and ( self.current_time == self.custom6[ "time" ] or ( self.current_time > self.custom6[ "time" ] and self.current_time < ( self.test_time( self.custom6[ "time" ], self.test_interval + self.custom6_delay ) ) ) ) and not self.custom6_time_trigger:
                self.trigger_builtin( self.custom6[ "script" ], "custom6" )
                self.custom6_time_trigger = True
            elif self.custom6[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom6[ "time" ], self.test_interval + 1):
                self.custom6_time_trigger = False
            elif self.custom6[ "cycle" ] == 2 and not self.custom6_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 6 Hourly Schedule, every %s Hours" % self.custom6_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom6_triggered = True
                self.custom6_timer_set = True
                self.custom6_timer = Timer( self.custom6[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom6[ "script" ], "custom6" ] )
                self.custom6_timer.setName('Custom6_Timer')
                self.custom6_timer.start()
        if self.custom7[ "enabled"] and not ( ( self.custom7[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom7[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom7[ "cycle" ] == 0 and self.current_day == self.custom7[ "day" ] and not self.custom7_day_triggerd:
                if ( self.current_time == self.custom7[ "time" ] or ( self.current_time > self.custom7[ "time" ] and self.current_time < ( self.test_time( self.custom7[ "time" ], self.test_interval + self.custom7_delay ) ) ) ) and not self.custom7_time_trigger:
                    self.trigger_builtin( self.custom7[ "script" ], "custom7" )
                    self.custom7_time_trigger = True
            elif self.custom7[ "cycle" ] == 0 and not self.current_day == self.custom7[ "day" ]:
                self.custom7_day_triggerd = False
                self.custom7_time_trigger = False
            elif self.custom7[ "cycle" ] == 1 and ( self.current_time == self.custom7[ "time" ] or ( self.current_time > self.custom7[ "time" ] and self.current_time < ( self.test_time( self.custom7[ "time" ], self.test_interval + self.custom7_delay ) ) ) ) and not self.custom7_time_trigger:
                self.trigger_builtin( self.custom7[ "script" ], "custom7" )
                self.custom7_time_trigger = True
            elif self.custom7[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom7[ "time" ], self.test_interval + 1 ):
                self.custom7_time_trigger = False
            elif self.custom7[ "cycle" ] == 2 and not self.custom7_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 7 Hourly Schedule, every %s Hours" % self.custom7_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom7_triggered = True
                self.custom7_timer_set = True
                self.custom7_timer = Timer( self.custom7[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom7[ "script" ], "custom7" ] )
                self.custom7_timer.setName('Custom7_Timer')
                self.custom7_timer.start()
        if self.custom8[ "enabled"] and not ( ( self.custom8[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom8[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom8[ "cycle" ] == 0 and self.current_day == self.custom8[ "day" ] and not self.custom8_day_triggerd:
                if ( self.current_time == self.custom8[ "time" ] or ( self.current_time > self.custom8[ "time" ] and self.current_time < ( self.test_time( self.custom8[ "time" ], self.test_interval + self.custom8_delay ) ) ) ) and not self.custom8_time_trigger:
                    self.trigger_builtin( self.custom8[ "script" ], "custom8" )
                    self.custom8_time_trigger = True
            elif self.custom8[ "cycle" ] == 0 and not self.current_day == self.custom8[ "day" ]:
                self.custom8_day_triggerd = False
                self.custom8_time_trigger = False
            elif self.custom8[ "cycle" ] == 1 and ( self.current_time == self.custom8[ "time" ] or ( self.current_time > self.custom8[ "time" ] and self.current_time < ( self.test_time( self.custom8[ "time" ], self.test_interval + self.custom8_delay ) ) ) ) and not self.custom8_time_trigger:
                self.trigger_builtin( self.custom8[ "script" ], "custom8" )
                self.custom8_time_trigger = True
            elif self.custom8[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom8[ "time" ], self.test_interval + 1 ):
                self.custom8_time_trigger = False
            elif self.custom8[ "cycle" ] == 2 and not self.custom8_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 8 Hourly Schedule, every %s Hours" % self.custom8_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom8_triggered = True
                self.custom8_timer_set = True
                self.custom8_timer = Timer( self.custom8[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom8[ "script" ], "custom8" ] )
                self.custom8_timer.setName('Custom8_Timer')
                self.custom8_timer.start()
        if self.custom9[ "enabled"] and not ( ( self.custom9[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom9[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom9[ "cycle" ] == 0 and self.current_day == self.custom9[ "day" ] and not self.custom9_day_triggerd:
                if ( self.current_time == self.custom9[ "time" ] or ( self.current_time > self.custom9[ "time" ] and self.current_time < ( self.test_time( self.custom9[ "time" ], self.test_interval + self.custom9_delay ) ) ) ) and not self.custom9_time_trigger:
                    self.trigger_builtin( self.custom9[ "script" ], "custom9" )
                    self.custom9_time_trigger = True
            elif self.custom9[ "cycle" ] == 0 and not self.current_day == self.custom9[ "day" ]:
                self.custom9_day_triggerd = False
                self.custom9_time_trigger = False
            elif self.custom9[ "cycle" ] == 1 and ( self.current_time == self.custom9[ "time" ] or ( self.current_time > self.custom9[ "time" ] and self.current_time < ( self.test_time( self.custom9[ "time" ], self.test_interval + self.custom9_delay ) ) ) ) and not self.custom9_time_trigger:
                self.trigger_builtin( self.custom9[ "script" ], "custom9" )
                self.custom9_time_trigger = True
            elif self.custom9[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom9[ "time" ], self.test_interval + 1):
                self.custom9_time_trigger = False
            elif self.custom9[ "cycle" ] == 2 and not self.custom9_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 9 Hourly Schedule, every %s Hours" % self.custom9_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom9_triggered = True
                self.custom9_timer_set = True
                self.custom9_timer = Timer( self.custom9[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom9[ "script" ], "custom9" ] )
                self.custom9_timer.setName('Custom9_Timer')
                self.custom9_timer.start()
        if self.custom10[ "enabled"] and not ( ( self.custom10[ "disabled_on_musicscan" ] and self.music_scan ) or ( self.custom10[ "disabled_on_videoscan" ] and self.video_scan ) ):
            if self.custom10[ "cycle" ] == 0 and self.current_day == self.custom10[ "day" ] and not self.custom10_day_triggerd:
                if ( self.current_time == self.custom10[ "time" ] or ( self.current_time > self.custom10[ "time" ] and self.current_time < ( self.test_time( self.custom10[ "time" ], self.test_interval + self.custom10_delay ) ) ) ) and not self.custom10_time_trigger:
                    self.trigger_builtin( self.custom10[ "script" ], "custom10" )
                    self.custom10_time_trigger = True
            elif self.custom10[ "cycle" ] == 0 and not self.current_day == self.custom10[ "day" ]:
                self.custom10_day_triggerd = False
                self.custom10_time_trigger = False
            elif self.custom10[ "cycle" ] == 1 and ( self.current_time == self.custom10[ "time" ] or ( self.current_time > self.custom10[ "time" ] and self.current_time < ( self.test_time( self.custom10[ "time" ], self.test_interval + self.custom10_delay ) ) ) ) and not self.custom10_time_trigger:
                self.trigger_builtin( self.custom10[ "script" ], "custom10" )
                self.custom10_time_trigger = True
            elif self.custom10[ "cycle" ] == 1 and self.current_time > self.test_time( self.custom10[ "time" ], self.test_interval + 1 ):
                self.custom10_time_trigger = False
            elif self.custom10[ "cycle" ] == 2 and not self.custom10_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 10 Hourly Schedule, every %s Hours" % self.custom10_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.custom10_triggered = True
                self.custom10_timer_set = True
                self.custom10_timer = Timer( self.custom10[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.custom10[ "script" ], "custom10" ] )
                self.custom10_timer.setName('Custom10_Timer')
                self.custom10_timer.start()
        if self.video_library[ "enabled"]:
            self.builtin_function = video_library_script
            if self.video_library[ "cycle" ] == 0 and self.current_day == self.video_library[ "day" ] and not self.video_library_day_triggerd:
                if ( self.current_time == self.video_library[ "time" ] or ( self.current_time > self.video_library[ "time" ] and self.current_time < ( self.test_time( self.video_library[ "time" ], self.test_interval ) ) ) ) and not self.video_library_time_trigger:
                    self.trigger_builtin( self.builtin_function, "video" )
                    self.video_library_time_trigger = True
            elif self.video_library[ "cycle" ] == 0 and not self.current_day == self.video_library[ "day" ]:
                self.video_library_day_triggerd = False
                self.video_library_time_trigger = False
            elif self.video_library[ "cycle" ] == 1 and ( self.current_time == self.video_library[ "time" ] or ( self.current_time > self.video_library[ "time" ] and self.current_time < ( self.test_time( self.video_library[ "time" ], self.test_interval + self.video_delay ) ) ) ) and not self.video_library_time_trigger:
                self.trigger_builtin( self.builtin_function, "video" )
                self.video_library_time_trigger = True
            elif self.video_library[ "cycle" ] == 1 and self.current_time > self.test_time( self.video_library[ "time" ], self.test_interval + 1 ):
                self.video_library_time_trigger = False
            elif self.video_library[ "cycle" ] == 2 and not self.video_library_triggered and not self.video_delay:
                xbmc.log( "[service.scheduler] - Starting music Library Hourly Schedule, every %s Hours" % self.video_library_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.video_library_triggered = True
                self.video_library_timer_set = True
                self.video_library_timer = Timer( self.video_library[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.builtin_function, "video" ] )
                self.video_library_timer.setName('Video_Library_Timer')
                self.video_library_timer.start()
        if self.music_library[ "enabled"] and not ( self.cdartmanager_update or self.cdartmanager_running ):
            self.builtin_function = music_library_script
            if self.music_library[ "cycle" ] == 0 and self.current_day == self.music_library[ "day" ] and not self.music_library_day_triggerd:
                if ( self.current_time == self.music_library[ "time" ] or ( self.current_time > self.music_library[ "time" ] and self.current_time < ( self.test_time( self.music_library[ "time" ], self.test_interval + self.music_delay ) ) ) ) and not self.music_library_time_trigger:
                    self.trigger_builtin( self.builtin_function, "music" )
                    self.music_library_time_trigger = True
            elif self.music_library[ "cycle" ] == 0 and not self.current_day == self.music_library[ "day" ]:
                self.music_library_day_triggerd = False
                self.music_library_time_trigger = False
            elif self.music_library[ "cycle" ] == 1 and ( self.current_time == self.music_library[ "time" ] or ( self.current_time > self.music_library[ "time" ] and self.current_time < ( self.test_time( self.music_library[ "time" ], self.test_interval + self.music_delay ) ) ) ) and not self.music_library_time_trigger:
                self.trigger_builtin( self.builtin_function, "music" )
                self.music_library_time_trigger = True
            elif self.music_library[ "cycle" ] == 1 and self.current_time > self.test_time( self.music_library[ "time" ], self.test_interval + 1 ):
                self.music_library_time_trigger = False
            elif self.music_library[ "cycle" ] == 2 and not self.music_library_triggered and not self.music_delay:
                xbmc.log( "[service.scheduler] - Starting music Library Hourly Schedule, every %s Hours" % self.music_library_interval, xbmc.LOGNOTICE )
                xbmc.sleep( 250 )
                self.music_library_triggered = True
                self.music_library_timer_set = True
                self.music_library_timer = Timer( self.music_library[ "interval" ] * hour_multiplier, self.trigger_builtin, [ self.builtin_function, "music" ] )
                self.music_library_timer.setName('Music_Library_Timer')
                self.music_library_timer.start()
                
    def start( self ):
        while (not xbmc.abortRequested):
            if not self._triggered_settings:
                self.set_settings_timer()
            if xbmcgui.Window(10000).getProperty( "cdart_manager_update" ) in ( "False", "True" ):
                self.cdartmanager_update = eval( xbmcgui.Window(10000).getProperty( "cdart_manager_update" ) )
            elif not xbmcgui.Window(10000).getProperty( "cdart_manager_update" ):
                self.cdartmanager_update = False
            if xbmcgui.Window(10000).getProperty( "cdart_manager_running" ) in ( "False", "True" ):
                self.cdartmanager_running = eval( xbmcgui.Window(10000).getProperty( "cdart_manager_running" ) )
            elif not xbmcgui.Window(10000).getProperty( "cdart_manager_running" ):
                self.cdartmanager_running = False
            if xbmc.getCondVisibility('Library.IsScanningVideo'):
                self.video_scan = True
            else:
                self.video_scan = False
            if xbmc.getCondVisibility('Library.IsScanningMusic'):
                self.music_scan = True
            else:
                self.music_scan = False
            if not self.interval:
                xbmc.log( "[service.scheduler] - cdart_manager_running: %s" % ( "False", "True" )[self.cdartmanager_running], xbmc.LOGDEBUG )
                xbmc.log( "[service.scheduler] - cdart_manager_update: %s" % ( "False", "True" )[self.cdartmanager_update], xbmc.LOGDEBUG )
                if self.video_scan:
                    xbmc.log( "[service.scheduler] - Video Library Scan in progress", xbmc.LOGDEBUG )
                if self.music_scan:
                    xbmc.log( "[service.scheduler] - Music Library Scan in progress", xbmc.LOGDEBUG )
                self.current_day = int( time.strftime('%w') )
                self.now = datetime.datetime.now()
                self.current_time = time.strftime( '%H:%M' )
                if not self.current_day == self.previous_day:
                    self.previous_day = self.current_day
                    xbmc.log( "[service.scheduler] - Current Day: %s" % ( "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" )[ self.current_day ], xbmc.LOGDEBUG )
                xbmc.log( "[service.scheduler] - Current Time: %s" % self.current_time, xbmc.LOGDEBUG )
                self.schedule_check()
                self.set_interval_timer()
            xbmc.sleep( 1000 )

if ( __name__ == "__main__" ):
    script = Scheduler()
    script.start()