#!/usr/bin/env bash
#source activate papers_p36

for i in {0..50000..100}
do
   echo "Calling fetch_papers with --start-index $i"
   ~/anaconda/envs/papers_p36/bin/python fetch_papers.py --start-index $i
   sleep 10s
done
