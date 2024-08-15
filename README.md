
# urlshortener

That is a small application based on FastAPI and MongoDB to create short links

# Usage

1. Create config.yaml file
2. Put this code into the config file

```yaml
 database:
  host: 'localhost'
  port: 27017
  name: 'urlshortener' # The name of the database in Mongo

jwt:
  secret_key: 'use "openssl rand -hex 32" to get the random key'
  algorithm: 'HS256'

  # Expiration time of access tokens.
  # It's allowed to use formats like '1 week', '2 days', etc.
  # Check the examples here: https://pypi.org/project/pytimeparse/
  access_token_expire_time: '2d'
```
3. Run ```fastapi run```

