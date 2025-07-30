import contextlib
import subprocess
from abc import ABC, abstractmethod
from socket import socket
from urllib.parse import urlunsplit, urlsplit

from ephemeral_port_reserve import reserve as reserve_port
from scrapy import signals
from twisted.internet import reactor
from twisted.internet.defer import Deferred


class ForwardingHttpToSocksProxyMiddleware(ABC):

    def __init__(self, crawler):
        self._proxy_to_local_port = {}
        self._deferred_ports = {}
        crawler.signals.connect(self.close, signal=signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    @abstractmethod
    def start_bridge(self, local_port, proxy_scheme, proxy_netloc):
        pass

    def process_request(self, request, spider):
        proxy = request.meta.get('proxy')
        if proxy:
            scheme, netloc, *_ = urlsplit(proxy)
            if scheme.startswith('socks'):
                local_port = self._proxy_to_local_port.get(proxy)
                if not local_port:
                    local_port = reserve_port()
                    self.start_bridge(local_port, scheme, netloc)
                    self._proxy_to_local_port[proxy] = local_port
                    self._defer_port(local_port)
                request.meta['proxy'] = f'http://localhost:{local_port}'
                request.meta['_socks_proxy'] = proxy
                # None or Deferred which resolves to None when bridge is ready
                return self._deferred_ports.get(local_port)

    def _defer_port(self, port):
        # Defers availability of local port until connection to bridge can be established.

        def check():
            with contextlib.closing(socket()) as sock:
                if sock.connect_ex(('localhost', port)) == 0:
                    self._deferred_ports.pop(port).callback(None)
                else:
                    reactor.callLater(1, check)

        self._deferred_ports[port] = Deferred()
        reactor.callLater(0.5, check)

    def process_response(self, request, response, spider):
        self._restore_proxy(request)
        return response

    def process_exception(self, request, exception, spider):
        self._restore_proxy(request)

    @staticmethod
    def _restore_proxy(request):
        if '_socks_proxy' in request.meta:
            request.meta['proxy'] = request.meta.pop('_socks_proxy')

    @abstractmethod
    def close(self):
        pass


class DeleGateSocksProxyMiddleware(ForwardingHttpToSocksProxyMiddleware):
    DEFAULT_EXECUTABLE = 'delegated'

    def __init__(self, crawler):
        super().__init__(crawler)
        self._delegate_executable = crawler.settings.get('DELEGATE_EXECUTABLE',
                                                         self.DEFAULT_EXECUTABLE)

    def start_bridge(self, local_port, proxy_scheme, proxy_netloc):
        socks_opt = ''
        if proxy_scheme == 'socks4':
            socks_opt = '-4'
        elif proxy_scheme == 'socks4a':
            socks_opt = '-4-r'
        proxy = urlunsplit(('socks', proxy_netloc, socks_opt, '', ''))
        subprocess.run([
            self._delegate_executable,
            'ADMIN=nobody',
            'RESOLV=""',
            f'-Plocalhost:{local_port}',
            'SERVER=http',
            f'FORWARD={proxy}',
        ])

    def stop_bridge(self, local_port):
        subprocess.run([
            self._delegate_executable,
            f'-Plocalhost:{local_port}',
            '-Fkill',
        ])

    def close(self):
        for port in self._proxy_to_local_port.values():
            self.stop_bridge(port)


class HptsSocksProxyMiddleware(ForwardingHttpToSocksProxyMiddleware):

    def __init__(self, crawler):
        super().__init__(crawler)
        self._hpts_processes = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def start_bridge(self, local_port, proxy_scheme, proxy_netloc):
        proxy = ':'.join(reversed(proxy_netloc.split('@', 1)))  # -> host:port:user:pass
        hpts_process = subprocess.Popen(f'hpts -s {proxy} -p {local_port}', shell=True)
        self._hpts_processes.append(hpts_process)

    def close(self):
        for hpts_process in self._hpts_processes:
            hpts_process.terminate()
