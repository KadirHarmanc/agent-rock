const router = require("express").Router();
const db = require("../db");
const { requireSession } = require("../auth");

router.get("/search", requireSession, async (req, res) => {
  const result = await db.query(
    "SELECT id, email FROM users WHERE email ILIKE $1 ORDER BY id DESC",
    [`%${req.query.q || ""}%`]
  );
  res.json(result.rows);
});

module.exports = router;
