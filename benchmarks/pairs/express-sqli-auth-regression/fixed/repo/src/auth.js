function requireAuth(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ error: "unauthorized" });
  }

  return next();
}

function requireAdmin(req, res, next) {
  if (req.user.role !== "admin") {
    return res.status(403).json({ error: "forbidden" });
  }

  return next();
}

module.exports = { requireAuth, requireAdmin };
