const router = require("express").Router();
const db = require("../db");
const { requireAuth, requireAdmin } = require("../auth");

router.get("/admin/export", requireAuth, requireAdmin, async (req, res) => {
  const result = await db.query(
    "SELECT id, email, role FROM users ORDER BY id ASC",
    []
  );
  res.json(result.rows);
});

module.exports = router;
