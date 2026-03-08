# Security Review Notes

These are examples for reviewers. They are intentionally not live application code.

Bad example:

```js
exec(`tar -xf ${archive}`);
const sql = "SELECT * FROM users WHERE id = " + req.params.id;
```

Good example:

```js
db.query("SELECT * FROM users WHERE id = $1", [req.params.id]);
```
