#!/bin/python

from .task import MBIOTask
from .xmlconfig import XMLConfig

from .netscan import MBIONetworkScanner
import requests


# Should use https://shelly-api-docs.shelly.cloud/gen2/General/RPCChannels
# https://shelly-api-docs.shelly.cloud/gen2/General/ComponentConcept
# https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Shelly
# Sys.GetConfig
# Shelly.GetConfig
# Shelly.ListMethods
# Shelly.GetDeviceInfo
# Shelly.GetComponents
# Switch.GetConfig?id=0
# Switch.GetStatus?id=0
# Switch.Toggle?id=0
# Switch.Set?id=0&on=true


class MBIOTaskShelly(MBIOTask):
    def initName(self):
        return 'shelly'

    def onInit(self):
        requests.packages.urllib3.disable_warnings()
        self.config.set('refreshperiod', 15)
        self._switches={}
        self._timeoutRefresh=0
        self.valueDigital('comerr', default=False)

    def onLoad(self, xml: XMLConfig):
        self.config.update('refreshperiod', xml.getInt('refresh'))

        items=xml.children('switch')
        if items:
            for item in items:
                name=item.get('name')
                ip=item.get('ip')
                cid=item.getInt('id', 0)
                if name and not self._switches.get(name):
                    data={}
                    data['state']=self.valueDigital('%s_state' % name, writable=True, commissionable=True)
                    data['state'].config.set('ip', ip)
                    data['state'].config.set('cid', cid)
                    # data['t']=self.value('%s_t' % name, unit='C', resolution=0.1)
                    self._switches[name.lower()]=data

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def url(self, ip, command):
        return 'http://%s/rpc/%s' % (ip, command)

    def run(self):
        for name in self._switches.keys():
            value=self._switches[name]['state']
            if value.isPendingSync():
                self.microsleep()
                try:
                    ip=value.config.ip
                    cid=value.config.cid
                    url=self.url(ip, 'Switch.Set')
                    state='false'
                    if value.toReachValue:
                        state='true'
                    params={'id': cid, 'on': state}
                    self.logger.debug('shelly(%s)->%s(%s)' % (value.key, url, params))
                    r=requests.get(url, params=params, timeout=3.0, verify=False)
                    if r and r.ok:
                        value.clearSync()
                        self._timeoutRefresh=0
                    else:
                        self.logger.error('shelly(%s)->%s(%s)' % (value.key, url, params))
                except:
                    pass
                value.clearSyncAndUpdateValue()

        if self.config.refreshperiod>0 and self.isTimeout(self._timeoutRefresh):
            self._timeoutRefresh=self.timeout(self.config.refreshperiod)
            error=False
            for name in self._switches.keys():
                self.microsleep()
                dev=self._switches[name]
                try:
                    value=dev['state']
                    ip=value.config.ip
                    cid=value.config.cid
                    url=self.url(ip, 'Switch.GetStatus')
                    params={'id': cid}
                    # self.logger.debug('shelly(%s)->%s(%s)' % (value.key, url, params))
                    r=requests.get(url, params=params, timeout=3.0, verify=False)
                    if r and r.ok:
                        data=r.json()
                        value.updateValue(data['output'])
                        value.setError(False)
                        continue
                    else:
                        self.logger.error('shelly(%s)->%s(%s)' % (value.key, url, params))
                        error=True
                except:
                    pass

                dev['state'].setError(True)
                # dev['t'].setError(True)
                error=True

            self.values.comerr.updateValue(error)

        return 5.0

    def scanner(self, network=None):
        network=network or self.getMBIO().network
        s=ShellyScanner(self, network)
        return s.scan()


class ShellyScanner(MBIONetworkScanner):
    def probe(self, host):
        try:
            url='http://%s/rpc/Sys.GetConfig' % (host)
            r=requests.get(url, timeout=1.0)
            if r and r.ok:
                data=r.json()
                return data['device']['mac']
        except:
            pass


if __name__ == "__main__":
    pass
