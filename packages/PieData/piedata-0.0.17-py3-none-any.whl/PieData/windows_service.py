import servicemanager
import win32serviceutil
import win32service
import win32event
import threading
import asyncio
from PieData.server import main_async as start_server

class PieDataWindowsService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PieDataServer'
    _svc_display_name_ = 'PieData Server'
    _svc_description_ = 'WebSocket-based database server for PieData.'

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.worker_thread = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # Сигналим потоку остановиться
        if self.worker_thread and self.worker_thread.is_alive():
            win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        # Логируем запуск
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        # Запускаем worker-поток, чтобы быстро вернуть управление Windows
        self.worker_thread = threading.Thread(target=self._run)
        self.worker_thread.start()
        # Ожидаем сигнала остановки
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))

    def _run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(start_server())
        except Exception as e:
            servicemanager.LogErrorMsg(f"PieDataServer exception: {e}")


def main():
    win32serviceutil.HandleCommandLine(PieDataWindowsService)

if __name__ == '__main__':
    main()
