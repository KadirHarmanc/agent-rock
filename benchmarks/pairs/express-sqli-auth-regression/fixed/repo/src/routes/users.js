const router = require("express").Router();
const db = require("../db");
const { requireAuth } = require("../auth");

router.get("/users/:id", requireAuth, async (req, res) => {
  const isOwner = String(req.user.id) === String(req.params.id);
  const isAdmin = req.user.role === "admin";

  if (!isOwner && !isAdmin) {
    return res.status(403).json({ error: "forbidden" });
  }

  const result = await db.query(
    "SELECT id, email, plan FROM users WHERE id = $1",
    [req.params.id]
  );
  res.json(result.rows[0] || null);
});

module.exports = router;
