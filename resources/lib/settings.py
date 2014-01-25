# -*- coding: utf-8 -*- 
import sys, os, traceback, re
import xbmcgui, xbmc, xbmcaddon, xbmcvfs

__addon__                = sys.modules[ "__main__" ].__addon__
__language__             = sys.modules[ "__main__" ].__language__
__scriptname__           = sys.modules[ "__main__" ].__scriptname__
__scriptID__             = sys.modules[ "__main__" ].__scriptID__
__author__               = sys.modules[ "__main__" ].__author__
__version__              = sys.modules[ "__main__" ].__version__
BASE_CURRENT_SOURCE_PATH = sys.modules[ "__main__" ].BASE_CURRENT_SOURCE_PATH
BASE_RESOURCE_PATH       = sys.modules[ "__main__" ].BASE_RESOURCE_PATH
settings_path            = os.path.join( BASE_CURRENT_SOURCE_PATH, "settings.xml" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import utils

true = True
false = False
null = None

class settings():
    def __init__( self, *args, **kwargs ):
        utils.log( 'settings() - __init__' )
        self.start()
      
    def start( self ):
        utils.log('settings() - start')
        self.setting_values = self.read_settings_xml()
        self.addon_work_folder                = xbmc.translatePath( __addon__.getAddonInfo('profile') ).decode('utf-8')
        self.log_file_path                    = os.path.join( addon_work_folder, "scheduler.log" )
        self.enable_logging                   = eval( __addon__.getSetting( "enable_logging" ) )
        self.cdartmanager                     = eval( __addon__.getSetting( "cdartmanager" ) )
        self.cdart_update                     = eval( __addon__.getSetting( "cdart_update" ) )
        self.video_library                    = eval( __addon__.getSetting( "video_library" ) )
        self.music_library                    = eval( __addon__.getSetting( "music_library" ) )
        self.custom1                          = eval( __addon__.getSetting( "custom1" ) )
        self.custom2                          = eval( __addon__.getSetting( "custom2" ) )
        self.custom3                          = eval( __addon__.getSetting( "custom3" ) )
        self.custom4                          = eval( __addon__.getSetting( "custom4" ) )
        self.custom5                          = eval( __addon__.getSetting( "custom5" ) )
        self.custom6                          = eval( __addon__.getSetting( "custom6" ) )
        self.custom7                          = eval( __addon__.getSetting( "custom7" ) )
        self.custom8                          = eval( __addon__.getSetting( "custom8" ) )
        self.custom9                          = eval( __addon__.getSetting( "custom9" ) )
        self.custom10                         = eval( __addon__.getSetting( "custom10" ) )
        self.cdart_disable_video              = eval( __addon__.getSetting( "cdart_disable_video" ) )
        self.cdart_update_disable_video       = eval( __addon__.getSetting( "cdart_update_disable_video" ) )
        self.custom1_disable_video            = eval( __addon__.getSetting( "custom1_disable_video" ) )
        self.custom2_disable_video            = eval( __addon__.getSetting( "custom2_disable_video" ) )
        self.custom3_disable_video            = eval( __addon__.getSetting( "custom3_disable_video" ) )
        self.custom4_disable_video            = eval( __addon__.getSetting( "custom4_disable_video" ) )
        self.custom5_disable_video            = eval( __addon__.getSetting( "custom5_disable_video" ) )
        self.custom6_disable_video            = eval( __addon__.getSetting( "custom6_disable_video" ) )
        self.custom7_disable_video            = eval( __addon__.getSetting( "custom7_disable_video" ) )
        self.custom8_disable_video            = eval( __addon__.getSetting( "custom8_disable_video" ) )
        self.custom9_disable_video            = eval( __addon__.getSetting( "custom9_disable_video" ) )
        self.custom10_disable_video           = eval( __addon__.getSetting( "custom10_disable_video" ) )
        self.cdart_disable_music              = eval( __addon__.getSetting( "cdart_disable_music" ) )
        self.cdart_update_disable_music       = eval( __addon__.getSetting( "cdart_update_disable_music" ) )
        self.custom1_disable_music            = eval( __addon__.getSetting( "custom1_disable_music" ) )
        self.custom2_disable_music            = eval( __addon__.getSetting( "custom2_disable_music" ) )
        self.custom3_disable_music            = eval( __addon__.getSetting( "custom3_disable_music" ) )
        self.custom4_disable_music            = eval( __addon__.getSetting( "custom4_disable_music" ) )
        self.custom5_disable_music            = eval( __addon__.getSetting( "custom5_disable_music" ) )
        self.custom6_disable_music            = eval( __addon__.getSetting( "custom6_disable_music" ) )
        self.custom7_disable_music            = eval( __addon__.getSetting( "custom7_disable_music" ) )
        self.custom8_disable_music            = eval( __addon__.getSetting( "custom8_disable_music" ) )
        self.custom9_disable_music            = eval( __addon__.getSetting( "custom9_disable_music" ) )
        self.custom10_disable_music           = eval( __addon__.getSetting( "custom10_disable_music" ) )
        if __addon__.getSetting( "default_interval" ) == "true":
            self.sleep_interval               = 900  # 15 Minutes
            self.test_interval                = 15   # number of minutes
        else:
            self.test_interval                = int( float( __addon__.getSetting( "sleep_interval" ) ) )
            self.sleep_interval               = test_interval * 60
        self.setting_interval                 = 86400 # interval to reload settings.  86400 seconds = 24 hours
        self.hour_multiplier                  = 3600  # Normally set to 3600 to convert hours into seconds
        self.cdart_time_delay                 = test_interval
        self.cdart_update_time_delay          = 15    # In minutes
        self.music_time_delay                 = 60    # In minutes
        self.video_time_delay                 = 60    # In minutes
        self.general_time_delay               = 60    # In minutes
        self.cdart_mode                  = int( __addon__.getSetting( "cdart_mode" ) ) # available modes autoall(0), autocdart(1), autocover(2), autofanart(3), autologo(4), autothumb(5), autobanner(6)
        self.cdart_cycle                 = int( __addon__.getSetting( "cdart_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.cdart_update_cycle          = int( __addon__.getSetting( "cdart_update_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.cdart_day                   = int( __addon__.getSetting( "cdart_day" ) )
        self.cdart_time                  =  __addon__.getSetting( "cdart_time" )
        self.cdart_interval              = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "cdart_interval" ) ) ]
        self.cdart_update_day            = int( __addon__.getSetting( "cdart_update_day" ) )
        self.cdart_update_time           = __addon__.getSetting( "cdart_update_time" )
        self.cdart_update_interval       = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "cdart_update_interval" ) ) ]
        self.video_library_cycle         = int( __addon__.getSetting( "video_library_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.video_library_day           = int( __addon__.getSetting( "video_library_day" ) )
        self.video_library_time          = __addon__.getSetting( "video_library_time" )
        self.video_library_interval      = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "video_library_interval" ) ) ]
        self.music_library_cycle         = int( __addon__.getSetting( "music_library_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.music_library_day           = int( __addon__.getSetting( "music_library_day" ) )
        self.music_library_time          = __addon__.getSetting( "music_library_time" )
        self.music_library_interval      = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "music_library_interval" ) ) ]
        self.custom1_cycle               = int( __addon__.getSetting( "custom1_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom1_script              = __addon__.getSetting( "custom1_script" )
        self.custom1_day                 = int( __addon__.getSetting( "custom1_day" ) )
        self.custom1_time                = __addon__.getSetting( "custom1_time" )
        self.custom1_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom1_interval" ) ) ]
        self.custom2_cycle               = int( __addon__.getSetting( "custom2_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom2_script              = __addon__.getSetting( "custom2_script" )
        self.custom2_day                 = int( __addon__.getSetting( "custom2_day" ) )
        self.custom2_time                = __addon__.getSetting( "custom2_time" )
        self.custom2_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom2_interval" ) ) ]
        self.custom3_cycle               = int( __addon__.getSetting( "custom3_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom3_script              = __addon__.getSetting( "custom3_script" )
        self.custom3_day                 = int( __addon__.getSetting( "custom3_day" ) )
        self.custom3_time                = __addon__.getSetting( "custom3_time" )
        self.custom3_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom3_interval" ) ) ]
        self.custom4_cycle               = int( __addon__.getSetting( "custom4_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom4_script              = __addon__.getSetting( "custom4_script" )
        self.custom4_day                 = int( __addon__.getSetting( "custom4_day" ) )
        self.custom4_time                = __addon__.getSetting( "custom4_time" )
        self.custom4_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom4_interval" ) ) ]
        self.custom5_cycle               = int( __addon__.getSetting( "custom5_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom5_script              = __addon__.getSetting( "custom5_script" )
        self.custom5_day                 = int( __addon__.getSetting( "custom5_day" ) )
        self.custom5_time                = __addon__.getSetting( "custom5_time" )
        self.custom5_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom5_interval" ) ) ]
        self.custom6_cycle               = int( __addon__.getSetting( "custom6_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom6_script              = __addon__.getSetting( "custom6_script" )
        self.custom6_day                 = int( __addon__.getSetting( "custom6_day" ) )
        self.custom6_time                = __addon__.getSetting( "custom6_time" )
        self.custom6_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom6_interval" ) ) ]
        self.custom7_cycle               = int( __addon__.getSetting( "custom7_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom7_script              = __addon__.getSetting( "custom7_script" )
        self.custom7_day                 = int( __addon__.getSetting( "custom7_day" ) )
        self.custom7_time                = __addon__.getSetting( "custom7_time" )
        self.custom7_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom7_interval" ) ) ]
        self.custom8_cycle               = int( __addon__.getSetting( "custom8_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom8_script              = __addon__.getSetting( "custom8_script" )
        self.custom8_day                 = int( __addon__.getSetting( "custom8_day" ) )
        self.custom8_time                = __addon__.getSetting( "custom8_time" )
        self.custom8_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom8_interval" ) ) ]
        self.custom9_cycle               = int( __addon__.getSetting( "custom9_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom9_script              = __addon__.getSetting( "custom9_script" )
        self.custom9_day                 = int( __addon__.getSetting( "custom9_day" ) )
        self.custom9_time                = __addon__.getSetting( "custom9_time" )
        self.custom9_interval            = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom9_interval" ) ) ]
        self.custom10_cycle              = int( __addon__.getSetting( "custom10_cycle" ) ) # intervals - Weekly(0), Daily(1), Hourly(2)
        self.custom10_script             = __addon__.getSetting( "custom10_script" )
        self.custom10_day                = int( __addon__.getSetting( "custom10_day" ) )
        self.custom10_time               = __addon__.getSetting( "custom10_time" )
        self.custom10_interval           = ( 1, 2, 4, 8, 12 )[ int( __addon__.getSetting( "custom10_interval" ) ) ]

    def read_settings_xml( self ):
        setting_values = {}
        try:
            utils.log( "Reading settings.xml" )
            settings_file = xbmcvfs.File( settings_path ).read()
            settings_list = settings_file.replace("<settings>\n","").replace("</settings>\n","").split("/>\n")
            for setting in settings_list:
                match = re.search('    <setting id="(.*?)" value="(.*?)"', setting)
                if match:
                    setting_values[ match.group( 1 ) ] =  match.group( 2 ) 
                else:
                    match = re.search("""    <setting id="(.*?)" value='(.*?)'""", setting)
                    if match:
                        setting_values[ match.group( 1 ) ] =  match.group( 2 )
        except:
            traceback.print_exc()
        return setting_values
        
    def settings_to_log( self ):
        try:
            utils.log( "Settings" )
            setting_values = self.read_settings_xml()
            for k, v in sorted( setting_values.items() ):
                utils.log( "%30s: %s" % ( k, str( utils.unescape( v.decode('utf-8', 'ignore') ) ) ) )
        except:
            traceback.print_exc()
            
    def store_settings( self ):
        try:
            utils.log( "Storing Settings" )
            setting_values = self.read_settings_xml()
            for k, v in sorted( setting_values.items() ):
                __addon__.setSetting( id=k, value=v )
        except:
            traceback.print_exc()
        return True
            
        