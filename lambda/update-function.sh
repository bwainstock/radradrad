pip install -t . -r lambdarequirements.txt
zip -ur9 lambda.zip *
aws lambda update-function-code --region us-west-2 --function-name radradradScraper --zip-file fileb://lambda.zip --publish
