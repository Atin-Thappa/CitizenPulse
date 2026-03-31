const BASE_URL = "http://localhost:8000"; // USe Render wala after hoist

const api = {
  login: (email: string, password: string) =>
    fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    }).then((r) => r.json()),

  logout: () =>
    fetch(`${BASE_URL}/logout`, {
      method: "POST",
      credentials: "include",
    }),

  submitComplaint: (data: {
    citizen_name: string;
    citizen_email: string;
    raw_text: string;
    category: string;
    district: string;
  }) =>
    fetch(`${BASE_URL}/complaint`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then((r) => r.json()),

  getClusters: () =>
    fetch(`${BASE_URL}/clusters`, {
      credentials: "include",
    }).then((r) => r.json()),

  getHeatmap: () =>
    fetch(`${BASE_URL}/heatmap`, {
      credentials: "include",
    }).then((r) => r.json()),

  getClusterComplaints: (clusterId: number) =>
    fetch(`${BASE_URL}/clusters/${clusterId}/complaints`, {
      credentials: "include",
    }).then((r) => r.json()),

  updateStatus: (complaintId: number, status: "Pending" | "In-Progress" | "Resolved") =>
    fetch(`${BASE_URL}/complaint/${complaintId}/status?status=${status}`, {
      method: "PUT",
      credentials: "include",
    }).then((r) => r.json()),
}

export default api