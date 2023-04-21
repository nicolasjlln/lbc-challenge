set -e

mongosh <<EOF
db = db.getSiblingDB('lbc')

db.createUser({
  user: 'user',
  pwd: 'password',
  roles: [{ role: 'readWrite', db: 'lbc' }],
});
db.createCollection('article')

EOF