# HoymilesDtuMi
## Hoymiles DTU-MI data wrapper for python.
### Retrieving pv data from DTU.

1. Example
```
import hoymilesdtumi

json = hoymilesdtumi.dtu_http_request('192.168.0.109')
print(json)
```

2. Scripts of this lib
```
$ pip3 install climatempopy
$ get_localeID YOUR_CLIMATEMPO_TOKEN LAT LON
$ get_weather_by_localeID YOUR_CLIMATEMPO_TOKEN LOCALE_ID