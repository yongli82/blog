#!/bin/bash

git add .
git commit -m "deploy"
git pull
git push
hexo generate
hexo deploy
