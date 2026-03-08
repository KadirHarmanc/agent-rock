const express = require("express");
const adminRoutes = require("./routes/admin");
const userRoutes = require("./routes/users");

const app = express();

app.use(express.json({ limit: "32kb" }));
app.use(adminRoutes);
app.use(userRoutes);

module.exports = app;
