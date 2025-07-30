#!/bin/sh

rm -rf ./dist

uv build

uv publish