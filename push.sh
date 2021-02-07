git config --global user.name "dungeontiger"
git config --global user.email "stephen.d.gibson@gmail.com"
git remote set-url --push origin https://dungeontiger:48e9ccaf6e6fce08ec1ad2cca233da1f0ee50d99/dungeontiger/lexicon.git
git checkout -b updates
git add .
git commit -m "lexicon updates"
git push
git checkout main
