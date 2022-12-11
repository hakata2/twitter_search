TIME=300

while true
do
  date
  python getTweet.py
  sleep $TIME
done
