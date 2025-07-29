import servicemanager
import win32serviceutil
import win32service
import win32event
import sys
import asyncio
from .server import main_async

class PieDataWindowsService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PieDataServer'
    _svc_display_name_ = 'PieData Server'
    _svc_description_ = 'WebSocket-based database server for PieData.'

    def __init__(self, args):
        super().__init__(args)
        # Создаем событие для остановки
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.loop = None

    def SvcStop(self):
        # Сообщаем Windows, что служба останавливается
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.loop:
            # Останавливаем цикл событий
            self.loop.call_soon_threadsafe(self.loop.stop)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        # Логируем запуск
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(main_async())
        except Exception as e:
            servicemanager.LogErrorMsg(f"PieDataServer exception: {e}")

        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))
def main():
    win32serviceutil.HandleCommandLine(PieDataWindowsService)

if __name__ == '__main__':
    # Обработка параметров: install, remove, start, stop и т.д.
    win32serviceutil.HandleCommandLine(PieDataWindowsService)
