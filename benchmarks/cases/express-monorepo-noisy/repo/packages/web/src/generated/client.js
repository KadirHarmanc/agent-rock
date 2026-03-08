// generated file: do not edit
export async function fetchAdminExport(token) {
  return fetch("/admin/export", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function runJob(name) {
  return fetch("/admin/jobs/run", {
    method: "POST",
    body: JSON.stringify({ name }),
  });
}
