function applySecurityHeaders(req, res, next) {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  return next();
}

function handleErrors(err, req, res, next) {
  void err;
  void next;
  return res.status(500).json({ error: "internal-error" });
}

module.exports = { applySecurityHeaders, handleErrors };
