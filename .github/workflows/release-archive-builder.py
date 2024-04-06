# This workflow will build a tar.gz archive of the program Python dependencies, run tests and lint with a single version of Python
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

name: Release Archive Builder

on:
  push:
    branches: [ "release" ]

permissions:
  contents: read

jobs:
  build:
    name: Create .tar.gz Package
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@master
      - name: Set release date
        run: echo "RELEASE_NAME=$(date +'%Y-%m-%dT%H:%M:%S')" >> $GITHUB_ENV
      - name: Compress action step
        uses: a7ul/tar-action@v1.1.0
        id: compress
        with:
          command: c
          cwd: ./
          files: |
            ./src
            ./statements
          outPath: {{ github.repository }}-{{ $RELEASE_NAME }}-{{ github.sha }}.tar.gz
