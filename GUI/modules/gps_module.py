#####################################################################################
# OSURC (Oregon State University Robotics Club) GPS SLIP MAP                        #
#                                                                                   #
# Author: Austin Dubina                                                             #
# Date: 2/8/2013                                                                    #
#                                                                                   #
# Description: A rendition of the open source osm-gps-map project                   #
# (http://nzjrs.github.com/osm-gps-map/). A PyGTK based program used to graphically #
# display points of interest and the geographical coordinates of the OSU mars rover.#
# This program downloads and caches maps from various open sourced tile servers and #
# displays them in a "slippy map" fashion.                                          #
#                                                                                   # 
# Dependencies: The following must be installed to sucessfully run the app          #
#               -osmgpsmap (sudo apt-get install libosmgpsmap-dev python-osmgpsmap) #
#                                                                                   #
#               -pango                                                              #
#                                                                                   #
#####################################################################################

import sys
import os.path
import gtk
import gobject
import osmgpsmap
import pango
import serial
import time

gobject.threads_init()
gtk.gdk.threads_init()

#Try static lib first
mydir = os.path.dirname(os.path.abspath(__file__))
libdir = os.path.abspath(os.path.join(mydir, "..", "python", ".libs"))
sys.path.insert(0, libdir)


class GpsLayer(gobject.GObject, osmgpsmap.GpsMapLayer):
    def __init__(self):
        gobject.GObject.__init__(self)

    def draw(self, map, drawable):
        pass

    def render(self, map):
        pass

    def button_press(self, map, event):
        return False

gobject.type_register(GpsLayer)

