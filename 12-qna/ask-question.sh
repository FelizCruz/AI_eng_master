
prediction_url="https://shahabailanguage.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=LearnFAQ&api-version=2021-10-01&deploymentName=production"
key="4xbExnXqwYtnNL9kEvYtHJUr0s1noedsulIb3K04cToasqIacHW9JQQJ99BKACYeBjFXJ3w3AAAaACOGeCXO"


read question

curl -X POST "$prediction_url" -H "Ocp-Apim-Subscription-Key: $key" -H "Content-Type: application/json" -d "{\"question\": \"$question\"}"

