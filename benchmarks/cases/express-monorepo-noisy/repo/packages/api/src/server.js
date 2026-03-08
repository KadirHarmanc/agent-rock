const express = require("express");
const adminRoutes = require("./routes/admin");
const jobsRoutes = require("./routes/jobs");
const searchRoutes = require("./routes/search");

const app = express();

app.use(express.json());
app.use(adminRoutes);
app.use(jobsRoutes);
app.use(searchRoutes);

app.use((err, req, res, next) => {
  if (err) {
    return res.status(500).json({ error: "internal" });
  }
  next();
});

module.exports = app;
