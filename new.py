import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class BrowserTab(QWebEngineView):
    def __init__(self, main_window):
        super(BrowserTab, self).__init__()
        self.main_window = main_window 
        self.setUrl(QUrl('https://loay.space/'))

    def createWindow(self, _type):
        new_tab = BrowserTab(self.main_window)
        self.main_window.add_new_tab_widget(new_tab)
        return new_tab


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Python Browser")
        self.showMaximized()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.setCentralWidget(self.tabs)

        self.add_new_tab(QUrl('https://google.com'), "New Tab")

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(lambda: self.current_tab().back())
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(lambda: self.current_tab().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(lambda: self.current_tab().reload())
        navbar.addAction(reload_btn)

        stop_btn = QAction('Stop', self)
        stop_btn.triggered.connect(lambda: self.current_tab().stop())
        navbar.addAction(stop_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.triggered.connect(self.open_new_tab)
        navbar.addAction(new_tab_btn)

        bookmark_btn = QAction('Bookmark', self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        navbar.addAction(bookmark_btn)

        bookmarks_menu = QMenu('Bookmarks', self)
        self.bookmarks_menu = bookmarks_menu
        navbar.addAction(bookmarks_menu.menuAction())

        zoom_in_btn = QAction('Zoom In', self)
        zoom_in_btn.triggered.connect(self.zoom_in)
        navbar.addAction(zoom_in_btn)

        zoom_out_btn = QAction('Zoom Out', self)
        zoom_out_btn.triggered.connect(self.zoom_out)
        navbar.addAction(zoom_out_btn)

        dark_mode_btn = QAction('Toggle Dark Mode', self)
        dark_mode_btn.triggered.connect(self.toggle_dark_mode)
        navbar.addAction(dark_mode_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.bookmarks = []
        self.dark_mode = False

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl('https://google.com/')

        browser = BrowserTab(self)
        browser.setUrl(qurl)
        browser.urlChanged.connect(self.update_url_bar)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def add_new_tab_widget(self, browser_widget, label="New Tab"):
        # Add a new tab with the given browser widget
        browser_widget.urlChanged.connect(self.update_url_bar)
        i = self.tabs.addTab(browser_widget, label)
        self.tabs.setCurrentIndex(i)

    def current_tab(self):
        return self.tabs.currentWidget()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open_new_tab(self):
        self.add_new_tab()

    def navigate_home(self):
        self.current_tab().setUrl(QUrl('https://google.com/'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        self.current_tab().setUrl(QUrl(url))

    def update_url_bar(self, q=None):
        if isinstance(q, int):
            if self.current_tab() is not None:
                q = self.current_tab().url()
            else:
                return

        if not hasattr(self, 'url_bar') or self.url_bar is None:
            return

        if q is not None:
            self.url_bar.setText(q.toString())
            self.tabs.setTabText(self.tabs.currentIndex(), q.toString())

    def add_bookmark(self):
        url = self.current_tab().url().toString()
        if url not in self.bookmarks:
            self.bookmarks.append(url)
            action = QAction(url, self)
            action.triggered.connect(lambda checked, url=url: self.current_tab().setUrl(QUrl(url)))
            self.bookmarks_menu.addAction(action)

    def zoom_in(self):
        self.current_tab().setZoomFactor(self.current_tab().zoomFactor() + 0.1)

    def zoom_out(self):
        self.current_tab().setZoomFactor(self.current_tab().zoomFactor() - 0.1)

    def toggle_dark_mode(self):
        if self.dark_mode:
            for i in range(self.tabs.count()):
                self.tabs.widget(i).page().setBackgroundColor(Qt.white)
            self.dark_mode = False
        else:
            for i in range(self.tabs.count()):
                self.tabs.widget(i).page().setBackgroundColor(Qt.black)
            self.dark_mode = True


app = QApplication(sys.argv)
QApplication.setApplicationName('Python Browser')
window = MainWindow()
app.exec_()
