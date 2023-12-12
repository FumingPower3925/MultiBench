# MultiBench
Benchmark aggregator with gui and clean graphs
---
# Roadmap

- [X] Add usage intructions to README
- [X] Add buttons to return to the menu
- [X] Execute sysbench from python and put the results in the required csv
- [X] Auto dependency instalation
- [X] Auto blank CSV generation
- [X] Add auto instalation of sysbench (ubuntu/debian and arch)
- [ ] Create a first release on github (v0.9)
- [ ] Add multithreded execution or another solution to show simultaniously the two memory graphs
- [ ] Improve visuals
- [ ] Add auto instalation of sysbench in more distributions (fedora, RHEL/CentOS, debian...)
- [ ] Add options selection to sysbench
- [ ] Second release (v1.0)
- [ ] Add more and different benchmarks
---
# Usage
`$ git clone https://github.com/FumingPower3925/MultiBench.git`

`$ cd MultiBench/app`

`$ python3 -m venv MultiBench`

`$ source MultiBench/bin/activate`

`$ pip install -r requirements.txt`

`$ python3 program.py`

# Requisites

## Python version we've tested it on
3.11.6

## Pip version we've tested it on
23.3.1

## On Ubuntu you will also need python3.XX-venv, were XX is the same version as python, in our case 11
