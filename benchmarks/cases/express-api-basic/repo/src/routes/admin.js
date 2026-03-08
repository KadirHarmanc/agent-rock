const router = require("express").Router();
const db = require("../db");

router.get("/admin/export", async (req, res) => {
  const result = await db.query("SELECT id, email, role FROM users");
  res.json(result.rows);
});

module.exports = router;
