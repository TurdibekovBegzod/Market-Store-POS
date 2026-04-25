from .barcode import BarcodeRouter
from .scanner import ScannerRouter
from .products import ProductsRouter
from .monitor import MonitorRouter
from .checking import CheckingRouter

class AppRouter:
    def __init__(self, ui):
        self.ui = ui
        self.include_routers()

    def include_routers(self):
        self.barcode = BarcodeRouter(self.ui)
        self.scanner = ScannerRouter(self.ui)
        self.products = ProductsRouter(self.ui)
        self.monitor = MonitorRouter(self.ui)
        self.checking = CheckingRouter(self.ui)

    def route(self, path):
        if path == "/barcode": self.barcode.activate()
        elif path == "/scanner": self.scanner.activate()
        elif path == "/products": self.products.activate()
        elif path == "/monitor": self.monitor.activate()
        elif path == "/checking": self.checking.activate()