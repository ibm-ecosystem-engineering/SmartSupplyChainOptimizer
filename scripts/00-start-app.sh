#!/usr/bin/env bash

cd /Users/gandhi/GandhiMain/700-Apps/SmartSupplyChainOptimizer

python -m venv myvenv
source myvenv/bin/activate

cd /Users/gandhi/GandhiMain/700-Apps/SmartSupplyChainOptimizer/src

python -m pip install -r requirements.txt

python main.py

