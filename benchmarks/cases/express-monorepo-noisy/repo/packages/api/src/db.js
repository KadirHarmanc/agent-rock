async function query(sql, params) {
  return { rows: [], sql, params };
}

module.exports = { query };
