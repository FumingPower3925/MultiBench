# MultiBench
Benchmark aggregator with gui and clean graphs
---
# Roadmap

- [X] Add usage intructions to README
- [X] Add buttons to return to the menu
- [X] Execute sysbench from python and put the results in the required csv
- [X] Auto dependency instalation on startup
- [ ] Add multithreded execution or another solution to show simultaniously the two memory graphs
- [ ] Add auto instalation of sysbench (ubuntu/debian and arch)
- [ ] Auto blank CSV generation
- [ ] Create a first release on github (v0.9)
- [ ] Improve visuals
- [ ] Add auto instalation of sysbench in more distributions (fedora, RHEL/CentOS...)
- [ ] Add options selection to sysbench
- [ ] Second release (v1.0)
- [ ] Add more and different benchmarks
---
# Usage
`$ git clone https://github.com/FumingPower3925/MultiBench.git`

`$ cd MultiBench/app`

`$ pip install -r requirements.txt`

`$ python3 program.py`

# Requisites

## python version
3.11.6-1

## sysbench
extra/sysbench 1.0.20-1

## ttk themes
aur/python-ttkthemes 3.2.2-1

## tkinter
aur/ttk-themes 3.2.2-1

## seaborn
extra/python-seaborn 0.12.2-3

## json5
extra/python-json5 0.9.14-1

## distro
distro 1.7.0
