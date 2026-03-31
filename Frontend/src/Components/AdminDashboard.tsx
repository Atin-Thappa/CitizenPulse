import { useState, useEffect } from "react"
import { MapContainer, TileLayer, useMap } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import L from "leaflet"

delete (L.Icon.Default.prototype as any)._getIconUrl

L.Icon.Default.mergeOptions({
  iconUrl: "/marker-icon.png",
  iconRetinaUrl: "/marker-icon-2x.png",
  shadowUrl: "/marker-shadow.png",
})

import "leaflet.heat"
import "leaflet.markercluster"
import "leaflet.markercluster/dist/MarkerCluster.css"
import "leaflet.markercluster/dist/MarkerCluster.Default.css"

interface Complaint {
  complaint_id: number
  citizen_name: string
  citizen_email: string
  raw_text: string
  category: string
  district: string
  status: string
}

const DISTRICT_COORDS: Record<string, [number, number]> = {
  "West Delhi":    [28.6539, 77.0688],
  "Dwarka":        [28.5921, 77.0460],
  "South Delhi":   [28.5244, 77.1855],
  "North Delhi":   [28.7041, 77.1025],
  "East Delhi":    [28.6508, 77.2773],
  "Central Delhi": [28.6448, 77.2167],
}

const STATUS_COLORS: Record<string, string> = {
  "Pending":     "text-red-400",
  "In-Progress": "text-yellow-400",
  "Resolved":    "text-green-400",
}

const CATEGORY_PRIORITY: Record<string, string> = {
  "Infrastructure": "P1",
  "Public Safety":  "P1",
  "Sanitation":     "P2",
  "Water Supply":   "P2",
  "Traffic":        "P3",
  "Maintenance":    "P3",
}

function HeatmapLayer({ complaints }: { complaints: Complaint[] }) {
  const map = useMap()

  useEffect(() => {
    const points = complaints.map(c => {
      const base = DISTRICT_COORDS[c.district] ?? [28.6139, 77.2090]
      return [
        base[0] + (Math.random() - 0.5) * 0.03,
        base[1] + (Math.random() - 0.5) * 0.03,
        1.0,
      ] as [number, number, number]
    })

    const heat = (L as any).heatLayer(points, {
      radius: 35,
      blur: 25,
      maxZoom: 13,
      gradient: { 0.2: "blue", 0.5: "orange", 0.8: "red" },
    }).addTo(map)

    return () => { map.removeLayer(heat) }
  }, [complaints, map])

  return null
}

function ClusterLayer({ complaints, onSelect }: { complaints: Complaint[], onSelect: (c: Complaint) => void }) {
  const map = useMap()

  useEffect(() => {
    const group = (L as any).markerClusterGroup()

    complaints.forEach(c => {
      const base = DISTRICT_COORDS[c.district] ?? [28.6139, 77.2090]
      const lat = base[0] + (Math.random() - 0.5) * 0.03
      const lng = base[1] + (Math.random() - 0.5) * 0.03
      const marker = L.marker([lat, lng])
      marker.bindPopup(`<b>#${c.complaint_id}</b><br/>${c.category}<br/>${c.district}`)
      marker.on("click", () => onSelect(c))
      group.addLayer(marker)
    })

    map.addLayer(group)
    return () => { map.removeLayer(group) }
  }, [complaints, map])

  return null
}

