const express = require("express");
const adminRoutes = require("./routes/admin");
const userRoutes = require("./routes/users");
const searchRoutes = require("./routes/search");
const { applySecurityHeaders, handleErrors } = require("./security");

const app = express();

app.use(express.json({ limit: "32kb" }));
app.use(applySecurityHeaders);
app.use(adminRoutes);
app.use(userRoutes);
app.use(searchRoutes);
app.use(handleErrors);

module.exports = app;