class UI(gtk.Window):
    def __init__(self):

        #POI and Track Lists
        self.track_list = []
        self.poi_list = []
        
        #initialize the window settings
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_default_size(640, 480)
        self.connect('destroy', lambda x: gtk.main_quit())
        self.set_title('OSURC GPS MAP VIEWER')
        self.set_position(gtk.WIN_POS_CENTER)

        #osmgpsmap object
        self.osm = osmgpsmap.GpsMap(repo_uri = "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/#Z/#Y/#X.jpg", show_trip_history = True, record_trip_history = True)
    
        #OSD object
        self.osm.layer_add(osmgpsmap.GpsMapOsd(show_dpad=False, show_zoom=False, show_gps_in_dpad=False))
        self.osm.props.has_tooltip = True

        #Event Monitoring       
        self.osm.connect("button_release_event", self.poi)
        self.osm.connect("query-tooltip", self.on_query_tooltip)

        #regullary timed callback function
        gobject.timeout_add(500, self.print_tiles)

        #initialize gui layout
        self.gui_layout()

    #################################################################################################################
    # intializes the GUI menu layout                                                                                #
    #################################################################################################################   

    def gui_layout(self):
        # Main program VBox layout (adding widgets to window from top down approach)
        self.vbox = gtk.VBox(False, 0)
        self.add(self.vbox)

        #################################################################################################################
        # Menu Bar                                                                                                      #
        #################################################################################################################
        
        mb = gtk.MenuBar()

        # File Menu
        file_menu = gtk.Menu()
        filem = gtk.MenuItem("File")
        filem.set_submenu(file_menu)

        # File Items
        import_list = gtk.MenuItem("Import")
        #import_list.connect("activate", )
        file_menu.append(import_list)

        export_list = gtk.MenuItem("Export")
        #export_list.connect("activate", gtk.)
        file_menu.append(export_list)

        quit = gtk.MenuItem("Quit")
        quit.connect("activate", gtk.main_quit)
        file_menu.append(quit)
        
        mb.append(filem)

        # Map Source Menu
        source_menu = gtk.Menu()
        sourcem = gtk.MenuItem("Map Source")
        sourcem.set_submenu(source_menu)

        # Map Source Items
        sat = gtk.MenuItem("satellite")
        sat.connect("activate", self.load_map_clicked, "http://maptile.maps.svc.ovi.com/maptiler/maptile/newest/satellite.day/#Z/#X/#Y/256/png8", "png")
        source_menu.append(sat)

        hybrid = gtk.MenuItem("Google Hybrid")
        hybrid.connect("activate", self.load_map_clicked, "http://mt1.google.com/vt/lyrs=y&x=#X&y=#Y&z=#Z", "png")
        source_menu.append(hybrid)

        topo = gtk.MenuItem("Topographical")
        topo.connect("activate", self.load_map_clicked, "http://s3-us-west-1.amazonaws.com/caltopo/topo/#Z/#X/#Y.png?v=1", "png")
        source_menu.append(topo)

        topo2 = gtk.MenuItem("Topographical2")
        topo2.connect("activate", self.load_map_clicked, "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/#Z/#Y/#X.jpg", "jpg")
        source_menu.append(topo2)

        mb.append(sourcem)

        self.vbox.pack_start(mb, False, False, 0)

        #################################################################################################################
        #Open street map object                                                                                         #
        #################################################################################################################

        self.vbox.pack_start(self.osm, expand=True, fill=True, padding=0)

        #################################################################################################################
        # Horizontal menu for map navitagtion menu buttons (zoom in, zoom out, home, track list, clear poi, clear track)#
        #################################################################################################################
        self.horz_button_menu = gtk.HBox(False, 0)
        self.vbox.pack_start(self.horz_button_menu, expand=False, fill=False, padding=4)

        zoom_in_button = gtk.Button('Zoom In')
        zoom_in_button.connect('clicked', self.zoom_in_clicked)
        self.horz_button_menu.pack_start(zoom_in_button)
        
        zoom_out_button = gtk.Button('Zoom Out')
        zoom_out_button.connect('clicked', self.zoom_out_clicked)
        self.horz_button_menu.pack_start(zoom_out_button)
        
        home_button = gtk.Button('Home')
        home_button.connect('clicked', self.home_clicked)
        self.horz_button_menu.pack_start(home_button)

        track_list_button = gtk.Button("Print GPS List")
        track_list_button.connect('clicked', self.print_track_list)
        self.horz_button_menu.pack_start(track_list_button)

        clear_poi_button = gtk.Button('Remove POIs')
        clear_poi_button.connect('clicked', self.remove_images)
        self.horz_button_menu.pack_start(clear_poi_button)

        clear_track_button = gtk.Button("Remove Track")
        clear_track_button.connect('clicked', self.clear_track)
        self.horz_button_menu.pack_start(clear_track_button)

        #################################################################################################################
        # horizontal menu for manually adding Lat and Lon cordinates to slip map                                        #
        #################################################################################################################
        self.horz_marker_menu = gtk.HBox(False, 0)
        self.horz_marker_menu.pack_start(gtk.Label("LAT: "), False)
        adj1 = gtk.Adjustment(0.0, -1000.0, 1000.0, 0.5, 100, 0)
        self.lat_spin_button = gtk.SpinButton(adj1, 1.0, 5)
        self.lat_spin_button.set_wrap(True)
        self.lat_spin_button.set_size_request(100, -1)
        self.horz_marker_menu.pack_start(self.lat_spin_button, False, True, 0)

        self.horz_marker_menu.pack_start(gtk.Label("LON: "), False)
        adj2 = gtk.Adjustment(0.0, -1000.0, 1000.0, 0.5, 100, 0)
        self.lon_spin_button = gtk.SpinButton(adj2, 1.0, 5)
        self.lon_spin_button.set_wrap(True)
        self.lon_spin_button.set_size_request(100, -1)
        self.horz_marker_menu.pack_start(self.lon_spin_button, False, True, 0)

        self.clear_entry = gtk.Button('Clear Field')
        self.horz_marker_menu.pack_start(self.clear_entry)
        self.clear_entry.connect('clicked', self.clear_field)

        self.set_poi_marker = gtk.Button('Place Marker')
        self.horz_marker_menu.pack_start(self.set_poi_marker)
        self.set_poi_marker.connect('clicked', self.place_marker)

        self.vbox.pack_start(self.horz_marker_menu, expand=False, fill=False, padding=4)

        self.horz_echo = gtk.HBox()
        self.horz_echo.pack_start(gtk.Label("Tile Monitor: "), False)

        #################################################################################################################
        # Tile monitor and general echo entry                                                                           #
        #################################################################################################################
        self.echo_entry = gtk.Entry()
        self.horz_echo.pack_start(self.echo_entry, expand=True, fill=True)
        self.vbox.pack_start(self.horz_echo, False)

    #################################################################################################################
    # unloads and redraws new gps slip map with newly specified map source                                          #
    #################################################################################################################
    def load_map_clicked(self, event, url, format):
        if self.osm:
            #remove old map
            self.vbox.remove(self.osm)
        try:
            self.osm = osmgpsmap.GpsMap(repo_uri = url,
                                        image_format = format,
                                        show_trip_history = True, 
                                        record_trip_history = True)
            self.osm.layer_add(osmgpsmap.GpsMapOsd(show_dpad=False, show_zoom=False, show_gps_in_dpad=False))
            self.vbox.pack_start(self.osm, expand=True, fill=True, padding=0)
            self.vbox.reorder_child(self.osm, 0)
            self.osm.props.has_tooltip = True
            self.osm.connect('button_release_event', self.poi)
            self.osm.connect("query-tooltip", self.on_query_tooltip)
            self.osm.show()   
            self.redraw_gps()

        except Exception, e:
            print "ERROR:", e
            self.osm = osmgpsmap.GpsMap(map_source = 12, show_trip_history = True, record_trip_history = True)

        if self.track_list:
            length = len(self.track_list)
            lat, lon = self.track_list[length-1]
            self.osm.set_center_and_zoom(lat,lon, 16)
    #################################################################################################################
    # redraws points of intrest and tracks stored in track_list and poi_list after a map reload                     #
    #################################################################################################################
    def redraw_gps(self):
        if self.track_list:
            for val in self.track_list:
                lat, lon = val
                self.osm.gps_add(lat, lon, heading=osmgpsmap.INVALID);

        if self.poi_list:
            pb = gtk.gdk.pixbuf_new_from_file_at_size ("poi.png", 30,20)
            for val in self.poi_list:
                lat, lon = val
                self.osm.image_add(lat,lon,pb)
                
    #################################################################################################################
    # clears the Lat and Lon spin wheel                                                                             #
    #################################################################################################################
    def clear_field(self, osm):
        self.lat_spin_button.set_value(0)
        self.lon_spin_button.set_value(0)

    ##################################################################################################################
    # prints the remaining number of tiles to be downloaded from current map source (located under map expander menu)#
    ##################################################################################################################
    def print_tiles(self):
        if self.osm.props.tiles_queued != 0:
            self.echo_entry.set_text("Downloading %s Tiles" % self.osm.props.tiles_queued)
        else:
            self.echo_entry.set_text("")
        return True

    #################################################################################################################
    # clears gps map of all POIs and removes them from stored list                                                  #
    ################################################################################################################# 
    def remove_images(self, osm):
        self.osm.image_remove_all()
        self.poi_list = []

    #################################################################################################################
    # Adds either POI or Gps Track to map depending on event button caller                                          #
    #################################################################################################################   
    def poi(self, osm, event):
        lat,lon = self.osm.get_event_location(event).get_degrees()
        if event.button == 2:
            self.osm.gps_add(lat, lon, heading=osmgpsmap.INVALID);
            #self.track.add_point(osmgpsmap.point_new_degrees(lat,lon))
            #self.osm.track_add(self.track)
            self.track_list.append([lat,lon])

        elif event.button == 3:
            
            #this forces program to close... why?
            #self.osm.layer_add(GpsLayer())
            GpsLayer()

            pb = gtk.gdk.pixbuf_new_from_file_at_size ("poi.png", 30,20)
            self.osm.image_add(lat,lon,pb)
            self.poi_list.append([lat,lon])

    #################################################################################################################
    # manually add a poi marker to map using Lat and Lon from spin wheel menu                                       #
    #################################################################################################################
    def place_marker(self, event):
        lat = self.lat_spin_button.get_value()
        lon = self.lon_spin_button.get_value()

        pb = gtk.gdk.pixbuf_new_from_file_at_size("poi.png", 30, 20)
        self.osm.image_add(lat, lon, pb)
        self.poi_list.append([lat, lon])

    #################################################################################################################
    # propogate tooltip with lat and lon from event location on map                                                 #
    #################################################################################################################
    def on_query_tooltip(self, widget, x, y, keyboard_tip, tooltip, data=None):
        if keyboard_tip:
            return False

        p = osmgpsmap.point_new_degrees(0.0, 0.0)
        self.osm.convert_screen_to_geographic(x, y, p)
        lat,lon = p.get_degrees()
        self.show_tooltips = True
        tooltip.set_markup("%+.5f, %+.5f" % p.get_degrees())
        tooltip.set_icon_from_stock(gtk.STOCK_HOME, gtk.ICON_SIZE_MENU)
        return True

    def zoom_in_clicked(self, button):
        self.osm.set_zoom(self.osm.props.zoom + 1)

    def zoom_out_clicked(self, button):
        self.osm.set_zoom(self.osm.props.zoom - 1)

    def home_clicked(self, button):
        self.osm.set_center_and_zoom(38.4064050, -110.7922800, 16)

    def cache_clicked(self, button):
        bbox = self.osm.get_bbox()
        self.osm.download_maps(
            *bbox,
            zoom_start=self.osm.props.zoom,
            zoom_end=self.osm.props.max_zoom
        )

    #################################################################################################################
    # prints a list of waypoints from track_list and poi_list (will later replace with text export functionality)   #
    #################################################################################################################
    def print_track_list(self, button):
        if self.track_list:
            print "Track List:"
            for idx, val in enumerate(self.track_list):
                print idx, val
        if self.poi_list:
            print "POI List:"
            for idx, val in enumerate(self.poi_list):
                print idx, val

    def clear_track(self, button):
        self.osm.gps_clear()
        self.track_list = []


l = osmgpsmap.get_default_cache_directory()
print l

if __name__ == "__main__":
    u = UI()
    u.show_all()
    if os.name == "nt": gtk.gdk.threads_enter()
    gtk.main()
    if os.name == "nt": gtk.gdk.threads_leave()
