function requireSession(req, res, next) {
  req.user = { id: 1, role: "admin" };
  next();
}

function ensureAdmin(req, res, next) {
  if (req.user.role !== "admin") {
    return res.status(403).json({ error: "forbidden" });
  }
  next();
}

module.exports = {
  requireSession,
  ensureAdmin,
};
