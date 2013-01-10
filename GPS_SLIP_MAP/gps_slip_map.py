import sys
import os.path
import gtk
import gobject
import osmgpsmap

gobject.threads_init()
gtk.gdk.threads_init()

#Try static lib first
mydir = os.path.dirname(os.path.abspath(__file__))
libdir = os.path.abspath(os.path.join(mydir, "..", "python", ".libs"))
sys.path.insert(0, libdir)

class UI(gtk.Window):
    def __init__(self):
        #initialize the window settings
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_default_size(640, 480)
        self.connect('destroy', lambda x: gtk.main_quit())
        self.set_title('OSURC GPS MAP VIEWER')
        self.set_position(gtk.WIN_POS_CENTER)

        #creating the osmgpsmap module (changes the default sources from-1)
        self.osm = osmgpsmap.GpsMap(map_source = 12)
        self.osm.layer_add(osmgpsmap.GpsMapOsd(show_dpad=True, show_zoom=True, show_gps_in_dpad=True))

        #Object initialization and Connections
        zoom_in_button = gtk.Button('Zoom In')
        zoom_in_button.connect('clicked', self.zoom_in_clicked)
        
        zoom_out_button = gtk.Button('Zoom Out')
        zoom_out_button.connect('clicked', self.zoom_out_clicked)
        
        home_button = gtk.Button('Home')
        home_button.connect('clicked', self.home_clicked)
        cache_button = gtk.Button('Cache')
        cache_button.connect('clicked', self.cache_clicked)
        
        clear_track_button = gtk.Button('Clear Track')
        clear_track_button.connect('clicked', self.remove_track)
        
        self.combobox = gtk.combo_box_new_text()
        self.combobox.connect('changed', self.set_map_source)
        self.combobox.insert_text(12, "test1")
        self.combobox.insert_text(1, "test2")
        self.combobox.insert_text(2, "test3")
        self.combobox.insert_text(3, "test4")
        self.combobox.insert_text(4, "test5")
        self.combobox.set_active(0)
        
        self.latlon_entry = gtk.Entry()
        self.echo_entry = gtk.Entry()

        #Program Layout
        self.vbox = gtk.VBox(False, 0)
        self.hbox = gtk.HBox(False, 0)
        self.add(self.vbox)
        
        self.vbox.pack_start(self.osm, expand=True, fill=True, padding=0)
        self.vbox.pack_start(self.latlon_entry, expand=False, fill=True, padding=0)
        self.vbox.pack_start(self.hbox, expand=False, fill=False, padding=4)
        
        self.hbox.pack_start(zoom_in_button)
        self.hbox.pack_start(zoom_out_button)
        self.hbox.pack_start(home_button)
        self.hbox.pack_start(cache_button)
        self.hbox.pack_start(clear_track_button)
        self.hbox.pack_start(self.combobox)

        self.vbox.pack_start(self.echo_entry, expand=False, fill=True)
        
        #Event Monitoring       
        self.osm.connect("motion_notify_event", self.mouse_hover)
        self.osm.connect("button_release_event", self.poi)

        #regullary timed callback function
        gobject.timeout_add(500, self.print_tiles)

    def set_map_source(self, combobox):
        active = self.combobox.get_active()
        if self.osm:
            #remove old map
            self.vbox.remove(self.osm)
        try:
            self.osm = osmgpsmap.GpsMap(map_source=active)
        except Exception, e:
            print "ERROR:", e
            self.osm = osmgpsmap.GpsMap()
        self.vbox.pack_start(self.osm, True)
        self.osm.show()


    def print_tiles(self):
        if self.osm.props.tiles_queued != 0:
            self.echo_entry.set_text("%s Tiles Queued" % self.osm.props.tiles_queued)
        else:
            self.echo_entry.set_text("0 Tiles Queued")
        return True

    def remove_track(self, osm):
        self.osm.track_remove_all
        self.osm.gps_clear

    def poi(self, osm, event):
        lat,lon = self.osm.get_event_location(event).get_degrees()
        if event.button == 3:
            self.osm.gps_add(lat, lon, heading=osmgpsmap.INVALID);
        elif event.button == 2:
            pb = gtk.gdk.pixbuf_new_from_file_at_size ("poi.png", 24,24)
            self.osm.image_add(lat,lon,pb)

        #Mouse Click on Map Event
    def mouse_hover(self, osm, event):
        lat,lon = self.osm.get_event_location(event).get_degrees()
        self.latlon_entry.set_text('LAT [%s] LON [%s]' % (lat, lon))

    def zoom_in_clicked(self, button):
        self.osm.set_zoom(self.osm.props.zoom + 1)

    def zoom_out_clicked(self, button):
        self.osm.set_zoom(self.osm.props.zoom - 1)

    def home_clicked(self, button):
        self.osm.set_center_and_zoom(44.5595092773, -123.281433105, 20)

    def cache_clicked(self, button):
        bbox = self.osm.get_bbox()
        self.osm.download_maps(
            *bbox,
            zoom_start=self.osm.props.zoom,
            zoom_end=self.osm.props.max_zoom
        )


   
if __name__ == "__main__":
    u = UI()
    u.show_all()
    if os.name == "nt": gtk.gdk.threads_enter()
    gtk.main()
    if os.name == "nt": gtk.gdk.threads_leave()
