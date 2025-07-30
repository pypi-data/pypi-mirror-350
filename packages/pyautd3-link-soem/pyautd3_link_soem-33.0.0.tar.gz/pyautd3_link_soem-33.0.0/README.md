# pyautd3_link_soem

![build](https://github.com/shinolab/pyautd3_link_soem/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/shinolab/pyautd3_link_soem/graph/badge.svg?precision=2)](https://codecov.io/gh/shinolab/pyautd3_link_soem)
[![PyPI version](https://img.shields.io/pypi/v/pyautd3_link_soem)](https://pypi.org/project/pyautd3_link_soem/)

[autd3-link-soem](https://github.com/shinolab/autd3-link-soem) library for python3.11+

## Install

```
pip install pyautd3_link_soem
```

## Example

see [example](./example)

## For macOS and Linux users

This library uses `libpcap` which requires root permission.
So, please add permission as follows.

### macOS

```
sudo chmod +r /dev/bpf*
```

### linux

```
sudo setcap cap_net_raw,cap_net_admin=eip <your python path>
```

## LICENSE

See [LICENSE](./LICENSE) and [ThirdPartyNotice](./ThirdPartyNotice.txt).

# Author

Shun Suzuki, 2022-2025
