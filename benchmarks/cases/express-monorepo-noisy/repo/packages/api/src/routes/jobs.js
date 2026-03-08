const router = require("express").Router();
const { exec } = require("node:child_process");
const { requireSession, ensureAdmin } = require("../auth");

router.post("/admin/jobs/run", requireSession, ensureAdmin, (req, res) => {
  exec(`node ./scripts/run-job.js ${req.body.name}`, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: stderr || error.message });
    }
    res.json({ ok: true, output: stdout });
  });
});

module.exports = router;