function AdminDashboard() {
  const [complaints, setComplaints] = useState<Complaint[]>([])
  const [selected, setSelected] = useState<Complaint | null>(null)
  const [showHeatmap, setShowHeatmap] = useState(true)
  const [statuses, setStatuses] = useState<Record<number, string>>({})

  useEffect(() => {
    fetch("/sample/complaints.json")
      .then(r => r.json())
      .then((data: Complaint[]) => {
        setComplaints(data)
        const initial: Record<number, string> = {}
        data.forEach(c => { initial[c.complaint_id] = c.status })
        setStatuses(initial)
      })
  }, [])

  function markAs(status: string) {
    if (!selected) return
    setStatuses(prev => ({ ...prev, [selected.complaint_id]: status }))
    setSelected(prev => prev ? { ...prev, status } : null)
  }

  const urgent = complaints.filter(c =>
    (statuses[c.complaint_id] ?? c.status) === "Pending" &&
    ["Infrastructure", "Public Safety"].includes(c.category)
  )

  return (
    <div className="flex flex-1 w-full overflow-hidden bg-[#0D1B2A]">

      <div className="w-80 min-w-[280px] flex flex-col bg-[#0D1B2A] text-white border-r border-slate-700 overflow-y-auto">

        <div className="p-4 border-b border-slate-700">
          <h2 className="text-lg font-semibold mb-3">Urgent Reports</h2>
          <div className="flex text-xs text-slate-400 mb-2 px-1 gap-2">
            <span className="w-16">ID</span>
            <span className="flex-1">Category</span>
            <span className="w-14">District</span>
          </div>
          <div className="flex flex-col gap-1">
            {urgent.slice(0, 6).map(c => (
              <button
                key={c.complaint_id}
                onClick={() => setSelected(c)}
                className={`flex items-center gap-2 text-left text-xs px-2 py-1.5 rounded-md transition-colors
                  ${selected?.complaint_id === c.complaint_id
                    ? "bg-slate-600"
                    : "hover:bg-slate-700"}`}
              >
                <span className="text-red-400 font-semibold w-16">
                  #{c.complaint_id} {CATEGORY_PRIORITY[c.category]}
                </span>
                <span className="flex-1 truncate">{c.category}</span>
                <span className="text-slate-400 w-14 truncate">{c.district.replace(" Delhi", "")}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="p-4 border-b border-slate-700">
          <label className="flex items-center gap-2 cursor-pointer mb-2 text-sm">
            <input
              type="radio"
              name="mapview"
              checked={showHeatmap}
              onChange={() => setShowHeatmap(true)}
              className="accent-blue-500"
            />
            Show Urban Heatmap
          </label>
          <label className="flex items-center gap-2 cursor-pointer text-sm">
            <input
              type="radio"
              name="mapview"
              checked={!showHeatmap}
              onChange={() => setShowHeatmap(false)}
              className="accent-blue-500"
            />
            Show Categorized Clusters
          </label>
        </div>

        <div className="p-4 border-b border-slate-700 flex-1">
          {selected ? (
            <div className="flex flex-col gap-1.5 text-sm">
              <p className="font-semibold text-white">#{selected.complaint_id} — {selected.category}</p>
              <p className="text-slate-400 text-xs">{selected.citizen_name} · {selected.citizen_email}</p>
              <p className="text-slate-300 text-xs mt-1">{selected.raw_text}</p>
              <p className="text-xs mt-1">
                Status: <span className={`font-semibold ${STATUS_COLORS[statuses[selected.complaint_id] ?? selected.status]}`}>
                  {statuses[selected.complaint_id] ?? selected.status}
                </span>
              </p>
            </div>
          ) : (
            <p className="text-slate-500 text-xs">Populating when a specific report is selected.</p>
          )}
        </div>

        <div className="p-4 flex flex-col gap-2">
          <button
            onClick={() => markAs("In-Progress")}
            disabled={!selected}
            className="w-full py-2 rounded-md text-sm font-medium bg-blue-700 hover:bg-blue-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          >
            Mark as In-Progress
          </button>
          <button
            onClick={() => markAs("Resolved")}
            disabled={!selected}
            className="w-full py-2 rounded-md text-sm font-medium bg-blue-700 hover:bg-blue-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          >
            Mark as Resolved
          </button>
          <button
            onClick={() => markAs("Spam")}
            disabled={!selected}
            className="w-full py-2 rounded-md text-sm font-medium bg-red-700 hover:bg-red-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          >
            Dismiss as Spam / Non-issue
          </button>
        </div>
      </div>

      <div className="flex-1 flex flex-col">

        <div className="flex justify-center gap-0 p-3 bg-[#0D1B2A]">
          <button
            onClick={() => setShowHeatmap(true)}
            className={`px-6 py-1.5 text-sm font-medium rounded-l-full border border-slate-500 transition-colors
              ${showHeatmap ? "bg-blue-700 text-white border-blue-700" : "bg-transparent text-slate-300 hover:bg-slate-700"}`}
          >
            Heat Map View
          </button>
          <button
            onClick={() => setShowHeatmap(false)}
            className={`px-6 py-1.5 text-sm font-medium rounded-r-full border border-slate-500 transition-colors
              ${!showHeatmap ? "bg-blue-700 text-white border-blue-700" : "bg-transparent text-slate-300 hover:bg-slate-700"}`}
          >
            Cluster View
          </button>
        </div>

        <div className="flex-1">
          <MapContainer
            center={[28.6139, 77.2090]}
            zoom={11}
            className="w-full h-full"
            zoomControl={true}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            />
            {complaints.length > 0 && showHeatmap && (
              <HeatmapLayer complaints={complaints} />
            )}
            {complaints.length > 0 && !showHeatmap && (
              <ClusterLayer complaints={complaints} onSelect={setSelected} />
            )}
          </MapContainer>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard