#!/bin/bash
export PATH=~/miniconda/bin:$PATH
source activate server

cd /root/arxiv-sanity-preserver/

echo $(which python) 
 
echo "started" >> /root/cron.log
python /root/arxiv-sanity-preserver/fetch_papers.py >> /root/cron.log
echo "fetched" >> /root/cron.log  
python /root/arxiv-sanity-preserver/download_pdfs.py >> /root/cron.log
echo "downloaded" >> /root/cron.log  
python /root/arxiv-sanity-preserver/parse_pdf_to_text.py >> /root/cron.log
echo "parsed" >> /root/cron.log  
python /root/arxiv-sanity-preserver/thumb_pdf.py >> /root/cron.log
echo "thumbed" >> /root/cron.log  
python /root/arxiv-sanity-preserver/analyze.py >> /root/cron.log
echo "analyzed" >> /root/cron.log  
python /root/arxiv-sanity-preserver/create_elastic_db.py >> /root/cron.log
echo "twitter_popularity" >> /root/cron.log  
python /root/arxiv-sanity-preserver/twitter_popularity.py >> /root/cron.log
echo "finished"   
