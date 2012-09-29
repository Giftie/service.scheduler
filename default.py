import os, traceback, socket, time, sys, datetime
from threading import Timer
import xbmcaddon, xbmc, xbmcgui, xbmcvfs

__addon__            = xbmcaddon.Addon( "service.scheduler" )
__language__         = __addon__.getLocalizedString
__scriptname__       = __addon__.getAddonInfo('name')
__scriptID__         = __addon__.getAddonInfo('id')
__author__           = __addon__.getAddonInfo('author')
__version__          = __addon__.getAddonInfo('version')

true = True
false = False
null = None

cdart_script                     = "RunScript(script.cdartmanager,%s)"
video_library_script             = "UpdateLibrary(video)"
music_library_script             = "UpdateLibrary(music)"
cdartmanager                     = eval( __addon__.getSetting( "cdartmanager" ) )
cdart_update                     = eval( __addon__.getSetting( "cdart_update" ) )
video_library                    = eval( __addon__.getSetting( "video_library" ) )
music_library                    = eval( __addon__.getSetting( "music_library" ) )
custom1                          = eval( __addon__.getSetting( "custom1" ) )
custom2                          = eval( __addon__.getSetting( "custom2" ) )
custom3                          = eval( __addon__.getSetting( "custom3" ) )
custom4                          = eval( __addon__.getSetting( "custom4" ) )
custom5                          = eval( __addon__.getSetting( "custom5" ) )
custom6                          = eval( __addon__.getSetting( "custom6" ) )
custom7                          = eval( __addon__.getSetting( "custom7" ) )
custom8                          = eval( __addon__.getSetting( "custom8" ) )
custom9                          = eval( __addon__.getSetting( "custom9" ) )
custom10                         = eval( __addon__.getSetting( "custom10" ) )
cdart_disable_video              = eval( __addon__.getSetting( "custom10_disable_video" ) )
cdart_update_disable_video       = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom1_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom2_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom3_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom4_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom5_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom6_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom7_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom8_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom9_disable_video            = eval( __addon__.getSetting( "custom10_disable_video" ) )
custom10_disable_video           = eval( __addon__.getSetting( "custom10_disable_video" ) )
cdart_disable_music              = eval( __addon__.getSetting( "custom10_disable_music" ) )
cdart_update_disable_music       = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom1_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom2_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom3_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom4_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom5_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom6_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom7_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom8_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom9_disable_music            = eval( __addon__.getSetting( "custom10_disable_music" ) )
custom10_disable_music           = eval( __addon__.getSetting( "custom10_disable_music" ) )
hour_multiplier                  = 3600  # Normally set to 3600 to convert hours into seconds
if __addon__.getSetting( "default_interval" ) == "true":
    sleep_interval               = 900  # 15 Minutes
    test_interval                = 15
else:
    test_interval                = int( float( __addon__.getSetting( "sleep_interval" ) ) )
    sleep_interval               = test_interval * 60
addon_work_folder                = xbmc.translatePath( __addon__.getAddonInfo('profile') ).decode('utf-8')
log_file_path                    = os.path.join( addon_work_folder, "scheduler.log" )

