function requireSession(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ error: "unauthorized" });
  }

  return next();
}

function ensureRole(role) {
  return function checkRole(req, res, next) {
    if (!req.user || req.user.role !== role) {
      return res.status(403).json({ error: "forbidden" });
    }

    return next();
  };
}

module.exports = { requireSession, ensureRole };
