const router = require("express").Router();
const db = require("../db");
const { requireAuth } = require("../auth");

router.get("/users/:id", requireAuth, async (req, res) => {
  const sql = "SELECT id, email, plan FROM users WHERE id = " + req.params.id;
  const result = await db.query(sql);
  res.json(result.rows[0] || null);
});

module.exports = router;
