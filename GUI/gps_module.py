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
        self.osm = osmgpsmap.GpsMap(repo_uri = "http://a.tile.opencyclemap.org/cycle/#Z/#X/#Y.png")
        #self.osm = osmgpsmap.GpsMap(repo_uri = "http://c.tile.stamen.com/toposm-contours/#Z/#X/#Y.png")
        self.osm.layer_add(osmgpsmap.GpsMapOsd(show_dpad=False, show_zoom=False, show_gps_in_dpad=False))
        self.osm.props.has_tooltip = True

        # Main program VBox layout (adding widgets to window from top down approach)
        self.vbox = gtk.VBox(False, 0)
        self.add(self.vbox)
        
        # (first VBox widget) Adding Open street map widget to main window
        self.vbox.pack_start(self.osm, expand=True, fill=True, padding=0)

        #self.latlon_entry = gtk.Entry()
        #self.vbox.pack_start(self.latlon_entry, expand=False, fill=True, padding=0)

        # (second Vbox widget) Hbox widget for map menu buttons (zoom in, zoom out, home, cache, and clear)
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

        cache_button = gtk.Button('Cache')
        cache_button.connect('clicked', self.cache_clicked)
        self.horz_button_menu.pack_start(cache_button)
        
        clear_track_button = gtk.Button('Remove POIs')
        clear_track_button.connect('clicked', self.remove_images)
        self.horz_button_menu.pack_start(clear_track_button)

        # (Third Vbox Entry) Hbox widget menu for manually adding Lat and Lon cordinates to slip map  
        self.horz_marker_menu = gtk.HBox(False, 0)

        self.horz_marker_menu.pack_start(gtk.Label("LAT: "), False)
        adj1 = gtk.Adjustment(0.0, -1000.0, 1000.0, 0.5, 100, 0)
        self.lat_spin_button = gtk.SpinButton(adj1, 1.0, 4)
        self.lat_spin_button.set_wrap(True)
        self.lat_spin_button.set_size_request(100, -1)
        self.horz_marker_menu.pack_start(self.lat_spin_button, False, True, 0)

        self.horz_marker_menu.pack_start(gtk.Label("LON: "), False)
        adj2 = gtk.Adjustment(0.0, -1000.0, 1000.0, 0.5, 100, 0)
        self.lon_spin_button = gtk.SpinButton(adj2, 1.0, 4)
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

        # Expander Menu for custom Map Repositories
        self.ex = gtk.Expander("<b>Map Repository URI</b>")
        self.vbox.pack_start(self.ex, expand=False, fill=False)
        self.ex.props.use_markup = True
        repo_vb = gtk.VBox()
        self.repouri_entry = gtk.Entry()
        self.repouri_entry.set_text(self.osm.props.repo_uri)
        self.image_format_entry = gtk.Entry()
        self.image_format_entry.set_text(self.osm.props.image_format)

        lbl = gtk.Label(
"""
Enter an repository URL to fetch map tiles from in the box below. Special metacharacters may be included in this url

<i>Metacharacters:</i>
\t#X\tMax X location
\t#Y\tMax Y location
\t#Z\tMap zoom (0 = min zoom, fully zoomed out)
\t#S\tInverse zoom (max-zoom - #Z)
\t#Q\tQuadtree encoded tile (qrts)
\t#W\tQuadtree encoded tile (1234)
\t#U\tEncoding not implemeted
\t#R\tRandom integer, 0-4""")
        lbl.props.xalign = 0
        lbl.props.use_markup = True
        lbl.props.wrap = True

        self.ex.add(repo_vb)
        repo_vb.pack_start(lbl, False)

        hb = gtk.HBox()
        hb.pack_start(gtk.Label("URI: "), False)
        hb.pack_start(self.repouri_entry, True)
        repo_vb.pack_start(hb, False)

        hb = gtk.HBox()
        hb.pack_start(gtk.Label("Image Format: "), False)
        hb.pack_start(self.image_format_entry, True)
        repo_vb.pack_start(hb, False)

        gobtn = gtk.Button("Load Map URI")
        #gobtn.connect("clicked", self.load_map_clicked)
        repo_vb.pack_start(gobtn, False)
        
        # (Fourth Vbox Entry) Echo entry widget to display tile downloading status
        self.echo_entry = gtk.Entry()
        self.vbox.pack_start(self.echo_entry, expand=False, fill=True)

        #Event Monitoring       
        #self.osm.connect("motion_notify_event", self.mouse_hover)
        self.osm.connect("button_release_event", self.poi)
        self.osm.connect("query-tooltip", self.on_query_tooltip)

        #regullary timed callback function
        gobject.timeout_add(500, self.print_tiles)

    def clear_field(self, osm):
        self.lat_spin_button.set_value(0)
        self.lon_spin_button.set_value(0)

    def print_tiles(self):
        if self.osm.props.tiles_queued != 0:
            self.echo_entry.set_text("Downloading %s Tiles" % self.osm.props.tiles_queued)
        else:
            self.echo_entry.set_text("")
        return True

    def remove_images(self, osm):
        self.osm.image_remove_all()

    def poi(self, osm, event):
        lat,lon = self.osm.get_event_location(event).get_degrees()
        if event.button == 2:
            self.osm.gps_add(lat, lon, heading=osmgpsmap.INVALID);
        elif event.button == 3:
            pb = gtk.gdk.pixbuf_new_from_file_at_size ("poi.png", 30,20)
            self.osm.image_add(lat,lon,pb)

    def place_marker(self, event):
        lat = self.lat_spin_button.get_value()
        lon = self.lon_spin_button.get_value()

        pb = gtk.gdk.pixbuf_new_from_file_at_size("poi.png", 30, 20)
        self.osm.image_add(lat, lon, pb)

    def on_query_tooltip(self, widget, x, y, keyboard_tip, tooltip, data=None):
        if keyboard_tip:
            return False

        p = osmgpsmap.point_new_degrees(0.0, 0.0)
        self.osm.convert_screen_to_geographic(x, y, p)
        lat,lon = p.get_degrees()
        self.show_tooltips = True
        tooltip.set_markup("%+.4f, %+.4f" % p.get_degrees())
        tooltip.set_icon_from_stock(gtk.STOCK_HOME, gtk.ICON_SIZE_MENU)
        return True

        #Mouse Click on Map Event
    def mouse_hover(self, osm, event):
        lat,lon = self.osm.get_event_location(event).get_degrees()
        #self.latlon_entry.set_text('LAT [%s] LON [%s]' % (lat, lon))

    def zoom_in_clicked(self, button):
        self.osm.set_zoom(self.osm.props.zoom + 1)

    def zoom_out_clicked(self, button):
        self.osm.set_zoom(self.osm.props.zoom - 1)

    def home_clicked(self, button):
        self.osm.set_center_and_zoom(38.4064050, -110.7922800, 20)

    def cache_clicked(self, button):
        bbox = self.osm.get_bbox()
        self.osm.download_maps(
            *bbox,
            zoom_start=self.osm.props.zoom,
            zoom_end=self.osm.props.max_zoom
        )

l = osmgpsmap.get_default_cache_directory()
print l
   
if __name__ == "__main__":
    u = UI()
    u.show_all()
    if os.name == "nt": gtk.gdk.threads_enter()
    gtk.main()
    if os.name == "nt": gtk.gdk.threads_leave()
