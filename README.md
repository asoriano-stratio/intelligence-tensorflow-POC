

https://github.com/tensorflow/ecosystem/tree/master/marathon


JSON deployment 
-----------------------------------

curl -i -H 'Content-Type: application/json' -d @mycluster.json http://marathon.mesos:8080/v2/groups


=> Necesitamos la cookie:

curl -i -H 'Content-Type: application/json' -H 'Cookie: eyJhbGciOiJIUzI1NiIsImtpZCI6InNlY3JldCIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0OTY0MDczNzQsInVpZCI6ImFkbWluQGRlbW8uc3RyYXRpby5jb20ifQ.OIuRG-ynyyvU39EvG8dAkUo_K33cpPKonvuF4ze-IUs' -d @tf_cluster.json http://leader.mesos:8080/v2/groups
