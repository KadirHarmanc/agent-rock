const express = require("express");
const adminRoutes = require("./routes/admin");
const userRoutes = require("./routes/users");
const searchRoutes = require("./routes/search");

const app = express();

app.use(express.json());
app.use(adminRoutes);
app.use(userRoutes);
app.use(searchRoutes);

module.exports = app;
