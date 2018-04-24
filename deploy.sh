#!/bin/bash

git add .
git commit -m "deploy"

hexo generate
hexo deploy

open "http://www.codeessay.com/"
