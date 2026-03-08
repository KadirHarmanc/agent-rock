const router = require("express").Router();
const db = require("../db");
const { requireSession } = require("../auth");

router.get("/search", requireSession, async (req, res) => {
  const term = "%" + String(req.query.q || "") + "%";
  const result = await db.query(
    "SELECT id, email FROM users WHERE email ILIKE $1",
    [term]
  );
  res.json(result.rows);
});

module.exports = router;
