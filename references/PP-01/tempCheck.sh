#!/bin/bash

#MEH MAYBE IMPORTANT

tlp-stat -t | grep temp | awk '{print $4}'
