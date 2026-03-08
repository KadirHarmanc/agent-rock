async function query(sql, params) {
  return { sql, params, rows: [] };
}

module.exports = { query };
