#!/bin/bash

#IMPORTANT can be used for new software

tlp-stat -b | grep status | awk '{print $3}'
