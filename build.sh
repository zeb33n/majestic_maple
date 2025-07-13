docker build -t majestic_maple .

if [ $1 = "-b" ]
then
  docker tag majestic_maple zebbo/arboretum:majestic_maple
  docker push zebbo/arboretum:majestic_maple
fi
