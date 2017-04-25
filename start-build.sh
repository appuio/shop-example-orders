#!/bin/bash
s2i build --incremental=true --loglevel 5 -s image:///usr/libexec/s2i . centos/python-35-centos7 shop-example-orders
