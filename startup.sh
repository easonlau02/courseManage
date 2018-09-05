#!/bin/bash

# name python env as lab, so if your python env is not equal to lab, please change it or do not use this scripts
# Author: Eason Lau <eason.lau02@hotmail.com>

num=$1

if [[ -n $num ]]; then
	sed -ig "s/PHASE = .*/PHASE = $num/g" properties.conf
	source activate lab
	python courseManage.py
	source deactivate lab
else
	echo Usage: $0 "[phase<int>]"
fi
