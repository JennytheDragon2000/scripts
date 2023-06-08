#! /bin/bash

npm config rm proxy
npm config rm https-proxy
npm config delete proxy
npm config delete https-proxy
npm config --global rm proxy
npm config --global rm https-proxy
npm config set registry "http://registry.npmjs.org"
npm config set strict-ssl false