class Scheduler():
    def __init__( self, *args, **kwargs ):
        self.set_trigger_variables()
        self.load_settings()
        
    def onInit( self ):
        self.start()
    
    def set_trigger_variables( self ):
        self.interval                         = False
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

    def load_settings( self ):
        if cdartmanager:
            self.cdart_mode                  = int( __addon__.getSetting( "cdart_mode" ) ) # available modes autoall(0), autocdart(1), autocover(2), autofanart(3), autologo(4), autothumb(5), autobanner(6)
            self.cdart_cycle                 = int( __addon__.getSetting( "cdart_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.cdart_update_cycle          = int( __addon__.getSetting( "cdart_update_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            if self.cdart_cycle == 0: # If Weekly set day of the week
                self.cdart_day               = int( __addon__.getSetting( "cdart_day" ) )
            if self.cdart_cycle == 0 or self.cdart_cycle == 1: # If Weekly or Daily, set start time
                self.cdart_time              =  __addon__.getSetting( "cdart_time" )
            if self.cdart_cycle == 2: # If Hourly, set hour interval
                self.cdart_interval          = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "cdart_interval" ) ) ]
            if self.cdart_update_cycle == 0: # If Weekly set day of the week
                self.cdart_update_day               = int( __addon__.getSetting( "cdart_update_day" ) )
            if self.cdart_update_cycle == 0 or self.cdart_cycle == 1: # If Weekly or Daily, set start time
                self.cdart_update_time     = __addon__.getSetting( "cdart_update_time" )
            if self.cdart_update_cycle == 2: # If Hourly, set hour interval
                self.cdart_update_interval          = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "cdart_update_interval" ) ) ]
        if video_library:
            self.video_library_cycle         = int( __addon__.getSetting( "video_library_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            if self.video_library_cycle == 0: # If Weekly set day of the week
                self.video_library_day       = int( __addon__.getSetting( "video_library_day" ) )
            if self.video_library_cycle == 0 or self.video_library_cycle == 1: # If Weekly or Daily, set start time
                self.video_library_time        = __addon__.getSetting( "video_library_time" )
            if self.video_library_cycle == 2: # If Hourly, set hour interval
                self.video_library_interval  = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "video_library_interval" ) ) ]
        if music_library:
            self.music_library_cycle         = int( __addon__.getSetting( "music_library_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            if self.music_library_cycle == 0: # If Weekly set day of the week
                self.music_library_day       = int( __addon__.getSetting( "music_library_day" ) )
            if self.music_library_cycle == 0 or self.music_library_cycle == 1: # If Weekly or Daily, set start time
                self.music_library_time        = __addon__.getSetting( "music_library_time" )
            if self.music_library_cycle == 2: # If Hourly, set hour interval
                self.music_library_interval  = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "music_library_interval" ) ) ]
        if custom1:
            self.custom1_cycle               = int( __addon__.getSetting( "custom1_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom1_script              = __addon__.getSetting( "custom1_script" )
            if self.custom1_cycle == 0: # If Weekly set day of the week
                self.custom1_day             = int( __addon__.getSetting( "custom1_day" ) )
            if self.custom1_cycle == 0 or self.custom1_cycle == 1: # If Weekly or Daily, set start time
                self.custom1_time            = __addon__.getSetting( "custom1_time" )
            if self.custom1_cycle == 2: # If Hourly, set hour interval
                self.custom1_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom1_interval" ) ) ]
        if custom2:
            self.custom2_cycle               = int( __addon__.getSetting( "custom2_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom2_script              = __addon__.getSetting( "custom2_script" )
            if self.custom2_cycle == 0: # If Weekly set day of the week
                self.custom2_day             = int( __addon__.getSetting( "custom2_day" ) )
            if self.custom2_cycle == 0 or self.custom2_cycle == 1: # If Weekly or Daily, set start time
                self.custom2_time            = __addon__.getSetting( "custom2_time" )
            if self.custom2_cycle == 2: # If Hourly, set hour interval
                self.custom2_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom2_interval" ) ) ]
        if custom3:
            self.custom3_cycle               = int( __addon__.getSetting( "custom3_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom3_script              = __addon__.getSetting( "custom3_script" )
            if self.custom3_cycle == 0: # If Weekly set day of the week
                self.custom3_day             = int( __addon__.getSetting( "custom3_day" ) )
            if self.custom3_cycle == 0 or self.custom3_cycle == 1: # If Weekly or Daily, set start time
                self.custom3_time            = __addon__.getSetting( "custom3_time" )
            if self.custom3_cycle == 2: # If Hourly, set hour interval
                self.custom3_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom3_interval" ) ) ]
        if custom4:
            self.custom4_cycle               = int( __addon__.getSetting( "custom4_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom4_script              = __addon__.getSetting( "custom4_script" )
            if self.custom4_cycle == 0: # If Weekly set day of the week
                self.custom4_day             = int( __addon__.getSetting( "custom4_day" ) )
            if self.custom4_cycle == 0 or self.custom4_cycle == 1: # If Weekly or Daily, set start time
                self.custom4_time            = __addon__.getSetting( "custom4_time" )
            if self.custom4_cycle == 2: # If Hourly, set hour interval
                self.custom4_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom4_interval" ) ) ]
        if custom5:
            self.custom5_cycle               = int( __addon__.getSetting( "custom5_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom5_script              = __addon__.getSetting( "custom5_script" )
            if self.custom5_cycle == 0: # If Weekly set day of the week
                self.custom5_day             = int( __addon__.getSetting( "custom5_day" ) )
            if self.custom5_cycle == 0 or self.custom5_cycle == 1: # If Weekly or Daily, set start time
                self.custom5_time            = __addon__.getSetting( "custom5_time" )
            if self.custom5_cycle == 2: # If Hourly, set hour interval
                self.custom5_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom5_interval" ) ) ]
        if custom6:
            self.custom6_cycle               = int( __addon__.getSetting( "custom6_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom6_script              = __addon__.getSetting( "custom6_script" )
            if self.custom6_cycle == 0: # If Weekly set day of the week
                self.custom6_day             = int( __addon__.getSetting( "custom6_day" ) )
            if self.custom6_cycle == 0 or self.custom6_cycle == 1: # If Weekly or Daily, set start time
                self.custom6_time            = __addon__.getSetting( "custom6_time" )
            if self.custom6_cycle == 2: # If Hourly, set hour interval
                self.custom6_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom6_interval" ) ) ]
        if custom7:
            self.custom7_cycle               = int( __addon__.getSetting( "custom7_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom7_script              = __addon__.getSetting( "custom7_script" )
            if self.custom7_cycle == 0: # If Weekly set day of the week
                self.custom7_day             = int( __addon__.getSetting( "custom7_day" ) )
            if self.custom7_cycle == 0 or self.custom7_cycle == 1: # If Weekly or Daily, set start time
                self.custom7_time            = __addon__.getSetting( "custom7_time" )
            if self.custom7_cycle == 2: # If Hourly, set hour interval
                self.custom7_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom7_interval" ) ) ]
        if custom8:
            self.custom8_cycle               = int( __addon__.getSetting( "custom8_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom8_script              = __addon__.getSetting( "custom8_script" )
            if self.custom8_cycle == 0: # If Weekly set day of the week
                self.custom8_day             = int( __addon__.getSetting( "custom8_day" ) )
            if self.custom8_cycle == 0 or self.custom8_cycle == 1: # If Weekly or Daily, set start time
                self.custom8_time            = __addon__.getSetting( "custom8_time" )
            if self.custom8_cycle == 2: # If Hourly, set hour interval
                self.custom8_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom8_interval" ) ) ]
        if custom9:
            self.custom9_cycle               = int( __addon__.getSetting( "custom9_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom9_script              = __addon__.getSetting( "custom9_script" )
            if self.custom9_cycle == 0: # If Weekly set day of the week
                self.custom9_day             = int( __addon__.getSetting( "custom9_day" ) )
            if self.custom9_cycle == 0 or self.custom9_cycle == 1: # If Weekly or Daily, set start time
                self.custom9_time            = __addon__.getSetting( "custom9_time" )
            if self.custom9_cycle == 2: # If Hourly, set hour interval
                self.custom9_interval        = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom9_interval" ) ) ]
        if custom10:
            self.custom10_cycle              = int( __addon__.getSetting( "custom10_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
            self.custom10_script             = __addon__.getSetting( "custom10_script" )
            if self.custom10_cycle == 0: # If Weekly set day of the week
                self.custom10_day            = int( __addon__.getSetting( "custom10_day" ) )
            if self.custom10_cycle == 0 or self.custom10_cycle == 1: # If Weekly or Daily, set start time
                self.custom10_time           = __addon__.getSetting( "custom10_time" )
            if self.custom10_cycle == 2: # If Hourly, set hour interval
                self.custom10_interval       = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom10_interval" ) ) ]

    def trigger_builtin( self, builtin_func, mode ):
        xbmc.log( "[service.scheduler] - Mode triggered: %s" % mode, xbmc.LOGNOTICE )
        xbmc.log( "[service.scheduler] - Built-in Function: %s" % builtin_func, xbmc.LOGNOTICE )
        xbmc.executebuiltin( "%s" % builtin_func )
        self.store_log_file( builtin_func, mode )
        if mode == "video":
            self.video_library_triggered      = False
            if self.video_library_timer_set:
                self.video_library_timer.cancel()
                self.video_library_timer_set = False
        elif mode == "music":
            self.music_library_triggered      = False
            if self.music_library_timer_set:
                self.music_library_timer.cancel()
                self.music_library_timer_set = False
        elif mode == "cdart":
            self.cdart_triggered              = False
            self.cdart_delay                  = 0
            self.cdart_update_delay           = 0
            if self.cdart_timer_set:
                self.cdart_timer.cancel()
                self.cdart_timer_set = False
        elif mode == "custom1":
            self.custom1_triggered            = False
            self.custom1_delay                = 0
            if self.custom1_timer_set:
                self.custom1_timer.cancel()
                self.custom1_timer_set = False
        elif mode == "custom2":
            self.custom2_triggered            = False
            self.custom2_delay                = 0
            if self.custom2_timer_set:
                self.custom2_timer.cancel()
                self.custom2_timer_set = False
        elif mode == "custom3":
            self.custom3_triggered            = False
            self.custom3_delay                = 0
            if self.custom3_timer_set:
                self.custom3_timer.cancel()
                self.custom3_timer_set = False
        elif mode == "custom4":
            self.custom4_triggered            = False
            self.custom4_delay                = 0
            if self.custom4_timer_set:
                self.custom4_timer.cancel()
                self.custom4_timer_set = False
        elif mode == "custom5":
            self.custom5_triggered            = False
            self.custom5_delay                = 0
            if self.custom5_timer_set:
                self.custom5_timer.cancel()
                self.custom5_timer_set = False
        elif mode == "custom6":
            self.custom6_triggered            = False
            self.custom6_delay                = 0
            if self.custom6_timer_set:
                self.custom6_timer.cancel()
                self.custom6_timer_set = False
        elif mode == "custom7":
            self.custom7_triggered            = False
            self.custom7_delay                = 0
            if self.custom7_timer_set:
                self.custom7_timer.cancel()
                self.custom7_timer_set = False
        elif mode == "custom8":
            self.custom8_triggered            = False
            self.custom8_delay                = 0
            if self.custom8_timer_set:
                self.custom8_timer.cancel()
                self.custom8_timer_set = False
        elif mode == "custom9":
            self.custom9_triggered            = False
            self.custom9_delay                = 0
            if self.custom9_timer_set:
                self.custom9_timer.cancel()
                self.custom9_timer_set = False
        elif mode == "custom10":
            self.custom10_triggered            = False
            self.custom10_delay                = 0
            if self.custom10_timer_set:
                self.custom10_timer.cancel()
                self.custom10_timer_set = False

    def store_log_file( self, builtin_func, mode ):
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

    def set_interval_timer( self ):
        xbmc.log( "[service.scheduler] - Setting Sleep Interval: %s seconds" % sleep_interval, xbmc.LOGDEBUG )
        self.sleep_timer = Timer( sleep_interval, self.clear_interval,() )
        self.sleep_timer.daemon = True
        self.sleep_timer.start()
        self.interval = True
        
    def test_time( self, value, interval ):
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
        return "%02d:%02d" % ( new_value_hour, new_value_min )
        
    def schedule_check( self ):
        if video_library:
            self.builtin_function = video_library_script
            self.video_scan = True
            if self.video_library_cycle == 0 and self.current_day == self.video_library_day and not self.video_library_day_triggerd:
                if ( self.current_time == self.video_library_time or ( self.current_time > self.video_library_time and self.current_time < ( self.test_time( self.video_library_time, test_interval ) ) ) ) and not self.video_library_time_trigger:
                    self.trigger_builtin( self.builtin_function, "video" )
                    self.video_library_time_trigger = True
            elif self.video_library_cycle == 0 and not self.current_day == self.video_library_day:
                self.video_library_day_triggerd = False
                self.video_library_time_trigger = False
            elif self.video_library_cycle == 1 and ( self.current_time == self.video_library_time or ( self.current_time > self.video_library_time and self.current_time < ( self.test_time( self.video_library_time, test_interval ) ) ) ) and not self.video_library_time_trigger:
                self.trigger_builtin( self.builtin_function, "video" )
                self.video_library_time_trigger = True
            elif self.video_library_cycle == 1 and self.current_time > self.test_time( self.video_library_time, test_interval + 1 ):
                self.video_library_time_trigger = False
            elif self.video_library_cycle == 2 and not self.video_library_triggered:
                xbmc.log( "[service.scheduler] - Starting music Library Hourly Schedule, every %s Hours" % self.video_library_interval, xbmc.LOGNOTICE )
                self.video_library_triggered = True
                self.video_library_timer_set = True
                self.video_library_timer = Timer( self.video_library_interval * hour_multiplier, self.trigger_builtin, [ self.builtin_function, "video" ] )
                self.video_library_timer.setName('Video_Library_Timer')
                self.video_library_timer.start()
        if music_library and not xbmcgui.Window(10000).getProperty( "cdart_manager_triggered" ) == "True":
            self.builtin_function = music_library_script
            self.music_scan = True
            if self.music_library_cycle == 0 and self.current_day == self.music_library_day and not self.music_library_day_triggerd:
                if ( self.current_time == self.music_library_time or ( self.current_time > self.music_library_time and self.current_time < ( self.test_time( self.music_library_time, test_interval ) ) ) ) and not self.music_library_time_trigger:
                    self.trigger_builtin( self.builtin_function, "music" )
                    self.music_library_time_trigger = True
            elif self.music_library_cycle == 0 and not self.current_day == self.music_library_day:
                self.music_library_day_triggerd = False
                self.music_library_time_trigger = False
            elif self.music_library_cycle == 1 and ( self.current_time == self.music_library_time or ( self.current_time > self.music_library_time and self.current_time < ( self.test_time( self.music_library_time, test_interval ) ) ) ) and not self.music_library_time_trigger:
                self.trigger_builtin( self.builtin_function, "music" )
                self.music_library_time_trigger = True
            elif self.music_library_cycle == 1 and self.current_time > self.test_time( self.music_library_time, test_interval + 1 ):
                self.music_library_time_trigger = False
            elif self.music_library_cycle == 2 and not self.music_library_triggered:
                xbmc.log( "[service.scheduler] - Starting music Library Hourly Schedule, every %s Hours" % self.music_library_interval, xbmc.LOGNOTICE )
                self.music_library_triggered = True
                self.music_library_timer_set = True
                self.music_library_timer = Timer( self.music_library_interval * hour_multiplier, self.trigger_builtin, [ self.builtin_function, "music" ] )
                self.music_library_timer.setName('Music_Library_Timer')
                self.music_library_timer.start()
        if cdartmanager and ( ( cdart_disable_music and self.music_scan ) or ( cdart_disable_video and self.video_scan ) ):
            if cdart_disable_music and self.music_scan:
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.cdart_delay, xbmc.LOGNOTICE )
                self.cdart_delay = 60
            if cdart_disable_video and self.video_scan:
                self.cdart_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.cdart_delay, xbmc.LOGNOTICE )
        elif cdartmanager and not ( ( cdart_disable_music and self.music_scan ) or ( cdart_disable_video and self.video_scan ) ) and not xbmcgui.Window(10000).getProperty( "cdart_manager_triggered" ) == "True" and not xbmcgui.Window(10000).getProperty( "cdart_manager_running" ) == "True":
            self.builtin_function = cdart_script % ( "autoall", "autocdart", "autocover", "autofanart", "autologo", "autothumb", "autobanner" )[ self.cdart_mode ]
            if self.cdart_cycle == 0 and self.current_day == self.cdart_day and not self.cdart_day_triggerd:
                if ( self.current_time == self.cdart_time or ( self.current_time > self.cdart_time and self.current_time < ( self.test_time( self.cdart_time, test_interval + self.cdart_delay ) ) ) ) and not self.cdart_time_trigger:
                    self.trigger_builtin( self.builtin_function, "cdart" )
                    self.cdart_time_trigger = True
            elif self.cdart_cycle == 0 and not self.current_day == self.cdart_day:
                self.cdart_day_triggerd = False
                self.cdart_time_trigger = False
            elif self.cdart_cycle == 1 and ( self.current_time == self.cdart_time or ( self.current_time > self.cdart_time and self.current_time < ( self.test_time( self.cdart_time, test_interval + self.cdart_delay ) ) ) ) and not self.cdart_time_trigger:
                self.trigger_builtin( self.builtin_function, "cdart" )
                self.cdart_time_trigger = True
            elif self.cdart_cycle == 1 and self.current_time > self.test_time( self.cdart_time, test_interval + 1 ):
                self.cdart_time_trigger = False
            elif self.cdart_cycle == 2 and not self.cdart_triggered:
                xbmc.log( "[service.scheduler] - Starting cdART Manager Hourly Schedule, every %s Hours" % self.cdart_interval, xbmc.LOGNOTICE )
                self.cdart_triggered = True
                self.cdart_timer_set = True
                self.cdart_timer = Timer( self.cdart_interval * hour_multiplier, self.trigger_builtin, [ self.builtin_function, "cdart" ] )
                self.cdart_timer.setName('cdART_Timer')
                self.cdart_timer.start()
        if cdart_update and ( ( cdart_update_disable_music and self.music_scan ) or ( cdart_update_disable_video and self.video_scan ) ):
            if cdart_update_disable_music and self.music_scan:
                self.cdart_update_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.cdart_update_delay, xbmc.LOGNOTICE )
            if cdart_update_disable_video and self.video_scan:
                self.cdart_update_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.cdart_update_delay, xbmc.LOGNOTICE )
        elif cdart_update and not ( ( cdart_update_disable_music and self.music_scan ) or ( cdart_update_disable_video and self.video_scan ) ) and not xbmcgui.Window(10000).getProperty( "cdart_manager_triggered" ) == "True" and not xbmcgui.Window(10000).getProperty( "cdart_manager_running" ) == "True":
            self.builtin_function = cdart_script % "update"
            if self.cdart_update_cycle == 0 and self.current_day == self.cdart_update_day and not self.cdart_update_day_triggerd:
                if ( self.current_time == self.cdart_update_time or ( self.current_time > self.cdart_update_time and self.current_time < ( self.test_time( self.cdart_update_time, test_interval + self.cdart_update_delay ) ) ) ) and self.cdart_update_time_trigger:
                    self.trigger_builtin( self.builtin_function, "cdart" )
                    self.cdart_update_time_trigger = True
            elif self.cdart_update_cycle == 0 and not self.current_day == self.cdart_update_day:
                self.cdart_update_day_triggerd = False
                self.cdart_update_time_trigger = False
            elif self.cdart_update_cycle == 1 and ( self.current_time == self.cdart_update_time or ( self.current_time > self.cdart_update_time and self.current_time < ( self.test_time( self.cdart_update_time, test_interval + self.cdart_update_delay ) ) ) ) and not self.cdart_update_time_trigger:
                self.trigger_builtin( self.builtin_function, "cdart" )
                self.cdart_update_time_trigger = True
            elif self.cdart_update_cycle == 1 and self.current_time > self.test_time( self.cdart_update_time, test_interval + 1 ):
                self.cdart_update_time_trigger = False
            elif self.cdart_update_cycle == 2 and not self.cdart_update_triggered:
                xbmc.log( "[service.scheduler] - Starting cdART Manager Update Hourly Schedule, every %s Hours" % self.cdart_update_interval, xbmc.LOGNOTICE )
                self.cdart_update_triggered = True
                self.cdart_timer_set = True
                self.cdart_timer = Timer( self.cdart_update_interval * hour_multiplier, self.trigger_builtin, [ self.builtin_function, "cdart" ] )
                self.cdart_timer.setName('cdART_Timer')
                self.cdart_timer.start()
        if custom1 and ( ( custom1_disable_music and self.music_scan ) or ( custom1_disable_video and self.video_scan ) ):
            if custom1_disable_music and self.music_scan:
                self.custom1_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom1_delay, xbmc.LOGNOTICE )
            elif custom1_disable_video and self.video_scan:
                self.custom1_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom1_delay, xbmc.LOGNOTICE )
        elif custom1 and not ( ( custom1_disable_music and self.music_scan ) or ( custom1_disable_video and self.video_scan ) ):
            if self.custom1_cycle == 0 and self.current_day == self.custom1_day and not self.custom1_day_triggerd:
                if ( self.current_time == self.custom1_time or ( self.current_time > self.custom1_time and self.current_time < ( self.test_time( self.custom1_time, test_interval + custom1_delay ) ) ) ) and not self.custom1_time_trigger:
                    self.trigger_builtin( self.custom1_script, "custom1" )
                    self.custom1_time_trigger = True
            elif self.custom1_cycle == 0 and not self.current_day == self.custom1_day:
                self.custom1_day_triggerd = False
                self.custom1_time_trigger = False
            elif self.custom1_cycle == 1 and ( self.current_time == self.custom1_time or ( self.current_time > self.custom1_time and self.current_time < ( self.test_time( self.custom1_time, test_interval + custom1_delay ) ) ) ) and not self.custom1_time_trigger:
                self.trigger_builtin( self.custom1_script, "custom1" )
                self.custom1_time_trigger = True
            elif self.custom1_cycle == 1 and self.current_time > self.test_time( self.custom1_time, test_interval + 1):
                self.custom1_time_trigger = False
            elif self.custom1_cycle == 2 and not self.custom1_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom1_interval, xbmc.LOGNOTICE )
                self.custom1_triggered = True
                self.custom1_timer_set = True
                self.custom1_timer = Timer( self.custom1_interval * hour_multiplier, self.trigger_builtin, [ self.custom1_script, "custom1" ] )
                self.custom1_timer.setName('Custom1_Timer')
                self.custom1_timer.start()
        if custom2 and ( ( custom2_disable_music and self.music_scan ) or ( custom2_disable_video and self.video_scan ) ):
            if custom2_disable_music and self.music_scan:
                self.custom2_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom2_delay, xbmc.LOGNOTICE )
            elif custom2_disable_video and self.video_scan:
                self.custom2_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom2_delay, xbmc.LOGNOTICE )
        elif custom2 and not ( ( custom2_disable_music and self.music_scan ) or ( custom2_disable_video and self.video_scan ) ):
            if self.custom2_cycle == 0 and self.current_day == self.custom2_day and not self.custom2_day_triggerd:
                if ( self.current_time == self.custom2_time or ( self.current_time > self.custom2_time and self.current_time < ( self.test_time( self.custom2_time, test_interval + custom2_delay ) ) ) ) and not self.custom2_time_trigger:
                    self.trigger_builtin( self.custom2_script, "custom2" )
                    self.custom2_time_trigger = True
            elif self.custom2_cycle == 0 and not self.current_day == self.custom2_day:
                self.custom2_day_triggerd = False
                self.custom2_time_trigger = False
            elif self.custom2_cycle == 1 and ( self.current_time == self.custom2_time or ( self.current_time > self.custom2_time and self.current_time < ( self.test_time( self.custom2_time, test_interval + custom2_delay ) ) ) ) and not self.custom2_time_trigger:
                self.trigger_builtin( self.custom2_script, "custom2" )
                self.custom2_time_trigger = True
            elif self.custom2_cycle == 1 and self.current_time > self.test_time( self.custom2_time, test_interval + 1):
                self.custom2_time_trigger = False
            elif self.custom2_cycle == 2 and not self.custom2_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom2_interval, xbmc.LOGNOTICE )
                self.custom2_triggered = True
                self.custom2_timer_set = True
                self.custom2_timer = Timer( self.custom2_interval * hour_multiplier, self.trigger_builtin, [ self.custom2_script, "custom2" ] )
                self.custom2_timer.setName('Custom2_Timer')
                self.custom2_timer.start()
        if custom3 and ( ( custom3_disable_music and self.music_scan ) or ( custom3_disable_video and self.video_scan ) ):
            if custom3_disable_music and self.music_scan:
                self.custom3_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom3_delay, xbmc.LOGNOTICE )
            elif custom3_disable_video and self.video_scan:
                self.custom3_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom3_delay, xbmc.LOGNOTICE )
        elif custom3 and ( ( custom3_disable_music and self.music_scan ) or ( custom3_disable_video and self.video_scan ) ):
            if self.custom3_cycle == 0 and self.current_day == self.custom3_day and not self.custom3_day_triggerd:
                if ( self.current_time == self.custom3_time or ( self.current_time > self.custom3_time and self.current_time < ( self.test_time( self.custom3_time, test_interval + custom3_delay ) ) ) ) and not self.custom3_time_trigger:
                    self.trigger_builtin( self.custom3_script, "custom3" )
                    self.custom3_time_trigger = True
            elif self.custom3_cycle == 0 and not self.current_day == self.custom3_day:
                self.custom3_day_triggerd = False
                self.custom3_time_trigger = False
            elif self.custom3_cycle == 1 and ( self.current_time == self.custom3_time or ( self.current_time > self.custom3_time and self.current_time < ( self.test_time( self.custom3_time, test_interval + custom3_delay ) ) ) ) and not self.custom3_time_trigger:
                self.trigger_builtin( self.custom3_script, "custom3" )
                self.custom3_time_trigger = True
            elif self.custom3_cycle == 1 and self.current_time > self.test_time( self.custom3_time, test_interval + 1 ):
                self.custom3_time_trigger = False
            elif self.custom3_cycle == 2 and not self.custom3_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom3_interval, xbmc.LOGNOTICE )
                self.custom3_triggered = True
                self.custom3_timer_set = True
                self.custom3_timer = Timer( self.custom3_interval * hour_multiplier, self.trigger_builtin, [ self.custom3_script, "custom3" ] )
                self.custom3_timer.setName('Custom3_Timer')
                self.custom3_timer.start()
        if custom4 and ( ( custom4_disable_music and self.music_scan ) or ( custom4_disable_video and self.video_scan ) ):
            if custom4_disable_music and self.music_scan:
                self.custom4_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom4_delay, xbmc.LOGNOTICE )
            elif custom4_disable_video and self.video_scan:
                self.custom4_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom4_delay, xbmc.LOGNOTICE )
        elif custom4 and not ( ( custom4_disable_music and self.music_scan ) or ( custom4_disable_video and self.video_scan ) ):
            if self.custom4_cycle == 0 and self.current_day == self.custom4_day and not self.custom4_day_triggerd:
                if ( self.current_time == self.custom4_time or ( self.current_time > self.custom4_time and self.current_time < ( self.test_time( self.custom4_time, test_interval + custom4_delay ) ) ) ) and not self.custom4_time_trigger:
                    self.trigger_builtin( self.custom4_script, "custom4" )
                    self.custom4_time_trigger = True
            elif self.custom4_cycle == 0 and not self.current_day == self.custom4_day:
                self.custom4_day_triggerd = False
                self.custom4_time_trigger = False
            elif self.custom4_cycle == 1 and ( self.current_time == self.custom4_time or ( self.current_time > self.custom4_time and self.current_time < ( self.test_time( self.custom4_time, test_interval + custom4_delay ) ) ) ) and not self.custom4_time_trigger:
                self.trigger_builtin( self.custom4_script, "custom4" )
                self.custom4_time_trigger = True
            elif self.custom4_cycle == 1 and self.current_time > self.test_time( self.custom4_time, test_interval + 1 ):
                self.custom4_time_trigger = False
            elif self.custom4_cycle == 2 and not self.custom4_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom4_interval, xbmc.LOGNOTICE )
                self.custom4_triggered = True
                self.custom4_timer_set = True
                self.custom4_timer = Timer( self.custom4_interval * hour_multiplier, self.trigger_builtin, [ self.custom4_script, "custom4" ] )
                self.custom4_timer.setName('Custom4_Timer')
                self.custom4_timer.start()
        if custom5 and ( ( custom5_disable_music and self.music_scan ) or ( custom5_disable_video and self.video_scan ) ):
            if custom5_disable_music and self.music_scan:
                self.custom5_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom5_delay, xbmc.LOGNOTICE )
            elif custom5_disable_video and self.video_scan:
                self.custom5_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom5_delay, xbmc.LOGNOTICE )
        elif custom5 and not ( ( custom5_disable_music and self.music_scan ) or ( custom5_disable_video and self.video_scan ) ):
            if self.custom5_cycle == 0 and self.current_day == self.custom5_day and not self.custom5_day_triggerd:
                if ( self.current_time == self.custom5_time or ( self.current_time > self.custom5_time and self.current_time < ( self.test_time( self.custom5_time, test_interval + custom5_delay ) ) ) ) and not self.custom5_time_trigger:
                    self.trigger_builtin( self.custom5_script, "custom5" )
                    self.custom5_time_trigger = True
            elif self.custom5_cycle == 0 and not self.current_day == self.custom5_day:
                self.custom5_day_triggerd = False
                self.custom5_time_trigger = False
            elif self.custom5_cycle == 1 and ( self.current_time == self.custom5_time or ( self.current_time > self.custom5_time and self.current_time < ( self.test_time( self.custom5_time, test_interval + custom5_delay ) ) ) ) and not self.custom5_time_trigger:
                self.trigger_builtin( self.custom5_script, "custom5" )
                self.custom5_time_trigger = True
            elif self.custom5_cycle == 1 and self.current_time > self.test_time( self.custom5_time, test_interval + 1 ):
                self.custom5_time_trigger = False
            elif self.custom5_cycle == 2 and not self.custom5_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom5_interval, xbmc.LOGNOTICE )
                self.custom5_triggered = True
                self.custom5_timer_set = True
                self.custom5_timer = Timer( self.custom5_interval * hour_multiplier, self.trigger_builtin, [ self.custom5_script, "custom5" ] )
                self.custom5_timer.setName('Custom5_Timer')
                self.custom5_timer.start()
        if custom6 and ( ( custom6_disable_music and self.music_scan ) or ( custom6_disable_video and self.video_scan ) ):
            if custom6_disable_music and self.music_scan:
                self.custom6_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom6_delay, xbmc.LOGNOTICE )
            elif custom6_disable_video and self.video_scan:
                self.custom6_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom6_delay, xbmc.LOGNOTICE )
        elif custom6 and not ( ( custom6_disable_music and self.music_scan ) or ( custom6_disable_video and self.video_scan ) ):
            if self.custom6_cycle == 0 and self.current_day == self.custom6_day and not self.custom6_day_triggerd:
                if ( self.current_time == self.custom6_time or ( self.current_time > self.custom6_time and self.current_time < ( self.test_time( self.custom6_time, test_interval + custom6_delay ) ) ) ) and not self.custom6_time_trigger:
                    self.trigger_builtin( self.custom6_script, "custom6" )
                    self.custom6_time_trigger = True
            elif self.custom6_cycle == 0 and not self.current_day == self.custom6_day:
                self.custom6_day_triggerd = False
                self.custom6_time_trigger = False
            elif self.custom6_cycle == 1 and ( self.current_time == self.custom6_time or ( self.current_time > self.custom6_time and self.current_time < ( self.test_time( self.custom6_time, test_interval + custom6_delay ) ) ) ) and not self.custom6_time_trigger:
                self.trigger_builtin( self.custom6_script, "custom6" )
                self.custom6_time_trigger = True
            elif self.custom6_cycle == 1 and self.current_time > self.test_time( self.custom6_time, test_interval + 1):
                self.custom6_time_trigger = False
            elif self.custom6_cycle == 2 and not self.custom6_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom6_interval, xbmc.LOGNOTICE )
                self.custom6_triggered = True
                self.custom6_timer_set = True
                self.custom6_timer = Timer( self.custom6_interval * hour_multiplier, self.trigger_builtin, [ self.custom6_script, "custom6" ] )
                self.custom6_timer.setName('Custom6_Timer')
                self.custom6_timer.start()
        if custom7 and ( ( custom7_disable_music and self.music_scan ) or ( custom7_disable_video and self.video_scan ) ):
            if custom7_disable_music and self.music_scan:
                self.custom7_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom7_delay, xbmc.LOGNOTICE )
            elif custom7_disable_video and self.video_scan:
                self.custom7_delay = 60
                xbmc.log( "[service.scheduler] - Library Library Scan in Progress, delaying %s Minutes " % self.custom7_delay, xbmc.LOGNOTICE )
        elif custom7 and not ( ( custom7_disable_music and self.music_scan ) or ( custom7_disable_video and self.video_scan ) ):
            if self.custom7_cycle == 0 and self.current_day == self.custom7_day and not self.custom7_day_triggerd:
                if ( self.current_time == self.custom7_time or ( self.current_time > self.custom7_time and self.current_time < ( self.test_time( self.custom7_time, test_interval + custom7_delay ) ) ) ) and not self.custom7_time_trigger:
                    self.trigger_builtin( self.custom7_script, "custom7" )
                    self.custom7_time_trigger = True
            elif self.custom7_cycle == 0 and not self.current_day == self.custom7_day:
                self.custom7_day_triggerd = False
                self.custom7_time_trigger = False
            elif self.custom7_cycle == 1 and ( self.current_time == self.custom7_time or ( self.current_time > self.custom7_time and self.current_time < ( self.test_time( self.custom7_time, test_interval + custom7_delay ) ) ) ) and not self.custom7_time_trigger:
                self.trigger_builtin( self.custom7_script, "custom7" )
                self.custom7_time_trigger = True
            elif self.custom7_cycle == 1 and self.current_time > self.test_time( self.custom7_time, test_interval + 1 ):
                self.custom7_time_trigger = False
            elif self.custom7_cycle == 2 and not self.custom7_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom7_interval, xbmc.LOGNOTICE )
                self.custom7_triggered = True
                self.custom7_timer_set = True
                self.custom7_timer = Timer( self.custom7_interval * hour_multiplier, self.trigger_builtin, [ self.custom7_script, "custom7" ] )
                self.custom7_timer.setName('Custom7_Timer')
                self.custom7_timer.start()
        if custom8 and ( ( custom8_disable_music and self.music_scan ) or ( custom8_disable_video and self.video_scan ) ):
            if custom8_disable_music and self.music_scan:
                self.custom8_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom8_delay, xbmc.LOGNOTICE )
            elif custom8_disable_video and self.video_scan:
                self.custom8_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom8_delay, xbmc.LOGNOTICE )
        elif custom8 and not ( ( custom8_disable_music and self.music_scan ) or ( custom8_disable_video and self.video_scan ) ):
            if self.custom8_cycle == 0 and self.current_day == self.custom8_day and not self.custom8_day_triggerd:
                if ( self.current_time == self.custom8_time or ( self.current_time > self.custom8_time and self.current_time < ( self.test_time( self.custom8_time, test_interval + custom8_delay ) ) ) ) and not self.custom8_time_trigger:
                    self.trigger_builtin( self.custom8_script, "custom8" )
                    self.custom8_time_trigger = True
            elif self.custom8_cycle == 0 and not self.current_day == self.custom8_day:
                self.custom8_day_triggerd = False
                self.custom8_time_trigger = False
            elif self.custom8_cycle == 1 and ( self.current_time == self.custom8_time or ( self.current_time > self.custom8_time and self.current_time < ( self.test_time( self.custom8_time, test_interval + custom8_delay ) ) ) ) and not self.custom8_time_trigger:
                self.trigger_builtin( self.custom8_script, "custom8" )
                self.custom8_time_trigger = True
            elif self.custom8_cycle == 1 and self.current_time > self.test_time( self.custom8_time, test_interval + 1 ):
                self.custom8_time_trigger = False
            elif self.custom8_cycle == 2 and not self.custom8_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom8_interval, xbmc.LOGNOTICE )
                self.custom8_triggered = True
                self.custom8_timer_set = True
                self.custom8_timer = Timer( self.custom8_interval * hour_multiplier, self.trigger_builtin, [ self.custom8_script, "custom8" ] )
                self.custom8_timer.setName('Custom8_Timer')
                self.custom8_timer.start()
        if custom9 and ( ( custom9_disable_music and self.music_scan ) or ( custom9_disable_video and self.video_scan ) ):
            if custom9_disable_music and self.music_scan:
                self.custom9_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom9_delay, xbmc.LOGNOTICE )
            elif custom9_disable_video and self.video_scan:
                self.custom9_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom9_delay, xbmc.LOGNOTICE )
        elif custom9 and not ( ( custom9_disable_music and self.music_scan ) or ( custom9_disable_video and self.video_scan ) ):
            if self.custom9_cycle == 0 and self.current_day == self.custom9_day and not self.custom9_day_triggerd:
                if ( self.current_time == self.custom9_time or ( self.current_time > self.custom9_time and self.current_time < ( self.test_time( self.custom9_time, test_interval + custom9_delay ) ) ) ) and not self.custom9_time_trigger:
                    self.trigger_builtin( self.custom9_script, "custom9" )
                    self.custom9_time_trigger = True
            elif self.custom9_cycle == 0 and not self.current_day == self.custom9_day:
                self.custom9_day_triggerd = False
                self.custom9_time_trigger = False
            elif self.custom9_cycle == 1 and ( self.current_time == self.custom9_time or ( self.current_time > self.custom9_time and self.current_time < ( self.test_time( self.custom9_time, test_interval + custom9_delay ) ) ) ) and not self.custom9_time_trigger:
                self.trigger_builtin( self.custom9_script, "custom9" )
                self.custom9_time_trigger = True
            elif self.custom9_cycle == 1 and self.current_time > self.test_time( self.custom9_time, test_interval + 1):
                self.custom9_time_trigger = False
            elif self.custom9_cycle == 2 and not self.custom9_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom9_interval, xbmc.LOGNOTICE )
                self.custom9_triggered = True
                self.custom9_timer_set = True
                self.custom9_timer = Timer( self.custom9_interval * hour_multiplier, self.trigger_builtin, [ self.custom9_script, "custom9" ] )
                self.custom9_timer.setName('Custom9_Timer')
                self.custom9_timer.start()
        if custom10 and ( ( custom10_disable_music and self.music_scan ) or ( custom10_disable_video and self.video_scan ) ):
            if custom10_disable_music and self.music_scan:
                self.custom10_delay = 60
                xbmc.log( "[service.scheduler] - Music Library Scan in Progress, delaying %s Minutes " % self.custom10_delay, xbmc.LOGNOTICE )
            elif ( custom10_disable_video and self.video_scan ):
                self.custom10_delay = 60
                xbmc.log( "[service.scheduler] - Video Library Scan in Progress, delaying %s Minutes " % self.custom10_delay, xbmc.LOGNOTICE )
        elif custom10 and not ( ( custom10_disable_music and self.music_scan ) or ( custom10_disable_video and self.video_scan ) ):
            if self.custom10_cycle == 0 and self.current_day == self.custom10_day and not self.custom10_day_triggerd:
                if ( self.current_time == self.custom10_time or ( self.current_time > self.custom10_time and self.current_time < ( self.test_time( self.custom10_time, test_interval ) ) ) ) and not self.custom10_time_trigger:
                    self.trigger_builtin( self.custom10_script, "custom10" )
                    self.custom10_time_trigger = True
            elif self.custom10_cycle == 0 and not self.current_day == self.custom10_day:
                self.custom10_day_triggerd = False
                self.custom10_time_trigger = False
            elif self.custom10_cycle == 1 and ( self.current_time == self.custom10_time or ( self.current_time > self.custom10_time and self.current_time < ( self.test_time( self.custom10_time, test_interval ) ) ) ) and not self.custom10_time_trigger:
                self.trigger_builtin( self.custom10_script, "custom10" )
                self.custom10_time_trigger = True
            elif self.custom10_cycle == 1 and self.current_time > self.test_time( self.custom10_time, test_interval + 1 ):
                self.custom10_time_trigger = False
            elif self.custom10_cycle == 2 and not self.custom10_triggered:
                xbmc.log( "[service.scheduler] - Starting Custom 1 Hourly Schedule, every %s Hours" % self.custom10_interval, xbmc.LOGNOTICE )
                self.custom10_triggered = True
                self.custom10_timer_set = True
                self.custom10_timer = Timer( self.custom10_interval * hour_multiplier, self.trigger_builtin, [ self.custom10_script, "custom10" ] )
                self.custom10_timer.setName('Custom10_Timer')
                self.custom10_timer.start()
                
    def start( self ):
        while (not xbmc.abortRequested):
            if xbmc.getCondVisibility('Library.IsScanningVideo'):
                self.video_scan = True
            else:
                self.video_scan = False
            if xbmc.getCondVisibility('Library.IsScanningMusic'):
                self.music_scan = True
            else:
                self.music_scan = False
            if not self.interval:
                xbmc.log( "[service.scheduler] - cdart_manager_running: %s" % xbmcgui.Window(10000).getProperty( "cdart_manager_running" ), xbmc.LOGDEBUG )
                xbmc.log( "[service.scheduler] - cdart_manager_triggered: %s" % xbmcgui.Window(10000).getProperty( "cdart_manager_triggered" ), xbmc.LOGDEBUG )
                if self.video_scan:
                    xbmc.log( "[service.scheduler] - Video Library Scan in progress", xbmc.LOGDEBUG )
                if self.music_scan:
                    xbmc.log( "[service.scheduler] - Music Library Scan in progress", xbmc.LOGDEBUG )
                self.current_day = int( time.strftime('%w') )
                self.now = datetime.datetime.now()
                self.current_time = time.strftime( '%H:%M' )
                if not self.current_day == self.previous_day:
                    self.previous_day = self.current_day
                    xbmc.log( "[service.scheduler] - Current Day: %s" % ( "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")[ self.current_day ], xbmc.LOGDEBUG )
                xbmc.log( "[service.scheduler] - Current Time: %s" % self.current_time, xbmc.LOGDEBUG )
                self.schedule_check()
                self.set_interval_timer()
            xbmc.sleep( 1000 )

if ( __name__ == "__main__" ):
    script = Scheduler()
    script.start()